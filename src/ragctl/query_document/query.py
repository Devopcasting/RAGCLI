from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from ragctl.embedding.bedrock import AWSBedrockEmbedding

class QueryDocuments:
    def __init__(self, question: str, document_path: str) -> None:
        self.question = question
        self.document_path = document_path
    
    def query(self) -> str:
        print("Querying the document...")
        # Create the prompt
        PROMPT_TEMPLATE = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """
        embedding = AWSBedrockEmbedding()
        db = Chroma(persist_directory=self.document_path,
                    embedding_function=embedding.get_aws_bedrock_embedding())
        # Similarity search
        docs = db.similarity_search(self.question, k=5)
        # Context
        context = "\n\n---\n\n".join([doc.page_content for doc in docs])
        # Prompt
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format_messages(context=context, question=self.question)
        # LLM
        llm = Ollama(model="mistral")
        # Response
        response = llm.invoke(prompt)
     
        # Source
        sources = [doc.metadata.get("source", None) for doc in docs]
        # Format the response
        formatted_response = f"""
Question: {self.question}

Response: {response}

Sources: {sources}
        """
        return formatted_response