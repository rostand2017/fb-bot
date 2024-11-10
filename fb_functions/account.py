import time
import random
import string
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from fb_functions import cookies
from server_functions.email_serv import get_facebook_registration_code

def generate_random_info():
    # TODO: generate normal first and lastname because facebook can recognize fake names
    response = requests.get('https://randomuser.me/api')
    data = response.json()['results'][0]
    first_name = data['name']['first']
    last_name = data['name']['last']
    email = data['email'].replace('@example.com', '@toncode.ca')
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    gender = data['gender']
    return first_name, last_name, email, password, gender

def create_account(driver):
    first_name, last_name, email, password, gender = generate_random_info()

    driver.get("https://www.facebook.com/r.php")
    cookies.ignore(driver)
    # Fill in the registration form
    driver.find_element(By.NAME, "firstname").send_keys(first_name)
    driver.find_element(By.NAME, "lastname").send_keys(last_name)
    driver.find_element(By.NAME, "reg_email__").send_keys(email)
    driver.find_element(By.NAME, "reg_passwd__").send_keys(password)

    # Select birthday
    driver.find_element(By.NAME, "birthday_month").send_keys(random.randint(1, 12))
    driver.find_element(By.NAME, "birthday_day").send_keys(random.randint(1, 28))
    driver.find_element(By.NAME, "birthday_year").send_keys(random.randint(1970, 2000))

    # Select gender
    if gender.lower() == "male":
        driver.find_element(By.XPATH, "//input[@name='sex' and @value='2']").click()
    else:
        driver.find_element(By.XPATH, "//input[@name='sex' and @value='1']").click()

    # Submit the form
    time.sleep(10)
    driver.find_element(By.NAME, "websubmit").click()
    confirm_email(driver, email)
    return email, password

def login(driver, email, password):
    driver.get("https://www.facebook.com")

    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.NAME, "login").click()

def confirm_email(driver, email):
    print("Confirmation of the email")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "code"))
    )
    code = get_facebook_registration_code(email)
    driver.find_element(By.NAME, "code").send_keys(code)
    driver.find_element(By.NAME, "confirm").click()