import toolneon
import random
import time

def generate(textSet, du):
  try:
    toolneon.generateGifPoster(
        textSet,
        './font/QingKe.ttf',
        100,
        (500, 500),
        time=du
        )
    random.seed(time.time())
    res = random.randint(0, 2)
    return f'../../backend/gen/newgen_{res}.gif'
  except(toolneon.OutofimgException):
    return None
  