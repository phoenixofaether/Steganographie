from typing import Any
from helpers.bitHelper import BitHelper
from helpers.fileHelper import FileHelper
from models.Synonym import Synonym

class Steganograph:
    __END_OF_SECRET = [1, 0, 0, 0, 0, 0, 0, 0] # ASCII charachter only use 7 bits, so the 8th bit can be used to mark the end
    synonyms: list[Synonym]
    isInitialized: bool
    def __init__(self, pathToConfig: str) -> None:
        self.synonyms = list()
        self.isInitialized = False
        self.__validateAndApplyConfig(FileHelper.read_json_file(pathToConfig))
        self.isInitialized = True
    
    def write(self, textToWriteTo: str, hiddenText: str) -> str:
        textToWriteToIndex = 0
        currentWord = ""
        generatedText = ""
        bits = BitHelper.string_to_bit_array(hiddenText).__add__(self.__END_OF_SECRET)
        currentBitIndex = 0

        while textToWriteToIndex < len(textToWriteTo):
            char = textToWriteTo[textToWriteToIndex]
            textToWriteToIndex += 1

            # read until non alphabetic character, which means word is complete
            if (char.isalpha()):
                currentWord += char
                continue

            # if no word exists, continue
            if (len(currentWord) == 0):
                continue

            # find match for current word
            match: Synonym | None = None
            for synonym in self.synonyms:
                if (currentWord == synonym.word or currentWord == synonym.synonym):
                    match = synonym
                    break  

            if (match is None):
                generatedText += currentWord
            else:
                # if match is found, replace it with synonym depending on currentBit
                currentBit = bits[currentBitIndex]
                currentBitIndex += 1
                
                if (currentBit == 0):
                    generatedText += match.word
                else:
                    generatedText += match.synonym
            
            currentWord = ""
            generatedText += char
            # if the secrettext is completed, the text as whole is returned 
            if (currentBitIndex == len(bits)):
                return generatedText + textToWriteTo[textToWriteToIndex:]
            
        raise ValueError("The provided text file is to small to hide your text.")

    def read(self, textToReadFrom: str) -> str:
        textToReadFromIndex = 0
        currentWord = ""
        secretTextByte: list[int] = []
        secretText = ""

        while textToReadFromIndex < len(textToReadFrom):
            char = textToReadFrom[textToReadFromIndex]
            textToReadFromIndex += 1

            # read until non alphabetic character, which means word is complete
            if (char.isalpha()):
                currentWord += char
                continue

            # if no word exists, continue
            if (len(currentWord) == 0):
                continue

            # find match for current word
            match: Synonym | None = None
            for synonym in self.synonyms:
                if (currentWord == synonym.word or currentWord == synonym.synonym):
                    match = synonym
                    break
            
            if (match is not None):
                # if match is found, translate match to secret coding and append to scretTextByte
                if (currentWord == synonym.word):
                    secretTextByte.append(0)
                else:
                    secretTextByte.append(1)
                
                # once secretTextByte contains 8 bits, convert it
                if (len(secretTextByte) == 8):
                    # if secretTextByte equals END_OF_SECRET constant stop reading and return secretText
                    if secretTextByte == self.__END_OF_SECRET:
                        return secretText
                    else:
                        secretText += BitHelper.bits_to_char(secretTextByte)
                    secretTextByte = []
            currentWord = ""
            
        raise ValueError("No secret was found in the text")

    def __validateAndApplyConfig(self, jsonData: Any) -> None:
        if not isinstance(jsonData, list):
            raise ValueError("The configuration file has a wrong format.")

        for index in range(len(jsonData)):
            item = jsonData[index]
            
            if isinstance(item, dict):
                item = Synonym(word=item['word'], synonym=item['synonym'])

            if not isinstance(item, Synonym): 
                raise ValueError(f"The value with the index {index} is invalid.")
            
            for existingSynonym in self.synonyms:
                if (existingSynonym.synonym == item.synonym or existingSynonym.word == item.synonym):
                    raise ValueError(f'The synonym "{item.synonym}" exists at least two times.')
                if (existingSynonym.synonym == item.word or existingSynonym.word == item.word):
                    raise ValueError(f'The synonym "{item.word}" exists at least two times.')

            self.synonyms.append(item)

    