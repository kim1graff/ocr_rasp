import sys
import getopt
import pytesseract
import cv2
import json
import numpy as np

params = sys.argv
arg_list = params[1:]
input_value = ""
output_value = ""

# Считываем параметры из командной строки.
try:
    short_options = "i:o:"
    long_options = ["input=", "output="]
    arguments, values = getopt.getopt(arg_list, short_options, long_options)
    for current_argument, current_value in arguments:
        if current_argument in ("-i", "--input"):
            input_value = current_value
        elif current_argument in ("-o", "--output"):
            output_value = current_value
except getopt.error as err:
    print(str(err))
    print("Не удалось распознать параметры")
    sys.exit(2)

# Для тестов. Раскомментировать для запуска.
# input_value = 'D:\\Work\\recognition\\тестирование\\frompdf.png'
# output_value = 'D:\\Work\\recognition\\тестирование\\log.json'

# Проверяем результат считывания.
if input_value == "" and output_value == "":
    print("Некорректно указаны параметры: input, output")
    sys.exit(2)

# Начинаем распознавание.
# Расположение библиотеки на 208 сервере.
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
img = cv2.imdecode(np.fromfile(input_value, dtype=np.uint8), cv2.IMREAD_COLOR)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

# Вывести изображение
# cv2.imshow('Result', img)
# cv2.waitKey(0)

# Для русского языка: lang='eng+rus'
# Старые настройки: config = r'--oem 3 --psm 3'
config = r'--oem 3 --psm 3'
data = pytesseract.image_to_data(img, lang='eng+rus', config=config)

words_json = {}
allWords = []
page_number = 1

for i, el in enumerate(data.splitlines()):

    if i == 0:
        continue

    word_info = el.split()
    if len(word_info) < 12:
        continue
    left = float(word_info[6])
    top = float(word_info[7])
    height = float(word_info[9])
    width = float(word_info[8])

    word_coord = {"textline": word_info[11],
                  "x1": left,
                  "y1": top + height,
                  "x2": left + width,
                  "y2": top,
                  "page": page_number}

    allWords.append(word_coord)

words_json["recognition"] = allWords

with open(output_value, "w") as write_file:
    json.dump(words_json, write_file, indent=4)

print("End of reading")
