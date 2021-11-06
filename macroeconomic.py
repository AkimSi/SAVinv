import lxml
import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd
import time
import schedule
import sys
from threading import Thread
class Macro_economic():
    def __init__(self):
        self.pmi = None
        schedule.every().day.at('23:16').do(self.loading_inernet_data)
        self.recess_count = 0
        self.stimul_count_assets = 0
##########################################Блок управления
    def main_control(self):
        self.inicialization_economic_data()
        update = Thread(target=self.update_control())
        communicate = Thread(target=self.communiation())
        update.start()
        communicate.start()
        update.join()
        communicate.join()
        # self.inicialization_economic_data()
        # self.loading_inernet_data()

    def update_control(self):
        schedule.run_pending()
    def communiation(self):
        self.control_func = input('Показать состояние экономики - 1: ')
        if self.control_func == '1':
            print(self.economic_data)
            self.main_control()

#############################Блок обработки полученных данных
    def processing_economic_data(self):
        data = [self.economic_ind, self.unempl_ind, self.pmi, self.credit_ind,
                self.corp_profits_ind, self.interest_rate_ind, self.inflation_rate_ind,
                self.assets_ind, self.inventories_and_sales]
        self.economic_data = pd.Series(data, index=['ВВП', 'Рынок труда', 'Промышленность',
                                         'Кредит', 'Корпоративные прибыли',
                                         'Ставка ФРС', 'Инфляция', 'Активы ФРС',
                                         'Запасы/Продажи'])
        self.economic_data.to_csv('macro_data\\economic_condition.csv', encoding='Windows-1251',
                                          header=False, sep=';',
                                          mode='w', index=False )

    def inicialization_economic_data(self):
        read_data = pd.read_csv('macro_data\\economic_condition.csv',  delimiter=';',
                                encoding='Windows-1251', header=None)
        read_data = read_data.values

        self.economic_ind = str(read_data[0])[2:-2]
        self.unempl_ind = str(read_data[1])[2:-2]
        self.pmi = str(read_data[2])[2:-2]
        self.credit_ind = str(read_data[3])[2:-2]
        self.corp_profits_ind = str(read_data[4])[2:-2]
        self.interest_rate_ind = str(read_data[5])[2:-2]
        self.inflation_rate_ind = str(read_data[6])[2:-2]
        self.assets_ind = str(read_data[7])[2:-2]
        self.inventories_and_sales = str(read_data[8])[2:-2]

        data = [self.economic_ind, self.unempl_ind, self.pmi, self.credit_ind,
                self.corp_profits_ind, self.interest_rate_ind, self.inflation_rate_ind,
                self.assets_ind, self.inventories_and_sales]
        self.economic_data = pd.Series(data, index=['ВВП', 'Рынок труда', 'Промышленность',
                                                    'Кредит', 'Корпоративные прибыли',
                                                    'Ставка ФРС', 'Инфляция', 'Активы ФРС',
                                                    'Запасы/Продажи'])

###########################################Блок сбора информации
    def update_process(self):
        ##Проверка запасов
        read_file_macro_data = pd.read_csv('macro_data\\invetories_indicate.csv',
                                           delimiter=';', encoding='Windows-1251',
                                           names=['Дата', 'Запасы', 'Запасы/Продажи', 'Продажи'])
        date = read_file_macro_data[['Дата']]
        date = str(date.tail(1).values)
        date = date[3:-3]
        if date == self.date_inv:
            print("Обновление запасов не требуется")
        else:
            self.processing_inventories_data()
        ##Проверка активов ФРС
        read_file_macro_data = pd.read_csv('macro_data\\total_assets_ind.csv', delimiter=';', encoding='Windows-1251',
                                           names=['Дата', 'Активы_ФРС'])
        date = read_file_macro_data[['Дата']]
        date = str(date.tail(1).values)
        date = date[3:-3]
        if date == self.date_assets:
            print("Обновление активов ФРС не требуется")
        else:
            self.processing_assets_rate()
        ##Проверка процентной ставки
        read_file_macro_data = pd.read_csv('macro_data\\interests_rate.csv', delimiter=';', encoding='Windows-1251',
                                           names=['Дата', 'Ставка'])
        date = read_file_macro_data[['Дата']]
        date = str(date.tail(1).values)
        date = date[3:-3]
        if date == self.date_funds_rate:
            print("Обновление процентной ставки не требуется")
        else:
            self.processing_inter_rate()

        ##Проверка инфляции
        read_file_macro_data = pd.read_csv('macro_data\\inflation_rate.csv', delimiter=';', encoding='Windows-1251',
                                           names=['Дата', 'Инфляция'])
        date = read_file_macro_data[['Дата']]
        date = str(date.tail(1).values)
        date = date[3:-3]
        if date == self.date_inflation:
            print("Обновление уровня инфляции не требуется")
        else:
            self.processing_inflation_rate()

        ##Проверка корпоративных доходов
        read_file_macro_data = pd.read_csv('macro_data\\corporate_profits.csv', delimiter=';', encoding='Windows-1251',
                                           names=['Дата', 'Кредит'])
        date = read_file_macro_data[['Дата']]
        date = str(date.tail(1).values)
        date = date[3:-3]
        if date == self.date_corp_profits:
            print("Обновление коропоративных доходов не требуется")
        else:
            self.processing_corp_profits()

        ##Проверка кредита
        read_file_macro_data = pd.read_csv('macro_data\\credit_rate.csv', delimiter=';', encoding='Windows-1251',
                                           names=['Дата', 'Доходы'])
        date = read_file_macro_data[['Дата']]
        date = str(date.tail(1).values)
        date = date[3:-3]
        if date == self.date_credit:
            print("Обновление уровня кредитов не требуется")
        else:
            self.processing_credit()

        ##Проверка безработицы
        read_file_macro_data = pd.read_csv('macro_data\\unemployment_rate.csv', delimiter=';', encoding='Windows-1251',
                                           names=['Дата', 'Безработица'])
        date = read_file_macro_data[['Дата']]
        date = str(date.tail(1).values)
        date = date[3:-3]
        if date == self.date_unempl:
            print("Обновление уровня безработицы не требуется")
        else:
            self.processing_unemployment_rate()

        ##Проверка экономической активности
        read_file_macro_data = pd.read_csv('macro_data\\unemployment_rate.csv', delimiter=';', encoding='Windows-1251',
                                           names=['Дата', 'Экон_индекс'])
        date = read_file_macro_data[['Дата']]
        date = str(date.tail(1).values)
        date = date[3:-3]
        if date == self.date_economic_index:
            print("Обновление экономического индекса не требуется")
        else:
            self.processing_economic_index()

        self.processing_economic_data()



    def cleaning_data(self, dirty_number):
        delete_list = [',']
        for element in dirty_number:
            if element in delete_list:
                clean_number = dirty_number.replace(element, '')
        return clean_number

    def loading_inernet_data(self):
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
        url_inventories_to_sales = 'https://fred.stlouisfed.org/series/ISRATIO'

        requests_answer = requests.get(url_inventories_to_sales, headers=headers)
        soup = BeautifulSoup(requests_answer.text, 'lxml')

        self.inv_to_sales = float(soup.find(class_ = 'series-meta-observation-value').text)
        ################################################
        time.sleep(5)
        #Total Business Inventories
        url_total_business_inventories = 'https://fred.stlouisfed.org/series/BUSINV'

        requests_answer = requests.get(url_total_business_inventories, headers=headers)
        soup = BeautifulSoup(requests_answer.text, 'lxml')

        self.inv = soup.find(class_ = 'series-meta-observation-value').text
        self.inv = int(self.cleaning_data(self.inv))
        self.date_inv = soup.find(class_ = 'initial-coed').get('value')
        ###################################################
        ############################################
        time.sleep(5)
        #############Безработица#############
        #Unemployment Rate
        url_unemployment_rate = 'https://fred.stlouisfed.org/series/UNRATE'

        requests_answer = requests.get(url_unemployment_rate, headers=headers)
        soup = BeautifulSoup(requests_answer.text, 'lxml')

        self.unemployments = float(soup.find(class_ = 'series-meta-observation-value').text)
        self.date_unempl = soup.find(class_ = 'initial-coed').get('value')

        time.sleep(5)
        #################Кредит##################
        #Revolving Consumer Credit Owned and Securitized
        url_revolving_cons_credit = 'https://fred.stlouisfed.org/series/REVOLSL'

        requests_answer = requests.get(url_revolving_cons_credit, headers=headers)
        soup = BeautifulSoup(requests_answer.text, 'lxml')

        self.credit = soup.find(class_ = 'series-meta-observation-value').text
        self.credit = float(self.cleaning_data(self.credit))
        self.date_credit = soup.find(class_ = 'initial-coed').get('value')
        ##############################################


        time.sleep(5)
        ###############Баланс ФРС, инфляция, процентная ставка#############################
        # Total Assets
        url_total_assets = 'https://fred.stlouisfed.org/series/WALCL'

        requests_answer = requests.get(url_total_assets, headers=headers)
        soup = BeautifulSoup(requests_answer.text, 'lxml')

        self.assets = soup.find(class_ = 'series-meta-observation-value').text
        self.assets = float(self.cleaning_data(self.assets))
        self.date_assets = soup.find(class_ = 'initial-coed').get('value')

        time.sleep(5)
        #5-Year Breakeven Inflation Rate
        url_breakeven_inflation_rate = 'https://fred.stlouisfed.org/series/T5YIE'

        requests_answer = requests.get(url_breakeven_inflation_rate, headers=headers)
        soup = BeautifulSoup(requests_answer.text, 'lxml')

        self.infl_rate = float(soup.find(class_ = 'series-meta-observation-value').text)
        self.date_inflation = soup.find(class_ = 'initial-coed').get('value')

        time.sleep(5)
        #Effective Federal Funds Rate
        url_effective_funds_rate = 'https://fred.stlouisfed.org/series/FEDFUNDS'

        requests_answer = requests.get(url_effective_funds_rate, headers=headers)
        soup = BeautifulSoup(requests_answer.text, 'lxml')

        self.inter_rate = float(soup.find(class_ = 'series-meta-observation-value').text)
        self.date_funds_rate = soup.find(class_ = 'initial-coed').get('value')
        time.sleep(5)
        ##############ВВП####################
        #Weekly Economic Index
        url_weekly_economic_index = 'https://fred.stlouisfed.org/series/WEI'

        requests_answer = requests.get(url_weekly_economic_index, headers=headers)
        soup = BeautifulSoup(requests_answer.text, 'lxml')

        self.ec_ind = float(soup.find(class_ = 'series-meta-observation-value').text)
        self.date_economic_index = soup.find(class_ = 'initial-coed').get('value')
        ###############################################
        time.sleep(5)
        #Industrial Production: Manufacturing
        # url_industrial_production_manufact = 'https://fred.stlouisfed.org/series/IPMAN'
        #
        # requests_answer = requests.get(url_pmi, headers=headers)
        # soup = BeautifulSoup(requests_answer.text, 'lxml')
        #
        # industrial_production_manufact = soup.find(class_ = 'series-meta-observation-value').text
        # self.date_funds_rate = soup.find(class_='series-meta-observation-value').get('title')
        # ###############################################
        # time.sleep(5)

        #############Коропоративная прибыль###################
        #Corporate Profits After Tax
        url_corporate_profit = 'https://fred.stlouisfed.org/series/CP'

        requests_answer = requests.get(url_corporate_profit, headers=headers)
        soup = BeautifulSoup(requests_answer.text, 'lxml')

        self.corp_profits = soup.find(class_ = 'series-meta-observation-value').text
        self.corp_profits = float(self.cleaning_data(self.corp_profits))
        self.date_corp_profits = soup.find(class_ = 'initial-coed').get('value')

        self.update_process()
        #######################################################
###############################################################################

##############Расчеты индикаторов#######################
# read_file_macro_data = pd.read_csv('test.csv', delimiter=';', encoding='Windows-1251',
#                                              names=['Дата', 'Склады/продажи', 'Склады',
#                                                     'Продажи', 'Профит/лосс',
#                                                     '% от портфеля', 'Количество бумаг(шт)',
#                                                     'Средняя цена покупки'])

    ##########################inventories
    def processing_inventories_data(self):
        # adding_macro_data = pd.read_csv('macro_data\\adding.csv', delimiter=';', encoding='Windows-1251',
        #                                               names=['Дата', 'Запасы', 'Запасы/Продажи', 'Продажи'])
        #
        #
        # list_inventories = list(adding_macro_data[['Запасы']].values)
        # list_inv_to_sales = list(adding_macro_data[['Запасы/Продажи']].values)
        # list_sales = list(adding_macro_data[['Продажи']].values)
        # data_list = list(adding_macro_data[['Дата']].values)
        # ind = 0

        # for inv in list_inventories:
        #     data = str(data_list[ind])
        #     inv = float(inv)
        #     inv_to_sales = float(list_inv_to_sales[ind])
        sales = self.inv/self.inv_to_sales
        #ind += 1
        read_file_macro_data = pd.read_csv('macro_data\\invetories_indicate.csv',
                                           delimiter=';', encoding='Windows-1251',
                                           names=['Дата', 'Запасы', 'Запасы/Продажи', 'Продажи'])
        inv_list = read_file_macro_data[['Запасы']]
        inv_list = inv_list.tail(24)
        aver_div = inv_list.Запасы.median()
        last_measure = float(inv_list.tail(1).values)
        #условие фазы рецессии
        if self.inv < last_measure and self.inv > aver_div and self.recess_count > 0:
            inventories_indicate = "RECESSION"
        elif self.inv < last_measure and self.inv > aver_div:
            self.recess_count += 1
            inventories_indicate = "RECESSION"
        #условие фазы развития и заката
        elif self.inv > aver_div:
            self.recess_count = 0
            inventories_indicate = "RISE"
        # условие фазы восхода
        elif self.inv < aver_div:
            self.recess_count = 0
            inventories_indicate = "E_RISE"
        else:
            self.recess_count = 0
            print("Something wrong")

        inv_list = read_file_macro_data[['Продажи']]
        inv_list = inv_list.tail(18)
        aver_div = inv_list.Продажи.median()
        last_measure = float(inv_list.tail(1).values)
        #условие для восхода
        if sales < aver_div and sales > last_measure:
            sales_indicate = "E_RISE"
            # условие для заката
        elif sales < last_measure and sales > aver_div:
            sales_indicate = "L_RISE"
        elif sales < last_measure + last_measure * 0.02  and sales > aver_div:
            sales_indicate = "L_RISE"
        #условие для роста
        elif sales > aver_div:
            sales_indicate = "RISE"
        elif sales == last_measure:
            sales_indicate = "RISE"
        #условие для рецессии
        elif sales < last_measure and sales < aver_div:
            sales_indicate = "RECESSION"
        elif sales == aver_div:
            sales_indicate = "L_RISE"
        else:
            print("Something wrong")

        if sales_indicate == 'RISE' and inventories_indicate == 'E_RISE':
            self.inventories_and_sales = 'Рост продаж выше среднего значения. ' \
                                         'Запасы ниже среднего. Фаза развития.'

        elif sales_indicate == 'RISE' and inventories_indicate == 'RISE':
            self.inventories_and_sales = 'Рост продаж выше среднего значения.' \
                                         ' Запасы на складах выше среднего значения.' \
                                         'Фаза развития'

        elif sales_indicate == 'L_RISE' and inventories_indicate == 'E_RISE':
            self.inventories_and_sales = 'Продажи упали ниже последнего значения.' \
                                         'Запасы ниже среднего.' \
                                         'Фаза заката'

        elif sales_indicate == 'L_RISE' and inventories_indicate == 'RISE':
            self.inventories_and_sales = 'Продажи упали ниже последнего значения.' \
                                         'Запасы на складах выше среднего значения.' \
                                         'Фаза заката'

        elif sales_indicate == 'RECESSION' and inventories_indicate == 'RECESSION':
            self.inventories_and_sales = 'Продажи,как и запасы на складах падают.' \
                                         'Фаза рецессии'

        elif sales_indicate == 'RECESSION' and inventories_indicate == 'E_RISE':
            self.inventories_and_sales = 'Продажи падают ниже средниъ значений.' \
                                         'Запасы на складах ниже среднего значения.' \
                                         'Фаза рецессии.'

        elif sales_indicate == 'E_RISE' and inventories_indicate == 'E_RISE':
            self.inventories_and_sales = 'Продажи улучшаются, но ниде среднего значения.' \
                                         'Запасы на складах ниже среднего значения.' \
                                         'Фаза восхода'

        elif sales_indicate == 'E_RISE' and inventories_indicate == 'RISE':
            self.inventories_and_sales = 'Продажи улучшаются, но ниде среднего значения.' \
                                         'Запасы на складах выше среднего значения.' \
                                         'Фаза восхода.'

        else:
            print(sales_indicate)
            print(inventories_indicate)
            print(self.date_inv)


        write_row = [self.date_inv, self.inv, self.inv_to_sales, sales]
        with open('macro_data\\invetories_indicate.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(write_row)
##################################
###############Баланс ФРС
    def processing_assets_rate(self):
        # adding_macro_data = pd.read_csv('macro_data\\adding.csv', delimiter=';', encoding='Windows-1251',
        #                                               names=['Дата', 'Баланс'])
        #
        #
        # list_assets = list(adding_macro_data[['Баланс']].values)
        # data_list = list(adding_macro_data[['Дата']].values)
        # count = 0
        # stimul_count = 0
        # for assets in list_assets:
        read_file_macro_data = pd.read_csv('macro_data\\total_assets_ind.csv', delimiter=';', encoding='Windows-1251',
                                           names=['Дата', 'Активы_ФРС'])
        # data = str(data_list[count])
        # count += 1
        assets_list = read_file_macro_data[['Активы_ФРС']]
        inv_list = assets_list.tail(20)
        aver_value = inv_list.Активы_ФРС.median()
        aver_div = inv_list.Активы_ФРС.std()
        last_measure = int(assets_list.tail(1).values)
        # assets = int(assets)
        # условие для фазы рецессии
        if self.assets > (aver_value + aver_div) and self.assets > last_measure and self.stimul_count_assets < 4:
            self.assets_ind = 'Сильное стимулирование. Фаза рецессии'
            self.stimul_count_assets += 1

            # условие для фазы развития
        elif (aver_value - aver_div) < self.assets and self.assets < (aver_value + aver_div):
            self.assets_ind = 'Устойчивый рост активов. Значительная поддрежка. Фаза рецессии.'
            self.stimul_count_assets = 0
        # условие для фазы заката
        elif self.assets < (aver_value - aver_div):
            self.assets_ind = "Соркащение активов. Сворачивание стимулирования. Фаза заката."
            self.stimul_count_assets = 0

        # условие для фазы восхода
        elif self.assets > (aver_value + aver_div):
            self.assets_ind = "Продолжение значительного стимулирования. Фаза восхода."
        else:
            print("Что-то пошло не так")

        write_row = [self.date_assets, self.assets]
        with open('macro_data\\total_assets_ind.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(write_row)


############Процентная ставка
    def processing_inter_rate(self):
        # adding_macro_data = pd.read_csv('macro_data\\adding.csv', delimiter=';', encoding='Windows-1251',
        #                                               names=['Дата', 'Ставка'])
        #
        #
        # list_int_rate = list(adding_macro_data[['Ставка']].values)
        # data_list = list(adding_macro_data[['Дата']].values)
        # count = 0
        # stimul_count = 0
        # for inter_rate in list_int_rate:
        read_file_macro_data = pd.read_csv('macro_data\\interests_rate.csv', delimiter=';', encoding='Windows-1251',
                                       names=['Дата', 'Ставка'])

        #     data = str(data_list[count])
        #     count += 1
        int_rate_list = read_file_macro_data[['Ставка']]
        int_list = int_rate_list.tail(12)
        aver_value = int_list.Ставка.median()
        aver_div = int_list.Ставка.std()
        last_measure = float(int_rate_list.tail(1).values)
        #inter_rate = float(inter_rate)
    #
        # условие для фазы развития
        if self.inter_rate < aver_value and self.inter_rate == last_measure:
            self.interest_rate_ind = 'Низкая процентная ставка. Стимулирование экономики.' \
                                     'Фаза восхода.'
        elif self.inter_rate < aver_value:
            self.interest_rate_ind = 'Низкая процентная ставка. Стимулирование экономики.' \
                                     'Фаза рецессии'
        #условие для фазы заката
        elif self.inter_rate > aver_value:
            self.interest_rate_ind = "Процентная ставка выше среднего значения. " \
                                     "Ужесточение монетарной политики." \
                                     "Фаза заката."
        elif self.inter_rate == last_measure or self.inter_rate > last_measure:
            self.interest_rate_ind = "Процентная ставка равнв реднему значению." \
                                     "Фаза роста."

        else:
            print("something wrong")
        write_row = [self.date_funds_rate, self.inter_rate]
        with open('macro_data\\interests_rate.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(write_row)
    #########################
###################Инфляция
    def processing_inflation_rate(self):
        # adding_macro_data = pd.read_csv('macro_data\\adding.csv', delimiter=';', encoding='Windows-1251',
        #                                               names=['Дата', 'Ставка'])
        #
        #
        # list_infl_rate = list(adding_macro_data[['Ставка']].values)
        # data_list = list(adding_macro_data[['Дата']].values)
        # count = 0
        # stimul_count = 0
        # for infl_rate in list_infl_rate:
        read_file_macro_data = pd.read_csv('macro_data\\interests_rate.csv', delimiter=';', encoding='Windows-1251',
                                           names=['Дата', 'Инфляция'])
        # data = str(data_list[count])
        #count += 1
        infl_rate_list = read_file_macro_data[['Инфляция']]
        infl_rate_list = infl_rate_list.tail(300)
        aver_value = infl_rate_list.Инфляция.median()
        # aver_div = infl_rate_list.Инфляция.std()
        # last_measure = float(infl_rate_list.tail(1).values)
        # infl_rate = float(self.infl_rate)
        if self.infl_rate < aver_value:
            self.inflation_rate_ind = 'Инфляция на низком уровне.' \
                                      'Ужесточение монетарной политики, не прогнозируется.'
        elif self.infl_rate > aver_value:
            self.inflation_rate_ind = 'Инфляция на высоком уровне. ' \
                                      'Высокая вероятность ужесточения монетарной политики.'
        elif self.infl_rate == aver_value:
            self.inflation_rate_ind = "Инфляция на среднем уровне."
        else:
            print("something wrong")
        write_row = [self.date_inflation, self.infl_rate]
        with open('macro_data\\inflation_rate.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(write_row)

###################Корпоративная прибыль
    def processing_corp_profits(self):
        # adding_macro_data = pd.read_csv('macro_data\\adding.csv', delimiter=';', encoding='Windows-1251',
        #                                               names=['Дата', 'Ставка'])
        #
        #
        # list_corp_profits = list(adding_macro_data[['Ставка']].values)
        # data_list = list(adding_macro_data[['Дата']].values)
        # count = 0
        # for corp_profits in list_corp_profits:
        read_file_macro_data = pd.read_csv('macro_data\\corporate_profits.csv', delimiter=';', encoding='Windows-1251',
                                               names=['Дата', 'Доходы'])
        #     data = str(data_list[count])
        #     count += 1
        profit_list = read_file_macro_data[['Доходы']]
        prft_list = profit_list.tail(6)
        aver_value = prft_list.Доходы.median()
        aver_div = prft_list.Доходы.std()
        last_measure = float(profit_list.tail(1).values)
        # corp_profits = float(corp_profits)

        #условие для фазы восхода
        if self.corp_profits > (aver_value + aver_div) and self.corp_profits > last_measure:
            self.corp_profits_ind = 'Корпоративная прибыль растет. Фаза роста.'
            # условие для фазы роста
        elif (aver_value - aver_div) < self.corp_profits and self.corp_profits < (aver_value + aver_div):
            self.corp_profits_ind = 'Корпоративна яприбыль на средних значениях. Фаза заката.'
        # условие для фазы заката
        elif self.corp_profits < (aver_value - aver_div):
            self.corp_profits_ind = "Корпоративная прибыли на низких значениях. Фаза заката."
        elif self.corp_profits > last_measure:
            self.corp_profits_ind = 'Корпоративная прибыль начинает расти. Фаза восхода.'
        else:
            print("something wrong")
            print(self.corp_profits)
        write_row = [self.date_corp_profits, self.corp_profits]
        with open('macro_data\\corporate_profits.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(write_row)
################Кредит
    def processing_credit(self):
        # adding_macro_data = pd.read_csv('macro_data\\adding.csv', delimiter=';', encoding='Windows-1251',
        #                                               names=['Дата', 'Кредит'])
        #
        #
        # list_credit = list(adding_macro_data[['Кредит']].values)
        # data_list = list(adding_macro_data[['Дата']].values)
        # count = 0
        # for credit in list_credit:
        read_file_macro_data = pd.read_csv('macro_data\\credit_rate.csv', delimiter=';', encoding='Windows-1251',
                                               names=['Дата', 'Кредит'])
        #     data = str(data_list[count])
        #     count += 1
        credit_list = read_file_macro_data[['Кредит']]
        credit_list = credit_list.tail(3)
        aver_value = credit_list.Кредит.median()
        # aver_div = credit_list.Кредит.std()
        # last_measure = float(credit_list.tail(1).values)
        # credit = float(self.credit)
        # different = last_measure - self.redit


        #условие для роста

        if self.credit > aver_value:
            self.credit_ind = 'Кредитование выше среднего значения. '
        # условие для фазы снижения
        elif aver_value > self.credit:
            self.credit_ind = 'Кредитование ниже среднего значения.'
        else:
            print("something wrong")
        write_row = [self.date_credit, self.credit]
        with open('macro_data\\credit_rate.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(write_row)
#########################################
#########################Безработица
    def processing_unemployment_rate(self):
        # adding_macro_data = pd.read_csv('macro_data\\adding.csv', delimiter=';', encoding='Windows-1251',
        #                                               names=['Дата', 'Безработица'])
        #
        #
        # list_unempl = list(adding_macro_data[['Безработица']].values)
        # data_list = list(adding_macro_data[['Дата']].values)
        # count = 0
        # stimul_count = 0
        # for unemployments in list_unempl:
        read_file_macro_data = pd.read_csv('macro_data\\unemployment_rate.csv', delimiter=';', encoding='Windows-1251',
                                               names=['Дата', 'Безработица'])
        #     data = str(data_list[count])
        #     count += 1
        unempl_list = read_file_macro_data[['Безработица']]
        unempl_list = unempl_list.tail(100)
        aver_value = unempl_list.Безработица.median()
        aver_div = unempl_list.Безработица.std()
        last_measure = float(unempl_list.tail(1).values)
        self.unemployments = float(self.unemployments)

        if self.unemployments > (aver_value + aver_div*0.5):
            self.unempl_ind = 'Высокий уровень безработицы.'

        elif (aver_value - aver_div*0.5) < self.unemployments and self.unemployments < (aver_value + aver_div*0.5):
            self.unempl_ind = 'Уровень безработицы на средних уровнях.'

        elif self.unemployments < (aver_value - aver_div*0.5):
            self.unempl_ind = "Низкий уровень безработицы."

        else:
            print("something wrong")
        write_row = [self.date_unempl, self.unemployments]
        with open('macro_data\\unemployment_rate.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(write_row)
##################################################
###########################ECONOMIC INDEX
    def processing_economic_index(self):
        # adding_macro_data = pd.read_csv('macro_data\\adding.csv', delimiter=';', encoding='Windows-1251',
        #                                               names=['Дата', 'Экон_индекс'])
        #
        #
        # list_ec_ind = list(adding_macro_data[['Экон_индекс']].values)
        # data_list = list(adding_macro_data[['Дата']].values)
        # count = 0
        # stimul_count = 0
        # for ec_ind in list_ec_ind:
        read_file_macro_data = pd.read_csv('macro_data\\unemployment_rate.csv', delimiter=';', encoding='Windows-1251',
                                               names=['Дата', 'Экон_индекс'])
        #     data = str(data_list[count])
        #     count += 1
        ec_list = read_file_macro_data[['Экон_индекс']]
        ec_list = ec_list.tail(24)
        aver_value = ec_list.Экон_индекс.median()
        aver_div = ec_list.Экон_индекс.std()
        last_measure = float(ec_list.tail(1).values)
        self.ec_ind = float(self.ec_ind)

        if self.ec_ind > 0 and self.ec_ind > aver_value - aver_div:
            self.economic_ind = 'Уровень экономического индекса. До средних значний. Фаза роста.'

        elif self.ec_ind < 0 and self.ec_ind > aver_value + aver_div:
            self.economic_ind = 'Уровень экономического индекса выше средних значений. Фаза восхода.'

        elif self.ec_ind < 0 and self.ec_ind < last_measure:
            self.economic_ind = 'Уровень экономичекого индекса снижается. Фаза заката.'

        elif self.ec_ind > 0 and self.ec_ind < aver_value - aver_div:
            self.economic_ind = "Уровень экономического индекса падает ниже среднего уровня. Фаза рецессии."

        else:
            print("something wrong")
        write_row = [self.date_economic_index, self.ec_ind]
        with open('macro_data\\economic_ind.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(write_row)
#######################################################
##############################
##############Запись данных в файл######################
# writing_list = []
# with open('portfel.csv', 'w', newline='') as file:
#     writer = csv.writer(file, delimiter=';')
#     writer.writerow(writing_list)


def main():
    ex = Macro_economic()
    ex.main_control()
    sys.exit()

if __name__ == '__main__':
    main()