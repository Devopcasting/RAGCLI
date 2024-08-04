# ragctl/ragctl.py

from typing import Dict, NamedTuple, Any, List
from pathlib import Path
from ragctl.database import DatabaseHandler
from ragctl import SUCCESS, DB_READ_ERROR, DB_WRITE_ERROR, DOC_ID_ERROR, DOC_EMBEDDING_ERROR, DOC_NOT_FOUND_ERROR
from ragctl.helper.validate_doc import ValidateDocumentFormat
from ragctl.document_process.process_doc import ProcessDocument
from ragctl.query_document.query import QueryDocuments
import os
import shutil
import hashlib

# Create a NamedTuple to store the Document result
class DocumentResult(NamedTuple):
    rag: Dict[str, Any]
    error: int

class RagDocOperations:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)
        # Set the documents folder path
        self._docs_path = Path(__file__).parent / "documents"
        # Set the vector database path
        self._vector_db_path = Path(__file__).parent / "vector_db"
    
    # Method: Add list of documents to the database
    def add_docs(self, documents_path: List[str]) -> DocumentResult:
        try:
            result = []
            for document in documents_path:
                # Check if the document exists
                if not os.path.exists(document):
                    result.append({
                        "document": document,
                        "status": 1,
                        "message": "Document path does'nt exists"
                    })
                    continue
                
                # Check if the document is in valid format
                if not ValidateDocumentFormat(document).validate():
                    result.append({
                        "document": document,
                        "status": 1,
                        "message": "Invalid document format"
                    })
                    continue
                
                # Find the document type
                document_format = ValidateDocumentFormat(document).get_document_format()

                # Get the document hash
                doc_hash = hashlib.sha256(document.encode()).hexdigest()
                
                # Check if the document already exists in the database
                read_document = self._db_handler.read()
                if any(doc['md5sum'] == doc_hash for doc in read_document.data):
                    result.append({
                        "document": document,
                        "status": 1,
                        "message": "Document already exists"
                    })
                    continue
                # Create a folder inside documents folder with the doc_hash last 4 characters
                doc_folder = self._docs_path / doc_hash[-4:]
                os.makedirs(doc_folder, exist_ok=True)
                
                # Get the document size
                doc_size = self._get_document_size(document)
                
                # Get the document basename
                doc_basename = os.path.basename(document)

                # Prepare the document info
                document_info = {
                    "id" : doc_hash[-4:],
                    "md5sum": doc_hash,
                    "size": doc_size,
                    "name": doc_basename,
                    "path": f"{doc_folder}/{doc_basename}",
                    "embedded": "False",
                    "type": document_format
                }
                # Copy the document to the documents folder
                shutil.copy(document, document_info['path'])

                # Add the document to the database
                read_db = self._db_handler.read()
                if read_db.error:
                    return DocumentResult({}, DB_READ_ERROR)
                read_db.data.append(document_info)
                write_db = self._db_handler.write(read_db.data)
                if write_db.error:
                    return DocumentResult({}, DB_WRITE_ERROR)
                result.append({
                        "document": document,
                        "status": 0,
                        "message": "Document added successfully"
                    })
            return DocumentResult(result, SUCCESS)
        except Exception as e:
            return DocumentResult({}, DB_WRITE_ERROR)
    
    # Method: Get the size of document
    def _get_document_size(self, document_path: str) -> int:
        # Get the file size in bytes
        size_in_bytes = os.path.getsize(document_path)
        
        # Determine the appropriate unit (KB, MB, GB, TB) based on the file size
        if size_in_bytes < 1024:
            return f"{size_in_bytes} bytes"
        # Convert to KB
        elif size_in_bytes < 1024 * 1024:
            return f"{size_in_bytes / 1024:.2f} KB"
        # Convert to MB
        elif size_in_bytes < 1024 * 1024 * 1024:
            return f"{size_in_bytes / (1024 * 1024):.2f} MB"
        # Convert to GB
        elif size_in_bytes < 1024 * 1024 * 1024 * 1024:
            return f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"
        # Convert to TB
        else:
            return f"{size_in_bytes / (1024 * 1024 * 1024 * 1024):.2f} TB"
    
    # Method: Get the list of documents from the database
    def get_docs_list(self) -> DocumentResult:
        try:
            read_db = self._db_handler.read()
            if read_db.error:
                return DocumentResult({}, DB_READ_ERROR)
            return DocumentResult(read_db.data, SUCCESS)
        except Exception as e:
            return DocumentResult({}, DB_READ_ERROR)
    
    # Method: Delete all the added documents
    def delete_all_documents(self) -> DocumentResult:
        try:
            # Check if the database is empty
            read_db = self._db_handler.read()
            if len(read_db.data) == 0:
                return DocumentResult({}, DOC_NOT_FOUND_ERROR)
            # Delete all the documents from the database
            write_to_db = self._db_handler.write([])
            if write_to_db.error:
                return DocumentResult({}, DB_WRITE_ERROR)
            # Delete all the documents from the document folder
            for file in os.listdir(self._docs_path):
                if file != "README.md":
                    shutil.rmtree(self._docs_path / file)
            # Delete all the documents from the database folder
            for file in os.listdir(self._vector_db_path):
                if file != "README.md":
                    shutil.rmtree(self._vector_db_path / file)
            return DocumentResult({}, SUCCESS)
        except Exception as e:
            return DocumentResult({}, DB_READ_ERROR)
            
            
    # Method: Delete the particular document
    def delete_document(self, document_id: str) -> DocumentResult:
        try:
            read_db = self._db_handler.read()
            if read_db.error:
                return DocumentResult({}, DB_READ_ERROR)
            
            # Check if document id exists
            document_id_found = False
            for doc in read_db.data:
                if doc['id'] == document_id:
                    document_id_found = True
                    break
            if not document_id_found:
                return DocumentResult({}, DOC_ID_ERROR)
            
            # Delete the document from the database
            updated_data = [doc for doc in read_db.data if doc['id'] != document_id]
            write_to_db = self._db_handler.write(updated_data)
            if write_to_db.error:
                return DocumentResult({}, DB_WRITE_ERROR)
            # Delete the document from the document folder and vector database
            if os.path.exists(self._docs_path / document_id):
                shutil.rmtree(self._docs_path / document_id)
            if os.path.exists(self._vector_db_path / document_id):
                shutil.rmtree(self._vector_db_path / document_id)
            return DocumentResult({}, SUCCESS)
        except Exception as e:
            print(e)
            return DocumentResult({}, DB_READ_ERROR)
    
    # Method: Process the added document and store it in the vector database
    def process_document(self, document_id: str) -> DocumentResult:
        try:
            read_db = self._db_handler.read()
            if read_db.error:
                return DocumentResult({}, DB_READ_ERROR)

            # Check if the document id exists
            document_id_found = False
            document_format = None
            document_hash = None
            document_path = None

            for doc in read_db.data:
                if doc['id'] == document_id:
                    if doc['embedded'] == "True":
                        return DocumentResult({}, DOC_EMBEDDING_ERROR)
                    document_id_found = True
                    # Get the document information
                    document_format = ValidateDocumentFormat(doc['path']).get_document_format()
                    document_hash = doc['md5sum']
                    document_path = doc['path']
                    break
            if not document_id_found:
                return DocumentResult({}, DOC_ID_ERROR)
            
            # Process the document and store it in the vector database
            process_doc = ProcessDocument(document_path, self._vector_db_path,
                                              document_hash, document_format)
            if process_doc.process():
                # Update the document status in the database
                for doc in read_db.data:
                    if doc['id'] == document_id:
                        doc['embedded'] = "True"
                        write_db = self._db_handler.write(read_db.data)
                        if write_db.error:
                            return DocumentResult({}, DB_WRITE_ERROR)
                        break
                return DocumentResult({}, SUCCESS)
            else:
                return DocumentResult({}, DB_WRITE_ERROR)
        except Exception as e:
            return DocumentResult({}, DB_READ_ERROR)
    
    # Method: Query the vector database
    def query_document(self, document_id:str, query: str) -> dict:
        try:
            # Read the database
            read_db = self._db_handler.read()
            if read_db.error:
                return {"error": DB_READ_ERROR}

            # Check if the document id exists and embedding is True
            document_id_found = False
            vector_db_path = None
            for doc in read_db.data:
                if doc['id'] == document_id:
                    if doc['embedded'] == "False":
                        return {"error": DOC_EMBEDDING_ERROR}
                    document_id_found = True
                    vector_db_path = os.path.join(self._vector_db_path, doc['id'])
                    break
            if not document_id_found:
                return {"error": DOC_ID_ERROR}
            
            # Query the vector database
            query_doc = QueryDocuments(f"{query}", vector_db_path)
            result = query_doc.query()
            return {
                "result": result,
                "error": SUCCESS
            }
        except Exception as e:
            print(f"Error querying document: {e}")
            return {"error": DB_READ_ERROR}