# [2023/06/30]-25:33#84 #
import time, machine
from servo import Servo
pin = [5, 21, 19, 18, 22, 23]
servo2 = Servo(machine.Pin(25),min_us=600,max_us=2400,angle=180)
def config():
    global star, mod
    mod  = 0
    star = 0
    wb.cls(0)
    wb.colors(999,999)
    servo2.write_angle(0)
    wb.str(str('Frequency Mode'),20,20,1,2)
def U():
    for i in range(star):
        wb.str(str('*'),i*20+21,star*20-20,1,3)
def u():
    global star
    wb.cls(0)
    wb.str(str('Star Mode'),20,20,1,2)
    while (wb.getkey()!=0):pass
    while (wb.getkey()==0):pass
    wb.cls(0)
    while (wb.getkey()!=16):
        if(wb.getkey()==1)and(star>1):
            wb.colors(0,0)
            U()
            star-=1
        if(wb.getkey()==2)and(star<6):
            wb.colors(999,999)
            star+=1
            U()
        servo2.write_angle(star*30)
        while (wb.getkey()!=0):pass
        time.sleep(0.02)
    config()
def R():
    global star
    wb.colors(0,0)
    wb.str(str(star),20,40,1,2)
    star = wb.rand(1,6)
    wb.colors(999,999)
    wb.str(str(star),20,40,1,2)
    time.sleep(0.1)
def r():
    global mod
    wb.cls(0)
    wb.str(str('Dice1 Mode'),20,20,1,2)
    while (wb.getkey()!=16):
        if(wb.getkey()==2):
            mod = 1
            R()
        if(mod==1):
            mod = 0
            for i in range(30):
                R()
    config()
def l():
    global mod
    n = 0
    a = 0
    wb.cls(0)
    wb.str(str('Dice2 Mode'),20,20,1,2)
    while (wb.getkey()!=16):
        for i in range(len(pin)):
            if(machine.Pin(pin[i],1).value()==1)and(n!=i+1):
                wb.colors(0,0)
                wb.str(str(n),20,40,1,2)
                n = i+1
                wb.colors(999,999)
                wb.str(str(n),20,40,1,2)
        if(wb.getkey()==1):mod=1
        if(wb.getkey()==2):mod=0
        if(mod==1):
            if(a==0):s=10
            if(a==180):s=-10
            a+=s
            servo2.write_angle(a)
            time.sleep(0.02)
    config()
config()
while True:
    if(wb.getkey()==32):u()
    if(wb.getkey()==4):r()
    if(wb.getkey()==8):l()