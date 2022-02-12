#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import datetime
import os

W = '\033[0m'
Y = '\033[33m'

# Mac
# CHROME_DRIVE_PATH = "/Users/ccy05327/Downloads/chromedriver"
# BINARY_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# USER_DATA_DIR = "/Users/ccy05327/Library/Application Support/Google/Chrome/Default"
# PROFILE_DIR = "/Users/ccy05327/Library/Application Support/Google/Chrome/Default/Profile 1"
# Windows
CHROME_DRIVE_PATH = "C:\\Users\\hanna\\.wdm\\drivers\\chromedriver\\win32\\98.0.4758.80\\chromedriver98.exe"
BINARY_PATH = "C:\\Program Files\\Google\\Chrome\Application\\chrome.exe"
USER_DATA_DIR = "C:\\Users\\hanna\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
PROFILE_DIR = "C:\\Users\\hanna\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Profile 1"
BSBC_HOME_TITLE = "Bachelor of Science in Computer Science | Home | Coursera"

login_url = "https://www.coursera.org/degrees/bachelor-of-science-computer-science-london?authMode=login"
url = "https://www.coursera.org/degrees/bachelor-of-science-computer-science-london/home"

# s = Service(ChromeDriverManager().install())
s = Service(CHROME_DRIVE_PATH)
options = Options()
options.binary_location = BINARY_PATH
options.add_argument("--user-data-dir="+USER_DATA_DIR)
options.add_argument("--profile-directory=Profile 1")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('log-level=3')
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options, service=s)
driver.set_window_position(0, 800000)
# driver.set_window_rect(1, 1)


def parsePage():
    # driver.minimize_window()
    found_grade = False

    while found_grade == False:
        # wait a bit and click the left button twice (change later as the week increases)
        LEFT_BUTTON_PATH = "//*[@id='home-tabpanel']/main/div/div/div/div/button[1]"
        time.sleep(1)
        driver.find_element(By.XPATH, LEFT_BUTTON_PATH).click()
        time.sleep(5)

        # find all of <a> tags
        A_TAG_PATH = "//a[@data-click-key='degree_home.degree_home_page.click.item_link']"
        a_tags = driver.find_elements(By.XPATH, A_TAG_PATH)
        time.sleep(2)

        # if there exists a keyword "In review", that's the one
        # then, exit the while loop
        # otherwise, keep searching by click the left button again
        if len(a_tags) > 0:
            for idx, txt in enumerate(a_tags):
                content = txt.get_attribute("aria-label")
                title_strings = txt.get_attribute(
                    "data-track-href").split("/")[2].split("-")
                title = " ".join(title_strings[1:])
                current_time = datetime.datetime.now()
                time.sleep(1)
                if 'In Review' in content:
                    found_grade = True
                    with open('D:\\GitHub\\Miscellaneous\\Trial\\grade_output.txt', 'w', encoding='utf-8') as file:
                        file.writelines([current_time, '#{} [{}]:\n{}'.format(
                            idx+1, title.upper(), content), '-'*76])
                    print(current_time)
                    print(Y+'#{} [{}]:\n{}'.format(idx +
                          1, title.upper(), content))
                    print(W+'-'*76)
        # print("\n")


def run():
    # time for you to be authorized
    # check if it's redirected to the BSCS home
    time.sleep(2)
    while driver.title != BSBC_HOME_TITLE:
        driver.get(url)
        os.system("cls")
        print("Validating...\n")
        try:
            parsePage()
        except Exception as e:
            driver.quit()
            # print(e)
        print("\n")
    driver.quit()


if __name__ == "__main__":
    run()
