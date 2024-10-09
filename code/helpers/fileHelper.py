import json
import tkinter as tk
from tkinter import filedialog
from typing import Any

class FileHelper:
    # From chatgpt.com
    @staticmethod
    def select_file() -> str:
        # Create a hidden Tkinter window
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        # Open the file dialog and allow the user to select a file
        file_path = filedialog.askopenfilename(title="Select a file")

        print(f"Selected file: '{file_path}'")

        return file_path
    
    @staticmethod
    def read_file(path: str) -> str:
        file = open(path, "r")
        return file.read()
    
    @staticmethod
    def read_json_file(path: str) -> Any:
        file = open(path, "r")
        return json.load(file)
    
    @staticmethod
    def write_file(path: str, content: str):
        with open(path, "w") as file:  # Open file in write mode, which overwrites existing content
            file.write(content)