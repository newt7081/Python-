# [2023/06/27]-43:03#89 #
import machine, time
from servo import Servo
pin = [5, 21, 19, 18, 22, 23]
def config():
    global star, servo2
    star = 0
    wb.cls(0)
    wb.colors(999, 999)
    wb.str(str('Frequency Mode'),20,20,1,2)
    servo2 = Servo(machine.Pin(25),min_us=600,max_us=2400,angle=180)
    servo2.write_angle(0)
class k():
    def u():
        global star
        wb.cls(0)
        wb.str(str('Star Mode'),20,20,1,2)
        def STAR(x,y):
            wb.colors(x, y)
            for z in range(star):
                wb.str(str('*'),z*20+21,star*20-20,1,3)
        while (wb.getkey()!=0):pass
        while (wb.getkey()==0):pass
        while (wb.getkey()!=16):
            servo2.write_angle(star*30)
            if(wb.getkey()==1)and(star>1):
                STAR(0,0)
                star-=1
                while (wb.getkey()!=0):pass
                time.sleep(0.025)
            if(wb.getkey()==2)and(star<6):
                if star==0:wb.cls(0)
                star+=1
                STAR(999,999)
                while (wb.getkey()!=0):pass
                time.sleep(0.025)
            time.sleep(0.1)
        config()
    def r():
        global a
        a   = 0
        mod = 0
        wb.cls(0)
        wb.str(str('Dice1 Mode'),20,20,1,2)
        def r_():
            global a
            wb.colors(0, 0)
            wb.str(str('%.0f'%a),20,40,1,2)
            a = wb.rand(1,6+1)
            wb.colors(999, 999)
            wb.str(str('%.0f'%a),20,40,1,2)
            time.sleep(0.1)
        while (wb.getkey()!=16):
            if(wb.getkey()==1):
                mod = 1
                r_()
            if mod==1:
                mod = 0
                for i in range(30):
                    r_()
        config()
    def l():
        wb.cls(0)
        wb.str(str('Dice2 Mode'),20,20,1,2)
        a   = 0
        s   = 10
        n   = 0
        mod = 0
        while (wb.getkey()!=16):
            if(wb.getkey()==1):mod = 1
            if(wb.getkey()==2):mod = 0
            if(mod==1):
                if(a>=180):s = -10
                if(a<=0):s   = 10
                a += s
                servo2.write_angle(a)
                time.sleep(0.02)
            for i in range(len(pin)):
                if machine.Pin(pin[i],1).value()==1 and  !=i+1:
                    wb.colors(0, 0)
                    wb.str(str( ),20,40,1,2)
                    mod = i+1
                    wb.colors(999, 999)
                    wb.str(str( ),20,40,1,2)
        config()
config()
while True:
    if(wb.getkey()==32):k.u()
    if(wb.getkey()==4):k.r()
    if(wb.getkey()==8):k.l()