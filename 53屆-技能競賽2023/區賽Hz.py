import machine
import utime

# 設定IO2腳位為輸入腳
input_pin = machine.Pin(26, machine.Pin.IN)

# 設定IO26腳位為類比輸入腳
adc_pin = machine.ADC(machine.Pin(2))
# 設定ADC為3.3V範圍
adc_pin.atten(machine.ADC.ATTN_11DB)
# 設定ADC為12BIT精度
adc_pin.width(machine.ADC.WIDTH_12BIT)

# 初始化各種變數初始值
last_time = utime.ticks_us()
current_time = 0

# 訊號週期計數變數
high_time = 0

# 顯示或是ADC轉換切換變數
count_show = 0

# IO2正負緣偵測變數
input_value = 0
last_input_value = 0

# 計算ADC的最大值和參考電壓設定
last_time_adc = utime.ticks_us()
max_adc = 2 ** 12 - 1  # 12位元的ADC最大值
ref_voltage = 3.3      # 參考電壓3.3V

# 計算頻率用變數
frequency = 0

# 清除螢幕
wb.cls()

while True:
    # 讀取輸入IO2狀態
    last_input_value = input_value    
    input_value = input_pin.value()

    # 如果檢測到IO2從高電位變為低電立時，開始記錄時間，並將count_show設為1
    current_time = utime.ticks_us()
    if input_value == 0 and last_input_value == 1 and count_show == 0:
        last_time = utime.ticks_us()
        count_show = 1
    else:
        # 如果檢測到IO2從高電位變為低電立時，並count_show為1時，計算週期長度，並計算頻率
        if input_value == 0 and last_input_value == 1 and count_show == 1:
            high_time = utime.ticks_diff(current_time, last_time)
            count_show = 0
            frequency = 1/(float(high_time)/1000000.0)
            
    # 每一秒讀取ADC並顯示電壓值，如一直沒有IO2輸入則每二秒讀取一次
    if (utime.ticks_diff(current_time, last_time_adc) > 1000000 and count_show == 1) or utime.ticks_diff(current_time, last_time_adc) > 2000000:
        # 讀取ADC並轉換為電壓
        last_time_adc = utime.ticks_us()
        adc_value = adc_pin.read_uv()
        voltage = adc_value/1000000.0
        # 顯示頻率和電壓值
        wb.cls()
        wb.str('Frequency: %.2f Hz' % frequency, 8, 0, 3, 1)
        wb.str('Voltage: %.2f V' % voltage, 8, 16, 3, 1)
