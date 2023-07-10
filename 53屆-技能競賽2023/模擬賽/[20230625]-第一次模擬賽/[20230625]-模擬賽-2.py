from servo import Servo
pin = {'servo':25, '555':26, '4017':[5, 21, 19, 18, 22, 23]}
def config():
    global servo1, mod, star, n
    n    = 0
    mod  = 0
    star = 0
    wb.cls()
    wb.str(str('H'),20,20,1,2)
    servo1 = Servo(machine.Pin(pin['servo']),min_us=600,max_us=2400,angle=180)
    servo1.write_angle(0)
def star_n(x, y):
    if y=='+':
    if y=='-':
    for z in range(x):
    	wb.str(str('*'),20,y*20,1,2)
while True:
    if(wb.getkey()==1)and(mod==3):n-=1# a
    if(wb.getkey()==2)and(mod==3):n+=1# b
    if((wb.getkey()==4)and(mod==0))or(mod==1):# r
        mod = 1
        wb.cls()
        wb.str(str('Dice1 Mod'),20,20,1,2)
    if((wb.getkey()==8)and(mod==0))or(mod==2):# l
        mod = 2
        wb.cls()
        wb.str(str('Dice2 Mod'),20,20,1,2)
    if(wb.getkey()==16)and(mod!=0):# d
        config()
    if((wb.getkey()==32)and(mod==0))or(mod==3):# u
        mod = 3
        wb.cls()
        wb.str(str('Star Mod'),20,20,1,2)
    if(wb.getkey()==64)and(mod==0):pass# start
