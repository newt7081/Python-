import machine
mod = 0
pin = [5, 21, 19, 18, 22, 23]
wb.cls(0)
def r():
    global n
    wb.cls(0)
    n = wb.rand(1,6)
    if n!=1:
        wb.box(20,20,20,20,(0xe637))
        wb.box(100,100,20,20,(0xe637))
    if n==1 or n==3 or n==5:
        wb.box(60,60,20,20,(0x00f8))
    if n==4 or n==5 or n==6:
        wb.box(20,100,20,20,(0xe637))
        wb.box(100,20,20,20,(0xe637))
    if n==6:
        wb.box(20,60,20,20,(0xe637))
        wb.box(100,60,20,20,(0xe637))
    time.sleep(0.1)
while True:
    if(wb.getkey()==1):
        mod = 1
        r()
    if(mod==1)and(wb.getkey()==0):
        for i in range(15):
            r()
        for i in range(len(pin)):
            if(machine.Pin(pin[i],3).value()):
                mod = i+1
        if mod==n:
            print('平手')
        elif mod>n:
            print('輸')
        elif mod<n:
            print('贏')
        mod = 0