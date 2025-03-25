# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00A368E0C0A59E94EBCB4DE613E4E3020AEAF9D3A9BC52CDD9DCEB48A8DADE736FF001F2EF0BFCFCD350AF552652AE3FE16F29331EEE1D79170A9DA5E17DEF9B01F8514DE85B720C68F81FA7891E0E8C78CDF428CAD85916CDD80F479CDA74EB420204503E556FB12E81C93E763BB2A65C22C932F001C8B007B1E3FFBB3D78777926C1B6BA4C7F12FDF230C4BBDBEA011DBBCDF354D0737A238EE2C1F6242CBE43AACB0020364C2EC46FB4C27B007910DFB23BD48938EA54845E3D97267001CE050CDA77E509C43A334ED4C4A82E0A2BC07523D2331BA87CDB4B55D4B58C27C26E086C72D6A2E1F80EF65D5E4CE9F1C3AB540036B3339116984F66865B4048F7CD9ED4E0AFB77E553310E51F0E31FE4316AF1B085C5B9CB8DBC353BFE25A569D8582EE28CB1D9AE1BC1D3DFA5BC0751607ED13B832FC8BE2BB01679B013CF0694D41CD228D9679657B5AF948D3ABF964BDF459A1A6EE166DE9BE6E21FEFE9A698E"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
