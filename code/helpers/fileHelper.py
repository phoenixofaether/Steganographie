import json
import tkinter as tk
from tkinter import filedialog

class FileHelper:
    # From chatgpt.com
    def select_file() -> str:
        # Create a hidden Tkinter window
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        # Open the file dialog and allow the user to select a file
        file_path = filedialog.askopenfilename(title="Select a file")

        return file_path
    
    def read_file(path: str) -> str:
        file = open(path, "r")
        return file.read()
    
    def read_json_file(path: str):
        file = open(path, "r")
        return json.load(file)