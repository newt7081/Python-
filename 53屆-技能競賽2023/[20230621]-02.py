from servo import Servo
import machine as ma
import time
a = 0# 當前
b = 1# 速度
n = 1# 速度2
mod = 0
servo1 = Servo(machine.Pin(25),min_us=600,max_us=2400,angle=180)
servo1.write_angle(a)
while True:
    if(wb.getkey()==1):
        mod=1# A
    if(wb.getkey()==2):
        b = 1
        mod=0# B
    #-----------------------------
    if mod==1:
        if a>=180:
            if b<=10:b+=1
            n = b-(b*2)
        if a<=0:
            if b<=10:b+=1
            n = b
        a += n
        servo1.write_angle(a)
        time.sleep(0.025)