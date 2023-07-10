# [2023/06/29]-00:57 #
import time
from servo import Servo
import machine

o = None

def _E5_81_9A_E4_BA_9B_E4_BB_80_E9_BA_BC():
    global o
    o = 0


for count in range(10):
    break

wb.cls(0)
wb.colors(0,0)
wb.str(str('Hello'),20,20,1,1)
if(wb.getkey()==1):
    pass

wb.rand(1,10+1)

time.ticks_us()

servo2 = Servo(machine.Pin(2),min_us=600,max_us=2400,angle=180)
servo2.write_angle(90)

machine.Pin(17,1).value()
