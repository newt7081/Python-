# 01:12-hz無功能
import time
from servo import Servo
pin = {'servo':25, '555':26, '4017':[5, 21, 19, 18, 22, 23]}
def config():
    global star, servo1, hz
    hz   = 0
    star = 0
    wb.cls(0)
    wb.colors(999,999)
    wb.str(str('Frequency Mod'),20,20,1,2)
    servo1 = Servo(machine.Pin(pin['servo']),min_us=600,max_us=2400,angle=180)
    servo1.write_angle(0)
    for z in range(len(pin['4017'])):
        machine.Pin(pin['4017'][z],1).value()
        
def u():
    global star
    time.sleep(0.3)
    wb.cls(0)
    wb.str(str('Star Mod'),20,20,1,2)
    while (wb.getkey()!=0):pass
    while (wb.getkey()==0):pass
    wb.cls(0)
    def r_(x):
        servo1.write_angle(star*30)
        if(x==0):wb.colors(0,0)
        if(x==1):wb.colors(999,999)
        for z in range(star):
            wb.str(str('*'),z*20+21,star*20-20,1,3)
        time.sleep(0.05)
    while (wb.getkey()!=16):
        if(wb.getkey()==2)and(star<6):
            star += 1
            r_(1)
            while (wb.getkey()!=0):pass
        if(wb.getkey()==1)and(star>1):
            r_(0)
            star -= 1
            r_(1)
            while (wb.getkey()!=0):pass
    config()
def r():
    n = 0
    wb.cls(0)
    wb.str(str('Dice1 Mod'),20,20,1,2)
    while (wb.getkey()!=16):
        if(wb.getkey()==1):
            n = 1
            wb.cls(0)
            wb.str(str(wb.rand(1,6+1)),20,20,1,3)
            time.sleep(0.1)
        if(wb.getkey()==0)and(n==1):
            n = 0
            for z in range(30):
                wb.cls(0)
                wb.str(str(wb.rand(1,6+1)),20,20,1,3)
                time.sleep(0.1)
    config()
def l():
    a   = 0
    s   = 10
    mod = 0
    wb.cls(0)
    wb.str(str('Dice2 Mod'),20,20,1,2)
    while (wb.getkey()!=16):
        if(wb.getkey()==1)and(mod==0):
            mod = 1
        if(wb.getkey()==2)and(mod==1):
            mod = 0
        if(mod==1):
            if a>=180:s=-10
            if a<=0:s=10
            a += s
            servo1.write_angle(a)
            time.sleep(0.022)
    config()
config()
while True:
    print(machine.Pin(pin['555'],1).value())
    time.sleep(0.1)
# while True:
#     if(machine.Pin(pin['555'],1).value()==0):
#         hz = time.ticks_us()
#         while 
#     if(machine.Pin(pin['555'],1).value()==1):
#         hz = hz-time.ticks_us()
#         print(hz)
#     if(wb.getkey()==32):u()#u
#     if(wb.getkey()==4):r()#r
#     if(wb.getkey()==8):l()#l
#     if(wb.getkey()==64):break#start