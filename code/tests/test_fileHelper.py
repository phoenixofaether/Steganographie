import unittest
from unittest.mock import patch, mock_open
import json
from helpers.fileHelper import FileHelper

class Test_FileHelper(unittest.TestCase):

    @patch('helpers.fileHelper.filedialog.askopenfilename', return_value="test.txt")
    @patch('helpers.fileHelper.tk.Tk')
    def test_select_file(self, mock_tk, mock_filedialog):
        """
        Test the select_file method to ensure the correct file path is returned.
        """
        result = FileHelper.select_file()
        self.assertEqual(result, "test.txt")
        mock_tk.assert_called_once()
        mock_filedialog.assert_called_once_with(title="Select a file")

    @patch('builtins.open', new_callable=mock_open, read_data="This is the content of the file.")
    def test_read_file(self, mock_file):
        """
        Test the read_file method to ensure it correctly reads file content.
        """
        result = FileHelper.read_file("test.txt")
        mock_file.assert_called_once_with("test.txt", "r")
        self.assertEqual(result, "This is the content of the file.")

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({"key": "value"}))
    def test_read_json_file(self, mock_file):
        """
        Test the read_json_file method to ensure it correctly parses JSON content.
        """
        result = FileHelper.read_json_file("config.json")
        mock_file.assert_called_once_with("config.json", "r")
        self.assertEqual(result, {"key": "value"})

    @patch('builtins.open', new_callable=mock_open)
    def test_write_file(self, mock_file):
        """
        Test the write_file method to ensure it correctly writes content to the file.
        """
        FileHelper.write_file("output.txt", "This is the content to write.")
        mock_file.assert_called_once_with("output.txt", "w")
        mock_file().write.assert_called_once_with("This is the content to write.")

if __name__ == "__main__":
    unittest.main()
