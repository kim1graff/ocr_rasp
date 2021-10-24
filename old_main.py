import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
img_path = 'C:\\Users\\ГурьяновВ\\PycharmProjects\\ORC_rasp\\hard_table.png'
xml_path = 'C:\\Users\\ГурьяновВ\\PycharmProjects\\ORC_rasp\\reading_log.txt'

def startreading():

    logfile = open(xml_path, 'w')
    logfile.close()
    logfile = open(xml_path, 'w')
    logfile.write('Старт считывания' + '\n')

    img = cv2.imread(img_path)
    clahe = cv2.createCLAHE(clipLimit=100, tileGridSize=(100, 100))
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different channels
    l2 = clahe.apply(l)  # apply CLAHE to the L-channel
    lab = cv2.merge((l2, a, b))  # merge channels
    img2 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR

    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    obr_img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    logfile.close()

startreading()