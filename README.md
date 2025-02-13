# Document Processing Script

This project contains a Python script designed to automate the process of renaming and saving documents into proper folders based on specific naming conventions and rules. This script was developed to streamline document management processes.

## Project Structure

- `observer.py`: Monitors file system events and triggers the main script when changes are detected.
- `config.py`: Contains configuration settings and naming conventions used in the project.
- `functions.py`: Includes helper functions for processing file names, reviewing references, and handling notifications.
- `classes.py`: Defines classes for document handling, including GUI components for user interaction.
- `main.py`: The main script that ties everything together and executes the document processing logic.

## Features

- **File Renaming**: Automatically renames files based on specific patterns.
- **File Sorting**: Moves files to appropriate directories based on their names.
- **Conflict Resolution**: Handles file conflicts by providing options to replace or keep both files.
- **Notifications**: Sends notifications to the user about the success or failure of operations.
## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/document-processing-script.git
    ```
2. **Navigate to the project directory**:
    ```sh
    cd document-processing-script
    ```
3. **Create a virtual environment** (optional but recommended):
    ```sh
    python -m venv venv
    ```
4. **Activate the virtual environment**:

    On Windows:
    ```sh
    .\venv\Scripts\activate
    ```

    On macOS and Linux:
    ```sh
    source venv/bin/activate
    ```
5. **Install the required packages**:
    ```sh
    pip install watchdog PyQt5 winotify
    ```

## Usage

To use the script, run the `observer.py` file to start monitoring the specified directory for changes:

```sh
python adapted_observer.py