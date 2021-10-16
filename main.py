import sys
import lxml
import requests
from bs4 import BeautifulSoup
import os
import time
import csv
import pandas as pd
import numpy as np
import interface
#from PyQt5 import QtWidgets

class App():
    def __init__(self):
        self.current_price = None
        self.buying_price = None
        self.stocks_fullname = None
        self.stocks_ticker = None
        self.average_price = None
        self.money_in_stock = None
        self.stocks_profit = None
        self.portfel_stocks_percent = None
        self.stocks_amount = None
        self.balance_price = None
        self.portfel_summ = None
        self.free_portfel_summ = None
        self.existing_stoks = []
        self.url = "https://ru.investing.com/equities/russia"


    def main_control(self):
        manage = input('Показать портфель - 1 \n'
                       'Купить акции - 2 \n'
                       'Продать акции - 3\n'
                       'Выход - 4\n'
                       'Выберите действие: ')
        if manage == '1':
            read_file_portfel_data = pd.read_csv('portfel.csv', delimiter=';', encoding='Windows-1251',
                                                 names=['Название', 'Тикер', 'Текущая цена',
                                                        'Средств в бумаге', 'Профит/лосс',
                                                        'Профит/лосс (%)', '% от портфеля',
                                                        'Количество бумаг(шт)', 'Средняя цена покупки',
                                                        'Балансовая цена'])
            print(read_file_portfel_data.head())
            self.main_control()
        elif manage == '2':
            self.getting_transaction_buying_data()
            self.main_control()
        elif manage == '3':
            self.getting_transaction_selling_data()
            self.main_control()
        elif manage == '4':
            exit()
        else:
            print('Введите цифру из перечня')
            self.main_control()


    #первая функция при запуске, проверяет наличие файла портфеля,
    # вызывает функцию проверки обновления базы данных
    def inicialization(self):
        if "sys.txt" in os.listdir():
            with open ('sys.txt', 'r', encoding='UTF-8') as file:
                r = []
                for line in file:
                    r.append(line)
                self.portfel_summ = float(r[0])
                self.free_portfel_summ = float(r[1])

        self.checking_update()
        relative_path = "D:\\my_programm\\SAVinv"
        os.chdir(relative_path)

        if "portfel.csv" in os.listdir():
            self.loading_data()
            print("Инициализация, обнаружение фйла портфеля")
            self.main_control()
        else:
            #добавить окно с просьбой установить размер портфеля
            print("Инициализация, фйла портфеля не обнаружено")
            self.getting_transaction_buying_data()

    #проверка обновления файла с базой данных ВСЕХ акций
    #проводится перед запуском остальных функций
    # при необходимости вызывает загрузчик данных с интернета

    def checking_update(self):
        relative_path = "D:\\my_programm\\SAVinv"
        os.chdir(relative_path)
        if "spb_stock_list.csv" in os.listdir():
            st = os.stat("spb_stock_list.csv")
            update_time_sec = 10
            pass_time = (time.time() - float(st.st_mtime))
            if pass_time > update_time_sec:
                print("Требуется обновление")
                self.stocks_data_loader()
            else:
                print("Обновление не требуется")
                #если файл в наличии и его обновлять не нужно
        else:
            self.stocks_data_loader()
    def write_system_data(self):
        with open ('sys.txt', 'w', encoding='UTF-8') as file:
            file.write(str(self.portfel_summ) + '\n')
            file.write(str(self.free_portfel_summ))
    #запускается после проверки частоты обнвлений
    # после выполнения вызывается функция поиска акций в портфеле
    #обращается к сайту, забирает данные и записывает их в файл csv
    #oсталась проблема с отображением % изменения за сутки
    #перед основной отладкой запустить систему запросов и перевести на режим записи
    #функция может быть использована для разных котировок этого сайта
    def stocks_data_loader(self):
        print("Загрузка данных с интернета")
        headers = {
            'accept': '* / *',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/92.0.4515.131 YaBrowser/21.8.1.476 Yowser/2.5 Safari/537.36'
        }
        url_spb_stocks = "https://smart-lab.ru/q/spbex/"

        #requests_answer = requests.get(url_spb_stocks, headers=headers)
        #soup = BeautifulSoup(requests_answer.text, 'lxml')

        with open('cite_page.html', 'r', encoding="UTF-8") as file:
            requests_answer = file.read()
        soup = BeautifulSoup(requests_answer, 'lxml')

#часть с записью заголовка в БД
        # part_for_searhing = soup.find('table', class_="simple-little-table trades-table").findAll('a')
        # table_top = []
        # for i in range(1, 7):
        #     table_top.append(part_for_searhing[int(i)].text)
        # with open('spb_stock_list.csv', 'w') as file:
        #     writer = csv.writer(file, delimiter=';')
        #     writer.writerow(table_top)

        part_for_searhing = soup.find('table', class_='simple-little-table trades-table').findAll('td')
        part_for_searhing.pop(240)
        part_for_searhing.pop(600)
        count_circle = 0
        writting_list = []
        with open('listing_data\\spb_stock_list.csv', 'w', newline='') as file:
            pass
        for element in part_for_searhing:
            count_circle += 1
            if count_circle == 15:
                with open('listing_data\\spb_stock_list.csv', 'a', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(writting_list)
                    count_circle = 0
                    writting_list = []
            else:
                #список индексов лишних элементов (для удаления)
                delete_index = [1, 2, 5, 6, 11, 12, 13, 14, 15]

                if count_circle in delete_index:
                    pass
                else:
                    writting_list.append(element.text)
        self.searching_element_in_portfel()

    # поиск акций в портфеле для дальнейшего вычисления и обновления
    # многоразовое обращение к функции calculation_data
    def searching_element_in_portfel(self):
        read_file_stoks_data = pd.read_csv('listing_data\\spb_stock_list.csv', delimiter=';',
                                           encoding='Windows-1251',
                                names=['Название', 'Тикер', 'Текущая цена', '$	Изм, %',
                                       '1 нед %', '1 м, %'])
        read_file_portfel_data = pd.read_csv('portfel.csv', delimiter=';', encoding='Windows-1251',
                                           names=['Название', 'Тикер', 'Текущая цена',
                                                        'Средств в бумаге', 'Профит/лосс',
                                                        'Профит/лосс (%)', '% от портфеля',
                                                        'Количество бумаг(шт)', 'Средняя цена покупки',
                                                        'Балансовая цена'])

        inner_list = read_file_portfel_data.merge(read_file_stoks_data, how = 'inner',
                                                  left_on ='Тикер', right_on = 'Тикер')

        new = inner_list[['Название_x', 'Тикер', 'Текущая цена_y', 'Средств в бумаге',
                          'Средняя цена покупки','Профит/лосс', 'Профит/лосс (%)',
                          '% от портфеля', 'Количество бумаг(шт)', 'Балансовая цена']]

        with open('portfel.csv', 'w', newline='') as file:
            pass

        read_file_stoks_data = None
        read_file_portfel_data = None
        inner_list = None



        #выбираем все тикеры компаний в портфеле
        portfel_stocs_list = new.Тикер
        portfel_stocs_list = list(portfel_stocs_list)
        for stock in portfel_stocs_list:
            data_list = new[new.Тикер == stock]
            self.stocks_fullname = str(data_list['Название_x'].values)
            self.stocks_fullname = self.stocks_fullname[2:-2]
            self.stocks_ticker = str(data_list['Тикер'].values)
            self.stocks_ticker = self.stocks_ticker[2:-2]
            self.current_price = float(data_list['Текущая цена_y'])
            self.money_in_stock = float(data_list['Средств в бумаге'].values)
            # self.stocks_profit = float(data_list['Профит/лосс'].values)
            # self.portfel_stocks_percent = float(data_list['% от портфеля'].values)
            self.stocks_amount = float(data_list['Количество бумаг(шт)'].values)
            self.average_price = float(data_list['Средняя цена покупки'].values)
            self.balance_price = float(data_list['Балансовая стоимость'])

            self.calculation_data_update()
    def back_to_main_control(self, control):
        if control == 'Прервать':
            self.main_control()
        else:
            pass
    # получение данных о проведенной транзакции
    # запуск функции searching_element_in_portfel
    def getting_transaction_buying_data(self):
        self.stocks_ticker = input('Введите тикер акции: ')
        self.buying_price = float(input('Введите цену покупки: '))
        self.buying_stocks_amount = int(input('Введите количество купленных акций: '))


        self.calculation_data_buying()

    def getting_transaction_selling_data(self):
        self.stocks_ticker = input('Введите тикер акции: ')
        self.buying_price = float(input('Введите цену продажи: '))
        self.buying_stocks_amount = int(input('Введите количество проданных акций: '))

        self.calculation_data_cell()
    # функция выполняется при отсутствии данной компании в портфеле
    # нижеперечисленные вычисления вынести в универсальную функцию
    def calculation_data_buying(self):
        if self.stocks_ticker in self.existing_stoks:
            read_file_portfel_data = pd.read_csv('portfel.csv', delimiter=';', encoding='Windows-1251',
                                                 names=['Название', 'Тикер', 'Текущая цена',
                                                        'Средств в бумаге', 'Профит/лосс',
                                                        'Профит/лосс (%)', '% от портфеля',
                                                        'Количество бумаг(шт)', 'Средняя цена покупки',
                                                        'Балансовая цена'])


            calculation_line = read_file_portfel_data[read_file_portfel_data.Тикер == self.stocks_ticker]
            ind = int(calculation_line.index.values)
            read_file_portfel_data = read_file_portfel_data.drop(ind)
            read_file_portfel_data.to_csv('portfel.csv', encoding='Windows-1251',
                                          header=False, sep=';',
                                          mode='w', index=False)


            self.stocks_fullname = str(calculation_line['Название'].values)
            self.current_price = float(calculation_line['Текущая цена'])
            if self.current_price/2 < self.buying_price < self.current_price*2:
                self.stocks_fullname = self.stocks_fullname[2:-2]
                self.balance_price = float(calculation_line['Балансовая цена']) + self.buying_price * self.buying_stocks_amount
                self.stocks_amount = float(calculation_line['Количество бумаг(шт)'])
                self.average_price = self.balance_price/(self.stocks_amount + self.buying_stocks_amount)
                self.stocks_amount = float(self.buying_stocks_amount) + self.stocks_amount
                self.money_in_stock = self.stocks_amount * self.current_price
                self.stocks_profit = (self.current_price - self.average_price)*self.stocks_amount
                self.stocks_percent_profit = (self.current_price / self.average_price - 1) * 100
                self.portfel_stocks_percent = round(self.money_in_stock * 10 / self.portfel_summ, 2)
                self.portfel_summ += self.current_price*self.buying_stocks_amount - self.buying_stocks_amount*self.buying_price
                self.free_portfel_summ = self.portfel_summ - self.money_in_stock

                self.write_system_data()

                self.writting_stocks_byuing_data_to_file()
            else:
                self.clear_current_data()
                self.main_control()


        else:
            read_file_stoks_data = pd.read_csv('listing_data\\spb_stock_list.csv', delimiter=';',
                                               encoding='Windows-1251',
                                               names=['Название', 'Тикер', 'Текущая цена', '$	Изм, %',
                                                      '1 нед %', '1 м, %'])
            search_line = read_file_stoks_data[read_file_stoks_data.Тикер == self.stocks_ticker]


            self.stocks_fullname = str(search_line['Название'].values)
            if self.stocks_fullname == '[]':
                print("Такой компании нет")
                self.main_control()
            else:
                self.current_price = float(search_line['Текущая цена'])
                if self.current_price / 2 < self.buying_price < self.current_price * 2:
                    self.stocks_fullname = self.stocks_fullname[2:-2]
                    self.money_in_stock = round(self.current_price * self.buying_stocks_amount, 2)
                    self.average_price = self.buying_price
                    self.stocks_amount = self.buying_stocks_amount
                    self.stocks_profit = round(self.money_in_stock - self.average_price * self.buying_stocks_amount, 2)
                    self.stocks_percent_profit = (self.current_price / self.average_price - 1) * 100
                    self.portfel_stocks_percent = round(self.money_in_stock * 10 / self.portfel_summ, 2)
                    self.balance_price = round(self.buying_price * self.buying_stocks_amount, 2)
                    self.portfel_summ += self.stocks_profit
                    self.free_portfel_summ = self.portfel_summ - self.money_in_stock

                    self.write_system_data()
                    self.writting_stocks_byuing_data_to_file()

                    self.clear_current_data()
                else:
                    self.clear_current_data()
                    self.main_control()

    def clear_current_data(self):
        self.current_price = None
        self.buying_price = None
        self.buying_value = None
        self.stocks_fullname = None
        self.stocks_ticker = None
        self.average_price = None
        self.money_in_stock = None
        self.stocks_profit = None
        self.portfel_stocks_percent = None
        self.stocks_amount = None
        self.balance_price = None
        self.different = None
        self.stocks_percent_profit = None

    def calculation_data_cell(self):
        if self.stocks_ticker in self.existing_stoks:
            read_file_portfel_data = pd.read_csv('portfel.csv', delimiter=';', encoding='Windows-1251',
                                                 names=['Название', 'Тикер', 'Текущая цена',
                                                        'Средств в бумаге', 'Профит/лосс',
                                                        '% от портфеля', 'Количество бумаг(шт)',
                                                        'Средняя цена покупки', 'Балансовая цена'])

            calculation_line = read_file_portfel_data[read_file_portfel_data.Тикер == self.stocks_ticker]
            ind = int(calculation_line.index.values)
            read_file_portfel_data = read_file_portfel_data.drop(ind)
            read_file_portfel_data.to_csv('portfel.csv', encoding='Windows-1251',
                                          header=False, sep=';',
                                          mode='w', index=False)

            self.stocks_fullname = str(calculation_line['Название'].values)
            self.current_price = float(calculation_line['Текущая цена'])
            if self.current_price / 2 < self.buying_price < self.current_price * 2:
                self.stocks_fullname = self.stocks_fullname[2:-2]
                self.stocks_amount = float(calculation_line['Количество бумаг(шт)'])
                self.average_price = round(float(calculation_line['Средняя цена покупки']), 2)
                self.balance_price = float(calculation_line['Балансовая цена'])
                self.balance_price = round(self.balance_price - self.balance_price / self.stocks_amount * self.buying_stocks_amount, 2)
                self.stocks_amount = self.stocks_amount - self.buying_stocks_amount
                self.money_in_stock = float(calculation_line['Средств в бумаге']) - self.buying_price * self.buying_stocks_amount
                self.stocks_profit = (self.buying_price - self.average_price) * self.buying_stocks_amount + (self.current_price - self.average_price)*self.stocks_amount
                self.stocks_percent_profit = (self.current_price / self.average_price - 1) * 100
                self.portfel_stocks_percent = round(self.money_in_stock * 10 / self.portfel_summ, 2)
                self.portfel_summ -= (self.buying_price - self.average_price) * self.buying_stocks_amount
                self.free_portfel_summ += self.buying_stocks_amount * self.buying_price
                self.write_system_data()
                if self.stocks_amount == 0:
                    pass
                else:
                    self.writting_stocks_byuing_data_to_file()
            else:
                self.clear_current_data()
                self.main_control()


        else:
            read_file_stoks_data = pd.read_csv('listing_data\\spb_stock_list.csv', delimiter=';',
                                               encoding='Windows-1251',
                                               names=['Название', 'Тикер', 'Текущая цена', '$	Изм, %',
                                                      '1 нед %', '1 м, %'])
            search_line = read_file_stoks_data[read_file_stoks_data.Тикер == self.stocks_ticker]

            self.stocks_fullname = str(search_line['Название'].values)
            if self.stocks_fullname == '[]':
                print("Такой компании нет")
                self.main_control()
            else:
                self.current_price = float(search_line['Текущая цена'])
                if self.current_price / 2 < self.buying_price < self.current_price * 2:
                    self.stocks_fullname = self.stocks_fullname[2:-2]

                    self.money_in_stock = round(self.current_price * self.buying_stocks_amount, 2)
                    self.average_price = self.buying_price
                    self.stocks_amount = self.buying_stocks_amount
                    self.stocks_profit = round(self.money_in_stock + self.average_price * self.buying_stocks_amount, 2)
                    self.stocks_percent_profit = (self.current_price / self.average_price - 1) * 100
                    self.portfel_stocks_percent = round(self.money_in_stock * 10 / self.portfel_summ, 2)
                    self.balance_price = round(self.buying_price * self.buying_stocks_amount, 2)
                    self.free_portfel_summ = self.portfel_summ - self.buying_price * self.buying_stocks_amount

                    self.write_system_data()
                    self.writting_stocks_byuing_data_to_file()

                    self.clear_current_data()
                else:
                    self.clear_current_data()
                    self.main_control()

    #вычисление данных при обновлении портфеля
    def calculation_data_update(self):
        self.stocks_profit = round((self.current_price - self.average_price) * self.stocks_amount, 2)
        self.different = self.money_in_stock - round(self.current_price * self.stocks_amount, 2)
        self.money_in_stock = round(self.current_price * self.stocks_amount, 2)
        self.portfel_stocks_percent = (self.money_in_stock * 10)/self.portfel_summ
        self.stocks_percent_profit = (self.current_price / self.average_price - 1) * 100
        self.portfel_summ += self.different
        self.free_portfel_summ = self.portfel_summ - self.money_in_stock
        print(self.portfel_summ)

        self.write_system_data()
        self.writing_transaction_data_to_cell()
        self.writting_stocks_data_to_file()
        self.clear_current_data()


    # поиск свободной ячейки и запись данных в ячейку и в файл portfel.csv
    def writing_transaction_data_to_cell(self):
        pass


    # вызов функции записи данных в соответствующую ячейку переделать спомощью pandas
    def writting_stocks_data_to_file(self):
        writing_list = [self.stocks_fullname, self.stocks_ticker, self.current_price,
                        self.money_in_stock, self.stocks_profit, self.stocks_percent_profit,
                        self.portfel_stocks_percent, self.stocks_amount, self.average_price,
                        self.balance_price]
        with open('portfel.csv', 'a+', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(writing_list)


    def writting_stocks_byuing_data_to_file(self):
        writing_list = [self.stocks_fullname, self.stocks_ticker, self.current_price,
                        self.money_in_stock, self.stocks_profit, self.stocks_percent_profit,
                        self.portfel_stocks_percent, self.stocks_amount, self.average_price,
                        self.balance_price]

        with open('portfel.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(writing_list)



        self.clear_current_data()

        self.loading_data()
        self.main_control()


    def loading_data(self):
        read_file_portfel_data = pd.read_csv('portfel.csv', delimiter=';', encoding='Windows-1251',
                                           names=['Название', 'Тикер', 'Текущая цена',
                                                  'Средств в бумаге', 'Профит/лосс',
                                                  '% от портфеля', 'Количество бумаг(шт)',
                                                  'Средняя цена покупки', 'Балансовая стоимость'])
        self.existing_stoks = read_file_portfel_data.Тикер
        self.existing_stoks = list(self.existing_stoks)






def main():
    ex = App()
    ex.inicialization()
    sys.exit()


if __name__ == '__main__':
    main()

