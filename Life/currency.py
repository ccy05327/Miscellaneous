from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime

url = "https://www.findrate.tw/GBP/"
CHROME_DRIVE_PATH = "C:\\Users\\hanna\\.wdm\\drivers\\chromedriver\\win32\\98.0.4758.80\\chromedriver98.exe"


def main():
    driver = webdriver.Chrome(CHROME_DRIVE_PATH)
    driver.get(url)
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find('table')
    time.sleep(2)
    driver.quit()

    for i in tables:
        tb = i.text.split()
    now = datetime.now()
    print(now)
    print('{}: {} {} '.format(tb[4], tb[5], tb[6]))

    with open(
            "D:\\GitHub\\Miscellaneous\\Life\\currency_output.txt", 'a+', encoding='utf-8') as file:
        file.write(str(now))
        file.write('\n{}: {} {} \n'.format(tb[4], tb[5], tb[6]))
        file.write('='*30)


if __name__ == "__main__":
    main()
