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



async def get_page_data():
    urls = ['https://terraceramica.ru/product/16443119']
    data = []
    for url in urls:

        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.get(url=url, data=data, headers=headers, cookies=cookies)
            soup = BeautifulSoup(await response.text(), "lxml")


            try:
                code = soup.find('div', class_='item_details_article').find('div', class_='value').text
            except AttributeError:
                code = ''

            
            try:
                title = soup.find('div', class_="col-12 col-md-6 col-lg-7  d-flex  custom").find('h1').text
            except AttributeError:
                title = '' 

            try:
                price = soup.find('div', class_="item_details_price_val").text
            except AttributeError:
                price = ''

            try:
                price_q = soup.find('div', class_="item_details_price_val").find('span').text
            except AttributeError:
                price_q = ''

            try:
                price_without_discount = soup.find('div',class_="item_details_price_val_base").find('div', class_='value').text
            except AttributeError:
                price_without_discount = ''

            try:
                price_without_discount_q = soup.find('div',class_="item_details_price_val_base").find('div', class_='value').find('span').text
            except AttributeError:
                price_without_discount_q = ''

            try:
                info = soup.find('div',class_="item_details_info").find_all('div', class_='item')#.find('div', class_='value').text
            except AttributeError:
                info = ''

            try:
                articul = info[0].find('div', class_='value').text
            except AttributeError:
                articul = ''

            try:
                collection = info[1].find('div', class_='value').text
            except AttributeError:
                collection = ''
            
            try:
                manufacture = info[2].find('div', class_='value').text
            except AttributeError:
                manufacture = ''

            try:
                color = info[3].find('div', class_='value').text
            except AttributeError:
                color = ''

            try:
                size = info[4].find('div', class_='value').text
            except AttributeError:
                size = ''

            try:
                thickness = info[5].find('div', class_='value').text
            except AttributeError:
                thickness = ''
            

            try:
                in_stock_cards = soup.find('div', class_='table_container').find_all('tr')
            except AttributeError:
                in_stock_cards = ''

            try:
                in_stock_1 = in_stock_cards[0].find('div', class_='stock').text
            except AttributeError:
                in_stock_1 = ''

            try:
                in_stock_1_tone = in_stock_cards[0].find('div', class_='tone').find('span').text
            except AttributeError:
                in_stock_1_tone = ''            

            try:
                in_stock_1_caliber = in_stock_cards[0].find('div', class_='caliber').find('span').text
            except AttributeError:
                in_stock_1_caliber = ''  

            try:
                in_stock_1_cost = in_stock_cards[0].find('div', class_='cost').find('span').text # остаток
            except AttributeError:
                in_stock_1_cost = '' 

            try:
                in_stock_2 = in_stock_cards[1].find('div', class_='stock').text
            except AttributeError:
                in_stock_2 = ''

            try:
                in_stock_2_tone = in_stock_cards[1].find('div', class_='tone').find('span').text
            except AttributeError:
                in_stock_2_tone = ''            

            try:
                in_stock_2_caliber = in_stock_cards[1].find('div', class_='caliber').find('span').text
            except AttributeError:
                in_stock_2_caliber = ''    

            try:
                in_stock_2_cost = in_stock_cards[1].find('div', class_='cost').find('span').text # остаток
            except AttributeError:
                in_stock_2_cost = '' 

            try:
                in_stock_3 = in_stock_cards[2].find('div', class_='stock').text
            except AttributeError:
                in_stock_3 = ''

            try:
                in_stock_3_tone = in_stock_cards[2].find('div', class_='tone').find('span').text
            except AttributeError:
                in_stock_3_tone = ''            

            try:
                in_stock_3_caliber = in_stock_cards[2].find('div', class_='caliber').find('span').text
            except AttributeError:
                in_stock_3_caliber = '' 

            try:
                in_stock_3_cost = in_stock_cards[2].find('div', class_='cost').find('span').text # остаток
            except AttributeError:
                in_stock_3_cost = '' 

            try:
                in_stock_4 = in_stock_cards[3].find('div', class_='stock').text
            except AttributeError:
                in_stock_4 = ''

            try:
                in_stock_4_tone = in_stock_cards[3].find('div', class_='tone').find('span').text
            except AttributeError:
                in_stock_4_tone = ''            

            try:
                in_stock_4_caliber = in_stock_cards[3].find('div', class_='caliber').find('span').text
            except AttributeError:
                in_stock_4_caliber = '' 

            try:
                in_stock_4_cost = in_stock_cards[3].find('div', class_='cost').find('span').text # остаток
            except AttributeError:
                in_stock_4_cost = ''     

            

        
                    
            print(in_stock_4_cost)


async def gather_data():

    url = 'https://terraceramica.ru'


    async with aiohttp.ClientSession(trust_env=True) as session:
        # response = await session.get(url=url, data=data, headers=headers, cookies=cookies)
        # soup = BeautifulSoup(await response.text(), "lxml")
        # links = []
        # cards: ResultSet = soup.find_all('div', class_="col-sm-6 col-md-6 col-lg-4 col-xl-4 col-xxl-3 d-flex")
        # for link in cards:
        #     link = link.find('a', class_='card_any').get('href')[0:17]
        #     link = f'{url}{link}'
        #     links.append(link)


        # links2 = []
        # for link in links:
        #     async with aiohttp.ClientSession(trust_env=True) as session:
        #         response = await session.get(url=link, data=data, headers=headers, cookies=cookies)
        #         soup = BeautifulSoup(await response.text(), "lxml")
        #         # print(soup)
        #         cards = soup.find_all('div', class_='col-sm-6 col-md-6 col-lg-4 col-xl-4 col-xxl-3 d-flex')
            
        #         for link in cards:
        #             # print(link)
        #             try:
        #                 link = link.find('a', class_='card_any').get('href')
        #             except AttributeError:
                        
        #                 link = link.find('a', class_='card_producer').get('href')
                        
        #             link = f'{url}{link}'
        #             # print(link + ' - FIRST PAGE URLS')
        #             links2.append(link)
        # # print(links2)

        # links3 = []
        
        # for link in links2:
        #     async with aiohttp.ClientSession(trust_env=True) as session:
        #         response = await session.get(url=link, data=data, headers=headers, cookies=cookies)
        #         soup = BeautifulSoup(await response.text(), "lxml")
        #         cards = soup.find_all('div', class_='col-sm-6 col-md-6 col-lg-4 col-xl-4 col-xxl-3 d-flex')
        #         a = 0
        #         for link in cards:
                    
        #             try:
        #                 link = link.find('a', calss_='card_collection').get('href')
        #             except AttributeError:
        #                 try:
        #                     link = link.find('a', class_='card_producer').get('href')
        #                 except AttributeError:
        #                     try:
        #                         link = link.find('a', class_="card_collection").get('href')
        #                     except AttributeError:
        #                         link = link.find('a', class_="card_any").get('href')
        #             link = f'{url}{link}'
        #             print(link + ' - SECOND PAGE')
        #             links3.append(link)

        # # print(links3)
        # links4 = []
        # for linkk in links3:
        #     async with aiohttp.ClientSession(trust_env=True) as session:
        #         response = await session.get(url=linkk, data=data, headers=headers, cookies=cookies)
        #         soup = BeautifulSoup(await response.text(), "lxml")
                
        #         cards = soup.find_all('div', class_='col-sm-6 col-md-6 col-lg-4 col-xl-4 col-xxl-3 d-flex')
        #         # print(cards)
        #         for link in cards:
        #             try:
        #                 link = link.find('a', class_='card_collection').get('href')
        #                 # link = f'{url}{link}'
        #                 # print(link + '    BBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        #                 # link = f'{url}{link}'
        #             except AttributeError:
        #                 try:
        #             #    print(link)
        #                     link = link.find('a', class_='card_any').get('href')
        #                     # link = f'{url}{link}'
        #                     # print(link + '    AAAAAAAAAAAAAAAAAAAAAA')
        #                 except AttributeError:
        #                     # print(link)
        #                     link = link.find('a', class_='card_producer').get('href')
        #                     # link = f'{url}{link}'
        #                     # print(link + '    VVVVVVVVVVVVVVVVVVVVVVVV')
        #             link = f'{url}{link}'
        #             # print(link + ' - done links i hope')
        #             links4.append(link)
        #             print(link + ' - THIRD PAGE')

        # # print(links4)
        # # print(products_page_urls)
        # # print(links4)


        # all_cards_links = []
        # for link in links3:
        #     async with aiohttp.ClientSession(trust_env=True) as session:
        #         response = await session.get(url=link, data=data, headers=headers, cookies=cookies)
        #         soup = BeautifulSoup(await response.text(), "lxml")
                
        #         cards = soup.find_all('div', class_="col-12 col-sm-6 col-md-4 col-lg-4 col-xl-4 col-xxl-3 d-flex")
        #         # print(cards)
        #         for card in cards:
        #             try:
        #                 card_link = card.find('a', class_='info_title').get('href')
        #                 card_link = f'{url}{card_link}'
        #                 print(card_link + '   - PRODUCT LINK 1')
        #                 all_cards_links.append(card_link)
        #             except AttributeError:
        #                 print('error')
                
                

        # # print(all_cards_links)

        # for link in links4:
        #     async with aiohttp.ClientSession(trust_env=True) as session:
        #         response = await session.get(url=link, data=data, headers=headers, cookies=cookies)
        #         soup = BeautifulSoup(await response.text(), "lxml")
                
        #         cards = soup.find_all('div', class_="col-12 col-sm-6 col-md-4 col-lg-4 col-xl-4 col-xxl-3 d-flex")
        #         # print(cards)
        #         for card in cards:
        #             try:
        #                 card_link = card.find('a', class_='info_title').get('href')
        #                 card_link = f'{url}{card_link}'
        #                 print(card_link + '   - PRODUCT LINK 2')
        #                 all_cards_links.append(card_link)
        #             except AttributeError:
        #                 print('error')
        
            

        task = asyncio.create_task(get_page_data())
        await asyncio.gather(task)


def main():
    asyncio.run(gather_data())
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")


if __name__ == "__main__":
    main()




# TODO:
# в наличии -> остаток поделить значение и ед измерения