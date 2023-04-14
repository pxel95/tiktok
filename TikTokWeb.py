#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@Description:TikTok.py
@Date       :2023/01/27 19:36:18
@Author     :imgyh
@version    :1.0
@Github     :https://github.com/imgyh
@Mail       :admin@imgyh.com
-------------------------------------------------
Change Log  :
-------------------------------------------------
'''

from flask import *
from TikTok import TikTok
import argparse

def work(share_link):
    tk = TikTok()

    url = tk.getShareLink(share_link)
    key_type, key = tk.getKey(url)
    if key_type == "aweme":
        datanew, dataraw = tk.getAwemeInfo(key)
    elif key_type == "live":
        datanew = tk.getLiveInfo(key, option=False)
    return datanew

def work2(share_link,max_cursor,mode,cookie):
    tk = TikTok()
    tk.headers["Cookie"] = cookie
    url = tk.getShareLink(share_link)
    key_type, key = tk.getKey(url)

    datalist = []
    cursor = max_cursor
    has_more = 0
    if key_type == "user":
        if mode == 'post' or mode == 'like':
            datalist, cursor, has_more = tk.getUserInfoApi(sec_uid=key, mode=mode, count=35, max_cursor=max_cursor)
        elif mode == 'mix':
            datalist, cursor, has_more = tk.getUserAllMixInfoApi(sec_uid=key, count=35, cursor=max_cursor)
    elif key_type == "mix":
        datalist, cursor, has_more = tk.getMixInfoApi(mix_id=key, count=35, cursor=max_cursor)
    elif key_type == "music":
        datalist, cursor, has_more = tk.getMusicInfoApi(music_id=key, count=35, cursor=max_cursor)

    datadict={}

    if datalist is not None and datalist != []:
        datadict["data"] = datalist
        datadict["cursor"] = cursor
        datadict["has_more"] = has_more
        datadict["status_code"] = 200
    else:
        datadict["status_code"] = 500
    return datadict

app = Flask(__name__)
# 设置编码
app.config['JSON_AS_ASCII'] = False

def argument():
    parser = argparse.ArgumentParser(description='抖音去水印工具 使用帮助')
    parser.add_argument("--port", "-p", help="Web端口",
                        type=int, required=False, default=5000)
    args = parser.parse_args()

    return args

@app.route("/douyin/music", methods=["POST"])
def douyinMusic():
    usefuldict = {}
    if request.method == "POST":
        result = request.form
    else:
        usefuldict["status_code"] = 500
        return jsonify(usefuldict)

    try:
        usefuldict = work2(result["share_link"], result["cursor"], "",result["cookie"])
        usefuldict["status_code"] = 200
    except Exception as error:
        usefuldict["status_code"] = 500
    return jsonify(usefuldict)

@app.route("/douyin/mix", methods=["POST"])
def douyinMix():
    usefuldict = {}
    if request.method == "POST":
        result = request.form
    else:
        usefuldict["status_code"] = 500
        return jsonify(usefuldict)

    try:
        usefuldict = work2(result["share_link"], result["cursor"], "",result["cookie"])
        usefuldict["status_code"] = 200
    except Exception as error:
        usefuldict["status_code"] = 500
    return jsonify(usefuldict)


@app.route("/douyin/user/mix", methods=["POST"])
def douyinUserMix():
    usefuldict = {}
    if request.method == "POST":
        result = request.form
    else:
        usefuldict["status_code"] = 500
        return jsonify(usefuldict)

    try:
        usefuldict = work2(result["share_link"], result["cursor"], "mix", result["cookie"])
        usefuldict["status_code"] = 200
    except Exception as error:
        usefuldict["status_code"] = 500
    return jsonify(usefuldict)

@app.route("/douyin/user/like", methods=["POST"])
def douyinUserLike():
    usefuldict = {}
    if request.method == "POST":
        result = request.form
    else:
        usefuldict["status_code"] = 500
        return jsonify(usefuldict)

    try:
        usefuldict = work2(result["share_link"], result["cursor"], "like", result["cookie"])
        usefuldict["status_code"] = 200
    except Exception as error:
        usefuldict["status_code"] = 500
    return jsonify(usefuldict)

@app.route("/douyin/user/post", methods=["POST"])
def douyinUserPost():
    usefuldict = {}
    if request.method == "POST":
        result = request.form
    else:
        usefuldict["status_code"] = 500
        return jsonify(usefuldict)

    try:
        usefuldict = work2(result["share_link"], result["cursor"], "post", result["cookie"])
        usefuldict["status_code"] = 200
    except Exception as error:
        usefuldict["status_code"] = 500
    return jsonify(usefuldict)

@app.route("/douyin", methods=["POST"])
def douyin():
    usefuldict = {}
    if request.method == "POST":
        result = request.form
        print(result)
    else:
        usefuldict["status_code"] = 500
        return jsonify(usefuldict)

    try:
        usefuldict = work(result["share_link"])
        usefuldict["status_code"] = 200
    except Exception as error:
        usefuldict["status_code"] = 500
    return jsonify(usefuldict)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    args = argument()
    app.run(debug=False, host="0.0.0.0", port=args.port)
