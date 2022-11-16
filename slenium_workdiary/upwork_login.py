import os.path
import pickle
import random
import time

import undetected_chromedriver as uc
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from slenium_workdiary.config import *

# local variables
LOGIN_URL = 'https://www.upwork.com/ab/account-security/login'


class Driver:
    """Get the chrome driver ready"""

    def __init__(self, url=LOGIN_URL, cookies=None):
        try:
            opt = uc.ChromeOptions()
            opt.add_argument("--auto-open-devtools-for-tabs")
            opt.add_argument("--incognito")
            self.driver = uc.Chrome(use_subprocess=True, options=opt)
            self.driver.get(url)
            if cookies:
                for cookie in cookies:
                    self.driver.add_cookie({'name': cookie['name'], 'value': cookie['value']})
            self.driver.refresh()

        except WebDriverException as e:
            print(str(e))
            # self.log(f'Failed to initiate chrome driver : {str(e)}')
            pass


class UpworkLogin(Driver):
    """Login into upwork and extract the cookies"""

    def __init__(self):
        Driver.__init__(self)
        self.wait = WebDriverWait(self.driver, ELEMENT_TIMEOUT)

    # @Common.retry(times=3, exceptions=(TimeoutException, ElementClickInterceptedException))
    def accept_cookies(self):
        accept_cookies = self.wait.until(ec.presence_of_element_located((By.XPATH, ACCEPT_COOKIES_XPATH)))
        try:
            accept_cookies.click()
        except (TimeoutException, ElementClickInterceptedException) as e:
            print(f'Error : {str(e)}')

    def login(self):

        # self.accept_cookies()

        email = self.wait.until(ec.presence_of_element_located((By.XPATH, EMAIL_XPATH)))
        email.click()
        email.send_keys(EMAIL)
        time.sleep(random.randint(1, 5))

        login_button = self.wait.until(ec.presence_of_element_located((By.XPATH, LOGIN_BUTTON_XPATH)))
        login_button.click()
        time.sleep(random.randint(1, 5))

        remember_login = self.wait.until(ec.presence_of_element_located((By.XPATH, REMEMBER_ME_XPATH)))
        remember_login.click()
        passw = self.wait.until(ec.presence_of_element_located((By.XPATH, PASS_XPATH)))
        passw.click()
        passw.send_keys(PASSW)
        time.sleep(random.randint(1, 5))

        login_button_2 = self.wait.until(ec.presence_of_element_located((By.XPATH, LOGIN_BUTTON_XPATH_2)))
        login_button_2.click()
        time.sleep(10)

        if 'best-matches' in self.driver.current_url:
            self.driver.get('https://www.upwork.com/nx/workdiary/')
            time.sleep(5)
            return True
        else:
            return False


if __name__ == '__main__':
    """
    # TODO:
    1. Find a Solution for re_captcha
    2. Make upwork_login a full reusable class
    3. Create an update function
    """
    if not os.path.exists('cookies.pkl'):
        print('Cookies found')
        with open('cookies.pkl', 'rb') as f:
            d = Driver(url='https://www.upwork.com/nx/workdiary/', cookies=pickle.load(f))
            time.sleep(20)
            print(d.driver.get_cookies())
            # pickle.dump(d.driver.get_cookies(), open("cookies.pkl", "wb"))
            print('Successfully updated the old cookies')
    else:
        try:
            upwork = UpworkLogin()
            if upwork.login():
                print('Succesfully Logged In')
                pickle.dump(upwork.driver.get_cookies(), open("cookies.pkl", "wb"))
                upwork.driver.close()
            else:
                print('Login Failed')
        except Exception as e:
            print(str(e))
