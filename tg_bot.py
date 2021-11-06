import telebot
from auth_data import token
import macroeconomic
from threading import Thread
import sys

class Stage(macroeconomic.Macro_economic):
    def __init__(self):
        super().__init__()

    def main_control(self):
        self.inicialization_economic_data()
        update = Thread(target=self.update_control())
        communicate = Thread(target=self.telegramm_bot(token))
        update.start()
        communicate.start()
        update.join()
        communicate.join()

    def telegramm_bot(self, token):
        bot = telebot.TeleBot(token)

        @bot.message_handler(commands=['start'])
        def start_message(message):
            self.economic_data = str(self.economic_data)
            text_message = self.economic_ind + '\n' + self.unempl_ind + '\n' + self.pmi + '\n' + \
                           self.credit_ind + '\n' + self.corp_profits_ind + '\n' + self.interest_rate_ind
            + '\n' + self.inflation_rate_ind + '\n' + self.assets_ind + '\n' + self.inventories_and_sales

            bot.send_message(message.chat.id, text = text_message)

        @bot.message_handler(commands=['help'])
        def help_message(message):
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(
                telebot.types.InlineKeyboardButton
                ('Message', url='telegram.me/akimsss')
            )
            bot.send_message(message.chat.id, 'Для просмотра макроэкономической обстановки нажмите 1',
                             reply_markup=keyboard)



        bot.polling()

def main():
    ex = Stage()
    ex.main_control()
    sys.exit()

if __name__ == '__main__':
    main()

