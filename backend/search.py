'''
Author: flwfdd
Date: 2021-11-13 16:30:46
LastEditTime: 2024-02-21 17:47:21
Description: 搜索模块
_(:з」∠)_
'''
# -*- coding: utf-8 -*-
import requests
import json
import urllib.parse
import html

import config

# 读入配置
header = config.header
api_search_url = config.api_base_url.copy()
api_search_url['C'] += "/search?keywords={}&type={}&limit={}&offset={}"
api_search_url['B'] = "https://api.bilibili.com/x/web-interface/search/type?keyword={}&search_type={}&page={}"


def cloud_search(keyword, Type, limit, offset):
    typet = {"music": "1", "lrc": "1006", "list": "1000", "user": "1002"}

    try:
        Type = typet[Type]
    except:
        Type = typet["music"]
    offset = str(int(offset)*int(limit))
    url = api_search_url["C"].format(keyword, Type, limit, offset)
    print(url)
    r = requests.get(url, headers=header)

    if Type == typet['music'] or Type == typet['lrc']:
        dic = json.loads(r.text)['result']['songs']
        for ind, i in enumerate(dic):
            x = {}
            x['type'] = 'music'
            x['mid'] = "C"+str(i['id'])
            x['name'] = i['name']
            x['artist'] = [j["name"] for j in i['ar']]
            x['album'] = {'name': i['al']["name"]}
            dic[ind] = x
    elif Type == typet['list']:
        dic = json.loads(r.text)['result']['playlists']
        for ind, i in enumerate(dic):
            x = {}
            x['type'] = 'list'
            x['mid'] = "C"+str(i['id'])
            x['name'] = i['name']
            x['artist'] = [i['creator']['nickname']]
            x['album'] = {'name': ""}
            dic[ind] = x
    elif Type == typet['user']:
        dic = json.loads(r.text)['result']['userprofiles']
        for ind, i in enumerate(dic):
            x = {}
            x['type'] = 'user'
            x['mid'] = "C"+str(i['userId'])
            x['name'] = i['nickname']
            x['artist'] = [i['nickname']]
            x['album'] = {'name': ""}
            dic[ind] = x
    return dic


def qq_search(keyword, Type, limit, offset):
    typet = {"music": "0", "lrc": "7"}
    try:
        Type = typet[Type]
    except:
        Type = typet["music"]
    data = {
        "music.search.SearchCgiService": {
            "method": "DoSearchForQQMusicDesktop",
            "module": "music.search.SearchCgiService",
            "param": {
                "num_per_page": int(limit),
                "page_num": int(offset)+1,
                "query": urllib.parse.unquote(keyword),
                "search_type": int(Type)
            }
        }
    }
    url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
    print(data)
    r = requests.post(url, data=json.dumps(
        data, ensure_ascii=False).encode('utf-8'))
    print(r.text)
    dic = r.json()[
        'music.search.SearchCgiService']['data']['body']['song']['list']

    for ind, i in enumerate(dic):
        if ind == 0:
            print(i)
        x = {}
        x['type'] = 'music'
        x['mid'] = "Q"+i['mid']
        x['name'] = i['name']
        x['artist'] = [j["name"] for j in i['singer']]
        x['album'] = {'name': i['album']['name']}
        dic[ind] = x

    return dic


def bili_search(keyword, Type, limit, offset):
    def remove_em(s):
        s = "".join(s.split("</em>"))
        s = "".join(s.split('<em class="keyword">'))
        s = html.unescape(s)
        return s
    typet = {"music": "video", "user": "bili_user"}
    try:
        Type = typet[Type]
    except:
        Type = typet["music"]

    url = "https://api.bilibili.com/x/web-interface/search/type?keyword={}&search_type={}&page={}&page_size={}"
    url = url.format(keyword, Type, str(int(offset)+1), limit)
    print(url)
    headers = config.header
    headers["Cookie"] = "buvid3=C6CE0BBD-51AF-CEC1-735A-B21679C581B811710infoc;"
    r = requests.get(url.format(keyword, offset), headers=headers)
    dic = json.loads(r.text)["data"]["result"]

    if Type == typet["music"]:
        for ind, i in enumerate(dic):
            x = {}
            x['type'] = 'p'
            x['mid'] = "Bav"+str(i['aid'])
            x['name'] = remove_em(i['title'])
            x['artist'] = [i["author"]]
            x['album'] = {'name': ""}
            dic[ind] = x
    elif Type == typet["user"]:
        for ind, i in enumerate(dic):
            x = {}
            x['type'] = 'user'
            x['mid'] = "B"+str(i['mid'])
            x['name'] = i['uname']
            x['artist'] = [i['usign']]
            x['album'] = {'name': ""}
            dic[ind] = x
    else:
        dic = []

    return dic


# 入口函数
def main(dic):
    offset = str(int(dic.get('offset', 0)))
    limit = dic.get('limit', '20')
    keyword = dic.get('keyword', '')
    Type = dic.get('type', 'music')
    platform = dic.get('platform', 'C')

    if platform == "C":
        res = cloud_search(keyword, Type, limit, offset)
    elif platform == "Q":
        res = qq_search(keyword, Type, limit, offset)
    elif platform == "B":
        res = bili_search(keyword, Type, limit, offset)

    return json.dumps(res, ensure_ascii=False)


if __name__ == "__main__":
    print(bili_search("cage", "music", 20, 0))
