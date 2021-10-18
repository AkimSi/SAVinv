import sys
import lxml
import requests
from bs4 import BeautifulSoup
headers = {
    ':authority': 'securepubads.g.doubleclick.net',
    ':method': 'GET',
    ':path': '/pcs/view?xai=AKAOjss1tBXir-y4QNBM2t6cuhFJJWj_vkGmfeZKEpzu7cJpMfj4NowF8lYRxd4xvHZ'
             '8aQxy3kmjw88mA_5dG52xA4XZD3eWM1P2JfL7_RGXSUZiKVAxNHtYuvzS9PNkSIWuXPrPjurgaRvA5ljkY'
             'WbSLSdFMb-dh5sbk9-1PVphYAGkjzIbtuBM4-xUJ4TebBSF_Uv-n8jKs8aQkVRZZs-WkMy5v35S4ewviis'
             'bB_1u6PR2NERLFYz-v0H1RfXd6TUj_rUONqsHjDyBk703ko7u4k2pt2SwASc6yjIBRA5n7lKQXfooZlERse'
             'B9hAxYhKXFPs4cnFySnoB3vF8mDcTbtyqjNP5zcPzahu4dOaEk3fw5hQA4kUa90GI4vNYmkg&sai=AMfl-Y'
             'TrGnXrNCHffL3pBPd1UcgEBiFAsb39T-R6hD4N58gary8Zxc4gGfGN9xoW4a7MdjvggAFnmU63zccUPmZdF'
             'S-p8w9S_L7dgruTCm4Gdj_83fNVbeuzfcTqD-xC3V0NQhdj&sig=Cg0ArKJSzCYtQvwcLNn0EAE&uach_m'
             '=[UACH]&adurl=',
    ':scheme': 'https',
    'accept': '* / *',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.0.1052'
                  ' Yowser/2.5 Safari/537.36',
    'cache-control': 'max-age=0',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru,en;q=0.9',
    "sec-ch-ua": "'Yandex';v='21', 'Not;A Brand';v='99', 'Chromium';v='93'",
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'cross-site'}
url_spb_stocks = "https://seekingalpha.com/symbol/AYX/earnings/estimates#figure_type=annual"

requests_answer = requests.get(url_spb_stocks, headers=headers)
requests_answer = requests_answer.text
soup = BeautifulSoup(requests_answer, 'lxml')
#table = soup.find('table', class_='borderless-table').find('tbody')
print(soup)