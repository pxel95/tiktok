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


def work(share_link, max_cursor, mode, cookie):
    tk = TikTok()

    if cookie is not None and cookie != "":
        tk.headers["Cookie"] = cookie

    url = tk.getShareLink(share_link)
    key_type, key = tk.getKey(url)

    datalist = None
    rawdatalist = None
    cursor = None
    has_more = None
    if key_type == "user":
        if mode == 'post' or mode == 'like':
            datalist, rawdatalist, cursor, has_more = tk.getUserInfoApi(sec_uid=key, mode=mode, count=35,
                                                                        max_cursor=max_cursor)
        elif mode == 'mix':
            datalist, rawdatalist, cursor, has_more = tk.getUserAllMixInfoApi(sec_uid=key, count=35, cursor=max_cursor)
    elif key_type == "mix":
        datalist, rawdatalist, cursor, has_more = tk.getMixInfoApi(mix_id=key, count=35, cursor=max_cursor)
    elif key_type == "music":
        datalist, rawdatalist, cursor, has_more = tk.getMusicInfoApi(music_id=key, count=35, cursor=max_cursor)
    elif key_type == "aweme":
        datalist, rawdatalist = tk.getAwemeInfoApi(aweme_id=key)
    elif key_type == "live":
        datalist, rawdatalist = tk.getLiveInfoApi(web_rid=key)

    datadict = {}

    if datalist is not None and datalist != []:
        datadict["data"] = datalist
        datadict["rawdata"] = rawdatalist
        datadict["cursor"] = cursor
        datadict["has_more"] = has_more
        datadict["status_code"] = 200
    else:
        datadict["status_code"] = 500
    return datadict


def deal(mode=None):
    usefuldict = {}
    if request.headers.get("content_type") == "application/json":
        result = request.get_json(force=True)
    else:
        result = request.form

    share_link = None
    cursor = 0
    cookie = None

    try:
        share_link = result["share_link"]
        cursor = result["cursor"]
        cookie = result["cookie"]
    except Exception as e:
        usefuldict["status_code"] = 500

    try:
        if share_link is not None and share_link != "":
            usefuldict = work(share_link, cursor, mode, cookie)
            usefuldict["status_code"] = 200
    except Exception as e:
        usefuldict["status_code"] = 500
    return jsonify(usefuldict)


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
    return deal()


@app.route("/douyin/mix", methods=["POST"])
def douyinMix():
    return deal()


@app.route("/douyin/user/mix", methods=["POST"])
def douyinUserMix():
    return deal(mode="mix")


@app.route("/douyin/user/like", methods=["POST"])
def douyinUserLike():
    return deal(mode="like")


@app.route("/douyin/user/post", methods=["POST"])
def douyinUserPost():
    return deal(mode="post")


@app.route("/douyin/aweme", methods=["POST"])
def douyinAweme():
    return deal()


@app.route("/douyin/live", methods=["POST"])
def douyinLive():
    return deal()


@app.route("/douyin", methods=["POST"])
def douyin():
    return deal()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    args = argument()
    app.run(debug=False, host="0.0.0.0", port=args.port)
