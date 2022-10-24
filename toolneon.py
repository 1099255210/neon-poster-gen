import cv2 as cv
import numpy as np
from typing import List
import random
import time

''' Self created libs ''' 
import toolfont

def addNeonText(
  text: str,
  img: cv.Mat,
  fontpath: str,
  pos= (0, 0),
  fontsize= 50,
  fontcolor= (0, 0, 0, 0),
  fontweight= 'regular',
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


  # This ratio is used to adjust the blurcore size.
  if fontweight == 'regular':
    ratio = 12
  elif fontweight == 'bold':
    ratio = 9
  elif fontweight == 'thin':
    ratio = 15
  blurcore = (fontsize // ratio, fontsize // ratio)

  img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
  img = toolfont.addTextToImg(
    text, img, fontpath, pos, fontsize, (0, 0, 0, 0))

  img_text = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.uint8)
  img_text = toolfont.addTextToImg(
    text, img_text, fontpath, pos, fontsize, fontcolor)

  img_blur = img_text.copy()
  img_blur = cv.blur(img_blur, blurcore)

  blend = cv.addWeighted(img_text, 0.5, img_blur, 0.9, 0.0)
  dst = cv.addWeighted(img, 1, blend, 1, 0.0)
  return dst


def addNeonTextSet(
  textSet: List[str],
  img: cv.Mat,
  fontpath: str,
  fontsize= 50
):
  '''
  Add a set of neon texts to image by passing text, image and fontpath,\n
  return the image in Mat.\n
  The color and position is randomly chosen(or using other algorithms).\n
  optional parameters:\n
  '''

  imgSize = (img.shape[0], img.shape[1])
  posSet = positionArrangement(imgSize, textSet, fontpath, fontsize)
  colorSet = colorArrangement(textSet)
  for pos, color, text in zip(posSet, colorSet, textSet):
    print(pos, color, text)
    img = addNeonText(text, img, fontpath, pos, fontsize, color)
  return img


def positionArrangement(
  imgSize: tuple[int, int],
  textSet: List[str],
  fontpath: str,
  fontsize= 50,
):

  random.seed(time.time())
  posSet = []
  for text in textSet:
    size = toolfont.getTextSize(text, fontpath, fontsize)
    maxX = imgSize[0] - size[0]
    maxY = imgSize[1] - size[1]
    posSet.append((random.randint(0, maxX), random.randint(0, maxY)))

  return posSet


def colorArrangement(textSet: List[str]):
  random.seed(time.time())
  colorSet = random.choices(
    list(toolcolor.NeonColorSet.values()), k = len(textSet)
  )
  colorSet = [item.toBGRAtuple() for item in colorSet]
  
  return colorSet



# Test unit
if __name__ == '__main__':
  import toolcolor
  
  img = cv.imread('./img/wall_03.jpg')
  
  # img = np.zeros((800, 800, 3), dtype=np.uint8)
  # img = addNeonText(
  #   'Shopping',
  #   img,
  #   './font/Nickainley.otf',
  #   (50, 50),
  #   150,
  #   toolcolor.VIVIDCOLOR1.toBGRAtuple(),
  #   'bold',
  # )
  textSet = ['Coffee', 'Bar', 'KTV']
  img = addNeonTextSet(textSet, img, './font/NeonSans.ttf', 200)
  cv.namedWindow("Display", cv.WINDOW_NORMAL)
  cv.imshow('Display', img)
  cv.waitKey(0)