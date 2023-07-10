import time
star = 0
wb.cls(0)
def n(x, z):
    for y in range(x):
        wb.box((x*4)+16,(120-y*4),4,4,z)
    time.sleep(0.1)
while True:
    if(wb.getkey()==1)and(star<30):
        star += 1
        n(star, (0x60fe))
    if(wb.getkey()==2)and(star>1):
        n(star, 0)
        star -= 1