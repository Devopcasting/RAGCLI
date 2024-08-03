import boto3
from langchain_community.embeddings import BedrockEmbeddings
import json

class AWSBedrockEmbedding:
    def __init__(self) -> None:
        self.bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-east-1'
        )
    
    def get_aws_bedrock_embedding(self):
        """Perform AWS Bedrock Embedding"""
        bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-east-1',
        )
        aws_bedrock_embedding = BedrockEmbeddings(
            credentials_profile_name="default", region_name="us-east-1", model_id="amazon.titan-embed-text-v1", client=bedrock_client
        )
        return aws_bedrock_embedding
        