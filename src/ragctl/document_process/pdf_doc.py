from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.schema.document import Document
from ragctl.data_chunk_process.chunk_process import DataChunkProcess
from ragctl.embedding.bedrock import AWSBedrockEmbedding
import os

class ProcessPDFDocument:
    def __init__(self, pdf_file, vector_db_path: str, hash: str):
        self.pdf_file = pdf_file
        # Join the vector_db_path and hash to get the folder path
        self.vector_db_path = os.path.join(vector_db_path, hash[-4:])
    
    def process(self) -> bool:
        try:
            # Load document
            data = self._load_document()
            # Split data into chunks
            data_chunk = self._split_data(data)
            # Create a hash named folder inside vector_db_path to store the embeddings
            os.makedirs(self.vector_db_path, exist_ok=True)
            self._save_to_chromadb(data_chunk)
            return True
        except Exception as e:
            return False

    def _load_document(self) -> list[Document]:
        loader = PyPDFLoader(self.pdf_file)
        data = loader.load()
        return data
    
    def _split_data(self, data) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, 
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False
        )
        return text_splitter.split_documents(data)

    def _save_to_chromadb(self, chunks: list[Document]) -> bool:
        try:
            processd_chunks = []
            for chunk in chunks:
                chunk_text = chunk.page_content
                data_chunk_processor = DataChunkProcess(chunk_text)
                processed_chunk = data_chunk_processor.process()
                # Create a new document with the processed chunk
                processd_chunks.append(Document(
                    page_content=processed_chunk["filtered_text"],
                    metadata=chunk.metadata))
            embedding = AWSBedrockEmbedding()
            vectordb = Chroma(persist_directory=self.vector_db_path, embedding_function=embedding.get_aws_bedrock_embedding())
            vectordb.add_documents(processd_chunks)
            return True
        except Exception as e:
            return False