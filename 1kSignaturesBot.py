
from selenium import webdriver as wd
from pyautogui import press
from time import sleep
from faker import Faker
import json
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

print("""
  ____  _             ____        _
 / ___|(_) __ _ _ __ | __ )  ___ | |_
 \___ \| |/ _` | '_ \|  _ \ / _ \| __|
  ___) | | (_| | | | | |_) | (_) | |_
 |____/|_|\__, |_| |_|____/ \___/ \__|
          |___/
""")

fname = json.loads(open('fnames.json').read())
lname = json.loads(open('lnames.json').read())
#defualt_driver = wd.Chrome()
fake = Faker()
link = input("Enter Petition Link: ")

options = wd.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
defualt_driver = wd.Chrome(options=options)

def sendForm(runs):
        randfname = random.randrange(1000)
        randlname = random.randrange(1000)
        randemail = fake.email()
        fnamebox = defualt_driver.find_element_by_name("firstName")
        lnamebox = defualt_driver.find_element_by_name("lastName")
        emailbox = defualt_driver.find_element_by_name("email")
        signbutton = defualt_driver.find_element_by_xpath('//*[@id="page"]/div[2]/div[3]/div[2]/div/div/div/div[2]/div[2]/form/button[2]')
        publiccheck = defualt_driver.find_element_by_name("public")
        print("Using name", fname[randfname], lname[randlname], "and email", randemail, "This is run number", runs)
        fnamebox.send_keys(fname[randfname])
        lnamebox.send_keys(lname[randlname])
        emailbox.send_keys(randemail)
        sleep(0.5)
        publiccheck.click()
        sleep(0.5)
        signbutton.click()
        sleep(3)
        try:
            WebDriverWait(defualt_driver, 1).until(EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
            WebDriverWait(defualt_driver, 11).until(
               EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
            input("press enter after filling captcha and signing")
        except:
            print()
        defualt_driver.delete_all_cookies()
        defualt_driver.get(link)

def main():
    defualt_driver.get(link)
    runsMade = 0
    for _ in range(1, 1000):
        try:
            sendForm(runsMade)
            runsMade += 1
        except:
            defualt_driver.delete_all_cookies()
            defualt_driver.get(link)
            print("Error filling form. Refreshing...")
main()
