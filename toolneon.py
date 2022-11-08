import cv2 as cv
import numpy as np
from typing import List
import random
import time
from enum import Enum
from PIL import Image
import imageio
import os

''' Self created libs ''' 
import toolfont

class PositionMode(Enum):
  RandomInCanvas = 1,
  RandomNoOverlap = 2,
  HorizentalCentralized = 3,
  HorizentalCentralizedEvenly = 4,


class OutofimgException(Exception):
  def __init__(self, ErrorInfo):
    super().__init__(self)
    self.errorinfo = ErrorInfo
  def __str__(self):
    return super().__str__()


def addNeonText(
  text: str,
  img: cv.Mat,
  fontpath: str,
  pos= (0, 0),
  fontsize= 50,
  fontcolor= (0, 0, 0, 0),
  fontweight= 'regular',
  direction= 'rtl',
):
  '''
  Add neon text to image by passing text, image and fontpath,\n
  return the image in Mat.\n
  optional parameters:\n
  - pos: tuple. Default: (0, 0).
  - fontsize: int. Default: 50.
  - fontcolor: tuple. Default: (0, 0, 0, 0). (It's BGRA)
  - fontweight: str. Default: 'regular'. Examples: 'bold', 'thin'.
  - direction: str. Default: 'rtl'. Examples: 'ttb'.
  '''

  # This ratio is used to adjust the blurcore size.
  # if fontweight == 'regular':
  #   ratio = 12
  # elif fontweight == 'bold':
  #   ratio = 9
  # elif fontweight == 'thin':
  #   ratio = 15
  # blurcore = (fontsize // ratio, fontsize // ratio)
  blurcore = (20, 20)

  img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
  img = toolfont.addTextToImg(
    text, img, fontpath, pos, fontsize, (0, 0, 0, 0), direction=direction)

  img_text = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.uint8)
  img_text = toolfont.addTextToImg(
    text, img_text, fontpath, pos, fontsize, fontcolor, direction=direction)

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
  directionSet = None,
):
  '''
  Add a set of neon texts to image by passing text, image and fontpath,\n
  return the image in Mat.\n
  The color and position is randomly chosen(or using other algorithms).\n
  optional parameters:\n
  - directionSet: str. Default: None. Examples: 'random', 'rtl', 'ttb'.\n
  '''

  imgSize = (img.shape[0], img.shape[1])
  # Generate direction set
  if directionSet == 'random':
    directionSet = dirctionArrangement(textSet)
  elif directionSet == 'rtl':
    directionSet = ['rtl' for _ in textSet]
  elif directionSet == 'ttb':
    directionSet = ['ttb' for _ in textSet]
  else:
    directionSet = ['rtl' for _ in textSet]
  # Generate position set
  try:
    posSet = positionArrangement(imgSize, textSet, fontpath, fontsize, directionSet=directionSet) if not posSet else posSet
  except(ValueError):
    raise OutofimgException("Text out of image range.")
  # Generate color set
  colorSet = colorArrangement(textSet) if not colorSet else colorSet
  for pos, color, text, direction in zip(posSet, colorSet, textSet, directionSet):
    print(pos, color, text, direction)
    img = addNeonText(text, img, fontpath, pos, fontsize, color, direction=direction)
  return img


def positionArrangement(
  imgSize: tuple[int, int],
  textSet: List[str],
  fontpath: str,
  fontsize= 50,
  mode= PositionMode.RandomInCanvas,
  directionSet= None,
):
  '''
  Given the image, text set, font&fontsize, generate a list of\n
  postion which matches the number of the text set.\n
  optional parameters:\n
  - mode: (class)PostionMode. Default: PostionMode.RandomInCanvas
  - directionSet: [List]str. Default: None
  '''

  directionSet = ['rtl' for _ in textSet] if not directionSet else directionSet

  if mode == PositionMode.RandomInCanvas:
    random.seed(time.time())
    posSet = []
    for text, direction in zip(textSet, directionSet):
      size = toolfont.getTextSize(text, fontpath, fontsize, direction)
      maxX = imgSize[0] - size[0]
      maxY = imgSize[1] - size[1]
      posSet.append((random.randint(0, maxX), random.randint(0, maxY)))
    return posSet
  else:
    return None


def colorArrangement(textSet: List[str]):
  '''
  Given a set of text, generate a list of color which matches the\n
  number of the text set.\n
  '''
  random.seed(time.time())
  colorSet = random.choices(
    list(toolcolor.NeonColorSet.values()), k = len(textSet)
  )
  colorSet = [item.toBGRAtuple() for item in colorSet]
  
  return colorSet


def dirctionArrangement(textSet: List[str]):
  '''
  Given a set of text, generate a list of direction which matches the\n
  number of the text set.\n
  '''
  random.seed(time.time())
  directionSet = []
  for _ in textSet:
    if random.randint(0, 1):
      directionSet.append('rtl')
    else:
      directionSet.append('ttb')
  
  return directionSet


def createNeonSeq(
  textSet: List[str],
  img: cv.Mat,
  fontpath: str,
  fontsize= 50,
  time = 5,
  directionSet= 'rtl'
) -> List[cv.Mat]:

  imgSize = (img.shape[0], img.shape[1])
  if directionSet == 'random':
    directionSet = dirctionArrangement(textSet)
  elif directionSet == 'rtl':
    directionSet = ['rtl' for _ in textSet]
  elif directionSet == 'ttb':
    directionSet = ['ttb' for _ in textSet]
  else:
    directionSet = ['rtl' for _ in textSet]
  try:
    posSet = positionArrangement(imgSize, textSet, fontpath, fontsize, directionSet=directionSet)
  except(ValueError):
    raise OutofimgException("Text out of image range.")
  frames:List[Image.Image] = []
  for _ in range(0, time // 1):
    tFrame = addNeonTextSet(
      textSet,
      img,
      fontpath,
      fontsize,
      posSet,
      colorArrangement(textSet),
      directionSet,
    )
    frames.append(tFrame)
  return frames


def generateGifPoster(
  textSet: List[str],
  fontpath: str,
  fontsize= 100,
  imgsize= (800, 800),
  img= None,
  time= 5,
  frametime= 0.5,
  destpath= './gen/',
  nums = 3,
  prefix = 'newgen_',
):
  if not img:
    img = np.zeros((imgsize[0], imgsize[1], 3), dtype=np.uint8)
  if not os.path.exists(destpath):
    os.mkdir(destpath)
  for i in range(nums):
    frames = createNeonSeq(textSet, img, fontpath, fontsize, time)
    filename = f'{destpath}{prefix}{i}.gif'
    with imageio.get_writer(filename, mode="I", duration=frametime) as writer:
      for idx, frame in enumerate(frames):
        writer.append_data(frame)

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
  #   200,
  #   toolcolor.VIVIDCOLOR1.toBGRAtuple(),
  #   'bold',
  # )
  # cv.namedWindow("Display", cv.WINDOW_AUTOSIZE)
  # cv.imshow('Display', img)
  # cv.waitKey(0)
  
  '''
  Generate neon text set
  '''
  # img = cv.imread('./img/wall_03.jpg')
  # img = np.zeros((800, 800, 3), dtype=np.uint8)

  # textSet = ['Coffee', 'BAR', 'KTV']
  # img = addNeonTextSet(textSet, img, './font/Nickainley.otf', 180)
  # cv.namedWindow("Display", cv.WINDOW_AUTOSIZE)
  # cv.imshow('Display', img)
  # cv.waitKey(0)


  '''
  Generate neon gif
  '''
  textSet = ['Coffee', 'BAR', 'KTV']
  generateGifPoster(textSet, './font/QingKe.ttf', 200, (300, 300))