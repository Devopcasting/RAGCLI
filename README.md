RAGCTL - A CLI tool for Retrieval Augmented Generation
=====================================================

RAGCTL is a command-line interface tool designed to facilitate Retrieval Augmented Generation tasks. This tool provides a range of commands to manage and process documents, interact with VectorDB, and more.

Getting Started
---------------

To get started with RAGCTL, simply run the command `ragctl` in your terminal. This will display the available options and commands.

Options
-------

The following options are available:

* `-v`, `--version`: Display the version of RAGCTL.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Display this help message and exit.

Commands
--------

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

Usage Examples
--------------

* `ragctl add <document_list>`: Add a list of documents to the database.
* `ragctl delete <document_id>`: Delete a specific document.
* `ragctl list`: List all added documents.
* `ragctl process <document_id>`: Process a document and embed it into VectorDB.
* `ragctl query <query_string>`: Query the document database.

Contributing
------------

If you'd like to contribute to RAGCTL, please fork the repository and submit a pull request.

License
-------

RAGCTL is licensed under [MIT].

Contact
-------

For any questions or issues, please contact [devopcasting@gmail.com].