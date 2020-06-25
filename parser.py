import requests
from bs4 import BeautifulSoup

URL = 'https://kolesa.kz/cars/audi/'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
HOST = 'https://kolesa.kz'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='row vw-item list-item blue a-elem')

    cars = []
    for item in items:
        cars.append({
            'title': item.find('span', class_='a-el-info-title').get_text(strip=True),
            'description': item.find('div', class_='a-search-description').get_text(strip=True),
            'link': HOST + item.find('a', class_='list-link ddl_product_link').get('href'),
            'price': item.find('span', class_='price').get_text(strip=True),
            'region': item.find('div', class_='list-region').get_text(strip=True)
        })
    print(cars)


def parse() -> None:
    html = get_html(URL)
    if html.status_code == 200:
        for i in range(5):
            txt = html.text
            get_content(txt)
            new_page = BeautifulSoup(txt, 'html.parser')
            new_url = HOST + new_page.find('span', class_='pag-next-page').find_next('a').get('href')
            html = get_html(new_url)

    else:
        print('Error')


parse()
