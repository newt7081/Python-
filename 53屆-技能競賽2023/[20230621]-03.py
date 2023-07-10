# ' * '距離:x=21, y=20
from servo import Servo
import machine as ma
import time, math
a = 0# 當前
b = 1# 速度
s = 1# 速度2
n = 0# 星星
mod = 0
wb.cls(0)
servo1 = Servo(machine.Pin(25),min_us=600,max_us=2400,angle=180)
servo1.write_angle(a)
def star(x):
    n = math.ceil(a/30)
    wb.colors(999,999)
    for z in range(x):
        wb.str(str('*'),x*20+1,100-z*20,1,3)
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
            s = b-(b*2)
        if a<=0:
            if b<=10:b+=1
            s = b
        a += s
        servo1.write_angle(a)
        print(math.ceil(a/30))
        if n!=math.ceil(a/30) and s>0 and math.ceil(a/30)<7:
            star(math.ceil(a/30))
        if n!=math.ceil(a/30) and s<0 and math.ceil(a/30)>0:
            pass
        time.sleep(0.025)

# wb.colors(0,0)
