import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import Headers
import Steam_Games_Gets
import MySQL_Connect
import re


headers = Headers.steam_headers()


def get_gamelist(n):
    linklist = []
    IDlist = []
    for pagenum in range(1, n):
        r = requests.get(
            'https://store.steampowered.com/search/?ignore_preferences=1&category1=998&os=win&filter=globaltopsellers'
            '&page=%d' % pagenum,
            headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        # print(soup)
        soups = soup.find_all(href=re.compile(r"https://store.steampowered.com/app/"),
                              class_="search_result_row ds_collapse_flag")
        for i in soups:
            i = i.attrs
            i = i['href']
            link = re.search('https://store.steampowered.com/app/(\d*?)/', i).group()
            ID = re.search('https://store.steampowered.com/app/(\d*?)/(.*?)/', i).group(1)
            linklist.append(link)
            IDlist.append(ID)
        print('已完成' + str(pagenum) + '页,目前共' + str(len(linklist)))
    return linklist, IDlist


def get_dataform(n):
    linklist, IDlist = get_gamelist(n)
    datadict = {
        'Link': linklist,
        'ID': IDlist
    }
    dataform = pd.DataFrame(datadict)
    return dataform


def get_all(x):
    try:
        request = requests.get(x['Link'], headers=headers, timeout=10)
    except:
        print('Server No Response For 1 Time!')
        try:
            request = requests.get(x['Link'], headers=headers, timeout=10)
        except:
            print('Server No Response For 2 Times!')
            try:
                request = requests.get(x['Link'], headers=headers, timeout=10)
            except:
                print('Server No Response For 3 Times!')
    try:
        soup = BeautifulSoup(request.text, 'lxml')
        all_games = Steam_Games_Gets.get_details(soup)
        for each in range(len(all_games)):
            all_games[each] += [x['Link'], x['ID']]
        print(all_games)
        return all_games
    except:
        print('get_details ERROR!')
        return [[]]


def main():
    pages = 2
    df1 = get_dataform(pages)
    results = df1.apply(get_all, axis=1)
    open('Price_Down_List.txt', 'r+').truncate()
    results.apply(MySQL_Connect.data_Check)


if __name__ == "__main__":
    main()
