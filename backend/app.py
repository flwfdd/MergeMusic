'''
Author: flwfdd
Date: 2022-01-03 13:33:31
LastEditTime: 2022-01-04 23:38:44
Description: 物理服务器Flask
_(:з」∠)_
'''
from flask_cors import CORS
from flask import Flask, request
import search
import music

app = Flask(__name__)
CORS(app, resources=r"/*")


@app.route("/")
def say_hello():
    return "Hello MergeMusic!"

# 搜索服务
@app.route('/search/', methods=['GET', 'POST'])
def search_():
    dic = request.values.to_dict()
    res = search.main(dic)

    return res

# 音乐服务
@app.route('/music/', methods=['GET', 'POST'])
def music_():
    dic = request.values.to_dict()
    res = music.main(dic)

    return res


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000)
