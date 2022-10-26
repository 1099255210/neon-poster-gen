import cv2 as cv
import numpy as np

''' Self created libs ''' 
import toolcolor
import toolfont

'''

NOTICE:
libraqm(https://github.com/HOST-Oman/libraqm) is needed.
If the system is Windows,
download (https://download.lfd.uci.edu/pythonlibs/archived/libraqm-0.7.1.dll.zip),
then put 'libraqm.dll' and 'fribidi-0.dll' into 'C:\Windows\System32',
then reboot the python kernel.

'''

# Read image & Create a board
path = './img/wall_01.jpg'
# img = cv.imread(path)
img = np.zeros((512,512,3), np.uint8)

# Configure font
eng_font_path = './font/NeonSans.ttf'
hand_font_path = './font/Nickainley.otf'
font_size = 100

# Set the text
text_to_add = 'Shopping'
text_color = toolcolor.VIVIDCOLOR1.toBGRAtuple()

# Horizental centralize
text_size = toolfont.getTextSize(text_to_add, hand_font_path, font_size)
start_x = (img.shape[1] - text_size[0]) / 2
position = (start_x, 50)

img = toolfont.addTextToImg(
  text_to_add, img, hand_font_path, position, font_size, text_color)

# Show image
cv.imshow('img', img)
cv.waitKey(0)
cv.destroyAllWindows()

# Save image
save_path = './img/01_save.png'
cv.imwrite(save_path, img)
