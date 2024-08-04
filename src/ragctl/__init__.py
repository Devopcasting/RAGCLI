# ragctl/__init__.py

__app_name__ = "ragctl"
__version__ = "0.1.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    JSON_ERROR,
    ID_ERROR,
    DB_WRITE_ERROR,
    DB_READ_ERROR,
    AWS_DIR_ERROR,
    AWS_FILE_ERROR,
    DOC_ID_ERROR,
    DOC_EMBEDDING_ERROR,
    DOC_NOT_FOUND_ERROR,
    DOC_PROCESS_ERROR
) = range(13)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    JSON_ERROR: "json file error",
    ID_ERROR: "document id error",
    DB_WRITE_ERROR: "database write error",
    DB_READ_ERROR: "database read error",
    AWS_DIR_ERROR: "aws directory error",
    AWS_FILE_ERROR: "aws file error",
    DOC_ID_ERROR: "document id not found",
    DOC_EMBEDDING_ERROR: "document is already embedded",
    DOC_NOT_FOUND_ERROR: "documents not found",
    DOC_PROCESS_ERROR: "document processing error"
}