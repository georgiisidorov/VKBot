# Мы парсим wordhelp.ru

import time
import requests
from bs4 import BeautifulSoup

url = 'https://wordhelp.ru/contains/'

num = input('Введите число: ')

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}

cbk = {'0': ['м', 'н'],
       '1': ['г', 'ж'],
       '2': ['д', 'т'],
       '3': ['к', 'х'],
       '4': ['ч', 'щ'],
       '5': ['б', 'п'],
       '6': ['ш', 'л'],
       '7': ['с', 'з'],
       '8': ['в', 'ф'],
       '9': ['р', 'ц']
}

glasnye = ['а', 'о', 'е', 'ю', 'я', 'ё', 'и', 'у', 'э', 'ы', 'ь', 'ъ', 'й']

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
    s = int(s)//100 + 1
    return s


for k in range(2):
    urlconst = 'https://wordhelp.ru/contains/'
    print('\nПарсинг буквы ' + cbk[num[0]][k] +'\n')
    f = cbk[num[0]][k]  #делаем запрос
    urlconst += f
    lastpage = str(lastpagenum(urlconst))
    for page in range(1, lastpagenum(urlconst) + 1): #стр
        time.sleep(1)
        url = urlconst + '/page/' + str(page)
        print('Парсинг ' + str(page) + ' страницы из ' + lastpage + '...')
        list = get_content(url)
        for word in range(len(list)):   #слова
            i = 0
            glas = 0
            for letter in range(len(list[word])): #буквы
                if glasnye.count(list[word][letter]) == 1:
                    continue
                if (list[word][letter] == cbk[num[i]][0]) or (list[word][letter] == cbk[num[i]][1]):
                    i += 1
                    if i == len(num):   #если прошёл все буквы, печатаем, i возвращаем на первую букву, выходим со слова
                        for j in range(len(list[word])):
                            if glasnye.count(list[word][j]) >= 1:
                                glas += 1
                        i = 0
                        if (len(list[word])-glas) == len(num):      #если длина слова минус все гласные == колво согласных по num, то это идеальное слово.
                            print(list[word])                       #Если поставить знак >=, то возможно будут лишние согласные
                        glas = 0
                        break
                else:   #если завалился, выходим со слова, вернув i на первую букву
                    i = 0
                    break


