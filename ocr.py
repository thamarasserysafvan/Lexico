import io
import os
import pytesseract
from PIL import Image
from py_common_subseq import find_common_subsequences

# Set the path to the Tesseract executable if it's not in your PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def getData(image_path):
    try:
        with io.open(image_path, 'rb') as image_file:
            image = Image.open(io.BytesIO(image_file.read()))
            image.show()
            text=''
            text = pytesseract.image_to_string(image_path, config="--psm 6")
            print(text)

            # text = pytesseract.image_to_string(image)
            character=''
            if len(text) == 1:
                character = text[0]
            else:
                print("Warning: Image contains more than one character.")

            print(f"Extracted character: {character}")
            print(text)
        return text
    except Exception as e:
        print(f"Error processing image: {e}")
        raise

def processData(text):
    symbolsData = [(char, 1) for char in text if char.isalnum()]
    word = "".join(char for char, _ in symbolsData)
    return word, symbolsData

def assess(origWord, writtenWord):
    lcs = max(find_common_subsequences(origWord, writtenWord), key=len)
    i = 0
    j = 0
    retList = []
    while i < len(lcs):
        if lcs[i] == origWord[j]:
            retList.append((origWord[j], 1))
            i += 1
        else:
            retList.append((origWord[j], 0))
        j += 1
    return retList

if __name__ == "__main__":
    writtenWord = processData(getData('static/image.png'))[0]
    print(assess("anggt", writtenWord))
