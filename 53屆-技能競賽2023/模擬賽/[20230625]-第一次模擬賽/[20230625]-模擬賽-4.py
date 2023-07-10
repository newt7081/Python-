# 2023/06/21
import machine as ma
from random import randint
from servo import Servo
def config():
    global servo1, star, t, pin, Hz
    wb.cls(0)
    wb.str(str('Frequency Mode'),20,20,1,2)
    t    = 0
    Hz   = 0
    star = 0
    pin = [5, 21, 19, 18, 22, 23]
    servo1 = Servo(machine.Pin(25),min_us=600,max_us=2400,angle=180)
    servo1.write_angle(0)
    for i in range(len(pin)):
        ma.Pin(pin[i], 1).value(0)
class key():
    def u():
        global star
        wb.cls()
        wb.str(str('Star Mode'),20,20,1,2)
        def mod_n():
            text = ''
            for i in range(star):
                text+='* '
                wb.str(str(text),20,i*10+40,1,2)
            time.sleep(0.1)
        while True:
            servo1.write_angle(star*30)
            if(wb.getkey()==2):
                if star!=6:star+=1
                wb.cls()
                mod_n()
                while wb.getkey()!=0:pass
            if(wb.getkey()==1):
                if star!=1 and star!=0:star-=1
                wb.cls()
                mod_n()
                while wb.getkey()!=0:pass
            if(wb.getkey()==16):
                servo1.write_angle(0)
                break
    def d():config()
    def r():
        n = 0
        wb.cls()
        wb.str(str('Dice2 Mode'),20,20,1,2)
        def ra_n():
            global ra
            ra = randint(1, 6)
            wb.cls()
            wb.str(str(ra),20,20,1,2)
            time.sleep(0.2)
        while True:
            while (wb.getkey()==2):
                ra_n()
                n = 1
            if n==1:
                for i in range(15):
                    ra_n()
                n = 0
            if(wb.getkey()==16):break
    def l():
        a    = 0
        s    = 10
        mod  = 0
        dice = 0
        wb.cls()
        wb.str(str('Dice1 Mode'),20,20,1,2)
        while True:
            for i in range(len(pin)):
                if machine.Pin(pin[i], 1).value()==1 and dice!=(i+1):
                    dice = i+1
                    wb.cls()
                    wb.str(str(dice),20,40,1,2)
            if(wb.getkey()==1)and(mod==0):
                mod = 1
            if(wb.getkey()==2)and(mod==1):
                mod = 0
            if(mod==1):
                if a>=180:s=-10
                if a<=0:s=10
                a += s
                servo1.write_angle(a)
                time.sleep(0.02)
            if(wb.getkey()==16):break
config()
while True:
    if machine.Pin(26, 1).value()==1 and Hz==0:
        t = time.ticks_us()
        Hz = 1
    elif machine.Pin(26, 1).value()==0 and Hz==1:
        a = str(round(100000000/(time.ticks_us()-t))/100)
        wb.cls()
        wb.str(str('Frequency Mode'),20,20,1,2)
        wb.str(a+'Hz',20,40,1,2)
        Hz = 0
    if (round(100000000/(time.ticks_us()-t))/100==0.00) and Hz!=2:
        config()
        Hz = 2
    if(wb.getkey()==32):key.u()# U
    if(wb.getkey()==16):key.d()# D
    if(wb.getkey()==4):key.r()#  R
    if(wb.getkey()==8):key.l()#  L
    if(wb.getkey()==64):break#   MENU
