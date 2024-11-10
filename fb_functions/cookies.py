from selenium.webdriver.common.by import By
import time

de_cookie_btn_text = "Optionale Cookies ablehnen"
en_cookie_btn_text = ""
fr_cookie_btn_text = ""

def ignore(driver):
    # Wait for and handle the cookie consent prompt
    time.sleep(5)
    ignore_cookie_btn = driver.find_element(By.CSS_SELECTOR, f"div[aria-label='{de_cookie_btn_text}']")
    ignore_cookie_btn.click()