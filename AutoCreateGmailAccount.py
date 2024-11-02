# -*- coding: utf-8 -*-
# @Author: Chao
# @Date:   2018-08-23 22:57:28
# @Last Modified by:   Chao
# @Last Modified time: 2018-11-02 10:04:50

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import random
import time
import sys


class CreateGmail:
    """Auto Create Gmail Accounts with popular names"""

    def __init__(self, firstname, lastname, username, pswd):
        self._firstname = firstname
        self._lastname = lastname
        self._username = username
        self._pswd = pswd
        self._Donefile = open("./data/CreatedAccounts.csv", "a")
        self.Initialize()

    def Initialize(self):
        self._browser = webdriver.Chrome()
        self._browser.delete_all_cookies()
        self._browser.get("https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp")

    def SetRecoveryEmail(self):
        CreatedEmails = pd.read_csv("./data/CreatedAccounts.csv")[
            "username"
        ].values
        if len(CreatedEmails) < 1:
            self.recovery_email = "pj.cs.vt@gmail.com"
        else:
            self.recovery_email = CreatedEmails[-1] + "@gmail.com"

    def CreateAccount(self):
        wait = WebDriverWait(self._browser, 20)
        
        # Fill in first name
        first_name_elem = wait.until(EC.presence_of_element_located((By.NAME, 'firstName')))
        first_name_elem.send_keys(self._firstname)
        time.sleep(1)
        
        # Fill in last name
        last_name_elem = wait.until(EC.presence_of_element_located((By.NAME, 'lastName')))
        last_name_elem.send_keys(self._lastname)
        time.sleep(1)
        
        # Fill in username
        username_elem = wait.until(EC.presence_of_element_located((By.NAME, 'Username')))
        username_elem.send_keys(self._username)
        time.sleep(1)
        
        # Fill in password
        password_elem = wait.until(EC.presence_of_element_located((By.NAME, 'Passwd')))
        password_elem.send_keys(self._pswd)
        time.sleep(1 + 3 * random.random())
        
        # Confirm password
        confirm_password_elem = wait.until(EC.presence_of_element_located((By.NAME, 'ConfirmPasswd')))
        confirm_password_elem.send_keys(self._pswd)
        
        # Click next button
        next_button_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']/parent::button")))
        next_button_elem.click()
        self._browser.implicitly_wait(10)

        try:
            month_elem = wait.until(EC.presence_of_element_located((By.ID, "month")))
            month_elem.click()
            month_option_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='month']/option[%d]" % random.randint(1, 12))))
            month_option_elem.click()
        except:
            self._browser.quit()
            sys.exit("IP Mac Limited. Stop the Script...")
        else:
            time.sleep(1 + 3 * random.random())
            day_elem = wait.until(EC.presence_of_element_located((By.ID, 'day')))
            day_elem.send_keys(random.randint(1, 28))
            time.sleep(1)
            year_elem = wait.until(EC.presence_of_element_located((By.ID, 'year')))
            year_elem.send_keys(random.randint(1990, 2000))
            time.sleep(1)
            try:
                gender_elem = wait.until(EC.element_to_be_clickable((By.ID, "gender")))
                gender_elem.click()
                gender_option_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='gender']/option[%d]" % random.randint(1, 4))))
                gender_option_elem.click()
            except:
                print("Cannot locate Gender Block, Please manually click it. Sleep 1 min...")
                time.sleep(60)
                pass
            time.sleep(1 + 3 * random.random())
            personal_details_next_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']/parent::button")))
            personal_details_next_elem.click()
            self._browser.implicitly_wait(10)
            time.sleep(1)
            while True:
                try:
                    captcha_elem = self._browser.find_element(By.CSS_SELECTOR, ".mUbCce")
                    captcha_elem.click()
                    time.sleep(1)
                except Exception as e:
                    print(e)
                    break
            terms_of_service_next_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='I agree']/parent::button")))
            terms_of_service_next_elem.click()
            self._browser.implicitly_wait(10)

            self._Donefile.write(self._username + "," + self._pswd + "\n")
            print(self._username + ": Success")
            self._browser.quit()

    @staticmethod
    def GetUserInfo(firstnamefile, lastnamefile):
        FirstName = pd.read_csv(firstnamefile).sample(frac=1)
        LastName = pd.read_csv(lastnamefile).sample(frac=1)
        num = min(len(FirstName), len(LastName))
        if len(FirstName) > len(LastName):
            UserInfo = LastName.copy()
            UserInfo["firstname"] = FirstName.iloc[:num].values.flatten()
        else:
            UserInfo = FirstName.copy()
            UserInfo["lastname"] = LastName.iloc[:num].values.flatten()
        UserInfo.index = range(num)
        UserInfo.dropna(inplace=True)
        suffix = "".join([str(random.randint(0, 9)) for _ in range(6)])
        UserInfo["username"] = UserInfo["firstname"] + UserInfo["lastname"] + suffix
        UserInfo["pswd"] = "super" + UserInfo["firstname"] + "233"
        return UserInfo

    def RunAppsScript(self, sharedlink):
        """So far, cannot auto totally
        
        Open sharedlink and then, plz manually finish Install. 
        """
        self._browser.get(sharedlink)
        time.sleep(10)


if __name__ == "__main__":
    SharedScript = "https://script.google.com/d/1yihwFAHrV17XHYmnrOJxQasqWGourSD57Xi-oFYO3sgY-B1_inPt5Vkc/edit?usp=sharing"

    firstnamefile = "./data/CSV_Database_of_First_Names.csv"
    lastnamefile = "./data/CSV_Database_of_Last_Names.csv"
    UserInfoDF = CreateGmail.GetUserInfo(firstnamefile, lastnamefile)
    for num in range(len(UserInfoDF)):
        UserInfoSeries = UserInfoDF.loc[num]
        CGM = CreateGmail(*UserInfoSeries)
        CGM.CreateAccount()
        # CGM.RunAppsScript(SharedScript)