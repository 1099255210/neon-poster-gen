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
  fontcolor= (0, 0, 0, 0),
  outline= 0,
)-> Mat:
  '''
  Add custom font to image by passing text, image and fontpath,\n
  return the image in Mat.\n
  optional parameters:\n
  - pos: tuple. Default: (0, 0).
  - fontsize: int. Default: 50.
  - fontcolor: tuple. Default: (0, 0, 0, 0). (It's BGRA)
  - outline: double. Default: 0.
  '''
  font = ImageFont.truetype(fontpath, fontsize)
  img_pil = Image.fromarray(img)
  d= ImageDraw.Draw(img_pil)
  d.text(pos, text, fontcolor, font, embedded_color=1)
  x = pos[0]
  y = pos[1]
  # d.text(pos, text, fontcolor, font, embedded_color=1)
  if outline > 0:
    d.text((x - outline, y), text, font=font, fill=fontcolor, embedded_color=1)
    d.text((x + outline, y), text, font=font, fill=fontcolor, embedded_color=1)
    d.text((x, y - outline), text, font=font, fill=fontcolor, embedded_color=1)
    d.text((x, y + outline), text, font=font, fill=fontcolor, embedded_color=1)
  return np.array(img_pil)


# Test unit.
if __name__ == '__main__':
  import cv2 as cv
  img = cv.imread('./img/wall_01.jpg')
  # img = np.zeros((512,512,3), np.uint8)
  img = addTextToImg('nihao', img, './font/NeonSans.ttf',pos=(50, 50), fontsize=200)
  cv.imshow('window', img)
  cv.waitKey(0)