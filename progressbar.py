import time
from multiprocessing import Process
import math


# class ProgressBar:
    
    # def __init__(self, w: int=10):
    #     self.DATA_SIZE = data_sz
    #     self.width = w

# todo: check for hard-float numbers (3.33, 2.51, 1.77, etc)
def progress(progress: float, msg: str='', space: str='░', w: int=10) -> None :
    sp_len = len(space)
    if sp_len == 0 or sp_len > 1:
        raise Exception('Space length must be 1')
    WALL = '|'
    BLOCK = '█'
    # SPACE = '░' # todo: allow to set any space (len=1 otherwise exception)
    blocks_len = round(progress*w)
    spaces_len = round((1 - progress)*w)
    line = (
        WALL + 
        BLOCK*blocks_len + 
        space*spaces_len +
        WALL
    )
    if msg != '':
        line += ' ' + msg
    print(line, end='\r')


def cl_line(w: int=30, timeout: int=5):
    time.sleep(timeout)
    print('\r' + ' '*w)

def print_str(s):
    print(s, end='')

if __name__ == "__main__":
    # p1 = Process(target=cl_line)
    # p1.start()
    # p2 = Process(target=print_str, args=('asfasdf',))
    # p2.start()

    # p1.join()  
    # p2.join()

    print('bla bla bla')

    sz = 100
    for i in range(sz+1):
        progress(i/sz, 'do something', w=40, space='😇')
        time.sleep(0.02)
    print()

    print('finish')