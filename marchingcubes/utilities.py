import cv2
import numpy as np
import pydicom


def read_dicom_image(path):
    dcm_image = pydicom.dcmread(path, force=True)
    dcm_image.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
    img = dcm_image.pixel_array

    png_path = path.replace('.dcm', '.png')
    cv2.imwrite(png_path, img)

    return png_path


def process_image(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, se)
    opening = (255 - opening)

    image = cv2.cvtColor(opening, cv2.COLOR_BGR2RGBA)
    image[np.all(image == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]

    cv2.imwrite(path, image)

    return path
