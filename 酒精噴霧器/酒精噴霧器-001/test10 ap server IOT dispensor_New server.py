#fangGu 2021 All rights reseverd.
#原開發者將保留所有著作權利。請勿修改、再發布相關的衍伸作品，否則就可能有侵害著作權的問題。

from machine import Pin, RTC, ADC, WDT
import time, socket, network, urequests, utime, gc, machine
from servo import Servo


wdt=WDT(timeout = 180*1000)   #(timeout = 秒*毫秒)設定看門狗，偵測系統是否當機，若當機則會自動重啟
ds = 0
IR = Pin(36, Pin.IN, Pin.PULL_UP)
Ms = Pin(22, Pin.OUT)                #控制馬達負極通電與否
button = Pin(23, Pin.IN, Pin.PULL_UP)
button_state = button.value()
butt = 0
print("BS:"+ str(button_state))
s1 = Servo(21)        #宣告伺服馬達物件腳位
minAngle = 170        #宣告放鬆時的馬達角度
maxAngle = 10         #宣告按壓時的馬達角度
sprayTime = 1.2       #宣告按壓後停留緩衝時間(秒)

ledR = Pin(17, Pin.OUT)
ledG = Pin(16, Pin.OUT)
ledB = Pin(2, Pin.OUT)

adc = ADC(Pin(34))
adc.atten(ADC.ATTN_6DB)    # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v) 
adc.width(ADC.WIDTH_10BIT)   # set 10 bit return values (returned range 0-1024)
value = adc.read()

RFT = 20                       #資料上傳時間(分)
web_query_delay = 60*60000     #時間更新間隔(分*60000ticks)
memory_renew = 5*60000         #噴霧次數存檔間隔(分*60000ticks) 噴一次就更新檔案，會太傷記憶體。
wifi = network.WLAN(network.STA_IF)

m = open('mode.txt')
mode = int(m.read())
m.close()
print("mode:"+ str(mode))


# ************************
# Configure the ESP32 wifi
# as Access Point mode.
ssid = 'fangGu_AD01'
password = '12345678'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)
while not ap.active():
    pass
print('network config:', ap.ifconfig())


# ************************
# Configure the socket connection
# over TCP/IP

# AF_INET - use Internet Protocol v4 addresses
# SOCK_STREAM means that it is a TCP socket.
# SOCK_DGRAM means that it is a UDP socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80)) # specifies that the socket is reachable by any address the machine happens to have
s.listen(5)     # max of 5 socket connections

# ************************
# Function for creating the
# web page to be displayed



print("initial done")        
#----------------分隔線，以下為副程式------------------

def web_page():
    if ds == 0:
        dev_state = 'Offine'
        print('device Offine')
    elif ds == 1:
        dev_state = 'Online'
        print('device Online')
        
    html_page = """<!DOCTYPE HTML>  
        <html>  
        <head>
          <meta name="viewport" content="width=device-width, initial-scale=1" charset="utf-8">
          <title>AD-01</title> 
        </head>  
        <body>  
           <center><h2> Web Server in IOT alcohol dispenser </h2></center>  
           <center>  
             <form> 
               <button type='submit' name="ds" value='0'> 離線模式(Offine Mode) </button>

               <p>WIFI帳號(wifi ssid):&nbsp;<input maxlength="30" name="Wifi ssid" size="20" type="text" /></p>
               <p>密碼(password):&nbsp;<input maxlength="50" name="password" size="20" type="password" /></p>
               <p>表單事件名稱(Google sheet value name):&nbsp;<input maxlength="30" name="Vn" size="10" type="text" />
               <p>表單金鑰(Google sheet key):&nbsp;<input maxlength="100" name="GSAk" size="20" type="password" /></p>
               <p>Line事件名稱(Line notify name):&nbsp;<input maxlength="30" name="LM" size="20" type="text" /></p>
               <p>Line金鑰(Line notify key):&nbsp;<input maxlength="100" name="Lk" size="20" type="password" /></p>
               <p>自訂設備代號(Name a device code):&nbsp;<input maxlength="30" name="DN" size="20" type="text" /></p>
               <p>關機提醒時間(Shutdown reminder): <select name="RM" size="1"><option value="1">開(On)</option><option value="0">關(Off)</option></select></p>
               <p>24小時制(ex:18點08分)&nbsp;<input maxlength="2" name="HH" size="3" type="text" /> 點 &nbsp;<input maxlength="2" name="MM" size="3" type="text" />分 </p>
               
               <p>酒精噴量(Spray Level):<select name="SP" size="1"><option value="6">少(Less)</option><option value="3">普通(Ordinary)</option><option value="1">多(More)</option></select></p>
               
               <button type='submit' name="ds" value='1'> 連接(Connect) </button>
                
             </form>
             </form> 
           </center>  
           <center><p>Device is now <strong>""" + dev_state + """</strong>.</p></center>  
           <center><p>fangGu 2021 </p></center>
        </body>  
        </html>"""
    wdt.feed()
    return html_page

def parse(str):                        #這個副程式專門用來處理資料
    arr = str.split('&')
    args = {}

    for item in arr:
        data = item.split('=')
        args[data[0]] = data[1]
    
    return args

def wifi_func():                      #wifi開啟程式，連接錯誤就要跳離線的功能還要改
    disConnect = -1
    
    print("連接 WiFi...")
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, pw)
        
    while not wifi.isconnected():
        disConnect += 1
        if disConnect <= 8:
            print("wifi not connect")
            print("連接失敗次數:" + str(disConnect))
            time.sleep(1)
            wdt.feed()
            pass
        else:
            ledR.value(1)
            ledG.value(1)
            time.sleep(1)
            offine_mode()
        pass

#*************酒精噴霧程式*****************
def online_mode():

    print("online mode is on")
    detected = True
    butt = 0
    f = open('data.txt')        #f = 打開檔名data.txt的檔案
    a = f.read()                #a = 閱讀data.txt
    f.close()                   #關閉檔案
    times = int(a)
    
    H = open('alcholM.txt')
    A = H.read()
    AM = float(A)
    print("酒精剩餘：" + str(AM) + "次")


    url = "https://maker.ifttt.com/trigger/"+ name +"/with/key/" + key     #ifttt api

    url_1 = "http://worldtimeapi.org/api/timezone/Asia/Taipei"              #時間對時 api
    
    url_2 = "http://maker.ifttt.com/trigger/"+ name2 +"/with/key/" + key2   #Line API
    

    rtc = RTC()         #建立rtc物件(real time clock microPython內鍵時間函數)

    s1.rotate(minAngle)   #命令馬達放鬆狀態


    update_time = utime.ticks_ms() - web_query_delay                      #剛開機時會是負值
    memory_update_time = (utime.ticks_ms() - memory_renew) + 6*60000       #為了讓判斷式開機後15分開始觸發

    while True:
        button = Pin(23, Pin.IN, Pin.PULL_UP)
        button_state = button.value()
        
        if button_state == 0:
            butt = 1
            for i in range(0, 200):
                button = Pin(23, Pin.IN, Pin.PULL_UP)
                button_state = button.value()
                time.sleep(0.01)
                if button_state != 0:
                    print("button_false")
                    butt = 0
                    break
        if butt == 1:
            H = open('alcholM.txt', 'W')
            AM = round(540-(250/int(SP)), 1)
            H.write(str(AM))
            H.close()
            butt = 0
            ledR.value(1)
            ledB.value(1)
            time.sleep(1)
            ledR.value(0)
            ledB.value(0)
            print("酒精剩餘：" + str(AM) + "次")
            
        
        #serch time
        if utime.ticks_ms() - update_time >= web_query_delay:         #查時間的判斷式
            
            wifi_func()
            response = urequests.get(url_1)                #呼叫校正時間API
        
            if response.status_code == 200:
            
                parsed = response.json()                 
                print("json 資料查詢成功")
                
                datetime_str = str(parsed["datetime"])   #取得鍵值datatime內容
                year = int(datetime_str[0:4])            #解析日期與時間資料
                month = int(datetime_str[5:7])
                day = int(datetime_str[8:10])
                hour = int(datetime_str[11:13])
                minute = int(datetime_str[14:16])
                second = int(datetime_str[17:19])
                subsecond = int(round(int(datetime_str[20:26])/10000))
                weekday = int(parsed["day_of_week"]) - 1  #取得星期幾的資料
                #將時機寫入rtc，更新系統時間
                rtc.datetime((year, month, day, weekday, hour, minute, second, subsecond))
                print("系統時間已更新")
                print(rtc.datetime())
            
                update_time = utime.ticks_ms()            #更新查詢時間
                
                response.close()                         #關閉response
                wifi.active(False)
                
                print('time回收前記憶體: ',gc.mem_free())
                gc.collect()
                print('time回收後記憶體: ',gc.mem_free())
                ledB.value(1)
                time.sleep(1)
                ledB.value(0)
            else:
                print("JSON 資料查詢失敗")
        #serch time
    
#        print(str(detected) + "值")
        
        if utime.ticks_ms() - memory_update_time >= memory_renew:
            f = open('data.txt', 'w')   #新增檔案，如果已經有了，就覆蓋它
            f.write(str(times))         #在檔案中寫入值，本範例為寫入變數times(變數times是噴霧次數)
            f.close()                   #關閉檔案
            H = open('alcholM.txt','w')
            H.write(str(AM))
            H.close
            print(times)
            print(AM)
            
            value = adc.read()
            val = round(coculate*value, 2)
            if val > 8.4:
                VAL = 8.4
                VALU = value
                WVAL = open('VAL.txt', 'w')
                WVAL.write(str(VAL))
                WVAL.close()
                WVALU = open('VALU.txt', 'w')
                WVALU.write(str(VALU))
                WVALU.close()
                machine.reset()
            memory_update_time = utime.ticks_ms()
            print('renew回收前記憶體: ',gc.mem_free())
            gc.collect()
            print('renew回收後記憶體: ',gc.mem_free())
            
            if val <= 6.4:
                ledR.value(1)
            else:
                ledR.value(0)
            if int(AM) <= 60:
                ledR.value(1)
                ledB.value(1)
            else:
                ledR.value(0)
                ledB.value(0)
        
        #酒精噴霧器作動觸發+旗標開關
        if IR.value() == 0 and detected == True:
            print("酒精噴霧啟動")
            ledR.value(1)
            ledG.value(1)
            ledB.value(1)
            
            for i in range(0, 70):
                time.sleep(0.01)
                if IR.value() != 0:
                    print("IR_false")
                    detected = False
                    ledR.value(0)
                    ledG.value(0)
                    ledB.value(0)
                    break
            if detected == True:
                ledR.value(0)
                ledG.value(0)
                ledB.value(0)
                Ms.value(1)
                time.sleep(0.2)           
                s1.rotate(maxAngle*int(SP))       #按壓
                time.sleep(sprayTime)     #按壓緩衝時間
                s1.rotate(minAngle)       #放鬆
                time.sleep(0.8)           #放鬆緩衝時間
                Ms.value(0)
            
                detected = False
                times += 1
                AM = int(AM)
                AM += -1
    #            f = open('data.txt', 'w')   #新增檔案，如果已經有了，就覆蓋它
    #            f.write(str(times))         #在檔案中寫入值，本範例為寫入變數times(變數times是噴霧次數)
    #            f.close()                   #關閉檔案
                print(times)
                print(AM)
        
        elif IR.value() == 1:
            detected = True
        #酒精噴霧器作動觸發+旗標開關
    
        if rtc.datetime()[5]%RFT == 0 and rtc.datetime()[6] == 0 :
            #更新google sheet資料
            value = adc.read()
            val = round(coculate*value, 2)
            wifi_func()
            f = open('data.txt')        #f = 打開檔名data.txt的檔案
            a = f.read()                #a = 閱讀data.txt
            f.close()                   #關閉檔案
            response = urequests.get(url + "?value1=" + str(a) + "&value2=" + str(val)  + "&value3=" + str(deviceN))
            
            
            if response.status_code == 200:
                print("IFTTT 呼叫成功: 傳送噴霧次數次數" + str(times) + " 次" + str(val) + "V" )
                times = 0         #傳送次數成功後，數值歸零
                f = open('data.txt', 'w')   #新增檔案，如果已經有了，就覆蓋它
                f.write(str(times))         #在檔案中寫入值，本範例為寫入變數times(變數times是噴霧次數)
                f.close()                   #關閉檔案
                response.close()                         #關閉response
                
                if val <= 6.4 or int(AM) <= 60:
                    valPer = round((val-6)/2.4*100, 1)
                    response1 = urequests.get(url_2 + "?value1="+ str(deviceN) + "&value2=" + str(val) + "(" + str(valPer) +"%)" + "&value3=" +str(AM) )      # + "?value1="+ str(deviceN) + "&value2=" + str(val) + "&value3=" +str(a)
                    print("Line")
                
                wifi.active(False)
                print('count回收前記憶體: ',gc.mem_free())
                gc.collect()
                print('count回收後記憶體: ',gc.mem_free())
                print(times)
                
            else:
                print("IFTTT 呼叫失敗")
            #更新google sheet資料
        if rtc.datetime()[4] == int(HH) and rtc.datetime()[5] == int(MM) and rtc.datetime()[6] == 0 and int(RM) == 1:
            value = adc.read()
            val = round(coculate*value, 2)
            valPer = round((val-6)/2.4*100, 1)
            wifi_func()
            response1 = urequests.get(url_2 + "?value1="+ str(deviceN) + "&value2=" + str(val) + "(" + str(valPer) +"%)" + "&value3=" +str(AM) )      # + "?value1="+ str(deviceN) + "&value2=" + str(val) + "&value3=" +str(a)
            print("Line")
   
#        print(IR.value())
#        print(times)
        wdt.feed()
        time.sleep(0.25)

def offine_mode():
#    Pin腳對照表
#    D0 = 16, D1 = 5, D2 = 4, D3 = 0, D4 = 2
#    D5 = 14, D6 = 12, D7 = 13, D8 = 15

    detected = True
    butt = 0
    
    f = open('data.txt')        #f = 打開檔名data.txt的檔案
    a = f.read()                #a = 閱讀data.txt
    f.close()                   #關閉檔案
    times = int(a)
    
    H = open('alcholM.txt')
    A = H.read()
    AM = float(A)
    H.close()
    print("酒精剩餘：" + str(AM) + "次")

    s1.rotate(minAngle)   #命令馬達放鬆狀態
    
    memory_update_time = (utime.ticks_ms() - memory_renew) + 6*60000       #為了讓判斷式開機後15分開始觸發
    
    print("離線酒精噴霧器已啟動")
    
    if utime.ticks_ms() - memory_update_time >= memory_renew:
        f = open('data.txt', 'w')   #新增檔案，如果已經有了，就覆蓋它
        f.write(times)         #在檔案中寫入值，本範例為寫入變數times(變數times是噴霧次數)
        f.close()                   #關閉檔案
        H = open('alcholM.txt','w')
        H.write(str(AM))
        H.close
        print(times)
        print(AM)
        value = adc.read()
        val = round(coculate*value, 2)
        memory_update_time = utime.ticks_ms()
        print('renew回收前記憶體: ',gc.mem_free())
        gc.collect()
        print('renew回收後記憶體: ',gc.mem_free())
        
        if val <= 6.4 and int(AM) > 60:
            ledR.value(1)
        elif val > 6.4 and int(AM) <= 60:
            ledR.value(1)
            ledB.value(1)
        if int(AM) <= 60:
            ledR.value(1)
            ledB.value(1)
        else:
            ledR.value(0)
            ledB.value(0)
        
        

    while True:
        #酒精噴霧器作動觸發+旗標開關
        button = Pin(23, Pin.IN, Pin.PULL_UP)
        button_state = button.value()
        
        if button_state == 0:
            butt = 1
            for i in range(0, 200):
                button = Pin(23, Pin.IN, Pin.PULL_UP)
                button_state = button.value()
                time.sleep(0.01)
                if button_state != 0:
                    print("button_false")
                    butt = 0
                    break
        if butt == 1:
            H = open('alcholM.txt', 'W')
            AM = round(540-(250/int(SP)), 0)
            H.write(str(AM))
            H.close()
            butt = 0
            ledR.value(1)
            ledB.value(1)
            time.sleep(1)
            ledR.value(0)
            ledB.value(0)
            
            print("酒精剩餘：" + str(AM) + "次")
            
        if IR.value() == 0 and detected == True:
            print("酒精噴霧啟動")
            ledR.value(1)
            ledG.value(1)
            ledB.value(1)
            Ms.value(1)
            for i in range(0, 100):
                time.sleep(0.01)
                if IR.value() != 0:
                    print("IR_false")
                    detected = False
                    ledR.value(0)
                    ledG.value(0)
                    ledB.value(0)
                    break
        
            if detected == True:
                ledR.value(0)
                ledG.value(0)
                ledB.value(0)
                Ms.value(1)
                time.sleep(0.2) 
                s1.rotate(maxAngle*int(SP))       #按壓
                time.sleep(sprayTime)     #按壓緩衝時間
                s1.rotate(minAngle)       #放鬆
                time.sleep(0.5)           #放鬆緩衝時間
                Ms.value(0)
            
                detected = False
                times += 1
                AM = int(AM)
                AM += -1
    #            f = open('data.txt', 'w')   #新增檔案，如果已經有了，就覆蓋它
    #            f.write(str(times))         #在檔案中寫入值，本範例為寫入變數times(變數times是噴霧次數)
    #            f.close()                   #關閉檔案
                print(times)
                print(AM)
        
        elif IR.value() == 1:
            detected = True

#        print(IR.value())
#        print(times)
        wdt.feed()
        time.sleep(0.25)
        
#*************酒精噴霧程式*****************


if button_state == 0:
    print("renew memory")
    ledG.value(1)
    time.sleep(1)
    ledG.value(0)
    while True:
        print(button.value())
        # Socket accept() 
        conn, addr = s.accept()
        print("Got connection from %s" % str(addr))
        
    # Socket receive()
        request = conn.recv(1024)
        request1 = request.decode('utf8')
        firstLine = request1.split('\r\n')[0]
        print("過濾後資訊:"+firstLine)
        

        # Socket send()
        request = str(request)
        onlineMode = request.find("/?Wifi")
        offineMode = request.find("/?ds=0")
        print("剩餘空間："+str(gc.mem_free()))
        print("onlinemode" + str(onlineMode))
        print("offinemode" + str(offineMode))
        
        if onlineMode == 6:
            str_b = firstLine.split(' ')          #firstLine字串以「空格」分開
            print("以空格分開後結果"+str(str_b))    #將結果輸出供我們觀察
            print("取出第2項"+str(str_b[1]))       #取第三項並將結果輸出供我們觀察
            str_c = parse(str_b[1])               #將取出的第三項利用副程式的功能處理產生字典
            print("產生字典"+str(str_c))           #輸出結果以供我們觀察
            ssid = str(str_c['/?Wifi+ssid'])
            pw = str(str_c['password'])
            key = str(str_c['GSAk'])
            name = str(str_c['Vn'])
            name2 = str(str_c['LM'])
            key2 = str(str_c['Lk'])
            deviceN = str(str_c['DN'])
            HH = str(str_c['HH'])
            MM = str(str_c['MM'])
            SP = str(str_c['SP'])
            RM = str(str_c['RM'])
            
            if ssid != '':
                a = open('ssid.txt', 'w')             #新增檔案，如果已經有了，就覆蓋它
                a.write(ssid)                         #在檔案中寫入值，本範例為寫入變數code(變數code是5，所以時繼被寫進數的是數字5)
                a.close()                             #關閉檔案
            else:
                a = open('ssid.txt')        #f = 打開檔名data.txt的檔案
                ssid = a.read()             #ssid = 閱讀ssid.txt
                print(ssid)                 #印出檔案內容
                a.close()                   #關閉檔案
            if pw != '':
                b = open('pw.txt', 'w')               #新增檔案，如果已經有了，就覆蓋它
                b.write(pw)                           #在檔案中寫入值，本範例為寫入變數code(變數code是5，所以時繼被寫進數的是數字5)
                b.close()                             #關閉檔案
            else:
                b = open('pw.txt')        #f = 打開檔名data.txt的檔案
                pw = b.read()             #ssid = 閱讀ssid.txt
                print(pw)                 #印出檔案內容
                b.close()                   #關閉檔案
            if key != '':
                c = open('key.txt', 'w')              #新增檔案，如果已經有了，就覆蓋它
                c.write(key)                          #在檔案中寫入值，本範例為寫入變數code(變數code是5，所以時繼被寫進數的是數字5)
                c.close()                             #關閉檔案
            else:
                c = open('key.txt')          #f = 打開檔名data.txt的檔案
                key = c.read()               #ssid = 閱讀ssid.txt
                print(key)                   #印出檔案內容
                c.close()                    #關閉檔案
                
            if name != '':
                d = open('name.txt', 'w')             #新增檔案，如果已經有了，就覆蓋它
                d.write(name)                         #在檔案中寫入值，本範例為寫入變數code(變數code是5，所以時繼被寫進數的是數字5)
                d.close()                             #關閉檔案
            else:
                d = open('name.txt')         #f = 打開檔名data.txt的檔案
                name = d.read()              #ssid = 閱讀ssid.txt
                print(name)                  #印出檔案內容
                d.close()                    #關閉檔案
            
            if name2 != '':
                e = open('name2.txt', 'w')
                e.write(name2)
                e.close()
            else:
                e = open('name2.txt')        #line notify 資料
                name2 = e.read()
                print(name2)
                e.close()
                
            if key2 != '':   
                f = open('key2.txt', 'w')
                f.write(key2)
                f.close()
            else:
                f = open('key2.txt')
                key2 = f.read()
                print(key2)
                f.close()
            
            if deviceN != '':     
                g = open('deviceN.txt', 'w')
                g.write(deviceN)
                g.close()
            else:
                g = open('deviceN.txt')
                deviceN = g.read()
                print(deviceN)
                g.close()
                
            if HH != '':    
                hh = open('HH.txt', 'w')
                hh.write(HH)
                hh.close()
            else:
                hh = open('HH.txt')
                HH = hh.read()
                print(HH)
                hh.close
            
            if MM != '':
                mm = open('MM.txt', 'w')
                mm.write(MM)
                mm.close()
            else:
                mm = open('MM.txt')
                MM = mm.read()
                print(MM)
                mm.close
                
            if SP != '':
                sp = open('SP.txt', 'w')
                sp.write(str(SP))
                sp.close()
            else:
                sp = open('SP.txt')
                SP = sp.read()
                print(SP)
                sp.close
                
            if RM != '':
                rm = open('RM.txt', 'w')
                rm.write(str(RM))
                rm.close()
            else:
                rm = open('RM.txt')
                RM = rm.read()
                print(RM)
                rm.close
            
            RVAL = open('VAL.txt')
            VAL = RVAL.read()
            print(VAL)
            RVAL.close
            
            RVALU = open('VALU.txt')
            VALU = RVALU.read()
            print(VALU)
            RVALU.close
            
            mode = 1                              #紀錄模式在記憶體，0=offine, 1=online
            m = open('mode.txt', 'w')
            m.write(str(mode))
            m.close()
            
            print("查詢wifi帳號:"+str(str_c['/?Wifi+ssid']))           #查詢wifi帳號並輸出密碼供我們觀察
            print("查詢api key:"+str(str_c['GSAk']))                        #查詢並輸出google api供我們觀察
            print("查詢wifi密碼:"+str(str_c['password']))               #查詢並輸出密碼供我們觀察
            ds = 1
            print("觸發線上模式")
            print("剩餘空間："+str(gc.mem_free()))
            
            coculate = round(float(VAL)/int(VALU), 4)
            
            conn.close()
            ap.active(False)
            online_mode()
            
        elif offineMode == 6:
            ds = 0
            print("觸發離線模式")
            str_b = firstLine.split(' ')          #firstLine字串以「空格」分開
            print("以空格分開後結果"+str(str_b))    #將結果輸出供我們觀察
            print("取出第2項"+str(str_b[1]))       #取第三項並將結果輸出供我們觀察
            str_c = parse(str_b[1])               #將取出的第三項利用副程式的功能處理產生字典
            print("產生字典"+str(str_c))           #輸出結果以供我們觀察
            ssid = str(str_c['Wifi+ssid'])
            pw = str(str_c['password'])
            key = str(str_c['GSAk'])
            name = str(str_c['Vn'])
            name2 = str(str_c['LM'])
            key2 = str(str_c['Lk'])
            deviceN = str(str_c['DN'])
            HH = str(str_c['HH'])
            MM = str(str_c['MM'])
            SP = str(str_c['SP'])
            RM = str(str_c['RM'])
            
            if ssid != '':
                a = open('ssid.txt', 'w')             #新增檔案，如果已經有了，就覆蓋它
                a.write(ssid)                         #在檔案中寫入值，本範例為寫入變數code(變數code是5，所以時繼被寫進數的是數字5)
                a.close()                             #關閉檔案
            else:
                a = open('ssid.txt')        #f = 打開檔名data.txt的檔案
                ssid = a.read()             #ssid = 閱讀ssid.txt
                print(ssid)                 #印出檔案內容
                a.close()                   #關閉檔案
            if pw != '':
                b = open('pw.txt', 'w')               #新增檔案，如果已經有了，就覆蓋它
                b.write(pw)                           #在檔案中寫入值，本範例為寫入變數code(變數code是5，所以時繼被寫進數的是數字5)
                b.close()                             #關閉檔案
            else:
                b = open('pw.txt')        #f = 打開檔名data.txt的檔案
                pw = b.read()             #ssid = 閱讀ssid.txt
                print(pw)                 #印出檔案內容
                b.close()                   #關閉檔案
            if key != '':
                c = open('key.txt', 'w')              #新增檔案，如果已經有了，就覆蓋它
                c.write(key)                          #在檔案中寫入值，本範例為寫入變數code(變數code是5，所以時繼被寫進數的是數字5)
                c.close()                             #關閉檔案
            else:
                c = open('key.txt')          #f = 打開檔名data.txt的檔案
                key = c.read()               #ssid = 閱讀ssid.txt
                print(key)                   #印出檔案內容
                c.close()                    #關閉檔案
                
            if name != '':
                d = open('name.txt', 'w')             #新增檔案，如果已經有了，就覆蓋它
                d.write(name)                         #在檔案中寫入值，本範例為寫入變數code(變數code是5，所以時繼被寫進數的是數字5)
                d.close()                             #關閉檔案
            else:
                d = open('name.txt')         #f = 打開檔名data.txt的檔案
                name = d.read()              #ssid = 閱讀ssid.txt
                print(name)                  #印出檔案內容
                d.close()                    #關閉檔案
            
            if name2 != '':
                e = open('name2.txt', 'w')
                e.write(name2)
                e.close()
            else:
                e = open('name2.txt')        #line notify 資料
                name2 = e.read()
                print(name2)
                e.close()
                
            if key2 != '':   
                f = open('key2.txt', 'w')
                f.write(key2)
                f.close()
            else:
                f = open('key2.txt')
                key2 = f.read()
                print(key2)
                f.close()
            
            if deviceN != '':     
                g = open('deviceN.txt', 'w')
                g.write(deviceN)
                g.close()
            else:
                g = open('deviceN.txt')
                deviceN = g.read()
                print(deviceN)
                g.close()
                
            if HH != '':    
                hh = open('HH.txt', 'w')
                hh.write(HH)
                hh.close()
            else:
                hh = open('HH.txt')
                HH = hh.read()
                print(HH)
                hh.close
            
            if MM != '':
                mm = open('MM.txt', 'w')
                mm.write(MM)
                mm.close()
            else:
                mm = open('MM.txt')
                MM = mm.read()
                print(MM)
                mm.close
                
            if SP != '':
                sp = open('SP.txt', 'w')
                sp.write(str(SP))
                sp.close()
            else:
                sp = open('SP.txt')
                SP = sp.read()
                print(SP)
                sp.close
            
            if RM != '':
                rm = open('RM.txt', 'w')
                rm.write(str(RM))
                rm.close()
            else:
                rm = open('RM.txt')
                RM = rm.read()
                print(RM)
                rm.close
            
            mode = 0                      #紀錄模式在記憶體，0=offine, 1=online
            m = open('mode.txt', 'w')
            m.write(str(mode))
            m.close()
            
            conn.close()
            ap.active(False)
            ledG.value(1)
            ledR.value(1)
            time.sleep(1)
            ledG.value(0)
            ledR.value(0)
            offine_mode()

            
        wdt.feed()
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)

        # Socket close()
        conn.close()
        print("時間"+ str(utime.ticks_ms()))

elif button_state == 1:
    print("memory callback")
    if mode == 0:
        ledG.value(1)
        ledR.value(1)
        time.sleep(1)
        ledG.value(0)
        ledR.value(0)
        ds = 0
        print("觸發離線模式")
                            
        ap.active(False)
        
        sp = open('SP.txt')
        SP = sp.read()
        print(SP)
        sp.close
        
        offine_mode()
                
    elif mode == 1:
        print("memory online mode")
        ledB.value(1)
        time.sleep(1)
        ledB.value(0)
                        
        a = open('ssid.txt')        #f = 打開檔名data.txt的檔案
        ssid = a.read()             #ssid = 閱讀ssid.txt
        print(ssid)                 #印出檔案內容
        a.close()                   #關閉檔案
                        
        b = open('pw.txt')          #f = 打開檔名data.txt的檔案
        pw = b.read()               #ssid = 閱讀ssid.txt
        print(pw)                   #印出檔案內容
        b.close()                   #關閉檔案

        c = open('key.txt')          #f = 打開檔名data.txt的檔案
        key = c.read()               #ssid = 閱讀ssid.txt
        print(key)                   #印出檔案內容
        c.close()                    #關閉檔案
                        
        d = open('name.txt')         #f = 打開檔名data.txt的檔案
        name = d.read()              #ssid = 閱讀ssid.txt
        print(name)                  #印出檔案內容
        d.close()                    #關閉檔案
        
        e = open('name2.txt')        #line notify 資料
        name2 = e.read()
        print(name2)
        e.close()
        
        f = open('key2.txt')
        key2 = f.read()
        print(key2)
        f.close()
        
        g = open('deviceN.txt')
        deviceN = g.read()
        print(deviceN)
        g.close()
        
        hh = open('HH.txt')
        HH = hh.read()
        print(HH)
        hh.close
        
        sp = open('SP.txt')
        SP = sp.read()
        print(SP)
        sp.close
        
        mm = open('MM.txt')
        MM = mm.read()
        print(MM)
        mm.close
        
        rm = open('RM.txt')
        RM = int(rm.read())
        print(int(RM))
        rm.close
        
        RVAL = open('VAL.txt')
        VAL = RVAL.read()
        print(VAL)
        RVAL.close
            
        RVALU = open('VALU.txt')
        VALU = RVALU.read()
        print(VALU)
        RVALU.close
        
        coculate = round(float(VAL)/int(VALU), 4)            #設定換算數值(量測到的電壓/ADC接收到的數值, 小數後四位)
        
        ap.active(False)
        online_mode()
