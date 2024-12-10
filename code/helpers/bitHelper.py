class BitHelper:
    """
    A utility class that provides static methods to convert strings to bit arrays and bits to characters,
    using consistent encoding (UTF-8 by default).
    """

    @staticmethod
    def string_to_bit_array(s: str, encoding='utf-8') -> list[int]:
        """
        Converts a string to a list of bits, using the specified encoding.

        Args:
            s (str): The input string to be converted.
            encoding (str): The encoding to use for the conversion (default is 'utf-8').

        Returns:
            list[int]: A list of integers (0 or 1) representing the bit array for the given string.

        Example:
            >>> BitHelper.string_to_bit_array('A')
            [0, 1, 0, 0, 0, 0, 0, 1]
        """
        byte_array = s.encode(encoding)
        return [int(bit) for byte in byte_array for bit in format(byte, '08b')]

    @staticmethod
    def bits_to_char(bits: list[int], encoding='utf-8') -> str:
        """
        Converts a list of bits back to a string using the specified encoding.

        Args:
            bits (list[int]): A list of bits to convert.
            encoding (str): The encoding used for conversion (default is 'utf-8').

        Returns:
            str: The decoded character.

        Example:
            >>> BitHelper.bits_to_char([0, 1, 0, 0, 0, 0, 0, 1])
            'A'
        """
        if len(bits) % 8 != 0:
            raise ValueError("Bit list length must be a multiple of 8.")

        # Group bits into bytes and convert each byte from binary to integer
        byte_array = bytes(
            int(''.join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8))

        return byte_array.decode(encoding)
