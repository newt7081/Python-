# [2023/07/08]-20:01#75 # *star *Hz
from servo import Servo
import machine, time
pin = [5, 21, 19, 18, 22, 23]
servo2 = Servo(machine.Pin(25),min_us=600,max_us=2400,angle=180)
def config():
    global star, mod
    star = 0
    mod  = 0
    wb.cls(0)
    wb.colors(999,999)
    wb.str(str('Frequency Mode'),20,20,1,2)
    servo2.write_angle(0)
def U():
    for i in range(star):
        wb.str(str('*'),i*20+21,star*20-20,1,3)
def u():
    global star
    wb.cls(0)
    wb.str(str('Star Mode'),20,20,1,2)
    while wb.getkey()!=0: pass
    while wb.getkey()==0 or wb.getkey()==2: pass
    wb.cls(0)
    while wb.getkey()!=16:
        if(wb.getkey()==1)and(star>1):
            wb.colors(0,0)
            U()
            star-=1
        if(wb.getkey()==2)and(star<6):
            wb.colors(999,999)
            star+=1
            U()
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
    global star, mod
    wb.cls(0)
    wb.str(str('Dice1 Mode'),20,20,1,2)
    while wb.getkey()!=16:
        if(wb.getkey()==2):
            mod = 1
            R()
        if(mod==1):
            mod = 0
            for i in range(30):
                R()
    config()
def a():pass
def b():pass
def l():
    global star, mod
    wb.cls(0)
    wb.str(str('Dice2 Mode'),20,20,1,2)
    while wb.getkey()!=16:
        for i in range(len(pin)):
            if machine.Pin(16,1).value()==1 and star!=i+1:
                wb.colors(0,0)
                wb.str(str(star),20,40,1,2)
                star = i+1
                wb.colors(999,999)
                wb.str(str(star),20,40,1,2)
        if(wb.getkey()==1):a()
        if(wb.getkey()==2):b()
    config()
config()
while True:
    if(wb.getkey()==32):u()
    if(wb.getkey()==4):r()
    if(wb.getkey()==8):l()






o = None

def _E5_81_9A_E4_BA_9B_E4_BB_80_E9_BA_BC():
    global o
    o = 0


wb.cls(0)
wb.colors(0,0)
wb.str(str('Hello'),20,20,1,1)
if(wb.getkey()==1):
    while wb.getkey()!=0: pass

while False:
    break

wb.rand(1,10+1)

servo2 = Servo(machine.Pin(2),min_us=600,max_us=2400,angle=180)
servo2.write_angle(90)
pin = machine.Pin(16,3).value(1)