# -*- coding:utf-8 -*-
import requests
import json
from MySQL_Connect import mysql_operations, name_modify
import Mail


def get_access_token():
    request = requests.get(
        '')
    data = json.loads(request.text)
    access_token = data['access_token']
    return access_token


def send_message(openid, platform):
    data = {
        "touser": openid,
        "template_id": "",
        "url": "",
        "data": {
            "first": {
                "value": "你订阅的{}有价格更新！".format(platform),
                "color": "#173177"
            },
            "keynote1": {
                "value": platform,
                "color": "#173177"
            },
            "keynote2": {
                "value": '点击查看你的降价游戏',
                "color": "#173177"
            },
            "remark": {
                "value": "由于网站流量限制，本次通知后默认不再进行第二次通知，如果您想要继续订阅该游戏，请在该游戏订阅界面重新订阅",
                "color": "#173177"
            }
        }
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(get_access_token())
    r = requests.post(url, json.dumps(data))


def main():
    file_object = open('Price_Down_List.txt')
    text = file_object.readlines()
    file_object.close()
    email_list = []
    wx_id_list = []
    for line in text:
        gamename = line.strip()
        wx_user_id = mysql_operations(
            'SELECT user_id FROM Wechat_wx_steamsubscriber WHERE steam_game_id = \'{}\' AND if_notified = 0;'.format(name_modify(gamename))).fetchall()
        if wx_user_id != ():
            for id in wx_user_id:
                wx_id_list.append([id[0], gamename])
        web_user_id = mysql_operations(
            'SELECT user_id FROM GameCrawler_steamsubscriber WHERE steam_game_id = \'{}\' AND if_notified = 0;'.format(name_modify(gamename))).fetchall()
        if web_user_id != ():
            for id in web_user_id:
                email = mysql_operations(
                    'SELECT email FROM GameCrawler_user WHERE web_openid = \'{}\';'.format(id[0])).fetchall()[0][0]
                email_list.append([email, id[0], gamename])

    final_wx_id_list = []
    for id in wx_id_list:
        if id not in final_wx_id_list:
            final_wx_id_list.append(id)
    for id in final_wx_id_list:
        send_message(id[0], 'Steam平台')
        sql = 'UPDATE Wechat_wx_steamsubscriber SET if_notified = 1 WHERE user_id = \'{}\' AND steam_game_id = \'{}\';'.format(id[0], name_modify(id[1]))
        execute = mysql_operations(sql)
        execute.execute()

    final_email_list = []
    for mail in email_list:
        if mail not in final_email_list:
            final_email_list.append(mail)
    for mail in final_email_list:
        Mail.send_mail([mail[0]], 'Steam订阅降价通知', 'Steam游戏', mail[1])
        sql = 'UPDATE GameCrawler_steamsubscriber SET if_notified = 1 WHERE user_id = \'{}\' AND steam_game_id = \'{}\';'.format(mail[1], name_modify(mail[2]))
        execute = mysql_operations(sql)
        execute.execute()

if __name__ == "__main__":
    main()