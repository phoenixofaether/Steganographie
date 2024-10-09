import unittest
from unittest.mock import call, patch
from code.steganography import Steganograph
from helpers.bitHelper import BitHelper
from helpers.fileHelper import FileHelper
from models.Synonym import Synonym

class TestSteganograph(unittest.TestCase):
    
    @patch('helpers.fileHelper.FileHelper.read_json_file')
    def test_init_valid_config(self, mock_read_json_file):
        # Arrange
        mock_read_json_file.return_value = [
            {"word": "happy", "synonym": "joyful"},
            {"word": "sad", "synonym": "unhappy"}
        ]
        
        # Act
        steganograph = Steganograph("config.json")
        
        # Assert
        self.assertTrue(steganograph.isInitialized)
        self.assertEqual(len(steganograph.synonyms), 2)
        self.assertEqual(steganograph.synonyms[0].word, "happy")
        self.assertEqual(steganograph.synonyms[0].synonym, "joyful")

    @patch('helpers.fileHelper.FileHelper.read_json_file')
    def test_init_invalid_config(self, mock_read_json_file):
        # Arrange
        mock_read_json_file.return_value = "invalid"
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            Steganograph("config.json")
        self.assertEqual(str(context.exception), "The configuration file has a wrong format.")
    
    def test_write_with_hidden_text(self):
        # Arrange
        steganograph = Steganograph.__new__(Steganograph)
        steganograph.synonyms = [
            Synonym(word="happy", synonym="joyful"),
            Synonym(word="sad", synonym="unhappy")
        ]
        steganograph.END_OF_SECRET = [1, 1]
        steganograph.isInitialized = True
        
        with patch('helpers.bitHelper.BitHelper.string_to_bit_array') as mock_bit_array:
            # Let's assume "ok" = [0, 1, 1, 0] (mocked) and add END_OF_SECRET = [1, 1]
            mock_bit_array.return_value = [0, 1, 1, 0] # 'ok'
            text_to_write = "I am happy today but also sad and joyful. I would be happy if the test runs, sad if it doesn't and joyful if the whole project runs."
            hidden_text = "ok"
        
            # Act
            result = steganograph.write(text_to_write, hidden_text)
        
        # Assert
        expected_result = "I am happy today but also unhappy and joyful. I would be happy if the test runs, unhappy if it doesn't and joyful if the whole project runs."
        print(result)
        self.assertEqual(result, expected_result)

    def test_write_text_too_small(self):
        # Arrange
        steganograph = Steganograph.__new__(Steganograph)
        steganograph.synonyms = [
            Synonym(word="happy", synonym="joyful")
        ]
        steganograph.isInitialized = True
        
        with patch('helpers.bitHelper.BitHelper.string_to_bit_array') as mock_bit_array:
            mock_bit_array.return_value = [1, 0, 1, 1]  # bit array + END_OF_SECRET will be too long
            text_to_write = "I am happy."
            hidden_text = "secret"
        
            # Act & Assert
            with self.assertRaises(ValueError) as context:
                steganograph.write(text_to_write, hidden_text)
            self.assertEqual(str(context.exception), "The provided text file is too small to hide your text.")
    
    def test_read_hidden_text(self):
        # Arrange
        steganograph = Steganograph.__new__(Steganograph)
        steganograph.synonyms = [
            Synonym(word="happy", synonym="joyful"),
            Synonym(word="sad", synonym="unhappy")
        ]
        steganograph.END_OF_SECRET = [1, 1]
        steganograph.LENGTH_OF_BYTE = 2
        steganograph.isInitialized = True
        text_with_hidden_message = "I am happy today but also unhappy and joyful. I would be happy if the test runs, unhappy if it doesn't and joyful if the whole project runs."

        with patch('helpers.bitHelper.BitHelper.bits_to_char') as mock_bits_to_char:
            mock_bits_to_char.return_value = "1"  
            expected_calls = [call(list([0, 1])), call(list([1, 0]))]

            # Act
            result = steganograph.read(text_with_hidden_message)

        # Assert
        self.assertEqual(result, "11")
        mock_bits_to_char.assert_has_calls(expected_calls, any_order=False)

    def test_read_no_hidden_message(self):
        # Arrange
        steganograph = Steganograph.__new__(Steganograph)
        steganograph.synonyms = [
            Synonym(word="happy", synonym="joyful")
        ]
        steganograph.isInitialized = True
        text_with_no_hidden_message = "I am happy."
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            steganograph.read(text_with_no_hidden_message)
        self.assertEqual(str(context.exception), "No secret was found in the text.")
    
if __name__ == '__main__':
    unittest.main()
