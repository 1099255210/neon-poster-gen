from collections import namedtuple

Color = namedtuple('RGB', ['red', 'green', 'blue'])

class RGB(Color):

  def __str__(self) -> str:
    return f'({self.red},{self.green},{self.blue})'
  
  def tohex(self) -> str:
    '''Return color in hex format.'''
    return f'#{self.red:02X}{self.green:02X}{self.blue:02X}'

  def toRGBtuple(self) -> tuple:
    '''Return color in RGB tuple.'''
    return (self.red, self.green, self.blue)

  def toBGRtuple(self) -> tuple:
    '''Return color in BGR tuple.'''
    return (self.blue, self.green, self.red)

  def toRGBAtuple(self) -> tuple:
    '''Return color in RGBA(Alpha) tuple.'''
    return (self.red, self.green, self.blue, 0)
  
  def toBGRAtuple(self) -> tuple:
    '''Return color in BGRA(Alpha) tuple.'''
    return (self.blue, self.green, self.red, 0)


def hex2rgb(hexstr:str) -> RGB:
  '''Convert hex color string to (class)RGB object.'''

  # Begin with '#'
  if hexstr[0] == '#':
    red = int(hexstr[1:3], base=16)
    green = int(hexstr[3:5], base=16)
    blue = int(hexstr[5:7], base=16)
    return RGB(red, green, blue)

  # Without '#'
  red = int(hexstr[0:2], base=16)
  green = int(hexstr[2:4], base=16)
  blue = int(hexstr[4:6], base=16)
  return RGB(red, green, blue)


# The palette part in this project.

PURECOLOR1 = RGB(255, 0, 255)
PURECOLOR2 = RGB(0, 255, 255)
PURECOLOR3 = RGB(255, 255, 0)

DIMEDCOLOR1 = RGB(246, 128, 186)
DIMEDCOLOR2 = RGB(121, 234, 249)
DIMEDCOLOR3 = RGB(254, 243, 83)

VIVIDCOLOR1 = RGB(241, 12, 125)
VIVIDCOLOR2 = RGB(0, 200, 244)
VIVIDCOLOR3 = RGB(254, 227, 4)

ColorSet = {
  'PURECOLOR1': RGB(255, 0, 255),
  'PURECOLOR2': RGB(0, 255, 255),
  'PURECOLOR3': RGB(255, 255, 0),

  'DIMEDCOLOR1': RGB(246, 128, 186),
  'DIMEDCOLOR2': RGB(121, 234, 249),
  'DIMEDCOLOR3': RGB(254, 243, 83),

  'VIVIDCOLOR1': RGB(241, 12, 125),
  'VIVIDCOLOR2': RGB(0, 200, 244),
  'VIVIDCOLOR3': RGB(254, 227, 4),
}

NeonColorSet = {
  'VIVIDCOLOR1': RGB(241, 12, 125),
  'VIVIDCOLOR2': RGB(0, 200, 244),
  'VIVIDCOLOR3': RGB(254, 227, 4),

  'DIMEDCOLOR1': RGB(246, 128, 186),
  'DIMEDCOLOR2': RGB(121, 234, 249),
  'DIMEDCOLOR3': RGB(254, 243, 83),
}

# Test unit.
if __name__ == '__main__':
  c1 = RGB(255, 0, 255)
  c2 = RGB(246, 128, 186)
  print(c1.tohex())
  print(c2.tohex())
  print(c1, c2)
  print(hex2rgb('#F680BA'))