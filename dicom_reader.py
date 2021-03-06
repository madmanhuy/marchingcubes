import cv2
import os
import pydicom
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# reads a dicom image, converts to png


def read_dicom_image(path):
    if(os.path.isfile(path)):
        print('Reading file {}'.format(path))
        ds = pydicom.dcmread(path, force=True)
        ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
        img = ds.pixel_array
        # creating png
        cv2.imwrite(path.replace('.dcm', '.png'), img)
        return path.replace('.dcm', '.png')
    else:
        print('invalid path!')


def main():
    path = read_dicom_image('C:/temp/scan.dcm')
    img = mpimg.imread(path)
    plt.imshow(img, cmap='gray', vmin=0, vmax=1)
    plt.show()


if __name__ == "__main__":
    main()
