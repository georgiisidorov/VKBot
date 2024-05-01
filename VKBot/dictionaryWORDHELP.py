import random
import time
import requests
from bs4 import BeautifulSoup

url = 'https://wordhelp.ru/contains/'

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й',
            'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
            'х', 'ц', 'ч', 'ш', 'щ', 'э', 'ю', 'я']
#намеренно пропустил Ъ Ы Ь, потому что они точно встретятся в словах с буквами, что я уже прописал

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    wordsblok = soup.find_all('ul', class_='list-inline results')
    a = []
    for i in range(len(wordsblok)):
        words = wordsblok[i].find_all('li')
        for j in range(len(words)):
            a.append(words[j].get_text().strip())
    return a


def lastpagenum(url):
    html = get_html(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    lastpagenum = soup.find('noindex').find('p').get_text()
    i = lastpagenum.find('из ') + 3
    s = ''
    while lastpagenum[i] != '.':
        s += lastpagenum[i]
        i += 1
    s = int(s) // 100 + 1
    return s

def save_file(items, path):
    file = open(path, 'w', newline='', encoding='utf-8')
    file.write(items)
    file.close()

def parse(alphabet):
    dictionary = set()
    for k in range(len(alphabet)):
        time.sleep(random.randint(1, 5))
        urlconst = 'https://wordhelp.ru/contains/'
        f = alphabet[k]  # делаем запрос
        urlconst += f
        lastpage = str(lastpagenum(urlconst))
        for page in range(1, lastpagenum(urlconst) + 1):  # стр
            time.sleep(random.randint(5, 10))
            url = urlconst + '/page/' + str(page)
            print((str(page) + '/' + lastpage), f)
            list = get_content(url)
            dictionary = dictionary.union(set(list))
    dictionary = list(dictionary)
    dictionary = sorted(dictionary)
    return dictionary

dictionary = parse(alphabet)

def joke(dictionary):
    path = 'Словарь_WORDHELP(' + str(len(dictionary)) + 'слов).txt'
    stroka = ''
    for i in range(len(dictionary)):
        stroka += dictionary[i] + ' '
    save_file(dictionary, path)

joke(dictionary)
