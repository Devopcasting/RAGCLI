# ragctl/cli.py

from typing import Optional, List
from pathlib import Path
import typer
typer.core.rich = None
from ragctl import (
    __app_name__, __version__, ERRORS, SUCCESS, config, database, ragctl
)
from rich.table import Table
from rich.console import Console
import json

# Create instance of Typer
app = typer.Typer(help="RAGCTL - A CLI tool for Retrieval Augmented Generation",
                  pretty_exceptions_enable=False)

# Function: version_callback
def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(None, "--version", "-v", callback=version_callback, is_eager=True)
) -> None:
    return

# Function: Check the Configuration and Database file
def get_docs() -> ragctl.RagDocOperations:
    if config.CONFIG_FILE.exists():
        config_path = database.get_database_path(config.CONFIG_FILE)
    else:
        typer.secho('RAGCTL configuration file not found, Please run "ragctl init"', fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)
    if config_path.exists():
        return ragctl.RagDocOperations(config_path)
    else:
        typer.secho('RAGCTL database not found, Please run "ragctl init"', fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)

# Function: Check the AWS configuration
def check_aws_config() -> ragctl.RagDocOperations:
    if config.AWS_CREDENTIALS_FILE.exists() and config.AWS_CONFIG_FILE.exists():
        return ragctl.RagDocOperations(config.CONFIG_FILE)
    else:
        typer.secho('AWS configuration not found, Please run "ragctl init_aws"', fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)
    
# Command: Initialize the application and database
@app.command(help="Initialize the RAGCTL application and database.")
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE),
        "--db-path",
        "--db",
        prompt="ragctl database location?",
    ),
) -> None:
    """
    Initialize the RAGCTL application and database.

    This command sets up the necessary configuration and database for the RAGCTL application.
    It prompts the user for the database location and initializes.

    Args:
        db_path (str): The path to the database file.
    Returns:
        None
    """
    try:
        # Initialize the RAGCTL application and database.
        _init_app(db_path)
        _init_database(db_path)
        typer.secho(f'Initialize application and database successfully!', fg=typer.colors.GREEN, bold=True)
    except Exception as e:
        typer.secho(f'Initialize application and database failed: "{e}"', fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)

def _init_app(db_path: str) -> None:
    # Initialize application
    init_application = config.init_app(db_path)
    if init_application != SUCCESS:
        typer.secho(f'Initialize application failed: "{ERRORS[init_application]}"', fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)

def _init_database(db_path: str) -> None:
    # Initialize database
    init_database = database.init_database(Path(db_path))
    if init_database != SUCCESS:
        typer.secho(f'Initialize database failed: "{ERRORS[init_database]}"', fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)
    
# Command: Initialize AWS configuration
@app.command(help="Initialize AWS configuration.")
def init_aws(
    aws_access_key_id: str = typer.Option(
        str(), "--aws-access-key-id", prompt="AWS Access Key ID", help="AWS access key id"
    ),
    aws_secret_access_key: str = typer.Option(
        str(), "--aws-secret-access-key", prompt="AWS Secret Access Key", help="AWS secret access key"
    ),
    aws_region: str = typer.Option(
        "us-east-1", "--aws-region", prompt="AWS Region", help="AWS region"
    ),
) -> None:
    """
    Initialize AWS configuration.

    This command sets up the necessary AWS configuration for the RAGCTL application.
    It prompts the user for the AWS credentials and config files and initializes.

    Args:
        None
    Returns:
        None
    """
    try:
        # Initialize AWS configuration
        init_aws = config.init_aws(aws_access_key_id, aws_secret_access_key, aws_region)
        if init_aws != SUCCESS:
            typer.secho(f'Initialize AWS configuration failed: "{ERRORS[init_aws]}"', fg=typer.colors.RED, bold=True)
            raise typer.Exit(code=1)
        typer.secho(f'Initialize AWS configuration successfully!', fg=typer.colors.GREEN, bold=True)
    except Exception as e:
        typer.secho(f'Initialize AWS configuration failed: "{e}"', fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)

# Command: Add the list of documents
@app.command(help="Add the list of documents to the database.")
def add(
    documents_path: List[str] = typer.Argument(..., help="List of documents to add to the database."),
) -> None:
    """
    Add the list of documents to the database.

    This command adds the list of documents to the database.

    Args:
        documents_path (List[str]): List of documents to add to the database.
    Returns:
        None
    """
    try:
        rag_doc_operations = get_docs()
        add_docs, error = rag_doc_operations.add_docs(documents_path)
        if error != SUCCESS:
            typer.secho(f'Add documents failed: "{ERRORS[add_docs.error]}"', fg=typer.colors.RED, bold=True)
            raise typer.Exit(code=1)
        else:
            for doc in add_docs:
                if doc['status'] == 1:
                    typer.secho(f'Add document failed: "{doc["message"]}"', fg=typer.colors.RED, bold=True)
                else:
                    typer.secho(f'Add document successfully: "{doc["document"]}"', fg=typer.colors.GREEN, bold=True)
    except Exception as e:
        typer.secho(f'Add documents failed: "{e}"', fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)

# Command: List all the added documents
@app.command(help="List all added documents")
def list(
    output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)."),
) -> None:
    """
    List all the added documents in the database.

    This command lists all the added documents in the database.

    Args:
        output (str): Output format (table or json).
    Returns:
        None
    """
    
    rag_doc_operations = get_docs()
    docs, error = rag_doc_operations.get_docs_list()
    if error != SUCCESS or len(docs) == 0:
        typer.secho('No documents found in the database.', fg=typer.colors.YELLOW, bold=True)
        raise typer.Exit(code=1)
    else:
        if output.lower() == "json":
            # Format the JSON output
            json_output = []
            for doc in docs:
                json_output.append({
                    "id": doc['id'],
                    "md5sum": doc['md5sum'],
                    "size": doc['size'],
                    "name": doc['name'],
                    "embedded": doc['embedded']
                })
            typer.echo(json.dumps(json_output, indent=4))
        else:
            table = Table(title_justify="left")
            table.add_column("ID", width=6)
            table.add_column("Document", width=40)
            table.add_column("Size", width=10)
            table.add_column("Embedded", width=9)
            for doc in docs:
                table.add_row(str(doc['id']), doc['name'], str(doc['size']), str(doc['embedded']))
            # Display the table
            console = Console()
            console.print(table)
            typer.secho(f'Total added documents: {len(docs)}', fg=typer.colors.GREEN, bold=True)
    
# Command: Delete all the documents
@app.command(help="Delete all the documents")
def delete_all(
    force: bool = typer.Option(...,prompt="Delete all the documents?",
                               help="Force delete all the documents")
) -> None:
    """
    Delete all the documents in the database.

    This command deletes all the documents in the database.

    Args:
        None
    Returns:
        None
    """
    rag_doc_operations = get_docs()
    if force:
        # Delete all documents
        error = rag_doc_operations.delete_all_documents().error
        if error != SUCCESS:
            typer.secho(f'Delete documents failed: "{ERRORS[error]}"', fg=typer.colors.RED, bold=True)
            raise typer.Exit(code=1)
        else:
            typer.secho('All documents deleted successfully!', fg=typer.colors.GREEN, bold=True)
    else:
        typer.secho('Delete all documents canceled.', fg=typer.colors.YELLOW, bold=True)
        raise typer.Exit(code=1)

# Command: Delete a specific document
# Argument required: --documment-id
@app.command(help="Delete a specific document")
def delete(
    document_id: str = typer.Option(..., "--document-id", "-d", help="Document ID to delete"),
) -> None:
    """
    Delete a specific document in the database.

    This command deletes a specific document in the database.

    Args:
        document_id (str): Document ID to delete.
    Returns:
        None
    """
    rag_doc_operations = get_docs()
    error = rag_doc_operations.delete_document(document_id).error
    if error != SUCCESS:
        typer.secho(f'Delete document failed: "{ERRORS[error]}"', fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)
    else:
        typer.secho(f'Document deleted successfully: "{document_id}"', fg=typer.colors.GREEN, bold=True)

# Command: Process the added document and embed it into VectorDB
@app.command(help="Process the added document and embed it into VectorDB")
def process(
    document_id: str = typer.Option(..., "--document-id", "-d", help="Document ID to process"),
) -> None:
    """
    Process the added document and embed it into VectorDB.

    This command processes the added document and embed it into VectorDB.

    Args:
        document_id (str): Document ID to process.
    Returns:
        None
    """
    rag_doc_operations = get_docs()
    error = rag_doc_operations.process_document(document_id).error
    if error != SUCCESS:
        typer.secho(f'Process document failed: "{ERRORS[error]}"', fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)
    else:
        typer.secho(f'Process document successfully: "{document_id}"', fg=typer.colors.GREEN, bold=True)

# Command: Query the document.
# Arguments required: document id and query string
@app.command(help="Query the document")
def query(
    document_id: str = typer.Option(..., "--document-id", "-d", help="Document ID to query"),
    query: str = typer.Option(..., "--query", "-q", help="Query string"),
) -> None:
    """
    Query the document.

    This command queries the document.

    Args:
        document_id (str): Document ID to query.
        query (str): Query string.
    Returns:
        None
    """
    rag_doc_operations = get_docs()
    response = rag_doc_operations.query_document(document_id, query)
    if response['error'] != SUCCESS:
        typer.secho(f'Query document failed: "{ERRORS[response["error"]]}"', fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)
    else:
        typer.echo(response['result'])