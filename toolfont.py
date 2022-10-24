from collections import namedtuple
from PIL import ImageFont, ImageDraw, Image
from cv2 import Mat
import numpy as np

Box = namedtuple('Size', ['width', 'height'])

class Size(Box):

  def __str__(self) -> str:
    return f'({self.width},{self.height})'


def getTextSize(text:str, fontpath:str, fontsize:int, direction='ltr') -> Size:
  '''
  Given the text, font, size, return the size of this text.\n
  optional parameters:\n
  - direction: str. Default: 'ltr'. Examples: 'rtl', 'ttb'
  '''
  font = ImageFont.truetype(fontpath, fontsize)
  return font.getsize(text, direction)


def addTextToImg(
  text: str,
  img: Mat,
  fontpath: str,
  pos= (0, 0),
  fontsize= 50,
  fontcolor= (0, 0, 0, 0)
)-> Mat:
  '''
  Add custom font to image by passing text, image and fontpath,\n
  return the image in Mat.\n
  optional parameters:\n
  - pos: tuple. Default: (0, 0).
  - fontsize: int. Default: 50.
  - fontcolor: tuple. Default: (0, 0, 0, 0). (It's BGRA)
  '''
  font = ImageFont.truetype(fontpath, fontsize)
  img_pil = Image.fromarray(img)
  ImageDraw.Draw(img_pil).text(pos, text, fontcolor, font)
  return np.array(img_pil)


# Test unit.
if __name__ == '__main__':
  import cv2 as cv
  img = cv.imread('./img/wall_01.jpg')
  # img = np.zeros((512,512,3), np.uint8)
  img = addTextToImg('nihao', img, './font/NeonSans.ttf',pos=(50, 50), fontsize=50)
  cv.imshow('window', img)
  cv.waitKey(0)