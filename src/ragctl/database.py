# ragctl/database.py

import configparser
from pathlib import Path
import json
from typing import Any, Dict, List, NamedTuple
from ragctl import (
    DB_WRITE_ERROR, SUCCESS, DB_READ_ERROR
)

# Set default database path
DEFAULT_DB_FILE = Path.home().joinpath("." + Path.home().stem + "_ragctl.json")

def get_database_path(config_file: Path) -> Path:
    """
        Args:
            config_file: Path to the configuration file
        Return:
            Path to the database file
    """
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    """
        Args:
            db_path: Path to the database file
        Return:
            SUCCESS if the database file is initialized successfully
            DB_WRITE_ERROR if there is an error writing to the database file
    """
    try:
        db_path.write_text("[]")
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR

class DBResponse(NamedTuple):
    """
        A named tuple to represent the response from the database
    """
    data: List[Dict[str, Any]]
    error: int

class DatabaseHandler:
    """
        A class to handle the database operations
    """
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
    
    def read(self) -> DBResponse:
        """
            Read the database file
            Return:
                DBResponse: A named tuple containing the data and error code
        """
        try:
            with open(self._db_path, "r") as file:
                try:
                    return DBResponse(json.load(file), SUCCESS)
                except json.JSONDecodeError:
                    return DBResponse([], DB_READ_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)
    
    def write(self, data: List[Dict[str, Any]]) -> DBResponse:
        """
            Write to the database file
            Args:
                data: List of dictionaries to be written to the database
            Return:
                DBResponse: A named tuple containing the data and error code
        """
        try:
            with open(self._db_path, "w") as file:
                json.dump(data, file, indent=4)
                return DBResponse(data, SUCCESS)
        except OSError:
            return DBResponse(data, DB_WRITE_ERROR)