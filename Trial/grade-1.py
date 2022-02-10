#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os

CHROME_DRIVE_PATH = "/Users/y/Downloads/chromedriver98"
BINARY_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
USER_DATA_DIR = '/Users/y/Library/Application Support/Google/Chrome/Default'
PROFILE_DIR = '/Users/y/Library/Application Support/Google/Chrome/Default/Person 1'
BSBC_HOME_TITLE = "Bachelor of Science in Computer Science | Home | Coursera"
EMAIL = ""
PASSWORD = ""

login_url = "https://www.coursera.org/degrees/bachelor-of-science-computer-science-london?authMode=login"
url = "https://www.coursera.org/degrees/bachelor-of-science-computer-science-london/home"

s=Service(ChromeDriverManager().install())
options = Options()
options.binary_location = BINARY_PATH
options.add_argument("user-data-dir="+USER_DATA_DIR)
options.add_argument("profile-directory="+PROFILE_DIR)

driver = webdriver.Chrome(options=options, service=s)
driver.set_window_position(0,0)
driver.set_window_rect(1,1)

def parsePage():
    driver.minimize_window()
    
    found_grade = False

    while found_grade == False:
        # wait a bit and click the left button twice (change later as the week increases)
        LEFT_BUTTON_PATH = '//*[@id="home-tabpanel"]/main/div/div/div/div/button[1]'

        time.sleep(1)

        driver.find_element_by_xpath(LEFT_BUTTON_PATH).click()

        time.sleep(4)

        # find all of <a> tags 
        A_TAG_PATH = '//a[@data-click-key="degree_home.degree_home_page.click.item_link"]'

        a_tags = driver.find_elements_by_xpath(A_TAG_PATH)

        # find all module titles
        SPAN_TAG_PATH = '//span[@class="bold"]'
        title_tags = driver.find_elements_by_xpath(SPAN_TAG_PATH)

        time.sleep(2)

        # if there exists a keyword "In review", that's the one
        # then, exit the while loop
        # otherwise, keep searching by click the left button again
        if len(a_tags) > 0:
            os.system("clear")
            print("Validating...\n")

            for idx, txt in enumerate(a_tags):
                content = txt.get_attribute("aria-label")
                time.sleep(1)
                if 'In Review' in content:
                    found_grade = True
                    print('#{} [{}]:\n {}\n-------------------------------------------'
                        .format(idx+1, title_tags[idx].text,content))
        print("\n")

def run():
    # time for you to be authorized
    time.sleep(2)

    # check if it's redirected to the BSCS home
    while driver.title != BSBC_HOME_TITLE:
        driver.get(url)
        parsePage()

    driver.close()

if __name__ == "__main__":
    run()