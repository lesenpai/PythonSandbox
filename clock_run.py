from clock import *


clock = Clock()
while True:
    try:
        clock.draw(datetime.now())``
        time.sleep(1)
    except KeyboardInterrupt:
        break