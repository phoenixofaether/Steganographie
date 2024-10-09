import json
import tkinter as tk
from tkinter import filedialog
from typing import Any

class FileHelper:
    """
    A utility class for file operations such as selecting, reading, and writing files.
    It provides static methods for interacting with files and handling JSON data.

    Methods:
        select_file() -> str:
            Opens a file dialog for the user to select a file and returns the selected file's path.

        read_file(path: str) -> str:
            Reads the contents of a file at the given path and returns it as a string.

        read_json_file(path: str) -> Any:
            Reads a JSON file from the given path and returns the parsed JSON data.

        write_file(path: str, content: str) -> None:
            Writes the provided content to the file at the given path, overwriting any existing content.
    """

    @staticmethod
    def select_file() -> str:
        """
        Opens a file dialog for the user to select a file. A hidden Tkinter window is created
        to allow file selection without displaying the main window.

        Returns:
            str: The full path of the selected file.

        Example:
            >>> file_path = FileHelper.select_file()
            Selected file: 'C:/path/to/selected_file.txt'
        """
        # Create a hidden Tkinter window
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        # Open the file dialog and allow the user to select a file
        file_path = filedialog.askopenfilename(title="Select a file")

        print(f"Selected file: '{file_path}'")

        return file_path

    @staticmethod
    def read_file(path: str) -> str:
        """
        Reads the contents of the file at the specified path and returns it as a string.

        Args:
            path (str): The path to the file to be read.

        Returns:
            str: The contents of the file.

        Example:
            >>> content = FileHelper.read_file("example.txt")
            >>> print(content)
            'This is the content of the file.'
        """
        file = open(path, "r")
        return file.read()

    @staticmethod
    def read_json_file(path: str) -> Any:
        """
        Reads the contents of a JSON file at the specified path and returns the parsed data.

        Args:
            path (str): The path to the JSON file to be read.

        Returns:
            Any: The parsed JSON data.

        Example:
            >>> data = FileHelper.read_json_file("config.json")
            >>> print(data)
            {'key': 'value', 'settings': {...}}
        """
        file = open(path, "r")
        return json.load(file)

    @staticmethod
    def write_file(path: str, content: str) -> None:
        """
        Writes the provided content to a file at the specified path. 
        If the file exists, it will be overwritten.

        Args:
            path (str): The path to the file where the content will be written.
            content (str): The content to write to the file.

        Example:
            >>> FileHelper.write_file("output.txt", "This is the content to write.")
        """
        with open(path, "w") as file:  # Open file in write mode, which overwrites existing content
            file.write(content)
