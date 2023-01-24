import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import aiohttp
import asyncio
from decouple import config
import time
import csv
import xlsxwriter 
from bs4 import ResultSet
import requests
from requests_html import HTMLSession




start_time = time.time()
result = []
cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

cookies = {
    'csrftoken': '38LU3tgTgto1PsaoIKjCNTDftxri2Pxrnb0AbnemmOKcA0Xp7pxg7h4dchdntUAg',
    'sessionid': '9tp28dt3d0j77m4wsf2tmijzpkcye9us',
    'is_authenticated': '1',
    'roomId': 'eae5ad52-85ee-44c5-b0c3-1f6239cc0ffe',
    'preRoomId': 'f8f6b1ab-47a4-4ba2-86e2-71af5e751cf7',
}

headers = {
    'authority': 'terraceramica.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'csrftoken=38LU3tgTgto1PsaoIKjCNTDftxri2Pxrnb0AbnemmOKcA0Xp7pxg7h4dchdntUAg; sessionid=9tp28dt3d0j77m4wsf2tmijzpkcye9us; is_authenticated=1; roomId=eae5ad52-85ee-44c5-b0c3-1f6239cc0ffe; preRoomId=f8f6b1ab-47a4-4ba2-86e2-71af5e751cf7',
    'origin': 'https://terraceramica.ru',
    'referer': 'https://terraceramica.ru/login/',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}

data = {
    'csrfmiddlewaretoken': config('TOKEN'),
    'username': config('LOGIN'),
    'password': config('PASSWORD'),
    'next': '',
}
url = 'https://terraceramica.ru'

# response = requests.post('https://terraceramica.ru/login/', cookies=cookies, headers=headers, data=data)
# print(response)
# res = requests.get('https://terraceramica.ru/')
# print(res.text)
# import time

class Parse():

    def get_html(url: str, headers: dict='', params: str=''):
        """ Функция для получения html кода """
        html = requests.get(
            url=url,
            headers=headers,
            params=params,
            cookies=cookies,
            verify=False 
        )
        return html

    def nomenclature_urls(html: str) -> ResultSet:
        """ Функция для получения url с главной страницы"""
        soup = BeautifulSoup(html.text, 'lxml')
        # print(soup)
        cards: ResultSet = soup.find_all('div', class_="col-sm-6 col-md-6 col-lg-4 col-xl-4 col-xxl-3 d-flex")
        links =[]
        for link in cards:
            link = link.find('a', class_='card_any').get('href')[0:17]
            # print(link)
            link = f'{url}{link}'
            links.append(link)
        return links

    nomenclature_urls = nomenclature_urls(get_html(url))
    def countries_urls(urls: list):
        """ Функция для получения url с страницы КЕРАМИКА"""
        # print(urls[0])
        # for url in urls:
        #     # print(url)
        html = requests.get(url=urls[0], headers=headers)
        # print(html.text)
        soup = BeautifulSoup(html.text, 'lxml')
        cards = soup.find_all('div', class_='col-sm-6 col-md-6 col-lg-4 col-xl-4 col-xxl-3 d-flex')
        links = []
        for link in cards:
            link = link.find('a', class_='card_any').get('href')
            link = f'{url}{link}'
            # print(link)
            links.append(link)
        return links

    def klinker_urls(urls: list):
        """ Функция для получения url с страницы КЛИНКЕР"""
        # print(urls[0])
        # for url in urls:
        #     # print(url)
        html = requests.get(url=urls[1], headers=headers)
        # print(html.text)
        soup = BeautifulSoup(html.text, 'lxml')
        cards = soup.find_all('div', class_='col-sm-6 col-md-6 col-lg-4 col-xl-4 col-xxl-3 d-flex')
        links = []
        for link in cards:
            # print(link)
            link = link.find('a', class_='card_producer').get('href')
            link = f'{url}{link}'
            # print(link)
            links.append(link)
        return links


    def st_urls(urls: list):
        """ Функция для получения url с страницы СТУПЕНИ"""
        # print(urls[0])
        # for url in urls:
        #     # print(url)
        html = requests.get(url=urls[2], headers=headers)
        # print(html.text)
        soup = BeautifulSoup(html.text, 'lxml')
        cards = soup.find_all('div', class_='col-sm-6 col-md-6 col-lg-4 col-xl-4 col-xxl-3 d-flex')
        links = []
        for link in cards:
            link = link.find('a', class_='card_any').get('href')
            link = f'{url}{link}'
            # print(link)
            links.append(link)
        return links   

    def gr_urls(urls: list):
        """ Функция для получения url с страницы КРУПНОФОРМАТНЫЙ КЕРАМИЧЕСКИЙ ГРАНИТ"""
        # print(urls[0])
        # for url in urls:
        #     # print(url)
        html = requests.get(url=urls[3], headers=headers)
        # print(html.text)
        soup = BeautifulSoup(html.text, 'lxml')
        cards = soup.find_all('div', class_='col-sm-6 col-md-6 col-lg-4 col-xl-4 col-xxl-3 d-flex')
        links = []
        for link in cards:
            # print(link)
            try:
                link = link.find('a', class_='card_producer').get('href')
            except AttributeError:
                link = link.find('a', class_='card_any').get('href')
            link = f'{url}{link}'
            # print(link)
            links.append(link)
        return links

   
    countries_urls(nomenclature_urls)
    klinker_urls(nomenclature_urls)
    st_urls(nomenclature_urls)
    gr_urls(nomenclature_urls)




      
a = Parse()
# html = a.get_html(url)
print(a)











