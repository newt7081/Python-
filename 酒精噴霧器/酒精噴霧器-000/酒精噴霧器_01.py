from machine import Pin
from time import sleep
from servo import Servo

'''變數設定'''
Ms = Pin(22, Pin.OUT)                #控制馬達負極通電與否
s1 = Servo(21)        #宣告伺服馬達物件腳位
minAngle = 170        #宣告放鬆時的馬達角度
maxAngle = 10         #宣告按壓時的馬達角度
sprayTime = 1.2       #宣告按壓後停留緩衝時間(秒)
s1.rotate(minAngle)   #命令馬達放鬆狀態
SP = 6

IR = Pin(36, Pin.IN, Pin.PULL_UP)
s1 = Servo(21)
ledR = Pin(17, Pin.OUT)
ledG = Pin(16, Pin.OUT)
ledB = Pin(2, Pin.OUT)

ledState = 0

'''程式執行'''
while True:
    IRV=IR.value()
    print(IRV)
    if IRV==0:
        Ms.value(1)
        sleep(0.2)
        ledState = not ledState
        ledG.value(ledState)
        s1.rotate(maxAngle*int(SP))       #按壓
        sleep(sprayTime)     #按壓緩衝時間
        s1.rotate(minAngle)       #放鬆
        sleep(1)           #放鬆緩衝時間
        Ms.value(0)
        ledState = not ledState
        ledG.value(ledState)
    sleep(0.5)