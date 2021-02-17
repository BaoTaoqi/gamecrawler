import MySQLdb
import re


Depository = 'SteamGames_depository'
ErrorCheck = 'SteamGames_errorcheck'
AllGames = 'GameCrawler_allgames'
db = MySQLdb.connect('', '', '', '')


# 数据库增删查改操作
class mysql_operations:
    def __init__(self, result):
        self.result = result

    def execute(self):
        cursor = db.cursor()
        cursor.execute(self.result)
        cursor.close()
        db.commit()

    def rowcount(self):
        cursor = db.cursor()
        cursor.execute(self.result)
        cursor.close()
        db.commit()
        return cursor.rowcount

    def fetchall(self):
        cursor = db.cursor()
        cursor.execute(self.result)
        results = cursor.fetchall()
        db.commit()
        return results


# 价格检查修改
def money_modify(old_money):
    if old_money.find('¥') != -1:  # 找到匹配字符
        new_money = re.sub('¥', '', old_money)
        if new_money.find(',') != -1:  # 找到匹配字符
            new_money = re.sub(',', '', new_money)
    else:
        new_money = '0'
    return new_money


# 名字检查修改
def name_modify(old_name):
    new_name = old_name
    if old_name.find('\'') != -1:
        new_name = re.sub('\'', '\\\'', old_name)
    return new_name


# 检查是否存在
def check_if_exist(Table, Value, Data):
    sql = 'select * From {} WHERE {} = \'{}\';'.format(Table, Value, Data)
    existence = mysql_operations(sql)
    if existence.rowcount() == 0:
        return False
    else:
        return True


def lowest_price_compare(FinalPrice):
    sql = 'SELECT LowestPrice FROM SteamGames_depository WHERE FinalPrice = \'{}\';'.format(FinalPrice)
    # print(sql)
    Price = mysql_operations(sql)
    LowestPrice = Price.fetchall()[0][0]
    if int(money_modify(FinalPrice)) <= int(money_modify(LowestPrice)):
        return True
    else:
        return False


def data_insert_to_mysql(Table, Data):
    ID = Data[6]
    Link = Data[5]
    GameName = name_modify(Data[0])
    BundleBaseDiscount = Data[1]
    DiscountPct = Data[2]
    OriginalPrice = Data[3]
    FinalPrice = Data[4]
    LowestPrice = FinalPrice
    LastPrice = FinalPrice

    sql = 'INSERT INTO {} VALUES ({}, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', {});'.format(
        Table,
        ID,
        Link,
        GameName,
        BundleBaseDiscount,
        DiscountPct,
        OriginalPrice,
        FinalPrice,
        LowestPrice,
        LastPrice,
        0
    )
    execute = mysql_operations(sql)
    execute.execute()


def data_update_to_mysql(Table, Value, Data, GameName):
    sql = 'UPDATE {} SET {} = \'{}\' WHERE GameName = \'{}\';'.format(Table, Value, Data, GameName)
    execute = mysql_operations(sql)
    execute.execute()


'''
0 Name
1 if_bundle
2 if_discount_pct
3 original_price
4 final_price
5 Link
6 ID
'''
'''
检查名字 或者价格中是否存在ERROR，有则放入SteamERROR

检查是否存在（凭 Name）

不存在则导入 ID, Link, Name, if_bundle, if_discount_pct, OriginalPrice, FinalPrice
检查 if_bundle 区分单体和捆绑包，单体则 bundle_base_discount 为 -1，捆绑包则输入基本折扣
检查 if_discount_pct，无现有折扣则 discount_pct 为 -1，有折扣则输入折扣
检查 original_price 和 final_price 没有则 -1 
第一次LowestPrice为FinalPrice 

存在则更新
'''

def data_Check(list):
    for i in range(len(list)):
        '''检查是否有Value存在ERROR'''
        if list == [[]]: continue
        if list[i][0] == 'name ERROR' or list[i][3] == 'original_price ERROR' or list[i][4] == 'final_price ERROR':
            print('check something ERROR!')
            list[i][0] = list[i][0] + ' ID=' + str(list[i][6])
            if check_if_exist(ErrorCheck, 'GameName', name_modify(list[i][0])) and check_if_exist(ErrorCheck, 'OriginalPrice', list[i][3]) and check_if_exist(ErrorCheck, 'FinalPrice', list[i][4]) and check_if_exist(ErrorCheck, 'Link', list[i][5]) and check_if_exist(ErrorCheck, 'ID', list[i][6]):
                print('  this ERROR already exists!')
            else:
                print('  new ERROR! will place in Steam_Error_Check!')
                data_insert_to_mysql(ErrorCheck, list[i])
        else:
            print('data check OK!')
            if check_if_exist(Depository, 'GameName', name_modify(list[i][0])):
                print('  this game already exists! will update it!')
                data_update_to_mysql(Depository, 'BundleBaseDiscount', list[i][1], name_modify(list[i][0]))
                data_update_to_mysql(Depository, 'DiscountPct', list[i][2], name_modify(list[i][0]))
                data_update_to_mysql(Depository, 'OriginalPrice', list[i][3], name_modify(list[i][0]))
                LastPriceSearch = mysql_operations('SELECT FinalPrice FROM SteamGames_depository WHERE GameName = \'{}\';'.format(name_modify(list[i][0])))
                LastPrice = LastPriceSearch.fetchall()[0][0]
                data_update_to_mysql(Depository, 'LastPrice', LastPrice, name_modify(list[i][0]))
                data_update_to_mysql(Depository, 'FinalPrice', list[i][4], name_modify(list[i][0]))
                if lowest_price_compare(list[i][4]):
                    print('    find new Lowest_Price!')
                    data_update_to_mysql(Depository, 'LowestPrice', list[i][4], name_modify(list[i][0]))
                if int(money_modify(list[i][4])) < int(money_modify(LastPrice)):
                    open('Price_Down_List.txt', 'a').write(list[i][0] + '\n')
            else:
                print('  this game no exist! will place in Steam_Games!')
                data_insert_to_mysql(Depository, list[i])


if __name__ == "__main__":
    db.close()






