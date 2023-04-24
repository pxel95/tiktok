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
Change Log  : 2023/02/11 修改接口
-------------------------------------------------
'''

import re
import requests
import json
import time
import os
import copy
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
# rich 进度条
# from functools import partial
# from urllib.request import urlopen
# import signal
# from threading import Event
# from rich.progress import (
#     BarColumn,
#     DownloadColumn,
#     Progress,
#     TaskID,
#     TextColumn,
#     TimeRemainingColumn,
#     TransferSpeedColumn
# )

from TikTokUtils import Utils
from TikTokUrls import Urls
from TikTokResult import Result
from TikTokDataBase import db


class TikTok(object):

    def __init__(self):
        self.urls = Urls()
        self.utils = Utils()
        self.result = Result()
        self.db = db()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'referer': 'https://www.douyin.com/',
            'accept-encoding': None,
            'Cookie': f"msToken={self.utils.generate_random_str(107)}; ttwid={self.utils.getttwid()}; odin_tt=324fb4ea4a89c0c05827e18a1ed9cf9bf8a17f7705fcc793fec935b637867e2a5a9b8168c885554d029919117a18ba69; passport_csrf_token=f61602fc63757ae0e4fd9d6bdcee4810;"
        }
        # 用于设置重复请求某个接口的最大时间
        self.timeout = 10

        # rich 进度条
        # self.progress = Progress(
        #     TextColumn("[bold blue]{task.fields[filename]}", justify="left"),
        #     BarColumn(bar_width=20),
        #     "[progress.percentage]{task.percentage:>3.1f}%",
        #     "•",
        #     DownloadColumn(),
        #     "•",
        #     TransferSpeedColumn(),
        #     "•",
        #     TimeRemainingColumn(),
        # )
        # self.done_event = Event()
        # signal.signal(signal.SIGINT, self.handle_sigint)

    # 从分享链接中提取网址
    def getShareLink(self, string):
        # findall() 查找匹配正则表达式的字符串
        return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)[0]

    # 得到 作品id 或者 用户id
    # 传入 url 支持 https://www.iesdouyin.com 与 https://v.douyin.com
    def getKey(self, url):
        key = None
        key_type = None

        try:
            r = requests.get(url=url, headers=self.headers)
        except Exception as e:
            print('[  错误  ]:输入链接有误！\r')
            return key_type, key

        # 抖音把图集更新为note
        # 作品 第一步解析出来的链接是share/video/{aweme_id}
        # https://www.iesdouyin.com/share/video/7037827546599263488/?region=CN&mid=6939809470193126152&u_code=j8a5173b&did=MS4wLjABAAAA1DICF9-A9M_CiGqAJZdsnig5TInVeIyPdc2QQdGrq58xUgD2w6BqCHovtqdIDs2i&iid=MS4wLjABAAAAomGWi4n2T0H9Ab9x96cUZoJXaILk4qXOJlJMZFiK6b_aJbuHkjN_f0mBzfy91DX1&with_sec_did=1&titleType=title&schema_type=37&from_ssr=1&utm_source=copy&utm_campaign=client_share&utm_medium=android&app=aweme
        # 用户 第一步解析出来的链接是share/user/{sec_uid}
        # https://www.iesdouyin.com/share/user/MS4wLjABAAAA06y3Ctu8QmuefqvUSU7vr0c_ZQnCqB0eaglgkelLTek?did=MS4wLjABAAAA1DICF9-A9M_CiGqAJZdsnig5TInVeIyPdc2QQdGrq58xUgD2w6BqCHovtqdIDs2i&iid=MS4wLjABAAAAomGWi4n2T0H9Ab9x96cUZoJXaILk4qXOJlJMZFiK6b_aJbuHkjN_f0mBzfy91DX1&with_sec_did=1&sec_uid=MS4wLjABAAAA06y3Ctu8QmuefqvUSU7vr0c_ZQnCqB0eaglgkelLTek&from_ssr=1&u_code=j8a5173b&timestamp=1674540164&ecom_share_track_params=%7B%22is_ec_shopping%22%3A%221%22%2C%22secuid%22%3A%22MS4wLjABAAAA-jD2lukp--I21BF8VQsmYUqJDbj3FmU-kGQTHl2y1Cw%22%2C%22enter_from%22%3A%22others_homepage%22%2C%22share_previous_page%22%3A%22others_homepage%22%7D&utm_source=copy&utm_campaign=client_share&utm_medium=android&app=aweme
        # 合集
        # https://www.douyin.com/collection/7093490319085307918
        urlstr = str(r.request.path_url)

        if "/user/" in urlstr:
            # 获取用户 sec_uid
            if '?' in r.request.path_url:
                for one in re.finditer(r'user\/([\d\D]*)([?])', str(r.request.path_url)):
                    key = one.group(1)
            else:
                for one in re.finditer(r'user\/([\d\D]*)', str(r.request.path_url)):
                    key = one.group(1)
            key_type = "user"
        elif "/video/" in urlstr:
            # 获取作品 aweme_id
            key = re.findall('video/(\d+)?', urlstr)[0]
            key_type = "aweme"
        elif "/note/" in urlstr:
            # 获取note aweme_id
            key = re.findall('note/(\d+)?', urlstr)[0]
            key_type = "aweme"
        elif "/mix/detail/" in urlstr:
            # 获取合集 id
            key = re.findall('/mix/detail/(\d+)?', urlstr)[0]
            key_type = "mix"
        elif "/collection/" in urlstr:
            # 获取合集 id
            key = re.findall('/collection/(\d+)?', urlstr)[0]
            key_type = "mix"
        elif "/music/" in urlstr:
            # 获取原声 id
            key = re.findall('music/(\d+)?', urlstr)[0]
            key_type = "music"
        elif "/webcast/reflow/" in urlstr:
            key1 = re.findall('reflow/(\d+)?', urlstr)[0]
            url = self.urls.LIVE2 + self.utils.getXbogus(
                f'live_id=1&room_id={key1}&app_id=1128')
            res = requests.get(url, headers=self.headers)
            resjson = json.loads(res.text)
            key = resjson['data']['room']['owner']['web_rid']
            key_type = "live"
        elif "live.douyin.com" in r.url:
            key = r.url.replace('https://live.douyin.com/', '')
            key_type = "live"

        if key is None or key_type is None:
            print('[  错误  ]:输入链接有误！无法获取 id\r')
            return key_type, key

        return key_type, key

    def getAwemeInfoApi(self, aweme_id):
        if aweme_id is None:
            return None
        start = time.time()  # 开始时间
        while True:
            try:
                jx_url = self.urls.POST_DETAIL + self.utils.getXbogus(
                    url=f'aweme_id={aweme_id}&device_platform=webapp&aid=6383')

                raw = requests.get(url=jx_url, headers=self.headers).text
                datadict = json.loads(raw)
                if datadict is not None and datadict["status_code"] == 0:
                    break
            except Exception as e:
                end = time.time()  # 结束时间
                if end - start > self.timeout:
                    return None

        # 清空self.awemeDict
        self.result.clearDict(self.result.awemeDict)

        # 默认为视频
        awemeType = 0
        try:
            if datadict['aweme_detail']["images"] is not None:
                awemeType = 1
        except Exception as e:
            pass

        # 转换成我们自己的格式
        self.result.dataConvert(awemeType, self.result.awemeDict, datadict['aweme_detail'])

        return self.result.awemeDict, datadict

    # 传入 aweme_id
    # 返回 数据 字典
    def getAwemeInfo(self, aweme_id):
        print('[  提示  ]:正在请求的作品 id = %s\r' % aweme_id)
        if aweme_id is None:
            return None

        start = time.time()  # 开始时间
        while True:
            # 接口不稳定, 有时服务器不返回数据, 需要重新获取
            try:
                # 单作品接口返回 'aweme_detail'
                # 主页作品接口返回 'aweme_list'->['aweme_detail']
                jx_url = self.urls.POST_DETAIL + self.utils.getXbogus(
                    url=f'aweme_id={aweme_id}&device_platform=webapp&aid=6383')

                raw = requests.get(url=jx_url, headers=self.headers).text
                datadict = json.loads(raw)
                if datadict is not None and datadict["status_code"] == 0:
                    break
            except Exception as e:
                end = time.time()  # 结束时间
                if end - start > self.timeout:
                    # raise RuntimeError("重复请求该接口" + str(self.timeout) + "s, 仍然未获取到数据")
                    print("[  提示  ]:重复请求该接口" + str(self.timeout) + "s, 仍然未获取到数据")
                    return {}, {}
                # print("[  警告  ]:接口未返回数据, 正在重新请求!\r")

        # 清空self.awemeDict
        self.result.clearDict(self.result.awemeDict)

        # 默认为视频
        awemeType = 0
        try:
            # datadict['aweme_detail']["images"] 不为 None 说明是图集
            if datadict['aweme_detail']["images"] is not None:
                awemeType = 1
        except Exception as e:
            print("[  警告  ]:接口中未找到 images\r")

        # 转换成我们自己的格式
        self.result.dataConvert(awemeType, self.result.awemeDict, datadict['aweme_detail'])

        return self.result.awemeDict, datadict

    def getUserInfoApi(self, sec_uid, mode="post", count=35, max_cursor=0):
        if sec_uid is None:
            return None

        awemeList = []

        start = time.time()  # 开始时间
        while True:
            try:
                if mode == "post":
                    url = self.urls.USER_POST + self.utils.getXbogus(
                        url=f'sec_user_id={sec_uid}&count={count}&max_cursor={max_cursor}&device_platform=webapp&aid=6383')
                elif mode == "like":
                    url = self.urls.USER_FAVORITE_A + self.utils.getXbogus(
                        url=f'sec_user_id={sec_uid}&count={count}&max_cursor={max_cursor}&device_platform=webapp&aid=6383')
                else:
                    return None

                res = requests.get(url=url, headers=self.headers)
                datadict = json.loads(res.text)
                if datadict is not None and datadict["status_code"] == 0:
                    break
            except Exception as e:
                end = time.time()  # 结束时间
                if end - start > self.timeout:
                    return None

        for aweme in datadict["aweme_list"]:
            # 清空self.awemeDict
            self.result.clearDict(self.result.awemeDict)

            # 默认为视频
            awemeType = 0
            try:
                if aweme["images"] is not None:
                    awemeType = 1
            except Exception as e:
                pass

            # 转换成我们自己的格式
            self.result.dataConvert(awemeType, self.result.awemeDict, aweme)

            if self.result.awemeDict is not None and self.result.awemeDict != {}:
                awemeList.append(copy.deepcopy(self.result.awemeDict))

        return awemeList, datadict, datadict["max_cursor"], datadict["has_more"]

    # 传入 url 支持 https://www.iesdouyin.com 与 https://v.douyin.com
    # mode : post | like 模式选择 like为用户点赞 post为用户发布
    def getUserInfo(self, sec_uid, mode="post", count=35, number=0, increase=False):
        print('[  提示  ]:正在请求的用户 id = %s\r\n' % sec_uid)
        if sec_uid is None:
            return None
        if number <= 0:
            numflag = False
        else:
            numflag = True

        max_cursor = 0
        awemeList = []
        increaseflag = False
        numberis0 = False

        print("[  提示  ]:正在获取所有作品数据请稍后...\r")
        print("[  提示  ]:会进行多次请求，等待时间较长...\r\n")
        times = 0
        while True:
            times = times + 1
            print("[  提示  ]:正在对 [主页] 进行第 " + str(times) + " 次请求...\r")

            start = time.time()  # 开始时间
            while True:
                # 接口不稳定, 有时服务器不返回数据, 需要重新获取
                try:
                    if mode == "post":
                        url = self.urls.USER_POST + self.utils.getXbogus(
                            url=f'sec_user_id={sec_uid}&count={count}&max_cursor={max_cursor}&device_platform=webapp&aid=6383')
                    elif mode == "like":
                        url = self.urls.USER_FAVORITE_A + self.utils.getXbogus(
                            url=f'sec_user_id={sec_uid}&count={count}&max_cursor={max_cursor}&device_platform=webapp&aid=6383')
                    else:
                        print("[  错误  ]:模式选择错误, 仅支持post、like、mix, 请检查后重新运行!\r")
                        return None

                    res = requests.get(url=url, headers=self.headers)
                    datadict = json.loads(res.text)
                    print('[  提示  ]:本次请求返回 ' + str(len(datadict["aweme_list"])) + ' 条数据\r')
                    # print('[  提示  ]:开始对 ' + str(len(datadict["aweme_list"])) + ' 条数据请求作品详情\r\n')
                    if datadict is not None and datadict["status_code"] == 0:
                        break
                except Exception as e:
                    end = time.time()  # 结束时间
                    if end - start > self.timeout:
                        # raise RuntimeError("重复请求该接口" + str(self.timeout) + "s, 仍然未获取到数据")
                        print("[  提示  ]:重复请求该接口" + str(self.timeout) + "s, 仍然未获取到数据")
                        return awemeList
                    # print("[  警告  ]:接口未返回数据, 正在重新请求!\r")

            for aweme in datadict["aweme_list"]:
                # 退出条件
                if increase is False and numflag and numberis0:
                    break
                if increase and numflag and numberis0 and increaseflag:
                    break
                # 增量更新, 找到非置顶的最新的作品发布时间
                if mode == "post":
                    if self.db.get_user_post(sec_uid=sec_uid, aweme_id=aweme['aweme_id']) is not None:
                        if increase and aweme['is_top'] == 0:
                            increaseflag = True
                    else:
                        self.db.insert_user_post(sec_uid=sec_uid, aweme_id=aweme['aweme_id'], data=aweme)
                elif mode == "like":
                    if self.db.get_user_like(sec_uid=sec_uid, aweme_id=aweme['aweme_id']) is not None:
                        if increase and aweme['is_top'] == 0:
                            increaseflag = True
                    else:
                        self.db.insert_user_like(sec_uid=sec_uid, aweme_id=aweme['aweme_id'], data=aweme)

                # 退出条件
                if increase and numflag is False and increaseflag:
                    break
                if increase and numflag and numberis0 and increaseflag:
                    break

                if numflag:
                    number -= 1
                    if number == 0:
                        numberis0 = True
                # 获取 aweme_id
                # aweme_id = aweme["aweme_id"]
                # 深拷贝 dict 不然list里面全是同样的数据
                # datanew, dataraw = self.getAwemeInfo(aweme_id)

                # 清空self.awemeDict
                self.result.clearDict(self.result.awemeDict)

                # 默认为视频
                awemeType = 0
                try:
                    if aweme["images"] is not None:
                        awemeType = 1
                except Exception as e:
                    print("[  警告  ]:接口中未找到 images\r")

                # 转换成我们自己的格式
                self.result.dataConvert(awemeType, self.result.awemeDict, aweme)

                if self.result.awemeDict is not None and self.result.awemeDict != {}:
                    awemeList.append(copy.deepcopy(self.result.awemeDict))

            if increase and numflag is False and increaseflag:
                print("\r\n[  提示  ]: [主页] 下作品增量更新数据获取完成...\r\n")
                break
            elif increase is False and numflag and numberis0:
                print("\r\n[  提示  ]: [主页] 下指定数量作品数据获取完成...\r\n")
                break
            elif increase and numflag and numberis0 and increaseflag:
                print("\r\n[  提示  ]: [主页] 下指定数量作品数据获取完成, 增量更新数据获取完成...\r\n")
                break

            # 更新 max_cursor
            max_cursor = datadict["max_cursor"]

            # 退出条件
            if datadict["has_more"] == 0 or datadict["has_more"] == False:
                print("\r\n[  提示  ]: [主页] 下所有作品数据获取完成...\r\n")
                break
            else:
                print("\r\n[  提示  ]:[主页] 第 " + str(times) + " 次请求成功...\r\n")

        return awemeList

    def getLiveInfoApi(self, web_rid: str):
        start = time.time()  # 开始时间
        while True:
            try:
                live_api = self.urls.LIVE + self.utils.getXbogus(
                    url=f'aid=6383&device_platform=web&web_rid={web_rid}')

                response = requests.get(live_api, headers=self.headers)
                live_json = json.loads(response.text)
                if live_json != {} and live_json['status_code'] == 0:
                    break
            except Exception as e:
                end = time.time()  # 结束时间
                if end - start > self.timeout:
                    return None

        # 清空字典
        self.result.clearDict(self.result.liveDict)

        # 类型
        self.result.liveDict["awemeType"] = 2
        # 是否在播
        self.result.liveDict["status"] = live_json['data']['data'][0]['status']

        if self.result.liveDict["status"] == 4:
            return self.result.liveDict, live_json

        # 直播标题
        self.result.liveDict["title"] = live_json['data']['data'][0]['title']

        # 直播cover
        self.result.liveDict["cover"] = live_json['data']['data'][0]['cover']['url_list'][0]

        # 头像
        self.result.liveDict["avatar"] = live_json['data']['data'][0]['owner']['avatar_thumb']['url_list'][0].replace(
            "100x100", "1080x1080")

        # 观看人数
        self.result.liveDict["user_count"] = live_json['data']['data'][0]['user_count_str']

        # 昵称
        self.result.liveDict["nickname"] = live_json['data']['data'][0]['owner']['nickname']

        # sec_uid
        self.result.liveDict["sec_uid"] = live_json['data']['data'][0]['owner']['sec_uid']

        # 直播间观看状态
        self.result.liveDict["display_long"] = live_json['data']['data'][0]['room_view_stats']['display_long']

        # 推流
        self.result.liveDict["flv_pull_url"] = live_json['data']['data'][0]['stream_url']['flv_pull_url']

        try:
            # 分区
            self.result.liveDict["partition"] = live_json['data']['partition_road_map']['partition']['title']
            self.result.liveDict["sub_partition"] = \
                live_json['data']['partition_road_map']['sub_partition']['partition']['title']
        except Exception as e:
            self.result.liveDict["partition"] = '无'
            self.result.liveDict["sub_partition"] = '无'

        flv = []

        for i, f in enumerate(self.result.liveDict["flv_pull_url"].keys()):
            flv.append(f)

        self.result.liveDict["flv_pull_url0"] = self.result.liveDict["flv_pull_url"][flv[0]]

        return self.result.liveDict, live_json

    def getLiveInfo(self, web_rid: str):
        print('[  提示  ]:正在请求的直播间 id = %s\r\n' % web_rid)

        # web_rid = live_url.replace('https://live.douyin.com/', '')

        start = time.time()  # 开始时间
        while True:
            # 接口不稳定, 有时服务器不返回数据, 需要重新获取
            try:
                live_api = self.urls.LIVE + self.utils.getXbogus(
                    url=f'aid=6383&device_platform=web&web_rid={web_rid}')

                response = requests.get(live_api, headers=self.headers)
                live_json = json.loads(response.text)
                if live_json != {} and live_json['status_code'] == 0:
                    break
            except Exception as e:
                end = time.time()  # 结束时间
                if end - start > self.timeout:
                    # raise RuntimeError("重复请求该接口" + str(self.timeout) + "s, 仍然未获取到数据")
                    print("[  提示  ]:重复请求该接口" + str(self.timeout) + "s, 仍然未获取到数据")
                    return {}

        # 清空字典
        self.result.clearDict(self.result.liveDict)

        # 类型
        self.result.liveDict["awemeType"] = 2
        # 是否在播
        self.result.liveDict["status"] = live_json['data']['data'][0]['status']

        if self.result.liveDict["status"] == 4:
            print('[   📺   ]:当前直播已结束，正在退出')
            return self.result.liveDict

        # 直播标题
        self.result.liveDict["title"] = live_json['data']['data'][0]['title']

        # 直播cover
        self.result.liveDict["cover"] = live_json['data']['data'][0]['cover']['url_list'][0]

        # 头像
        self.result.liveDict["avatar"] = live_json['data']['data'][0]['owner']['avatar_thumb']['url_list'][0].replace(
            "100x100", "1080x1080")

        # 观看人数
        self.result.liveDict["user_count"] = live_json['data']['data'][0]['user_count_str']

        # 昵称
        self.result.liveDict["nickname"] = live_json['data']['data'][0]['owner']['nickname']

        # sec_uid
        self.result.liveDict["sec_uid"] = live_json['data']['data'][0]['owner']['sec_uid']

        # 直播间观看状态
        self.result.liveDict["display_long"] = live_json['data']['data'][0]['room_view_stats']['display_long']

        # 推流
        self.result.liveDict["flv_pull_url"] = live_json['data']['data'][0]['stream_url']['flv_pull_url']

        try:
            # 分区
            self.result.liveDict["partition"] = live_json['data']['partition_road_map']['partition']['title']
            self.result.liveDict["sub_partition"] = \
                live_json['data']['partition_road_map']['sub_partition']['partition']['title']
        except Exception as e:
            self.result.liveDict["partition"] = '无'
            self.result.liveDict["sub_partition"] = '无'

        info = '[   💻   ]:直播间：%s  当前%s  主播：%s 分区：%s-%s\r' % (
            self.result.liveDict["title"], self.result.liveDict["display_long"], self.result.liveDict["nickname"],
            self.result.liveDict["partition"], self.result.liveDict["sub_partition"])
        print(info)

        flv = []
        print('[   🎦   ]:直播间清晰度')
        for i, f in enumerate(self.result.liveDict["flv_pull_url"].keys()):
            print('[   %s   ]: %s' % (i, f))
            flv.append(f)

        rate = int(input('[   🎬   ]输入数字选择推流清晰度：'))

        self.result.liveDict["flv_pull_url0"] = self.result.liveDict["flv_pull_url"][flv[rate]]

        # 显示清晰度列表
        print('[   %s   ]:%s' % (flv[rate], self.result.liveDict["flv_pull_url"][flv[rate]]))
        print('[   📺   ]:复制链接使用下载工具下载')
        return self.result.liveDict

    def getMixInfoApi(self, mix_id: str, count=35, cursor=0):
        if mix_id is None:
            return None

        awemeList = []

        start = time.time()  # 开始时间
        while True:
            try:
                url = self.urls.USER_MIX + self.utils.getXbogus(
                    url=f'mix_id={mix_id}&cursor={cursor}&count={count}&device_platform=webapp&aid=6383')

                res = requests.get(url=url, headers=self.headers)
                datadict = json.loads(res.text)
                if datadict is not None:
                    break
            except Exception as e:
                end = time.time()  # 结束时间
                if end - start > self.timeout:
                    return None

        for aweme in datadict["aweme_list"]:

            # 清空self.awemeDict
            self.result.clearDict(self.result.awemeDict)

            # 默认为视频
            awemeType = 0
            try:
                if aweme["images"] is not None:
                    awemeType = 1
            except Exception as e:
                pass

            # 转换成我们自己的格式
            self.result.dataConvert(awemeType, self.result.awemeDict, aweme)

            if self.result.awemeDict is not None and self.result.awemeDict != {}:
                awemeList.append(copy.deepcopy(self.result.awemeDict))

        return awemeList, datadict, datadict["cursor"], datadict["has_more"]

    def getMixInfo(self, mix_id: str, count=35, number=0, increase=False, sec_uid=''):
        print('[  提示  ]:正在请求的合集 id = %s\r\n' % mix_id)
        if mix_id is None:
            return None
        if number <= 0:
            numflag = False
        else:
            numflag = True

        cursor = 0
        awemeList = []
        increaseflag = False
        numberis0 = False

        print("[  提示  ]:正在获取合集下的所有作品数据请稍后...\r")
        print("[  提示  ]:会进行多次请求，等待时间较长...\r\n")
        times = 0
        while True:
            times = times + 1
            print("[  提示  ]:正在对 [合集] 进行第 " + str(times) + " 次请求...\r")

            start = time.time()  # 开始时间
            while True:
                # 接口不稳定, 有时服务器不返回数据, 需要重新获取
                try:
                    url = self.urls.USER_MIX + self.utils.getXbogus(
                        url=f'mix_id={mix_id}&cursor={cursor}&count={count}&device_platform=webapp&aid=6383')

                    res = requests.get(url=url, headers=self.headers)
                    datadict = json.loads(res.text)
                    print('[  提示  ]:本次请求返回 ' + str(len(datadict["aweme_list"])) + ' 条数据\r')
                    # print('[  提示  ]:开始对 ' + str(len(datadict["aweme_list"])) + ' 条数据请求作品详情\r\n')
                    if datadict is not None:
                        break
                except Exception as e:
                    end = time.time()  # 结束时间
                    if end - start > self.timeout:
                        # raise RuntimeError("重复请求该接口" + str(self.timeout) + "s, 仍然未获取到数据")
                        print("[  提示  ]:重复请求该接口" + str(self.timeout) + "s, 仍然未获取到数据")
                        return awemeList
                    # print("[  警告  ]:接口未返回数据, 正在重新请求!\r")

            for aweme in datadict["aweme_list"]:
                # 退出条件
                if increase is False and numflag and numberis0:
                    break
                if increase and numflag and numberis0 and increaseflag:
                    break
                # 增量更新, 找到非置顶的最新的作品发布时间
                if self.db.get_mix(sec_uid=sec_uid, mix_id=mix_id, aweme_id=aweme['aweme_id']) is not None:
                    if increase and aweme['is_top'] == 0:
                        increaseflag = True
                else:
                    self.db.insert_mix(sec_uid=sec_uid, mix_id=mix_id, aweme_id=aweme['aweme_id'], data=aweme)

                # 退出条件
                if increase and numflag is False and increaseflag:
                    break
                if increase and numflag and numberis0 and increaseflag:
                    break

                if numflag:
                    number -= 1
                    if number == 0:
                        numberis0 = True
                # 获取 aweme_id
                # aweme_id = aweme["aweme_id"]
                # 深拷贝 dict 不然list里面全是同样的数据
                # datanew, dataraw = self.getAwemeInfo(aweme_id)

                # 清空self.awemeDict
                self.result.clearDict(self.result.awemeDict)

                # 默认为视频
                awemeType = 0
                try:
                    if aweme["images"] is not None:
                        awemeType = 1
                except Exception as e:
                    print("[  警告  ]:接口中未找到 images\r")

                # 转换成我们自己的格式
                self.result.dataConvert(awemeType, self.result.awemeDict, aweme)

                if self.result.awemeDict is not None and self.result.awemeDict != {}:
                    awemeList.append(copy.deepcopy(self.result.awemeDict))

            if increase and numflag is False and increaseflag:
                print("\r\n[  提示  ]: [合集] 下作品增量更新数据获取完成...\r\n")
                break
            elif increase is False and numflag and numberis0:
                print("\r\n[  提示  ]: [合集] 下指定数量作品数据获取完成...\r\n")
                break
            elif increase and numflag and numberis0 and increaseflag:
                print("\r\n[  提示  ]: [合集] 下指定数量作品数据获取完成, 增量更新数据获取完成...\r\n")
                break

            # 更新 max_cursor
            cursor = datadict["cursor"]

            # 退出条件
            if datadict["has_more"] == 0 or datadict["has_more"] == False:
                print("\r\n[  提示  ]:[合集] 下所有作品数据获取完成...\r\n")
                break
            else:
                print("\r\n[  提示  ]:[合集] 第 " + str(times) + " 次请求成功...\r\n")

        return awemeList

    def getUserAllMixInfoApi(self, sec_uid, count=35, cursor=0):

        if sec_uid is None:
            return None

        mixIdlist = []

        start = time.time()  # 开始时间
        while True:
            try:
                url = self.urls.USER_MIX_LIST + self.utils.getXbogus(
                    url=f'sec_user_id={sec_uid}&count={count}&cursor={cursor}&device_platform=webapp&aid=6383')

                res = requests.get(url=url, headers=self.headers)
                datadict = json.loads(res.text)
                if datadict is not None and datadict["status_code"] == 0:
                    break
            except Exception as e:
                end = time.time()  # 结束时间
                if end - start > self.timeout:
                    return None

        for mix in datadict["mix_infos"]:
            mixIdNameDict = {}
            mixIdNameDict["https://www.douyin.com/collection/" + mix["mix_id"]] = mix["mix_name"]
            mixIdlist.append(mixIdNameDict)

        return mixIdlist, datadict, datadict["cursor"], datadict["has_more"]

    def getUserAllMixInfo(self, sec_uid, count=35, number=0):
        print('[  提示  ]:正在请求的用户 id = %s\r\n' % sec_uid)
        if sec_uid is None:
            return None
        if number <= 0:
            numflag = False
        else:
            numflag = True

        cursor = 0
        mixIdNameDict = {}

        print("[  提示  ]:正在获取主页下所有合集 id 数据请稍后...\r")
        print("[  提示  ]:会进行多次请求，等待时间较长...\r\n")
        times = 0
        while True:
            times = times + 1
            print("[  提示  ]:正在对 [合集列表] 进行第 " + str(times) + " 次请求...\r")

            start = time.time()  # 开始时间
            while True:
                # 接口不稳定, 有时服务器不返回数据, 需要重新获取
                try:
                    url = self.urls.USER_MIX_LIST + self.utils.getXbogus(
                        url=f'sec_user_id={sec_uid}&count={count}&cursor={cursor}&device_platform=webapp&aid=6383')

                    res = requests.get(url=url, headers=self.headers)
                    datadict = json.loads(res.text)
                    print('[  提示  ]:本次请求返回 ' + str(len(datadict["mix_infos"])) + ' 条数据\r')
                    # print('[  提示  ]:开始对 ' + str(len(datadict["mix_infos"])) + ' 条数据请求作品详情\r\n')
                    if datadict is not None and datadict["status_code"] == 0:
                        break
                except Exception as e:
                    end = time.time()  # 结束时间
                    if end - start > self.timeout:
                        # raise RuntimeError("重复请求该接口" + str(self.timeout) + "s, 仍然未获取到数据")
                        print("[  提示  ]:重复请求该接口" + str(self.timeout) + "s, 仍然未获取到数据")
                        return mixIdNameDict
                    # print("[  警告  ]:接口未返回数据, 正在重新请求!\r")

            for mix in datadict["mix_infos"]:
                mixIdNameDict[mix["mix_id"]] = mix["mix_name"]
                if numflag:
                    number -= 1
                    if number == 0:
                        break
            if numflag and number == 0:
                print("\r\n[  提示  ]:[合集列表] 下指定数量合集数据获取完成...\r\n")
                break

            # 更新 max_cursor
            cursor = datadict["cursor"]

            # 退出条件
            if datadict["has_more"] == 0 or datadict["has_more"] == False:
                print("[  提示  ]:[合集列表] 下所有合集 id 数据获取完成...\r\n")
                break
            else:
                print("\r\n[  提示  ]:[合集列表] 第 " + str(times) + " 次请求成功...\r\n")

        return mixIdNameDict

    def getMusicInfoApi(self, music_id: str, count=35, cursor=0):
        if music_id is None:
            return None

        awemeList = []

        start = time.time()  # 开始时间
        while True:
            try:
                url = self.urls.MUSIC + self.utils.getXbogus(
                    url=f'music_id={music_id}&cursor={cursor}&count={count}&device_platform=webapp&aid=6383')

                res = requests.get(url=url, headers=self.headers)
                datadict = json.loads(res.text)
                if datadict is not None and datadict["status_code"] == 0:
                    break
            except Exception as e:
                end = time.time()  # 结束时间
                if end - start > self.timeout:
                    return None

        for aweme in datadict["aweme_list"]:
            # 清空self.awemeDict
            self.result.clearDict(self.result.awemeDict)

            # 默认为视频
            awemeType = 0
            try:
                if aweme["images"] is not None:
                    awemeType = 1
            except Exception as e:
                pass

            # 转换成我们自己的格式
            self.result.dataConvert(awemeType, self.result.awemeDict, aweme)

            if self.result.awemeDict is not None and self.result.awemeDict != {}:
                awemeList.append(copy.deepcopy(self.result.awemeDict))

        return awemeList, datadict, datadict["cursor"], datadict["has_more"]

    def getMusicInfo(self, music_id: str, count=35, number=0, increase=False):
        print('[  提示  ]:正在请求的音乐集合 id = %s\r\n' % music_id)
        if music_id is None:
            return None
        if number <= 0:
            numflag = False
        else:
            numflag = True

        cursor = 0
        awemeList = []
        increaseflag = False
        numberis0 = False

        print("[  提示  ]:正在获取音乐集合下的所有作品数据请稍后...\r")
        print("[  提示  ]:会进行多次请求，等待时间较长...\r\n")
        times = 0
        while True:
            times = times + 1
            print("[  提示  ]:正在对 [音乐集合] 进行第 " + str(times) + " 次请求...\r")

            start = time.time()  # 开始时间
            while True:
                # 接口不稳定, 有时服务器不返回数据, 需要重新获取
                try:
                    url = self.urls.MUSIC + self.utils.getXbogus(
                        url=f'music_id={music_id}&cursor={cursor}&count={count}&device_platform=webapp&aid=6383')

                    res = requests.get(url=url, headers=self.headers)
                    datadict = json.loads(res.text)
                    print('[  提示  ]:本次请求返回 ' + str(len(datadict["aweme_list"])) + ' 条数据\r')
                    # print('[  提示  ]:开始对 ' + str(len(datadict["aweme_list"])) + ' 条数据请求作品详情\r\n')
                    if datadict is not None and datadict["status_code"] == 0:
                        break
                except Exception as e:
                    end = time.time()  # 结束时间
                    if end - start > self.timeout:
                        # raise RuntimeError("重复请求该接口" + str(self.timeout) + "s, 仍然未获取到数据")
                        print("[  提示  ]:重复请求该接口" + str(self.timeout) + "s, 仍然未获取到数据")
                        return awemeList
                    # print("[  警告  ]:接口未返回数据, 正在重新请求!\r")

            for aweme in datadict["aweme_list"]:
                if increase is False and numflag and numberis0:
                    break
                if increase and numflag and numberis0 and increaseflag:
                    break
                # 增量更新, 找到非置顶的最新的作品发布时间
                if self.db.get_music(music_id=music_id, aweme_id=aweme['aweme_id']) is not None:
                    if increase and aweme['is_top'] == 0:
                        increaseflag = True
                else:
                    self.db.insert_music(music_id=music_id, aweme_id=aweme['aweme_id'], data=aweme)

                # 退出条件
                if increase and numflag is False and increaseflag:
                    break
                if increase and numflag and numberis0 and increaseflag:
                    break

                if numflag:
                    number -= 1
                    if number == 0:
                        numberis0 = True
                # 获取 aweme_id
                # aweme_id = aweme["aweme_id"]
                # 深拷贝 dict 不然list里面全是同样的数据
                # datanew, dataraw = self.getAwemeInfo(aweme_id)

                # 清空self.awemeDict
                self.result.clearDict(self.result.awemeDict)

                # 默认为视频
                awemeType = 0
                try:
                    if aweme["images"] is not None:
                        awemeType = 1
                except Exception as e:
                    print("[  警告  ]:接口中未找到 images\r")

                # 转换成我们自己的格式
                self.result.dataConvert(awemeType, self.result.awemeDict, aweme)

                if self.result.awemeDict is not None and self.result.awemeDict != {}:
                    awemeList.append(copy.deepcopy(self.result.awemeDict))

            if increase and numflag is False and increaseflag:
                print("\r\n[  提示  ]: [音乐集合] 下作品增量更新数据获取完成...\r\n")
                break
            elif increase is False and numflag and numberis0:
                print("\r\n[  提示  ]: [音乐集合] 下指定数量作品数据获取完成...\r\n")
                break
            elif increase and numflag and numberis0 and increaseflag:
                print("\r\n[  提示  ]: [音乐集合] 下指定数量作品数据获取完成, 增量更新数据获取完成...\r\n")
                break

            # 更新 cursor
            cursor = datadict["cursor"]

            # 退出条件
            if datadict["has_more"] == 0 or datadict["has_more"] == False:
                print("\r\n[  提示  ]:[音乐集合] 下所有作品数据获取完成...\r\n")
                break
            else:
                print("\r\n[  提示  ]:[音乐集合] 第 " + str(times) + " 次请求成功...\r\n")

        return awemeList

    # rich 进度条
    # https://github.com/textualize/rich/blob/master/examples/downloader.py
    # def handle_sigint(self, signum, frame):
    #     self.done_event.set()
    #
    # def copy_url(self, task_id: TaskID, url: str, path: str) -> None:
    #     """Copy data from a url to a local file."""
    #     # self.progress.console.log(f"Requesting {url}")
    #     response = urlopen(url)
    #     try:
    #         # This will break if the response doesn't contain content length
    #         self.progress.update(task_id, total=int(response.info()["Content-length"]))
    #         with open(path, "wb") as dest_file:
    #             self.progress.start_task(task_id)
    #             for data in iter(partial(response.read, 32768), b""):
    #                 dest_file.write(data)
    #                 self.progress.update(task_id, advance=len(data))
    #                 if self.done_event.is_set():
    #                     return
    #     except Exception as e:
    #         # 下载异常 删除原来下载的文件, 可能未下成功
    #         if os.path.exists(path):
    #             os.remove(path)
    #         print("[  错误  ]:下载出错\r")

    # 来自 https://blog.csdn.net/weixin_43347550/article/details/105248223
    def progressBarDownload(self, url, filepath, desc):
        response = requests.get(url, stream=True, headers=self.headers)
        chunk_size = 1024  # 每次下载的数据大小
        content_size = int(response.headers['content-length'])  # 下载文件总大小
        try:
            if response.status_code == 200:  # 判断是否响应成功
                # print('[开始下载]:文件大小:{size:.2f} MB'.format(
                #     size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小
                with open(filepath, 'wb') as file, tqdm(total=content_size,
                                                        unit="iB",
                                                        desc=desc,
                                                        unit_scale=True,
                                                        unit_divisor=1024,

                                                        ) as bar:  # 显示进度条
                    for data in response.iter_content(chunk_size=chunk_size):
                        size = file.write(data)
                        bar.update(size)
        except Exception as e:
            # 下载异常 删除原来下载的文件, 可能未下成功
            if os.path.exists(filepath):
                os.remove(filepath)
            print("[  错误  ]:下载出错\r")

    def awemeDownload(self, awemeDict: dict, music=True, cover=True, avatar=True, resjson=True, savePath=os.getcwd()):
        if awemeDict is None:
            return
        if not os.path.exists(savePath):
            os.mkdir(savePath)

        try:
            # 使用作品 创建时间+描述 当文件夹
            file_name = awemeDict["create_time"] + "_" + self.utils.replaceStr(awemeDict["desc"])
            aweme_path = os.path.join(savePath, file_name)
            if not os.path.exists(aweme_path):
                os.mkdir(aweme_path)

            # 保存获取到的字典信息
            # print("[  提示  ]:正在保存获取到的信息到 result.json\r\n")
            if resjson:
                try:
                    with open(os.path.join(aweme_path, "result.json"), "w", encoding='utf-8') as f:
                        f.write(json.dumps(awemeDict, ensure_ascii=False, indent=2))
                        f.close()
                except Exception as e:
                    print("[  错误  ]:保存 result.json 失败... 作品名: " + file_name + "\r\n")

            desc = file_name[:30]
            # 下载  视频
            if awemeDict["awemeType"] == 0:
                # print("[  提示  ]:正在下载视频...\r")
                video_path = os.path.join(aweme_path, file_name + ".mp4")

                if os.path.exists(video_path):
                    # print("[  提示  ]:视频已存在为您跳过...\r\n")
                    pass
                else:
                    try:
                        url = awemeDict["video"]["play_addr"]["url_list"][0]
                        if url != "":
                            self.isdwownload = False
                            # task_id = self.progress.add_task("download", filename="[ 视频 ]:" + desc, start=False)
                            # self.alltask.append(self.pool.submit(self.copy_url, task_id, url, video_path))
                            self.alltask.append(
                                self.pool.submit(self.progressBarDownload, url, video_path, "[ 视频 ]:" + desc))
                    except Exception as e:
                        print("[  警告  ]:视频下载失败,请重试... 作品名: " + file_name + "\r\n")

            # 下载 图集
            if awemeDict["awemeType"] == 1:
                # print("[  提示  ]:正在下载图集...\r")
                for ind, image in enumerate(awemeDict["images"]):
                    image_path = os.path.join(aweme_path, "image" + str(ind) + ".jpeg")
                    if os.path.exists(image_path):
                        # print("[  提示  ]:图片已存在为您跳过...\r\n")
                        pass
                    else:
                        try:
                            url = image["url_list"][0]
                            if url != "":
                                self.isdwownload = False
                                # task_id = self.progress.add_task("download", filename="[ 图集 ]:" + desc, start=False)
                                # self.alltask.append(self.pool.submit(self.copy_url, task_id, url, image_path))
                                self.alltask.append(
                                    self.pool.submit(self.progressBarDownload, url, image_path, "[ 图集 ]:" + desc))
                        except Exception as e:
                            print("[  警告  ]:图片下载失败,请重试... 作品名: " + file_name + "\r\n")

            # 下载  音乐
            if music:
                # print("[  提示  ]:正在下载音乐...\r")
                music_name = self.utils.replaceStr(awemeDict["music"]["title"])
                music_path = os.path.join(aweme_path, music_name + ".mp3")

                if os.path.exists(music_path):
                    # print("[  提示  ]:音乐已存在为您跳过...\r\n")
                    pass
                else:
                    try:
                        url = awemeDict["music"]["play_url"]["url_list"][0]
                        if url != "":
                            self.isdwownload = False
                            # task_id = self.progress.add_task("download", filename="[ 原声 ]:" + desc, start=False)
                            # self.alltask.append(self.pool.submit(self.copy_url, task_id, url, music_path))
                            self.alltask.append(
                                self.pool.submit(self.progressBarDownload, url, music_path, "[ 原声 ]:" + desc))
                    except Exception as e:
                        print("[  警告  ]:音乐(原声)下载失败,请重试... 作品名: " + file_name + "\r\n")

            # 下载  cover
            if cover and awemeDict["awemeType"] == 0:
                # print("[  提示  ]:正在下载视频cover图...\r")
                cover_path = os.path.join(aweme_path, "cover.jpeg")

                if os.path.exists(cover_path):
                    # print("[  提示  ]:cover 已存在为您跳过...\r\n")
                    pass
                else:
                    try:
                        url = awemeDict["video"]["cover"]["url_list"][0]
                        if url != "":
                            self.isdwownload = False
                            # task_id = self.progress.add_task("download", filename="[ 封面 ]:" + desc, start=False)
                            # self.alltask.append(self.pool.submit(self.copy_url, task_id, url, cover_path))
                            self.alltask.append(
                                self.pool.submit(self.progressBarDownload, url, cover_path, "[ 封面 ]:" + desc))
                    except Exception as e:
                        print("[  警告  ]:cover下载失败,请重试... 作品名: " + file_name + "\r\n")

            # 下载  avatar
            if avatar:
                # print("[  提示  ]:正在下载用户头像...\r")
                avatar_path = os.path.join(aweme_path, "avatar.jpeg")

                if os.path.exists(avatar_path):
                    # print("[  提示  ]:avatar 已存在为您跳过...\r\n")
                    pass
                else:
                    try:
                        url = awemeDict["author"]["avatar"]["url_list"][0]
                        if url != "":
                            self.isdwownload = False
                            # task_id = self.progress.add_task("download", filename="[ 头像 ]:" + desc, start=False)
                            # self.alltask.append(self.pool.submit(self.copy_url, task_id, url, avatar_path))
                            self.alltask.append(
                                self.pool.submit(self.progressBarDownload, url, avatar_path, "[ 头像 ]:" + desc))
                    except Exception as e:
                        print("[  警告  ]:avatar下载失败,请重试... 作品名: " + file_name + "\r\n")
        except Exception as e:
            print("[  错误  ]:下载作品时出错\r\n")

    # def userDownload(self, awemeList: list, music=True, cover=True, avatar=True, resjson=True, savePath=os.getcwd(), thread=5):
    #     if awemeList is None:
    #         return
    #     if not os.path.exists(savePath):
    #         os.mkdir(savePath)
    #
    #     self.alltask = []
    #
    #     start = time.time()  # 开始时间
    #
    #     # 分块下载
    #     for i in range(0, len(awemeList), thread):
    #         batchAwemeList = awemeList[i:i + thread]
    #
    #
    #     for awemeList2 in batchAwemeList:
    #         with self.progress:
    #             with ThreadPoolExecutor(max_workers=thread) as self.pool:
    #                 # self.progress.console.log("请耐心等待下载完成(终端尺寸越长显示的进度条越多)...")
    #                 for aweme in awemeList2:
    #                     self.awemeDownload(awemeDict=aweme, music=music, cover=cover, avatar=avatar, resjson=resjson, savePath=savePath)
    #                     # time.sleep(0.5)
    #         wait(self.alltask, return_when=ALL_COMPLETED)
    #         # self.alltask = []
    #         # 清除上一步的进度条
    #         # for taskid in self.progress.task_ids:
    #         #     self.progress.remove_task(taskid)
    #
    #     # 检查下载是否完成
    #     while True:
    #         self.isdwownload = True
    #         # 下载上一步失败的
    #         with self.progress:
    #             with ThreadPoolExecutor(max_workers=thread) as self.pool:
    #                 self.progress.console.log("正在检查下载是否完成...")
    #                 for aweme in awemeList:
    #                     self.awemeDownload(awemeDict=aweme, music=music, cover=cover, avatar=avatar, resjson=resjson, savePath=savePath)
    #                     # time.sleep(0.5)
    #         wait(self.alltask, return_when=ALL_COMPLETED)
    #         # self.alltask = []
    #         # 清除上一步的进度条
    #         # for taskid in self.progress.task_ids:
    #         #     self.progress.remove_task(taskid)
    #
    #         if self.isdwownload:
    #             break
    #
    #     end = time.time()  # 结束时间
    #     print('\n' + '[下载完成]:耗时: %d分钟%d秒\n' % (int((end - start) / 60), ((end - start) % 60)))  # 输出下载用时时间

    def userDownload(self, awemeList: list, music=True, cover=True, avatar=True, resjson=True, savePath=os.getcwd(),
                     thread=5):
        if awemeList is None:
            return
        if not os.path.exists(savePath):
            os.mkdir(savePath)

        self.alltask = []
        self.pool = ThreadPoolExecutor(max_workers=thread)

        start = time.time()  # 开始时间

        for aweme in awemeList:
            self.awemeDownload(awemeDict=aweme, music=music, cover=cover, avatar=avatar, resjson=resjson,
                               savePath=savePath)
            # time.sleep(0.5)
        wait(self.alltask, return_when=ALL_COMPLETED)

        # 检查下载是否完成
        while True:
            print("[  提示  ]:正在检查下载是否完成...")
            self.isdwownload = True
            # 下载上一步失败的
            for aweme in awemeList:
                self.awemeDownload(awemeDict=aweme, music=music, cover=cover, avatar=avatar, resjson=resjson,
                                   savePath=savePath)
                # time.sleep(0.5)
            wait(self.alltask, return_when=ALL_COMPLETED)

            if self.isdwownload:
                break

        end = time.time()  # 结束时间
        print('\n' + '[下载完成]:耗时: %d分钟%d秒\n' % (int((end - start) / 60), ((end - start) % 60)))  # 输出下载用时时间


if __name__ == "__main__":
    pass
