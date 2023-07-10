from servo import Servo
import time, machine
pin = {'servo':25, '555':26, '4017':[5, 21, 19, 18, 22, 23]}
def config():
    global servo1, star, mod
    mod = 0
    star = 0
    wb.cls(0)
    wb.str(str('Hello'),20,20,1,1)
    servo1 = Servo(machine.Pin(pin['servo']),min_us=600,max_us=2400,angle=180)
    servo1.write_angle(0)
def r():# Dice1 Mod
    wb.cls(0)
    wb.str(str('Dice1 Mod'),20,20,1,2)
def l():# Dice2 Mod
    wb.cls(0)
    wb.str(str('Dice2 Mod'),20,20,1,2)
def d():pass
def u():# Star Mod
    wb.cls(0)
    if star>6:star=6
    if star>1:star=1
    wb.str(str('*'),20,20,1,3)
config()
while True():
    if(wb.getkey()==1):
        pass# a
#     if(wb.getkey()==2) and mod==3:star+=1# b
#     if(wb.getkey()==4) and mod==0 or mod==1:# r
#         mod = 1
#     if(wb.getkey()==8) and mod==0 or mod==2:# l
#         mod = 2
#     if(wb.getkey()==16) and mod!=0:# d
#         mod = 0
#         config()
#     if(wb.getkey()==32) and mod==0 or mod==3:# u
#         mod = 3
#     if wb.getkey()==64 and mod==0:break# start
