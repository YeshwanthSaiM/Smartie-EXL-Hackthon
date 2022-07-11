"""We extract text from a document.
"""

# libraries
import numpy as np
import pandas as pd
import cv2 as cv 
import cv2
from google.colab.patches import cv2_imshow # for image display
from skimage import io
from PIL import Image 
import matplotlib.pylab as plt
import pytesseract


def extractTextFromImg(img_file_path):
    # loading the image :: Original 
    img = io.imread(img_file_path) 
    output = pytesseract.image_to_string(img)
    return output
    
