from servo import Servo
import machine as ma
import time
a = 0
n = -10
mod = 0
servo1 = Servo(machine.Pin(25),min_us=600,max_us=2400,angle=180)
servo1.write_angle(a)
while True:
    if(wb.getkey()==1):mod=1# A
    if(wb.getkey()==2):mod=0# B
    if mod==1:
        if a>=180:n=-10
        if a<=0:n=10
        a += n
        servo1.write_angle(a)
        time.sleep(0.025)