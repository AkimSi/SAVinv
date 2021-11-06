from selenium import webdriver
import time
import random
import requests
import lxml
from bs4 import BeautifulSoup as bs
import csv
import time


def processing_html_data():
    write_row = []
    with open('sector_page.html', 'r', encoding="UTF-8") as file:
        requests_answer = file.read()
    soup = bs(requests_answer, 'lxml')
    find_sector_name = soup.findAll(class_='js-search-input inputDropDown')
    for_print = find_sector_name[2].get('value')
    write_row.append(for_print)
    print(for_print)
    find_companies = soup.findAll(class_='symbol left bold elp')
    for element in find_companies:
        write_row.append(element.find('a').text)
    with open('macro_data\\sector_division.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(write_row)
    write_row = []


options = webdriver.ChromeOptions()
options.add_argument('accept = * / *')
options.add_argument('(Windows NT 10.0; Win64; x64) Chrome/95.0.4638.69')
driver = webdriver.Chrome(executable_path='D:\\my_programm\\SAVinv\\web_driver\\chromedriver',
                          options = options)





try:
    for number in range(1, 24, 1):
        url = 'https://ru.investing.com/stock-screener/?sp=country::56%7Csector' \
              '::'+str(number)+'%7Cindustry::a%7CequityType::a%3Ceq_market_cap;1'
        driver.get(url=url)
        time.sleep(5)

        with open ('sector_page.html', 'w', encoding='UTF-8') as file:
            file.write(driver.page_source)
            processing_html_data()
        open_page = driver.find_elements_by_class_name('pagination')
        for page in open_page:
            page.click()
            time.sleep(5)
            with open('sector_page.html', 'w', encoding='UTF-8') as file:
                file.write(driver.page_source)
                processing_html_data()
        time.sleep(random.randint(5,9))
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()


headers = {
            'accept': '* / *',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.2.'
                          '172 Yowser/2.5 Safari/537.36'
        }

