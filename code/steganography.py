from helpers.bitHelper import BitHelper
from helpers.fileHelper import FileHelper
from models.Synonym import Synonym

class Steganograph:
    """
    A class that hides and retrieves secret text inside another text using synonym substitution
    and bit-level encoding.

    Attributes:
        LENGTH-OF-BYTE: A constand defining the number of bits that result in a byte
        END_OF_SECRET (list[int]): A constant marking the end of the hidden message in a bit array.
        synonyms (list[Synonym]): A list of `Synonym` objects used for encoding and decoding.
        isInitialized (bool): A flag indicating if the configuration has been successfully loaded.

    Methods:
        __init__(pathToConfig: str) -> None:
            Initializes the Steganograph object and loads configuration from the provided JSON file.
        
        write(textToWriteTo: str, hiddenText: str) -> str:
            Hides the `hiddenText` inside the `textToWriteTo` using synonyms and bit-level encoding.
        
        read(textToReadFrom: str) -> str:
            Extracts the hidden message from the `textToReadFrom` text using synonym substitution.
        
        __validateAndApplyConfig(jsonData: Any) -> None:
            Validates and applies the configuration for the synonyms from a JSON object.
    """
    LENGTH_OF_BYTE: int = 8
    END_OF_SECRET = [1, 1, 1, 1, 1, 1, 1, 1]  # extremely rare unicode character
    synonyms: list[Synonym]
    isInitialized: bool

    def __init__(self, pathToConfig: str) -> None:
        """
        Initializes the Steganograph object by loading and applying a configuration file.

        Args:
            pathToConfig (str): The file path to the JSON configuration file containing synonyms.

        Raises:
            ValueError: If the configuration file format is invalid.
        """
        self.synonyms = list()
        self.isInitialized = False
        self.__validateAndApplyConfig(FileHelper.read_json_file(pathToConfig))
        self.isInitialized = True

    def write(self, textToWriteTo: str, hiddenText: str) -> str:
        """
        Hides the provided `hiddenText` inside `textToWriteTo` using synonyms for encoding
        and bit-level manipulation.

        Args:
            textToWriteTo (str): The text in which the hidden message will be embedded.
            hiddenText (str): The message to hide inside the main text.

        Returns:
            str: The text with the hidden message encoded.

        Raises:
            ValueError: If the provided text is too small to hide the entire secret message.

        Example:
            >>> steganograph.write("This is a sample text.", "secret")
            'This is a synonym-based encoded text.'
        """
        textToWriteToIndex = 0
        currentWord = ""
        generatedText = ""
        bits = BitHelper.string_to_bit_array(hiddenText).__add__(self.END_OF_SECRET)
        currentBitIndex = 0

        while textToWriteToIndex < len(textToWriteTo):
            char = textToWriteTo[textToWriteToIndex]
            textToWriteToIndex += 1

            # read until non-alphabetic character, which means word is complete
            if char.isalpha():
                currentWord += char
                continue

            # if no word exists, continue
            if len(currentWord) == 0:
                generatedText += char
                continue

            # find match for current word
            match: Synonym | None = None
            for synonym in self.synonyms:
                if currentWord == synonym.word or currentWord == synonym.synonym:
                    match = synonym
                    break  

            if match is None:
                generatedText += currentWord
            else:
                # if match is found, replace it with synonym depending on currentBit
                currentBit = bits[currentBitIndex]
                currentBitIndex += 1
                
                if currentBit == 0:
                    generatedText += match.word
                else:
                    generatedText += match.synonym
            
            currentWord = ""
            generatedText += char

            # if the secret text is completed, return the whole text
            if currentBitIndex == len(bits):
                return generatedText + textToWriteTo[textToWriteToIndex:]
            
        raise ValueError("The provided text file is too small to hide your text.")

    def read(self, textToReadFrom: str) -> str:
        """
        Extracts the hidden message from the provided text by decoding the synonyms back into bits.

        Args:
            textToReadFrom (str): The text from which to extract the hidden message.

        Returns:
            str: The hidden message extracted from the text.

        Raises:
            ValueError: If no secret message is found in the text.

        Example:
            >>> steganograph.read("This is a synonym-based encoded text.")
            'secret'
        """
        textToReadFromIndex = 0
        currentWord = ""
        secretTextBits: list[int] = []

        while textToReadFromIndex < len(textToReadFrom):
            char = textToReadFrom[textToReadFromIndex]
            textToReadFromIndex += 1

            # read until non-alphabetic character, which means word is complete
            if char.isalpha():
                currentWord += char
                continue

            # if no word exists, continue
            if len(currentWord) == 0:
                continue

            # find match for current word
            match: Synonym | None = None
            for synonym in self.synonyms:
                if currentWord == synonym.word or currentWord == synonym.synonym:
                    match = synonym
                    break
            
            if match is not None:
                # if match is found, translate match to secret coding and append to secretTextBits
                if currentWord == synonym.word:
                    secretTextBits.append(0)
                else:
                    secretTextBits.append(1)
                
                # if the newest bits equal the END_OF_SECRET, convert and return the secret
                if len(secretTextBits) % self.LENGTH_OF_BYTE == 0 and len(secretTextBits) > len(self.END_OF_SECRET):
                    if secretTextBits[-len(self.END_OF_SECRET):] == self.END_OF_SECRET:
                        return BitHelper.bits_to_char(secretTextBits[:-len(self.END_OF_SECRET)])
            currentWord = ""
            
        raise ValueError("No secret was found in the text.")

    def __validateAndApplyConfig(self, jsonData: dict | list) -> None:
        """
        Validates and applies the configuration for synonyms from a given JSON data.

        Args:
            jsonData (dict | list): The JSON data containing the configuration for the synonyms.

        Raises:
            ValueError: If the configuration file format or synonym structure is invalid.
        """
        if not isinstance(jsonData, list):
            raise ValueError("The configuration file has a wrong format.")

        for index in range(len(jsonData)):
            item = jsonData[index]
            
            if isinstance(item, dict):
                item = Synonym(word=item['word'], synonym=item['synonym'])

            if not isinstance(item, Synonym): 
                raise ValueError(f"The value with the index {index} is invalid.")
            
            for existingSynonym in self.synonyms:
                if existingSynonym.synonym == item.synonym or existingSynonym.word == item.synonym:
                    raise ValueError(f'The synonym "{item.synonym}" exists at least two times.')
                if existingSynonym.synonym == item.word or existingSynonym.word == item.word:
                    raise ValueError(f'The synonym "{item.word}" exists at least two times.')

            self.synonyms.append(item)
