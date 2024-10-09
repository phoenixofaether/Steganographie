from helpers.fileHelper import FileHelper
from steganography import Steganograph

steganograph: Steganograph | None = None

print("Welcome to this steganography application.\nDevelopt by Nico Glaner, Marc Güntensperger and David Oberkalmsteiner.")
print("---------------------------------------------------------------------")


while not steganograph or not steganograph.isInitialized:
    print("Press enter and select the JSON-file with your synonyms:")
    input()
    try:
        steganograph = Steganograph(FileHelper.select_file())
    except Exception as error:
        print(error)

while True:
    print("What would you like to do?")
    print("Type \"1\" to read a hidden text from a file (default), type \"2\" to hide something inside a text, type \"3\" to exit:")
    actionInput = input()


    if actionInput == "2":
        print("Select the text file you want to hide a text in:")
        textToWriteToPath = FileHelper.select_file()
        textToWriteTo = FileHelper.read_file(textToWriteToPath)
        print("Type in the text you would like to hide inside the file:")
        hiddenText = input()
        updatedtext = steganograph.write(textToWriteTo, hiddenText)
        FileHelper.write_file(textToWriteToPath, updatedtext)
        print("Successfully hidden your text inside the text file.")
    elif actionInput == "3":
        exit()
    else:
        print("Select the txt file you want to read a hidden text from:")
        textToReadFrom = FileHelper.read_file(FileHelper.select_file())
        hiddenText = steganograph.read(textToReadFrom)
        print(f'The hidden text is: "{hiddenText}"')