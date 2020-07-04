from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
    time.sleep(1)

    browser.get('https://shimo.im')
    login_btn = browser.find_element_by_xpath("//button[@class='login-button btn_hover_style_8']")
    login_btn.click()

    browser.find_element_by_xpath("//input[@name='mobileOrEmail']").send_keys("356545057@qq.com")
    browser.find_element_by_xpath("//input[@type='password']").send_keys("test123test456")
    time.sleep(1)
    browser.find_element_by_xpath("//button[@class='sm-button submit sc-1n784rm-0 bcuuIb']")

    cookies = browser.get_cookies()
    print(cookies)
    time.sleep(3)

except Exception as e:
    print(e)

finally:
    browser.close()
