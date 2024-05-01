# Мы парсим wordhelp.ru
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

cbk_reverse = {'м': '0', 'н': '0', 'г': '1', 'ж': '1',
               'д': '2', 'т': '2', 'к': '3', 'х': '3',
               'ч': '4', 'щ': '4', 'б': '5', 'п': '5',
               'ш': '6', 'л': '6', 'с': '7', 'з': '7',
               'в': '8', 'ф': '8', 'р': '9', 'ц': '9'
               }

glasnye = ['а', 'о', 'е', 'ю', 'я', 'ё', 'и', 'у', 'э', 'ы', 'ь', 'ъ', 'й', '-']


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

numstr100_1 = []
numstr100_2 = []
numstr1000_1 = []
numstr1000_2 = []
numstr10000 = []

for i in range(100):
    numstr100_1.append(set())
    numstr100_2.append(set())
for i in range(1000):
    numstr1000_1.append(set())
    numstr1000_2.append(set())
for i in range(10000):
    numstr10000.append(set())

def parse(numstr100_1, numstr100_2, numstr1000_1, numstr1000_2, numstr10000, cbk, cbk_reverse, glasnye):
    for n in range(10):
        for k in range(2):
            time.sleep(random.randint(1, 5))
            urlconst = 'https://wordhelp.ru/contains/'
            f = cbk[str(n)][k]  # делаем запрос
            urlconst += f
            lastpage = str(lastpagenum(urlconst))
            for page in range(1, lastpagenum(urlconst) + 1):  # стр
                time.sleep(random.randint(1, 5))
                url = urlconst + '/page/' + str(page)
                print((str(page) + '/' + lastpage), f)
                list = get_content(url)
                for word in range(len(list)):  # слова
                    i = 0
                    glas = 0
                    num = ''
                    for letter in range(len(list[word])):  # буквы
                        if glasnye.count(list[word][letter]) == 0:
                            i += 1
                            num += cbk_reverse[list[word][letter]]
                            if i == 2:  #для 100
                                for j in range(len(list[word])):
                                    if glasnye.count(list[word][j]) == 1:
                                        glas += 1
                                if (len(list[word]) - glas) == len(num):  # если "==" -  идеальное кол-во согласных, ">" - неидеальное
                                    numstr100_1[int(num)].add(list[word])
                                    i = 0
                                    glas = 0
                                    num = ''
                                    break
                                if (len(list[word]) - glas) > len(num):  # если "==" -  идеальное кол-во согласных, ">" - неидеальное
                                    numstr100_2[int(num)].add(list[word])
                                    glas = 0
                            if i == 3:  #для 1000
                                for j in range(len(list[word])):
                                    if glasnye.count(list[word][j]) == 1:
                                        glas += 1
                                if (len(list[word]) - glas) == len(num):  # если "==" -  идеальное кол-во согласных, ">" - неидеальное
                                    numstr1000_1[int(num)].add(list[word])
                                    i = 0
                                    glas = 0
                                    num = ''
                                    break
                                if (len(list[word]) - glas) > len(num):  # если "==" -  идеальное кол-во согласных, ">" - неидеальное
                                    numstr1000_2[int(num)].add(list[word])
                                    glas = 0
                            if i == 4:  #для 10000
                                for j in range(len(list[word])):
                                    if glasnye.count(list[word][j]) == 1:
                                        glas += 1
                                if (len(list[word]) - glas) >= len(num):  # если ">=" - вперемешку
                                    numstr10000[int(num)].add(list[word])
                                i = 0
                                glas = 0
                                num = ''
                                break

    numstr = [numstr100_1, numstr100_2, numstr1000_1, numstr1000_2, numstr10000]
    return numstr


numbers = parse(numstr100_1, numstr100_2, numstr1000_1, numstr1000_2, numstr10000, cbk, cbk_reverse, glasnye)

numstr100_1 = numbers[0]
numstr100_2 = numbers[1]
numstr1000_1 = numbers[2]
numstr1000_2 = numbers[3]
numstr10000 = numbers[4]

def joke(numbers, ideal, joke):
    path = 'СЧСx' + str(joke) + ideal +'.txt'
    stroka = ''
    for i in range(joke):
        num = str(i)
        numbers[i] = list(numbers[i])
        numbers[i] = sorted(numbers[i])
        if len(num) < len(str(joke)) - 1:
            num = '0' * (len(str(joke)) - 1 - len(num)) + num
        stroka += '\n\n' + num + '\n\n'
        if len(numbers[i]) != 0:
            for j in range(len(numbers[i])):
                stroka += numbers[i][j] + ' '
        else:
            stroka += '— — —'
    save_file(stroka, path)

joke(numstr100_1, 'идеал', 100)
joke(numstr100_2, 'лишн', 100)
joke(numstr1000_1, 'идеал', 1000)
joke(numstr1000_2, 'лишн', 1000)
joke(numstr10000, 'все', 10000)
