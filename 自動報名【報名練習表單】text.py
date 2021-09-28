'''
{pip install selenium}
# 瀏覽器驅動程式網址
Chrome: http://chromedriver.chromium.org/downloads
Firefox: https://github.com/mozilla/geckodriver/releases
'''
# ------------------------------------------------------------>
'''練習表單'''
from selenium import webdriver  
import os
import time

'''初始設定'''
#引入chromedriver.exe
chromedriver = "C:/Program Files/Google/Chrome/Application/chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)
#設定瀏覽器需要開啟的url
url = "https://forms.gle/YdKrpTpS3XCGmxUN7"
browser.get(url)

# if browser.isElementPresent("class","appsMaterialWizToggleRadiogroupOffRadio exportOuterCircle") is True:
# 	time.sleep(3)
# 	browser.refresh()
# else:
# 	time.sleep(3)
# 	print("123")
# 	browser.refresh()

# ------------------------------------------------------------>
'''第一頁'''
# 選擇
browser.find_element_by_css_selector("[class='appsMaterialWizToggleRadiogroupOffRadio exportOuterCircle']").click()
# 繼續(下一頁)
browser.find_element_by_css_selector("[jsname='OCpkoe']").click()
time.sleep(0.5)

'''第二頁'''
# 簡答
browser.find_element_by_css_selector("[aria-labelledby='i1']").click()
browser.find_element_by_css_selector("[aria-labelledby='i1']").send_keys("李秋林")
browser.find_element_by_css_selector("[aria-labelledby='i29']").click()
browser.find_element_by_css_selector("[aria-labelledby='i29']").send_keys("0906823786")
browser.find_element_by_css_selector("[aria-labelledby='i33']").click()
browser.find_element_by_css_selector("[aria-labelledby='i33']").send_keys("celine556688@gmail.com")
# 選擇
browser.find_element_by_css_selector("[data-value='男']").click()
browser.find_element_by_css_selector("[data-value='非會員  \(15歲以上歡迎免費加入\)  tinyurl.com/9vduyjsz']").click()
# 下拉選單
time.sleep(0.2)
browser.find_element_by_css_selector("[aria-labelledby='i37']").click()
browser.find_element_by_css_selector("[data-value='退休']").click()
