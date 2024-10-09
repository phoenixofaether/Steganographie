class Synonym:
    """
    A class representing a pair of words that are considered synonyms, used in steganographic encoding.

    Attributes:
        word (str): The main word of the synonym pair. Translates to the bit 0.
        synonym (str): The synonym of the main word. Translates to the bit 1.

    Methods:
        __init__(word: str, synonym: str):
            Initializes the Synonym object with a word and its synonym.
    """

    word: str
    synonym: str

    def __init__(self, word: str, synonym: str):
        """
        Initializes the Synonym object with a word and its synonym.

        Args:
            word (str): The main word of the synonym pair.
            synonym (str): The synonym of the main word.

        Example:
            >>> synonym = Synonym("quick", "fast")
            >>> synonym.word
            'quick'
            >>> synonym.synonym
            'fast'
        """
        self.word = word
        self.synonym = synonym
