class BitHelper:
    @staticmethod
    def string_to_bit_array(s: str) -> list[int]:
        return [int(bit) for char in s for bit in format(ord(char), '08b')]
    
    @staticmethod
    def bits_to_char(bits: list[int]) -> str:
        print(bits)
        binary_str = ''.join(str(bit) for bit in bits)
        
        ascii_value = int(binary_str, 2)
        
        return chr(ascii_value)