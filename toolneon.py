import cv2 as cv
import numpy as np
from typing import List
import random
import time
from enum import Enum
from PIL import Image
import imageio

''' Self created libs ''' 
import toolfont

class PositionMode(Enum):
  RandomInCanvas = 1,
  RandomNoOverlap = 2,
  HorizentalCentralized = 3,
  HorizentalCentralizedEvenly = 4,


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
  fontsize= 50,
  posSet= None,
  colorSet = None,
):
  '''
  Add a set of neon texts to image by passing text, image and fontpath,\n
  return the image in Mat.\n
  The color and position is randomly chosen(or using other algorithms).\n
  optional parameters:\n
  '''

  imgSize = (img.shape[0], img.shape[1])
  posSet = positionArrangement(imgSize, textSet, fontpath, fontsize) if not posSet else posSet
  colorSet = colorArrangement(textSet) if not colorSet else colorSet
  for pos, color, text in zip(posSet, colorSet, textSet):
    print(pos, color, text)
    img = addNeonText(text, img, fontpath, pos, fontsize, color)
  return img


def positionArrangement(
  imgSize: tuple[int, int],
  textSet: List[str],
  fontpath: str,
  fontsize= 50,
  mode= PositionMode.RandomInCanvas
):
  '''
  Given the image, text set, font&fontsize, generate a list of\n
  postion which matches the number of the text set.\n
  optional parameters:\n
  - mode: (class)PostionMode. Default: PostionMode.RandomInCanvas
  '''

  if mode == PositionMode.RandomInCanvas:
    random.seed(time.time())
    posSet = []
    for text in textSet:
      size = toolfont.getTextSize(text, fontpath, fontsize)
      maxX = imgSize[0] - size[0]
      maxY = imgSize[1] - size[1]
      posSet.append((random.randint(0, maxX), random.randint(0, maxY)))
    return posSet
  else:
    return None


def colorArrangement(textSet: List[str]):
  '''
  Given a set of text, generate a list of color which matchse the\n
  number of the text set.\n
  '''
  random.seed(time.time())
  colorSet = random.choices(
    list(toolcolor.NeonColorSet.values()), k = len(textSet)
  )
  colorSet = [item.toBGRAtuple() for item in colorSet]
  
  return colorSet


def createNeonSeq(
  textSet: List[str],
  img: cv.Mat,
  fontpath: str,
  fontsize= 50,
  time = 5,
) -> List[cv.Mat]:

  imgSize = (img.shape[0], img.shape[1])
  posSet = positionArrangement(imgSize, textSet, fontpath, fontsize)
  frames:List[Image.Image] = []
  for _ in range(0, time // 1):
    tFrame = addNeonTextSet(
      textSet,
      img,
      './font/Nickainley.otf',
      200,
      posSet,
      colorArrangement(textSet)
    )
    frames.append(tFrame)
  return frames



# Test unit
if __name__ == '__main__':
  import toolcolor
  
  '''
  Generate single neon text
  '''
  # img = cv.imread('./img/wall_03.jpg')
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
  # cv.namedWindow("Display", cv.WINDOW_NORMAL)
  # cv.imshow('Display', img)
  # cv.waitKey(0)
  
  '''
  Generate neon text set
  '''
  # img = cv.imread('./img/wall_03.jpg')
  # img = np.zeros((800, 800, 3), dtype=np.uint8)

  # textSet = ['Coffee', 'Bar', 'KTV']
  # img = addNeonTextSet(textSet, img, './font/Nickainley.otf', 180)
  # cv.namedWindow("Display", cv.WINDOW_NORMAL)
  # cv.imshow('Display', img)
  # cv.waitKey(0)


  '''
  Generate neon gif
  '''
  for i in range(0, 10):
    img = np.zeros((800, 800, 3), dtype=np.uint8)
    textSet = ['Coffee', 'Bar', 'KTV']
    frames = createNeonSeq(textSet, img, './font/Nickainley.otf', 180, 8)
    with imageio.get_writer(f"gen_{i}.gif", mode="I", duration=0.5) as writer:
      for idx, frame in enumerate(frames):
        print("Adding frame to GIF file: ", idx + 1)
        writer.append_data(frame)