import cv2 as cv
import numpy as np

''' Self created libs ''' 
import toolcolor
import toolfont

img = np.zeros((512,512,3), np.uint8)
img_tobemerged = img.copy()
font_path = './font/Nickainley.otf'
font_size = 150
text_to_add = 'Shopping'
text_size = toolfont.getTextSize(text_to_add, font_path, font_size)
start_x = (img.shape[1] - text_size[0]) / 2
text_color = toolcolor.VIVIDCOLOR3.toBGRAtuple()
position = (start_x, 50)
core = (font_size // 12, font_size // 12)

img = toolfont.addTextToImg(
  text_to_add, img, font_path, position, font_size, text_color)
img_tobemerged = toolfont.addTextToImg(
  text_to_add, img_tobemerged, font_path, position, font_size, text_color)
img_tobemerged = cv.blur(img_tobemerged, core)

dst = cv.addWeighted(img, 0.5, img_tobemerged, 0.8, 0.0)

cv.imshow('img', dst)
cv.waitKey(0)
cv.destroyAllWindows()
