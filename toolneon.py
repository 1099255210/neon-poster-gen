import cv2 as cv
from cv2 import Mat
import numpy as np

''' Self created libs ''' 
import toolcolor
import toolfont

def addNeonText(
  text:str,
  img:Mat,
  fontpath:str,
  pos=(0, 0),
  fontsize=50,
  fontcolor=(0, 0, 0, 0),
  fontweight='regular',
):
  '''
  Add neon text to image by passing text, image and fontpath,\n
  return the image in Mat.\n
  optional parameters:\n
  - pos: tuple. Default: (0, 0).
  - fontsize: int. Default: 50.
  - fontcolor: tuple. Default: (0, 0, 0, 0). (It's BGRA)
  - fontweight: str. Default: 'regular'. Examples: 'bold', 'thin'.
  '''
  img_tobemerged = img.copy()
  # img_tobemerged = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.uint8)
  # This ratio is used to adjust the blurcore size.
  if fontweight == 'regular':
    ratio = 12
  elif fontweight == 'bold':
    ratio = 9
  elif fontweight == 'thin':
    ratio = 15
  blurcore = (fontsize // ratio, fontsize // ratio)
  img = toolfont.addTextToImg(
    text, img, fontpath, pos, fontsize, fontcolor)
  img_tobemerged = toolfont.addTextToImg(
    text, img_tobemerged, fontpath, pos, fontsize, fontcolor)
  img_tobemerged = cv.blur(img_tobemerged, blurcore)

  dst = cv.addWeighted(img, 0.5, img_tobemerged, 0.8, 0.0)
  return dst


# Test unit
if __name__ == '__main__':
  # img = cv.imread('./img/wall_01.jpg')
  
  img = np.zeros((512, 512, 3), dtype=np.uint8)
  img = addNeonText(
    '购物天堂',
    img,
    './font/QingKe.ttf',
    (50, 50),
    150,
    toolcolor.VIVIDCOLOR3.toBGRAtuple(),
    'bold',
  )
  cv.imshow('window', img)
  cv.waitKey(0)