# [2023/06/30]-04:47#18 #
import time, machine
from servo import Servo
servo2 = Servo(machine.Pin(25),min_us=600,max_us=2400,angle=180)
def config():
    global star, mod
    mod  = 0
    star = 0
    wb.cls(0)
    wb.colors(999,999)
    servo2.write_angle(0)
    wb.str(str('Frequency Mode'),20,20,1,2)
config()
t = 0
h = 2
text = 0
time_ = 0
while True:
    if(machine.Pin(26,1).value()==1)and(h==2):
        h = 1
        t = time.ticks_us()
    elif(machine.Pin(26,1).value()==0)and(h==1):h = 0
    elif(machine.Pin(26,1).value()==1)and(h==0):
        h = 2
        t = 1000000/(time.ticks_us()-t)
        if(time.ticks_us()-time_>=1000000):
            wb.colors(0,0)
            wb.str(str('%.2f Hz'%text),20,40,1,2)
            wb.colors(999,999)
            wb.str(str('%.2f Hz'%t),20,40,1,2)
            text = t
            time_ = time.ticks_us()
    if(wb.getkey()==32):pass
    if(wb.getkey()==4):pass
    if(wb.getkey()==8):pass