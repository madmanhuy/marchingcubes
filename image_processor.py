import numpy as np 
import matplotlib.pyplot as plt 
import cv2

def process_image(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # threshold to segment
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # open image
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    open = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, se)
    open = (255-open)
    image = cv2.cvtColor(open, cv2.COLOR_BGR2RGBA)
    image[np.all(image == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]
    cv2.imwrite(path, image)
    return path

print(process_image("C:/temp/test (1).png"))