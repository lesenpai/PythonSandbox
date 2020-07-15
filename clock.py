""" 
tip: можно завернуть .py в .exe (или даже .apk) и отправить другу :)
"""

from datetime import datetime
import sys
import copy
import time
from multiprocessing import Process
from ctypes import * 
STD_OUTPUT_HANDLE = -11
class COORD(Structure):
    pass
COORD._fields_ = [("X", c_short), ("Y", c_short)]
def print_at(y, x, s):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(x, y))
    x = s.encode("windows-1252")
    windll.kernel32.WriteConsoleA(h, c_char_p(x), len(x), None, None)

STOPWATCH_COORD_Y = 10
STOPWATCH_END_COORD_X = 17

class Clock:
    LINES_COUNT = 9

    clear_clock_sprite = [
        #         11 11
        #12345678901 10987654321
        '           12'            ,
        '     11         01'       ,
        '  10               02'    ,
        '                   '      ,
        '09         o         03'  ,
        '                   '      ,
        '  08               04'    ,
        '     07         05'       ,
        '           06'
    ]

    tr_quarter_sprites = {
        0: [
            [2, '       |       '],
            [3, '       |       ']
        ],
        5: [
            [2, '          /    '],
            [3, '         /     ']
        ],
        10: [
            [3, '          ---- '],
            [4, '         o --      ']
        ],
        15: [
            [4, '         o ------  '],
        ]
    }

    clock_sprite_line_offsets = {
        1: (7,-2),
        2: (4,-2),
        3: (4,-2),
        4: (2,-2),
        5: (4,-2),
        6: (4,-2),
        7: (7,-2)
    }

    def hreflect(self, s):
        # center line id
        CLID = 4
        if s in [0,5,10,15]:
            spt = copy.deepcopy(self.tr_quarter_sprites[s])
            for i in range(len(spt)):
                spt[i][0] = 2*CLID - spt[i][0]
                if s == 5:
                    spt[i][1] = spt[i][1].replace('/', '\\')
            return spt
        else:
            raise Exception("Unsupported second value")


    def vreflect(self, s):
        if s in [0,5,10,15]:
            spt = copy.deepcopy(self.tr_quarter_sprites[s])
            for i in range(len(spt)):
                lid = spt[i][0]
                if s == 5:
                    spt[i][1] = spt[i][1].replace('/', '\\')
                spt[i][1] = spt[i][1][::-1]
            return spt
        else:
            raise Exception("Unsupported second value")


    def hvreflect(self, s):
        # center line id
        CLID = 4
        if s in [0,5,10,15]:
            spt = copy.deepcopy(self.tr_quarter_sprites[s])
            for i in range(len(spt)):
                spt[i][0] = 2*CLID - spt[i][0] # h reflect
                spt[i][1] = spt[i][1][::-1] # v reflect
            return spt
        else:
            raise Exception("Unsupported second value")


    def __draw(self, spt: list, print_mode = False):
        if not print_mode:
            for i in range(self.LINES_COUNT):
                print_at(i, 0, spt[i])
        else:
            for i in range(self.LINES_COUNT):
                print(spt[i])
        print_at(STOPWATCH_COORD_Y, STOPWATCH_END_COORD_X, '')


    def draw_second(self, s, print_mode = False):
        VALID_SECOND_VALUES = [0,5,10,15,20,25,30,35,40,45,50,55]

        def get_sprite(s):
            if s == 0:  return self.tr_quarter_sprites[0]
            if s == 5:  return self.tr_quarter_sprites[5]
            if s == 10: return self.tr_quarter_sprites[10]
            if s == 15: return self.tr_quarter_sprites[15]
            if s == 20: return self.hreflect(10)
            if s == 25: return self.hreflect(5)
            if s == 30: return self.hvreflect(0)
            if s == 35: return self.hvreflect(5)
            if s == 40: return self.hvreflect(10)
            if s == 45: return self.vreflect(15)
            if s == 50: return self.vreflect(10)
            if s == 55: return self.vreflect(5)
            raise Exception('Unsupported second value')


        if s == 0 or s%5 == 0:
            clock = self.clear_clock_sprite.copy()
            spt = get_sprite(s)
            for l in spt:
                lid = l[0]
                clock[lid] = ''.join((
                    clock[lid][:self.clock_sprite_line_offsets[lid][0]],
                    l[1],
                    clock[lid][self.clock_sprite_line_offsets[lid][1]:]
                ))

            self.__draw(clock, print_mode)


    def draw(self, t: datetime, print_mode = False):
        self.draw_second(t.second, print_mode=print_mode)



def now(): return datetime.now()


def upline(): 
    sys.stdout.write("\x1b[1A")
    sys.stdout.flush()

# clear line
def cll(): 
    sys.stdout.write("\x1b[2K")
    sys.stdout.flush()

def upncll(): 
    upline()
    cll()

def printnow(s, end_='\n'): print(s, flush=True, end=end_)


def clock_loop():
    clock = Clock()
    while True:
        try:
            clock.draw(datetime.now())
            time.sleep(0.3)
        except KeyboardInterrupt:
            break


def stopwatch_loop(y, x):
    while True:
        try:
            t = datetime.now()
            print_at(y, x, t.strftime('%H:%M:%S,') + f'{t.microsecond//10_000:02d}')
            # sys.stdout.flush()
            time.sleep(0.05)
        except KeyboardInterrupt:
            break




if __name__ == "__main__":
    clockloop = Process(target=clock_loop)
    swloop = Process(target=stopwatch_loop, args=(10,6))
    try:
        clockloop.start()
        swloop.start()
        clockloop.join()
        swloop.join()
    except KeyboardInterrupt:
        clockloop.close()
        swloop.close()
    


