import unittest
from unittest.mock import call, patch
from code.steganography import Steganograph
from models.Synonym import Synonym

class TestSteganograph(unittest.TestCase):
    
    @patch('helpers.fileHelper.FileHelper.read_json_file')
    def test_init_valid_config(self, mock_read_json_file):
        # Test the initialization of Steganograph with a valid configuration file.
        # Arrange: Mock the read_json_file method to return a list of valid synonyms.
        mock_read_json_file.return_value = [
            {"word": "happy", "synonym": "joyful"},
            {"word": "sad", "synonym": "unhappy"}
        ]
        
        # Act: Create a Steganograph instance with the mocked configuration.
        steganograph = Steganograph("config.json")
        
        # Assert: Verify the instance is initialized and synonyms are correctly loaded.
        self.assertTrue(steganograph.isInitialized)
        self.assertEqual(len(steganograph.synonyms), 2)
        self.assertEqual(steganograph.synonyms[0].word, "happy")
        self.assertEqual(steganograph.synonyms[0].synonym, "joyful")

    @patch('helpers.fileHelper.FileHelper.read_json_file')
    def test_init_invalid_config(self, mock_read_json_file):
        # Test the initialization of Steganograph with an invalid configuration file.
        # Arrange: Mock the read_json_file method to return an invalid data format.
        mock_read_json_file.return_value = "invalid"
        
        # Act & Assert: Ensure an exception is raised when the configuration is invalid.
        with self.assertRaises(ValueError) as context:
            Steganograph("config.json")
        self.assertEqual(str(context.exception), "The configuration file has a wrong format.")
    
    def test_write_with_hidden_text(self):
        # Test the embedding of a hidden message in a given text using synonyms.
        # Arrange: Manually initialize a Steganograph instance with predefined synonyms.
        steganograph = Steganograph.__new__(Steganograph)
        steganograph.synonyms = [
            Synonym(word="happy", synonym="joyful"),
            Synonym(word="sad", synonym="unhappy")
        ]
        steganograph.END_OF_SECRET = [1, 1]
        steganograph.isInitialized = True
        
        with patch('helpers.bitHelper.BitHelper.string_to_bit_array') as mock_bit_array:
            # Mock the bit array conversion for the hidden text.
            mock_bit_array.return_value = [0, 1, 1, 0]  # Example bit array for 'ok'.
            text_to_write = "I am happy today but also sad and joyful. I would be happy if the test runs, sad if it doesn't and joyful if the whole project runs."
            hidden_text = "ok"
        
            # Act: Write the hidden text into the provided text.
            result = steganograph.write(text_to_write, hidden_text)
        
        # Assert: Check if the resulting text contains the hidden message.
        expected_result = "I am happy today but also unhappy and joyful. I would be happy if the test runs, unhappy if it doesn't and joyful if the whole project runs."
        print(result)
        self.assertEqual(result, expected_result)

    def test_write_text_too_small(self):
        # Test the behavior when the provided text is too small to embed the hidden message.
        # Arrange: Manually initialize a Steganograph instance and mock bit array conversion.
        steganograph = Steganograph.__new__(Steganograph)
        steganograph.synonyms = [
            Synonym(word="happy", synonym="joyful")
        ]
        steganograph.isInitialized = True
        
        with patch('helpers.bitHelper.BitHelper.string_to_bit_array') as mock_bit_array:
            # Mock the bit array to be too long for the given text.
            mock_bit_array.return_value = [1, 0, 1, 1]
            text_to_write = "I am happy."
            hidden_text = "secret"
        
            # Act & Assert: Ensure an exception is raised when the text is too small.
            with self.assertRaises(ValueError) as context:
                steganograph.write(text_to_write, hidden_text)
            self.assertEqual(str(context.exception), "The provided text file is too small to hide your text.")
    
    def test_read_hidden_text(self):
        # Test the extraction of a hidden message from a text containing embedded bits.
        # Arrange: Manually initialize a Steganograph instance and mock bit-to-char conversion.
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
            # Mock the bit-to-char conversion and define expected calls.
            mock_bits_to_char.return_value = "11"  
            expected_calls = [call(list([0, 1, 1, 0]))]

            # Act: Read the hidden message from the text.
            result = steganograph.read(text_with_hidden_message)
            print(result)

        # Assert: Verify the extracted hidden message matches expectations.
        self.assertEqual(result, "11")
        mock_bits_to_char.assert_has_calls(expected_calls, any_order=False)

    def test_read_no_hidden_message(self):
        # Test the behavior when no hidden message is present in the text.
        # Arrange: Manually initialize a Steganograph instance with predefined synonyms.
        steganograph = Steganograph.__new__(Steganograph)
        steganograph.synonyms = [
            Synonym(word="happy", synonym="joyful")
        ]
        steganograph.isInitialized = True
        text_with_no_hidden_message = "I am happy."
        
        # Act & Assert: Ensure an exception is raised when no hidden message is found.
        with self.assertRaises(ValueError) as context:
            steganograph.read(text_with_no_hidden_message)
        self.assertEqual(str(context.exception), "No secret was found in the text.")
    
if __name__ == '__main__':
    unittest.main()
