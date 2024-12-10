import unittest
from helpers.bitHelper import BitHelper


class TestBitHelper(unittest.TestCase):
    def test_string_to_bit_array_ascii(self):
        # Test with a simple ASCII character
        result = BitHelper.string_to_bit_array('A')
        expected = [0, 1, 0, 0, 0, 0, 0, 1]  # Binary for ASCII 'A'
        self.assertEqual(result, expected)

    def test_string_to_bit_array_extended_unicode(self):
        # Test with an extended Unicode character (e.g., ö)
        result = BitHelper.string_to_bit_array('ö')
        # UTF-8 encoding for ö is two bytes: [11000011, 10110110]
        expected = [1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0]
        self.assertEqual(result, expected)

    def test_bits_to_char_ascii(self):
        # Test converting bits back to ASCII character
        bits = [0, 1, 0, 0, 0, 0, 0, 1]  # Binary for ASCII 'A'
        result = BitHelper.bits_to_char(bits)
        self.assertEqual(result, 'A')

    def test_bits_to_char_extended_unicode(self):
        # Test converting bits back to an extended Unicode character (e.g., ö)
        bits = [1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1,
                1, 0, 1, 1, 0]  # Binary for UTF-8 'ö'
        result = BitHelper.bits_to_char(bits)
        self.assertEqual(result, 'ö')

    def test_string_to_bit_array_and_back(self):
        # Round trip test: convert string to bits and back to string
        original_string = "Hello, 🌍!"
        bits = BitHelper.string_to_bit_array(original_string)
        decoded_string = BitHelper.bits_to_char(bits)
        self.assertEqual(decoded_string, original_string)

    def test_bits_to_char_invalid_length(self):
        # Test with an invalid number of bits (not a multiple of 8)
        bits = [1, 0, 1]  # Invalid length
        with self.assertRaises(ValueError) as context:
            BitHelper.bits_to_char(bits)
        self.assertIn("Bit list length must be a multiple of 8",
                      str(context.exception))


if __name__ == '__main__':
    unittest.main()
