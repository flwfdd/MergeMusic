'''
Author: flwfdd
Date: 2022-01-03 13:32:11
LastEditTime: 2022-01-04 23:38:04
Description: 阿里云函数计算入口
_(:з」∠)_
'''
# -*- coding: utf-8 -*-

import json
import re
import urllib

import search
import music


def handler(environ, start_response):
    request_url = urllib.parse.urlparse(environ['fc.request_uri']).path
    dic = urllib.parse.parse_qs(environ['QUERY_STRING'])
    for i in dic:
        dic[i] = dic[i][0]
    if request_url.endswith("/search/"):
        res = search.main(dic)
    elif request_url.endswith("/music/"):
        res = music.main(dic)

    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [res.encode("utf-8")]
