import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://kolesa.kz/cars/volvo/'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
HOST = 'https://kolesa.kz'
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('div', class_='pager')
    if pagination:
        pagination = pagination.find_all('a')
        prelast_item_pagination = pagination[-2]
        return int(prelast_item_pagination.get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='row vw-item list-item blue a-elem')

    cars = []
    for item in items:
        cars.append({
            'title': item.find('span', class_='a-el-info-title').get_text(strip=True),
            #'description': item.find('div', class_='a-search-description').get_text(strip=True),
            'link': HOST + item.find('a', class_='list-link ddl_product_link').get('href'),
            'price': item.find('span', class_='price').get_text(strip=True),
            'region': item.find('div', class_='list-region').get_text(strip=True)
        })
    return cars


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title','link','price','region'])
        for item in items:
            writer.writerow([item['title'],item['link'],item['price'],item['region']])


def parse() -> None:
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count+1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print(f'Получено {len(cars)} автомобилей')
    else:
        print('Error')


parse()
