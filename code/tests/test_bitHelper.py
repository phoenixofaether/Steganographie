import unittest

from code.helpers.bitHelper import BitHelper

class Test_BitHelper(unittest.TestCase):
    def test_string_to_bit_array(self):
        result = BitHelper.string_to_bit_array("A")
        expected = [0, 1, 0, 0, 0, 0, 0, 1]  # ASCII for 'A' is 65 or '01000001' in binary
        self.assertEqual(result, expected)

        result = BitHelper.string_to_bit_array("B")
        expected = [0, 1, 0, 0, 0, 0, 1, 0]  # ASCII for 'B' is 66 or '01000010' in binary
        self.assertEqual(result, expected)

    def test_bits_to_char(self):
        result = BitHelper.bits_to_char([0, 1, 0, 0, 0, 0, 0, 1])
        expected = "A"  # should convert back to 'A'
        self.assertEqual(result, expected)

        result = BitHelper.bits_to_char([0, 1, 0, 0, 0, 0, 1, 0])
        expected = "B"  # should convert back to 'B'
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()