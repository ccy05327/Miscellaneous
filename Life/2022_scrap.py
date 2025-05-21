from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime

url1 = "https://bank.sinopac.com/MMA8/bank/html/rate/bank_ExchangeRate.html"
url2 = "https://accessibility.scsb.com.tw/portlet/Other/ExchangeRate/begin.do"
CHROME_DRIVE_PATH = "C:\\Users\\hanna\\.wdm\\drivers\\chromedriver\\win32\\98.0.4758.80\\chromedriver98.exe"


def main():
    driver = webdriver.Chrome(CHROME_DRIVE_PATH)
    driver.get(url1)
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    GBP1 = soup.find('table').find('td', id='_GBP_rs')
    time.sleep(2)
    # driver.quit()

    driver.get(url2)
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table').find_all(class_="gray")
    time.sleep(2)
    driver.quit()

    for tr in table:
        for td in tr.find_all('td'):
            if td.find_all('span')[0].text == 'GBP':
                GBP2 = tr.find_all('span')[-1].text

    now = datetime.now()

    with open("D:\\GitHub\\Miscellaneous\\Life\\currency_output.txt",
              'a+', encoding='utf-8') as file:
        file.write('\n' + str(now))
        file.write('\nGBP(英鎊) Bank Sell (永豐): {}'.format(GBP1.text))
        file.write('\nGBP(英鎊) Bank Sell (上海): {}\n'.format(GBP2))
        file.write('='*35)


if __name__ == "__main__":
    main()
