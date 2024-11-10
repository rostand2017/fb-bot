import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from fb_functions.account import create_account
from fb_functions.account import login

def main():
    driver = webdriver.Chrome()  # Make sure you have ChromeDriver installed and in PATH

    while True:
        try:
            # Check if logged in
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "facebook")))
            # login(driver, email, password)
        except TimeoutException:
            # If not logged in, create a new account or log in with existing credentials
            try:
                print("==== Creation of the user...")
                email, password = create_account(driver)
                print("==== New created user")
                print("Email: " + email + " Password: " +password)
            except:
                print("==== Something went wrong ====")

        # Wait for 24 hours before the next iteration
        time.sleep(24 * 60 * 60)

if __name__ == "__main__":
    main()