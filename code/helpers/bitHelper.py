class BitHelper:
    """
    A utility class that provides static methods to convert strings to bit arrays and bits to characters.
    """

    @staticmethod
    def string_to_bit_array(s: str) -> list[int]:
        """
        Converts a string to a list of bits, where each character in the string is represented
        by an 8-bit binary number (ASCII).

        Args:
            s (str): The input string to be converted.

        Returns:
            list[int]: A list of integers (0 or 1) representing the bit array for the given string.
        
        Example:
            >>> BitHelper.string_to_bit_array('A')
            [0, 1, 0, 0, 0, 0, 0, 1]
        """
        return [int(bit) for char in s for bit in format(ord(char), '08b')]

    @staticmethod
    def bits_to_char(bits: list[int]) -> str:
        """
        Converts a list of bits (0s and 1s) back to a character by interpreting the bits as an ASCII value.

        Args:
            bits (list[int]): A list of bits (0s and 1s) that represent a single character.

        Returns:
            str: The corresponding character represented by the bits.

        Example:
            >>> BitHelper.bits_to_char([0, 1, 0, 0, 0, 0, 0, 1])
            'A'
        """
        binary_str = ''.join(str(bit) for bit in bits)
        ascii_value = int(binary_str, 2)
        return chr(ascii_value)
