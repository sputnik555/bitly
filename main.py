import requests
import os
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, url):
    api_method_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {'Authorization': 'Bearer {}'.format(token)}
    payload = {
      'long_url': url
    }
    response = requests.post(api_method_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']


def is_bitlink(token, url):
    parsed_url = urlparse(url)
    api_template = 'https://api-ssl.bitly.com/v4/bitlinks/{}{}'
    api_method_url = api_template.format(parsed_url.netloc, parsed_url.path)
    headers = {'Authorization': 'Bearer {}'.format(token)}
    response = requests.get(api_method_url, headers=headers)
    return response.ok


def count_clicks(token, url):
    parsed_url = urlparse(url)
    api_template = 'https://api-ssl.bitly.com/v4/bitlinks/{}{}/clicks/summary' 
    api_method_url = api_template.format(parsed_url.netloc, parsed_url.path)
    headers = {'Authorization': 'Bearer {}'.format(token)}
    response = requests.get(api_method_url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def main():
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')

    parser = argparse.ArgumentParser(description='Генерация новых ссылок bitly, получение статистики переходов')
    parser.add_argument('url', help='Ссылка')
    url = parser.parse_args().url

    if is_bitlink(token, url):
        try:
            total_clicks = count_clicks(token, url)
            print('Количество кликов:', total_clicks)
        except requests.exceptions.HTTPError:
            print('Ошибка получения статистики кликов')
    else:
        try:
            bitlink = shorten_link(token, url)
            print('Битлинк:', bitlink)
        except requests.exceptions.HTTPError:
             print('Ошибка при формировании нового битлинка')

if __name__ == '__main__':
    main()
