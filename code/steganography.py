from helpers.fileHelper import FileHelper
from models.Synonym import Synonym

class Steganograph:
    synonyms: list[Synonym]
    isInitialized: bool
    def __init__(self, pathToConfig: str) -> None:
        self.synonyms = list()
        self.isInitialized = False
        self.__validateAndApplyConfig(FileHelper.read_json_file(pathToConfig))
        self.isInitialized = True
    
    def write(self, textToWriteTo: str, hiddenText: str):
        pass

    def read(self, textToReadFrom: str):
        pass

    def __validateAndApplyConfig(self, jsonData: any) -> None:
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