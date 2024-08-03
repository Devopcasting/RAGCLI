# ragctl/config.py

import configparser
from pathlib import Path
import typer
import os

from ragctl import (
    DIR_ERROR, FILE_ERROR, DB_WRITE_ERROR, SUCCESS ,__app_name__, AWS_DIR_ERROR, AWS_FILE_ERROR
)

# Set configuration path
CONFIG_PATH = Path(typer.get_app_dir(__app_name__))

# Set configuration file path
CONFIG_FILE = CONFIG_PATH / "config.ini"

# Set AWS folder path
AWS_PATH = os.path.join(os.path.expanduser("~"), ".aws")

# Set AWS Credentials path
AWS_CREDENTIALS_FILE = os.path.join(os.path.expanduser("~"), ".aws", "credentials")

# Set AWS Config path
AWS_CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".aws", "config")

# Function: Initialize the application
def init_app(db_path: str) -> int:
    init_config = _create_config()
    if init_config != SUCCESS:
        return init_config
    init_database = _create_database(db_path)
    if init_database != SUCCESS:
        return init_database
    return SUCCESS

# Function: Initialize AWS credentials and config
def init_aws(aws_access_key_id: str, aws_secret_access_key: str, aws_region: str) -> int:
    """
    Initialize AWS credentials and config files.

    Args:
        aws_access_key_id (str): The AWS access key ID.
        aws_secret_access_key (str): The AWS secret access key.
        aws_region (str): The AWS region.

    Returns:
        int: SUCCESS or an error code.
    """
    try:
        # Create AWS folder if it doesn't exist
        if not os.path.exists(AWS_PATH):
            try:
                os.makedirs(AWS_PATH, exist_ok=True)
            except OSError:
                return AWS_DIR_ERROR
    
        # Check if aws_access_key_id and aws_secret_access_key are provided
        if not aws_access_key_id and aws_secret_access_key:
            return AWS_FILE_ERROR
    
        # Write the AWS credentials to the credentials file
        with open(AWS_CREDENTIALS_FILE, "w") as credentials_file:
            credentials_file.write("[default]\n")
            credentials_file.write(f"aws_access_key_id = {aws_access_key_id}\n")
            credentials_file.write(f"aws_secret_access_key = {aws_secret_access_key}\n")
    
        # Check if aws_region is provided
        if aws_region:
            # Write the AWS config to the config file
            with open(AWS_CONFIG_FILE, "w") as config_file:
                config_file.write("[default]\n")
                config_file.write(f"region = {aws_region}\n")
                config_file.write("output = json\n")
        else:
            # Write the default AWS region to the config file
            with open(AWS_CONFIG_FILE, "w") as config_file:
                config_file.write("[default]\n")
                config_file.write("region = us-east-1\n")
                config_file.write("output = json\n")
        return SUCCESS
    except OSError:
            return AWS_FILE_ERROR

# Function: Create configuration file
def _create_config() -> int:
    # Check if configuration path exists
    if not CONFIG_PATH.exists():
        try:
            CONFIG_PATH.mkdir(parents=True, exist_ok=True)
        except OSError:
            return DIR_ERROR
    
    # Check if configuration file exists
    if not CONFIG_FILE.exists():
        try:
            CONFIG_FILE.touch(exist_ok=True)
        except OSError:
            return FILE_ERROR
    return SUCCESS

# Function: Create database
def _create_database(db_path: str) -> int:
    try:
        config_parser = configparser.ConfigParser()
        config_parser["General"] = {"database": db_path}
        with open(CONFIG_FILE, "w") as configfile:
            config_parser.write(configfile)
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR