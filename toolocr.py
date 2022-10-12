import easyocr
from typing import List

def getTextFromImage(path:str, lang=['ch_sim', 'en'], log=False) -> List[str]:
  '''
  Given the image's path string, return a list of text in the image.\n
  optional parameter :\n
  - lang: List[str]. Default: ['ch_sim, 'en'].
  - log: bool. Default: False.
  '''

  reader = easyocr.Reader(lang_list=lang, gpu=False)
  res = reader.readtext(path)
  # For each items in res: 
  # [0] 4 points xy coordinates
  # [1] texts
  # [2] confidence
  ret = [lines[1] for lines in res]
  if log:
    print(ret)
  return ret