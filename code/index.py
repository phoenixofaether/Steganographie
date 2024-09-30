from helpers.fileHelper import FileHelper
from steganography import Steganograph

steganograph: Steganograph = None

print("Welcome to this steganography application.\nDevelopt by Nico Glaner, Marc Güntensperger and David Oberkalmsteiner.")
print("---------------------------------------------------------------------")
print("Press enter and select the JSON-file with your synonyms:")
input()

while not steganograph or not steganograph.isInitialized:
    try:
        steganograph = Steganograph(FileHelper.select_file())
    except Exception as error:
        print(error)
        input()

print("What would you like to do?")
print("Type 1 to read a hidden Text from a file (default), type 2 to hide something inside a text:")
input = input()


if input == "2":
    print("Hide in text")
    #hide in text
else:
    print("Read from text")
    #read from text