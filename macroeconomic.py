import lxml
import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd
headers = {
            'accept': '* / *',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/92.0.4515.131 YaBrowser/21.8.1.476 Yowser/2.5 Safari/537.36'
        }

############Индекс промышленности PMI############
#PMI USA
# url_consumer_price_index = 'https://ru.fxempire.com/macro/indicators/manufacturing-pmi'
# requests_answer = requests.get(url_consumer_price_index, headers=headers)
# soup = BeautifulSoup(requests_answer.text, 'lxml')
# cons_prise_ind = soup.find('span', text=re.compile('Соединенные Штаты')).next_element\
#     .next_element.find('span', class_ = 'Span-sc-1abytr7-0 ftxBIP').text
# print(cons_prise_ind)
###############################################
#################################################

###############Запасы и продажи###############
#Total Business: Inventories to Sales Ratio
# url_inventories_to_sales = 'https://fred.stlouisfed.org/series/ISRATIO'
#
# requests_answer = requests.get(url_inventories_to_sales, headers=headers)
# soup = BeautifulSoup(requests_answer.text, 'lxml')
#
# cons_invent_to_sales_ind = soup.find(class_ = 'series-meta-observation-value').text
################################################

#Total Business Inventories
# url_total_business_inventories = 'https://fred.stlouisfed.org/series/BUSINV'
#
# requests_answer = requests.get(url_total_business_inventories, headers=headers)
# soup = BeautifulSoup(requests_answer.text, 'lxml')
#
# cons_total_busn_inv = soup.find(class_ = 'series-meta-observation-value').text
###################################################
############################################


#############Безработица#############
#Unemployment Rate
# url_unemployment_rate = 'https://fred.stlouisfed.org/series/UNRATE'
#
# requests_answer = requests.get(url_unemployment_rate, headers=headers)
# soup = BeautifulSoup(requests_answer.text, 'lxml')
#
# cons_unempl_rate = soup.find(class_ = 'series-meta-observation-value').text

#################Кредит##################
#Revolving Consumer Credit Owned and Securitized
# url_revolving_cons_credit = 'https://fred.stlouisfed.org/series/REVOLSL'
#
# requests_answer = requests.get(url_revolving_cons_credit, headers=headers)
# soup = BeautifulSoup(requests_answer.text, 'lxml')
#
# revolving_cons_credit = soup.find(class_ = 'series-meta-observation-value').text
##############################################



###############Баланс ФРС, инфляция, процентная ставка#############################
# Total Assets
# url_total_assets = 'https://fred.stlouisfed.org/series/WALCL'
#
# requests_answer = requests.get(url_total_assets, headers=headers)
# soup = BeautifulSoup(requests_answer.text, 'lxml')
#
# total_assets = soup.find(class_ = 'series-meta-observation-value').text

#5-Year Breakeven Inflation Rate
# url_breakeven_inflation_rate = 'https://fred.stlouisfed.org/series/T5YIE'
#
# requests_answer = requests.get(url_breakeven_inflation_rate, headers=headers)
# soup = BeautifulSoup(requests_answer.text, 'lxml')
#
# breakeven_inflation_rate = soup.find(class_ = 'series-meta-observation-value').text


#Forward Inflation Expectation Rate
# url_inflation_expectation_rate = 'https://fred.stlouisfed.org/series/T5YIFR'
#
# requests_answer = requests.get(url_inflation_expectation_rate, headers=headers)
# soup = BeautifulSoup(requests_answer.text, 'lxml')
#
# inflation_expectation_rate = soup.find(class_ = 'series-meta-observation-value').text

#Effective Federal Funds Rate
# url_effective_funds_rate = 'https://fred.stlouisfed.org/series/FEDFUNDS'
#
# requests_answer = requests.get(url_effective_funds_rate, headers=headers)
# soup = BeautifulSoup(requests_answer.text, 'lxml')
#
# effective_funds_rate = soup.find(class_ = 'series-meta-observation-value').text


##############ВВП####################
#Weekly Economic Index
# url_weekly_economic_index = 'https://fred.stlouisfed.org/series/WEI'
#
# requests_answer = requests.get(url_weekly_economic_index, headers=headers)
# soup = BeautifulSoup(requests_answer.text, 'lxml')
#
# weekly_economic_index = soup.find(class_ = 'series-meta-observation-value').text
###############################################

#Industrial Production: Manufacturing
#url_industrial_production_manufact = 'https://fred.stlouisfed.org/series/IPMAN'
#
# requests_answer = requests.get(url_pmi, headers=headers)
# soup = BeautifulSoup(requests_answer.text, 'lxml')
#
# industrial_production_manufact = soup.find(class_ = 'series-meta-observation-value').text
###############################################



#############Коропоративная прибыль###################
#Corporate Profits After Tax
# url_corporate_profit = 'https://fred.stlouisfed.org/series/CP'
#
# requests_answer = requests.get(url_pmi, headers=headers)
# soup = BeautifulSoup(requests_answer.text, 'lxml')
#
# corporate_profit = soup.find(class_ = 'series-meta-observation-value').text
#######################################################



##############Расчеты индикаторов#######################
# read_file_macro_data = pd.read_csv('test.csv', delimiter=';', encoding='Windows-1251',
#                                              names=['Дата', 'Склады/продажи', 'Склады',
#                                                     'Продажи', 'Профит/лосс',
#                                                     '% от портфеля', 'Количество бумаг(шт)',
#                                                     'Средняя цена покупки'])


##########################inventories
# adding_macro_data = pd.read_csv('macro_data\\adding.csv', delimiter=';', encoding='Windows-1251',
#                                               names=['Дата', 'Запасы', 'Запасы/Продажи', 'Продажи'])
#
#
# list_inventories = list(adding_macro_data[['Запасы']].values)
# list_inv_to_sales = list(adding_macro_data[['Запасы/Продажи']].values)
# list_sales = list(adding_macro_data[['Продажи']].values)
# data_list = list(adding_macro_data[['Дата']].values)
# ind = 0
# recess_count = 0
# for inv in list_inventories:
#     data = str(data_list[ind])
#     inv = float(inv)
#     inv_to_sales = float(list_inv_to_sales[ind])
#     sales = float(list_sales[ind])
#     ind += 1
#     read_file_macro_data = pd.read_csv('macro_data\\invetories_indicate.csv',
#                                        delimiter=';', encoding='Windows-1251',
#                                        names=['Дата', 'Запасы', 'Запасы/Продажи', 'Продажи'])
#     inv_list = read_file_macro_data[['Запасы']]
#     inv_list = inv_list.tail(24)
#     aver_div = inv_list.Запасы.median()
#     last_measure = float(inv_list.tail(1).values)
#     #условие фазы рецессии
#     if inv < last_measure and inv > aver_div and recess_count > 0:
#         inventories_indicate = "RECESSION"
#     elif inv < last_measure and inv > aver_div:
#         recess_count += 1
#         inventories_indicate = inventories_indicate
#     #условие фазы развития и заката
#     elif inv > aver_div:
#         recess_count = 0
#         inventories_indicate = "RISE"
#     # условие фазы восхода
#     elif inv < aver_div:
#         recess_count = 0
#         inventories_indicate = "E_RISE"
#     else:
#         recess_count = 0
#         print("Something wrong")
#
#     inv_list = read_file_macro_data[['Продажи']]
#     inv_list = inv_list.tail(18)
#     aver_div = inv_list.Продажи.median()
#     last_measure = float(inv_list.tail(1).values)
#     #условие для восхода
#     if sales < aver_div and sales > last_measure:
#         sales_indicate = "E_RISE"
#         # условие для заката
#     elif sales < last_measure and sales > aver_div:
#         sales_indicate = "L_RISE"
#     elif sales < last_measure + last_measure * 0.02  and sales > aver_div:
#         sales_indicate = "L_RISE"
#     #условие для роста
#     elif sales > aver_div:
#         sales_indicate = "RISE"
#     elif sales == last_measure:
#         sales_indicate = "RISE"
#     #условие для рецессии
#     elif sales < last_measure and sales < aver_div:
#         sales_indicate = "RECESSION"
#     elif sales == aver_div:
#         sales_indicate = "L_RISE"
#     else:
#         print("Something wrong")
#
#     if sales_indicate == 'RISE' and inventories_indicate == 'E_RISE':
#         inventories_and_sales = 'Развитие'
#     elif sales_indicate == 'RISE' and inventories_indicate == 'RISE':
#         inventories_and_sales = 'Развитие'
#     elif sales_indicate == 'L_RISE' and inventories_indicate == 'E_RISE':
#         inventories_and_sales = 'Развитие'
#     elif sales_indicate == 'L_RISE' and inventories_indicate == 'RISE':
#         inventories_and_sales = 'Закат'
#     elif sales_indicate == 'RECESSION' and inventories_indicate == 'RECESSION':
#         inventories_and_sales = 'Рецессия'
#     elif sales_indicate == 'RECESSION' and inventories_indicate == 'E_RISE':
#         inventories_and_sales = 'Рецессия'
#     elif sales_indicate == 'E_RISE' and inventories_indicate == 'E_RISE':
#         inventories_and_sales = 'Восход'
#     elif sales_indicate == 'E_RISE' and inventories_indicate == 'RISE':
#         inventories_and_sales = 'Восход'
#     else:
#         print(sales_indicate)
#         print(inventories_indicate)
#         print(data)


    # write_row = [data, inv, inv_to_sales, sales]
    # with open('macro_data\\invetories_indicate.csv', 'a', newline='') as file:
    #     writer = csv.writer(file, delimiter=';')
    #     writer.writerow(write_row)
##################################
###############Баланс ФРС
adding_macro_data = pd.read_csv('macro_data\\adding.csv', delimiter=';', encoding='Windows-1251',
                                              names=['Дата', 'Баланс'])


list_assets = list(adding_macro_data[['Баланс']].values)
data_list = list(adding_macro_data[['Дата']].values)
read_file_macro_data = pd.read_csv('test.csv', delimiter=';', encoding='Windows-1251',
                                   names=['Дата', 'Активы_ФРС', 'Склады',
                                          'Продажи', 'Профит/лосс',
                                          '% от портфеля', 'Количество бумаг(шт)',
                                          'Средняя цена покупки'])
for assets in list_assets:
    assets_list = read_file_macro_data[['Активы_ФРС']]
    inv_list = assets_list.tail(24)
    aver_div = inv_list.Активы_ФРС.median()
    last_measure = float(assets_list.tail(1).values)
    rand_div = aver_div * 0.015

    assets = int(assets)
    # условие для фазы рецессии
    if assets > (aver_div + rand_div) and assets > last_measure:
        assets_ind = 'STIMULATE'
    # условие для фазы развития
    elif (assets - rand_div) < aver_div < (assets + rand_div):
        assets_ind = 'RISE'
    # условие для фазы восхода
    elif assets > aver_div:
        assets_ind = "L_RISE"
    # условие для фазы заката
    elif assets < aver_div - rand_div:
        assets_ind = "L_RISE"
    else:
        print("something wrong")
    print(assets_ind)
    print(assets)
    print(data)
    write_row = [data, assets]
    with open('macro_data\\total_assets_ind.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(write_row)

############Процентная ставка
# adding_macro_data = pd.read_csv('test_adding.csv', delimiter=';', encoding='Windows-1251',
#                                              names=['Дата', 'ставка_ФРС'])
# adding_asset = adding_macro_data[['ставка_ФРС']].values
# adding_data = adding_macro_data[['Дата']].values
# adding_data = list(adding_data)
#
# count = 1
# for federal_fund_rate in adding_asset:
#     federal_fund_rate = float(federal_fund_rate)
#     #
#     read_file_macro_data = pd.read_csv('test.csv', delimiter=';', encoding='Windows-1251',
#                                        names=['Дата', 'ставка_ФРС', 'Склады',
#                                               'Продажи', 'Профит/лосс',
#                                               '% от портфеля', 'Количество бумаг(шт)',
#                                               'Средняя цена покупки'])
#
#     assets_list = read_file_macro_data[['ставка_ФРС']]
#     inv_list = assets_list.tail(15)
#     aver_div = assets_list.ставка_ФРС.median()
#     last_measure = float(assets_list.tail(1).values)
#     rand_div = aver_div * 0.05
#
#
#     # условие для фазы развития
#     if (federal_fund_rate - rand_div) < aver_div and aver_div < (federal_fund_rate + rand_div):
#         assets_ind = 'NEUTRAL'
#     #условие для фазы заката
#     elif federal_fund_rate > (aver_div + rand_div):
#         assets_ind = "HARD"
#     elif federal_fund_rate < aver_div:
#         assets_ind = 'STIMULATE'
#     else:
#         print("something wrong")
#
#     if assets_ind == 'STIMULATE':
#         regulate_ind = "Рецессия-Воход"
#     elif assets_ind == 'HARD':
#         regulate_ind = "Закат"
#     elif assets_ind == 'NEUTRAL':
#         regulate_ind = "Рост"
#     else:
#         print('Something Wrong')
#     print(regulate_ind)
#     print(adding_data[count])
#     write_row = [adding_data[count], federal_fund_rate]
#     count += 1
#     with open('test.csv', 'a', newline='') as file:
#         writer = csv.writer(file, delimiter=';')
#         writer.writerow(write_row)
##########################
###################Корпоративная прибыль
# adding_macro_data = pd.read_csv('test_adding.csv', delimiter=';', encoding='Windows-1251',
#                                              names=['Дата', 'Корпоративная_прибыль'])
# adding_asset = adding_macro_data[['Корпоративная_прибыль']].values
# adding_data = adding_macro_data[['Дата']].values
# adding_data = list(adding_data)
#
# count = 1
# for corporate_profit in adding_asset:
#     corporate_profit = float(corporate_profit)
#     #
#     read_file_macro_data = pd.read_csv('test.csv', delimiter=';', encoding='Windows-1251',
#                                        names=['Дата', 'Корпоративная_прибыль', 'Склады',
#                                               'Продажи', 'Профит/лосс',
#                                               '% от портфеля', 'Количество бумаг(шт)',
#                                               'Средняя цена покупки'])
#
#     assets_list = read_file_macro_data[['Корпоративная_прибыль']]
#     inv_list = assets_list.tail(3)
#     aver_div = assets_list.Корпоративная_прибыль.median()
#     last_measure = float(assets_list.tail(1).values)
#     rand_div = aver_div * 0.05
#
#
#     # условие для фазы заката
#     if (corporate_profit - rand_div) < aver_div and aver_div < (corporate_profit + rand_div):
#         assets_ind = 'NEUTRAL'
#     #условие для фазы заката
#     elif corporate_profit < (aver_div - rand_div):
#         assets_ind = "DOWN"
#     elif corporate_profit > aver_div + rand_div:
#         assets_ind = 'UP'
#     else:
#         print("something wrong")
#
#     if assets_ind == 'DOWN':
#         regulate_ind = "Рецессия"
#     elif assets_ind == 'NEUTRAL':
#         regulate_ind = "Закат"
#     elif assets_ind == 'UP':
#         regulate_ind = "Восход - Рост"
#     else:
#         print('Something Wrong')
#     print(regulate_ind)
#     print(adding_data[count])
#     write_row = [adding_data[count], corporate_profit]
#     count += 1
#     with open('test.csv', 'a', newline='') as file:
#         writer = csv.writer(file, delimiter=';')
#         writer.writerow(write_row)
################Кредит
# adding_macro_data = pd.read_csv('test_adding.csv', delimiter=';', encoding='Windows-1251',
#                                              names=['Дата', 'Закредитованность'])
# adding_asset = adding_macro_data[['Закредитованность']].values
# adding_data = adding_macro_data[['Дата']].values
# adding_data = list(adding_data)
#
# count = 1
# for credit in adding_asset:
#     credit = float(credit)
#     #
#     read_file_macro_data = pd.read_csv('test.csv', delimiter=';', encoding='Windows-1251',
#                                        names=['Дата', 'Закредитованность', 'Склады',
#                                               'Продажи', 'Профит/лосс',
#                                               '% от портфеля', 'Количество бумаг(шт)',
#                                               'Средняя цена покупки'])
#
#     assets_list = read_file_macro_data[['Закредитованность']]
#     inv_list = assets_list.tail(3)
#     aver_div = inv_list.Закредитованность.median()
#     last_measure = float(assets_list.tail(1).values)
#     rand_div = aver_div * 0.006
#
#     # условие для фазы заката
#     if credit > (aver_div - rand_div / 2) and credit < (aver_div + rand_div / 2):
#         assets_ind = 'NEUTRAL'
#     #условие для фазы рота
#     elif credit > (aver_div + rand_div):
#         assets_ind = "UP"
#     # условие для фазы вохода
#     elif credit > last_measure and credit < aver_div + rand_div:
#         assets_ind = 'SUPER_UP'
#     # условие для фазы рецессии
#     elif credit < aver_div and credit < last_measure:
#         assets_ind = 'DOWN'
#     else:
#         print("something wrong")
#
#     if assets_ind == 'DOWN':
#         credit_ind = "Рецессия"
#     elif assets_ind == 'NEUTRAL':
#         credit_ind = "Закат"
#     elif assets_ind == 'UP':
#         credit_ind = "Рост"
#     elif assets_ind == 'SUPER_UP':
#         credit_ind = "Восход"
#     else:
#         print('Something Wrong')
#     print(credit_ind)
#     print(adding_data[count])
#     write_row = [adding_data[count], credit]
#     count += 1
#     with open('test.csv', 'a', newline='') as file:
#         writer = csv.writer(file, delimiter=';')
#         writer.writerow(write_row)
##############Запись данных в файл######################
# writing_list = []
# with open('portfel.csv', 'w', newline='') as file:
#     writer = csv.writer(file, delimiter=';')
#     writer.writerow(writing_list)
