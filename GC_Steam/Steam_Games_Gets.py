"""
1 先区分捆绑包 game_area_purchase_game_dropdown_subscription game_area_purchase_game 及数量 再确定单独包 game_area_purchase_game
2 单独包：
确定名字 h1
（如果正在打折）
折扣截止日期 game_purchase_discount_countdown
现在折扣力度 discount_pct
原价 discount_original_price
折扣后价格 discount_final_price
（如果没有打折）
原价 game_purchase_price price
3 捆绑包
确定名字 h1
（新增折扣力度）
固有折扣 bundle_base_discount
新增折扣 discount_pct
原价 discount_original_price
折扣后价格 discount_final_price
（固有折扣力度）
固有折扣 bundle_base_discount
折扣后价格 discount_final_price 或者 game_purchase_price price
"""


from bs4 import BeautifulSoup
import re
import requests
import Headers


headers = Headers.steam_headers()


'''名称获取'''
def get_name(soup):
    name_list = soup.find('h1')
    name = re.search('购买(.*?)<|预购(.*?)<|玩(.*?)<|下载(.*?)<', str(name_list))
    if name:
        name = name.group()
        name = re.sub('购买', '', name)
        name = re.sub('预购', '', name)
        name = re.sub('玩', '', name)
        name = re.sub('下载', '', name)
        name = re.sub('<', '', name)
        name = re.sub('&amp;', '&', name)
        name = name.strip()
        return name


'''捆绑包固有折扣获取'''
def get_bundle_base_discount(soup):
    bundle_base_discount = soup.findAll(class_='bundle_base_discount')
    discount = re.search('-(.*?)%', str(bundle_base_discount))

    if discount:
        return discount.group()
    else:
        return None


'''新增折扣获取'''
def get_discount_pct(soup):
    discount_pct = soup.find(class_='discount_pct')
    discount_pct = re.search('-(.*?)%', str(discount_pct))
    if discount_pct:
        return discount_pct.group()
    else:
        return None


'''原价获取'''
def get_discount_original_price(soup):
    original_price = soup.find(class_='discount_original_price')
    original_price = re.search('¥ \w+,\w+|¥ \w+|免费|Free', str(original_price))
    if original_price:
        return original_price.group()
    else:
        return None


'''现价获取1'''
def get_discount_final_price(soup):
    final_price = soup.find(class_='discount_final_price')
    final_price = re.search('¥ \w+,\w+|¥ \w+|免费|Free', str(final_price))
    if final_price:
        return final_price.group()
    else:
        return None


'''现价获取2'''
def get_game_purchase_price_price(soup):
    game_purchase_price_price = soup.find(class_='game_purchase_price price')
    game_purchase_price_price = re.search('¥ \w+,\w+|¥ \w+|免费|Free', str(game_purchase_price_price))
    if game_purchase_price_price:
        return game_purchase_price_price.group()
    else:
        return None



def get_details(soup):
    all_games = soup.findAll(class_='game_area_purchase_game')
    count = 0
    for each_game in all_games:
        file = open('{}.html'.format(count), 'w')
        file.write(str(each_game))
        file.close()
        count += 1
    game_list = []

    for count in range(len(all_games)):
        game_detail = []
        with open('{}.html'.format(count), 'r') as file:
            each_soup = BeautifulSoup(file, 'lxml')

        '''获取游戏名称'''
        game_name = get_name(each_soup)
        if get_name(each_soup) is None:
            print('get name ERROR!')
            game_detail.append('name ERROR')
        else:
            print('get {}!'.format(game_name))
            game_detail.append(game_name)

        '''如果是捆绑包，获取基本折扣'''
        if_bundle = False
        bundle_base_discount = get_bundle_base_discount(each_soup)
        if get_bundle_base_discount(each_soup) is None:
            print('  not a bundle!')
            game_detail.append('not bundle')
        else:
            print('  get bundle_base_discount {}!'.format(bundle_base_discount))
            game_detail.append(bundle_base_discount)
            if_bundle = True

        '''捆绑包和单体分类'''
        if_bundle_discount_pct = False
        if_individual_discount_pct = False
        if if_bundle:
            bundle_discount_pct = get_discount_pct(each_soup)
            '''没有新增折扣'''
            if get_discount_pct(each_soup) is None:
                print('    get no discount_pct!')
                game_detail.append('no discount_pct')
            else:
                print('    get discount_pct {}!'.format(bundle_discount_pct))
                game_detail.append(bundle_discount_pct)
                if_bundle_discount_pct = True
        else:
            individual_discount_pct = get_discount_pct(each_soup)
            '''没有新增折扣'''
            if get_discount_pct(each_soup) is None:
                print('    get no discount_pct!')
                game_detail.append('no discount_pct')
            else:
                print('    get discount_pct {}!'.format(individual_discount_pct))
                game_detail.append(individual_discount_pct)
                if_individual_discount_pct = True

        '''捆绑包有无新增折扣分类'''
        if if_bundle is True and if_bundle_discount_pct is True:
            bundle_original_price = get_discount_original_price(each_soup)
            bundle_final_price = get_discount_final_price(each_soup)
            '''获取原价和现价'''
            if bundle_original_price is None or bundle_final_price is None:
                print('      get original_price & final_price ERROR!')
                game_detail.append('original_price ERROR')
                game_detail.append('final_price ERROR')
            else:
                print('      get original_price {} & final_price {}!'.format(bundle_original_price, bundle_final_price))
                game_detail.append(bundle_original_price)
                game_detail.append(bundle_final_price)
        elif if_bundle is True and if_bundle_discount_pct is False:
            bundle_final_price = get_discount_final_price(each_soup)
            '''获取原价'''
            if bundle_final_price is None:
                print('      get no final_price, try game_purchase_price_price!')
                bundle_game_purchase_price_price = get_game_purchase_price_price(each_soup)
                '''获取原价'''
                if bundle_game_purchase_price_price is None:
                    print('      get final_price ERROR!')
                    game_detail.append('no original_price')
                    game_detail.append('final_price ERROR')
                else:
                    print('      get final_price {}!'.format(bundle_game_purchase_price_price))
                    game_detail.append('no original_price')
                    game_detail.append(bundle_game_purchase_price_price)
            else:
                print('      get final_price {}!'.format(bundle_final_price))
                game_detail.append('no original_price')
                game_detail.append(bundle_final_price)

        '''单体有无新增折扣分类'''
        if if_bundle is False and if_individual_discount_pct is True:
            individual_original_price = get_discount_original_price(each_soup)
            individual_final_price = get_discount_final_price(each_soup)
            '''获取原价和现价'''
            if individual_original_price is None or individual_final_price is None:
                print('      get original_price & final_price ERROR!')
                game_detail.append('original_price ERROR')
                game_detail.append('final_price ERROR')
            else:
                print('      get original_price {} & final_price {}!'.format(individual_original_price,
                                                                             individual_final_price))
                game_detail.append(individual_original_price)
                game_detail.append(individual_final_price)
        elif if_bundle is False and if_individual_discount_pct is False:
            individual_final_price = get_discount_final_price(each_soup)
            '''获取原价'''
            if individual_final_price is None:
                print('      get no final_price, try game_purchase_price_price!')
                individual_game_purchase_price_price = get_game_purchase_price_price(each_soup)
                '''获取原价'''
                if individual_game_purchase_price_price is None:
                    print('      get final_price ERROR!')
                    game_detail.append('no original_price')
                    game_detail.append('final_price ERROR')
                else:
                    print('      get final_price {}!'.format(individual_game_purchase_price_price))
                    game_detail.append('no original_price')
                    game_detail.append(individual_game_purchase_price_price)
            else:
                print('      get final_price {}!'.format(individual_final_price))
                game_detail.append('no original_price')
                game_detail.append(individual_final_price)


        game_list.append(game_detail)
    return game_list
