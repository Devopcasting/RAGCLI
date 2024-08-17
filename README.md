# RAGCTL - A CLI Tool for Retrieval Augmented Generation

RAGCTL is a command-line interface tool designed for Retrieval Augmented Generation (RAG). It allows users to upload documents in various formats, including DOCX, TEXT, and PDFs, and enables them to ask questions directly from the uploaded content.

## Technology Stack

RAGCTL is built using the following technologies:

1. **Langchain Framework**: Provides the foundation for the RAG workflow, enabling seamless integration of language models and document processing.
2. **Ollama**: A platform used to manage and deploy language models efficiently.
3. **Ollama Model Mistral**: The specific language model used within RAGCTL for generating responses.
4. **Python Typer**: A fast and intuitive library for building command-line interfaces in Python, which powers RAGCTL's CLI.
5. **Amazon Titan Text Embeddings Models**: Utilized for generating text embeddings, essential for document processing and querying within VectorDB.

## Getting AWS Secret Key and Access Key

To use RAGCTL with AWS services, you'll need to configure your AWS Secret Key and Access Key. Here's how you can obtain them:

1. **Log in to AWS Management Console**: Go to the [AWS Management Console](https://aws.amazon.com/console/) and sign in with your AWS credentials.

2. **Navigate to IAM**: In the AWS Management Console, search for **IAM** (Identity and Access Management) and click on it.

3. **Create a New User**:
   - In the IAM dashboard, click on **Users** and then **Add user**.
   - Provide a username and select **Programmatic access** as the access type.
   - Click **Next: Permissions** to set permissions.

4. **Set Permissions**:
   - You can attach existing policies directly or add the user to a group with the appropriate permissions.
   - For full access, you might attach the **AdministratorAccess** policy (be cautious with this level of access).

5. **Review and Create**:
   - Review the user's details and click **Create user**.

6. **Download or Copy the Access Keys**:
   - After the user is created, you will be provided with an **Access Key ID** and a **Secret Access Key**. You can download these credentials as a `.csv` file or copy them directly.

   **Important**: Keep these credentials secure and do not share them publicly.

## Getting Started

To get started with RAGCTL, simply run the command `ragctl` in your terminal. This will display the available options and commands.

## Options

The following options are available:

* `-v`, `--version`: Display the version of RAGCTL.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Display this help message and exit.

## Commands

RAGCTL provides the following commands:

### add

Add the list of documents to the database.

### delete

Delete a specific document.

### delete-all

Delete all the documents.

### init

Initialize the RAGCTL application and database.

### init-aws

Initialize AWS configuration.

### list

List all added documents.

### process

Process the added document and embed it into VectorDB.

### query

Query the document.

## Usage Examples

* `ragctl add <document_list>`: Add a list of documents to the database.
* `ragctl delete <document_id>`: Delete a specific document.
* `ragctl list`: List all added documents.
* `ragctl process <document_id>`: Process a document and embed it into VectorDB.
* `ragctl query <query_string>`: Query the document database.

## Contributing

If you'd like to contribute to RAGCTL, please fork the repository and submit a pull request.

## License

RAGCTL is licensed under [MIT].

## Contact

For any questions or issues, please contact [devopcasting@gmail.com].
