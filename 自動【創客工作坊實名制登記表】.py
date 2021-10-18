'''
{pip install selenium}
# 瀏覽器驅動程式網址
Chrome: http://chromedriver.chromium.org/downloads
Firefox: https://github.com/mozilla/geckodriver/releases
'''
# ------------------------------------------------------------>
'''【創客工作坊報名表單】'''
from selenium import webdriver  
import os
import time

'''初始設定'''
#引入chromedriver.exe
chromedriver = "C:/Program Files/Google/Chrome/Application/chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)
#設定瀏覽器需要開啟的url
url = "https://reurl.cc/zW6KLV"
browser.get(url)

# ------------------------------------------------------------>
'''第一頁'''
# 簡答
browser.find_element_by_css_selector("[aria-labelledby='i1']").click()
browser.find_element_by_css_selector("[aria-labelledby='i1']").send_keys("李俊頡")
browser.find_element_by_css_selector("[aria-labelledby='i5']").click()
browser.find_element_by_css_selector("[aria-labelledby='i5']").send_keys("0906823786")
# 選擇
browser.find_element_by_css_selector("[data-value='學生']").click()
browser.find_element_by_css_selector("[data-value='參加工作坊課程']").click()
browser.find_element_by_css_selector("[id='i94']").click()
browser.find_element_by_css_selector("[id='i104']").click()
browser.find_element_by_css_selector("[id='i114']").click()
browser.find_element_by_css_selector("[id='i136']").click()
browser.find_element_by_css_selector("[id='i146']").click()
# browser.find_element_by_css_selector("[id='i160']").click()
browser.find_element_by_css_selector("[id='i163']").click()   # 疫苗是
browser.find_element_by_css_selector("[id='i170']").click()
browser.find_element_by_css_selector("[jsname='M2UYVd']").click()
