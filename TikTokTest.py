#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@Description:TikTok.py
@Date       :2023/02/11 13:06:23
@Author     :imgyh
@version    :1.0
@Github     :https://github.com/imgyh
@Mail       :admin@imgyh.com
-------------------------------------------------
Change Log  :
-------------------------------------------------
'''
import TikTokUtils
from TikTok import TikTok


def getAwemeInfo():
    share_link_video = "3.56 uSy:/ 复制打开抖音，看看【小透明的作品】没有女朋友就用我的吧哈哈哈哈 # 表情包锁屏  https://v.douyin.com/BugmVVD/"
    share_link_pic = "8.20 MJI:/ 复制打开抖音，看看【舍溪的图文作品】我又来放图集啦～还有你们要的小可爱大图也放啦～# ... https://v.douyin.com/BugrFTN/"
    tk = TikTok()

    url = tk.getShareLink(share_link_pic)
    key_type, key = tk.getKey(url)
    datanew, dataraw = tk.getAwemeInfo(key)
    print(datanew)


def getUserInfo():
    share_link_post = "1- 长按复制此条消息，打开抖音搜索，查看TA的更多作品。 https://v.douyin.com/BupCppt/"
    share_link_like = "2- 长按复制此条消息，打开抖音搜索，查看TA的更多作品。 https://v.douyin.com/BusJrfr/"
    tk = TikTok()

    url = tk.getShareLink(share_link_like)
    key_type, key = tk.getKey(url)
    awemeList = tk.getUserInfo(key, mode="like", count=35)
    print(awemeList)


def getLiveInfo():
    live_link = "https://live.douyin.com/40768897856"
    tk = TikTok()

    url = tk.getShareLink(live_link)
    key_type, key = tk.getKey(url)
    live_json = tk.getLiveInfo(key)
    print(live_json)


def getMixInfo():
    mix_link = 'https://v.douyin.com/B3J63Le/'
    tk = TikTok()

    url = tk.getShareLink(mix_link)
    key_type, key = tk.getKey(url)
    awemeList = tk.getMixInfo(key, count=35)
    print(len(awemeList))


def getUserAllMixInfo():
    user_all_mix_link = 'https://v.douyin.com/B38oovu/'
    tk = TikTok()

    url = tk.getShareLink(user_all_mix_link)
    key_type, key = tk.getKey(url)
    mixIdNameDict = tk.getUserAllMixInfo(key, count=35)
    print(mixIdNameDict)


def getMusicInfo():
    music_link = 'https://v.douyin.com/S6YMNXs/'
    tk = TikTok()

    url = tk.getShareLink(music_link)
    key_type, key = tk.getKey(url)
    awemeList = tk.getMusicInfo(key, count=35)
    print(len(awemeList))


def test():
    utils = TikTokUtils.Utils()
    user_all_mix_link = 'https://www.douyin.com/aweme/v1/web/aweme/favorite/?' + \
                        utils.getXbogus(
                            url='device_platform=webapp&aid=6383&sec_user_id=MS4wLjABAAAAjQn6ONfaGgUpk0Q1ep8dPiD3W4T_lxTJmemfy3MTJ64&max_cursor=1676441180000&count=10')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'referer': 'https://www.douyin.com/',
        'accept-encoding': None,
        'Cookie': 'ttwid=1|oLudm-Hi5ikxQQhmAnv4Km4LjwwvLa4Qk_JGrKffuYU|1681878460|b0f581d97797bb67d2260bf92d65e8808b90713afc08bf5d8100f571fd70a275; passport_csrf_token=570d671dcd8d8598fcde4c3f7c99664d; passport_csrf_token_default=570d671dcd8d8598fcde4c3f7c99664d; s_v_web_id=verify_lgn70gzw_sAVtjJdD_Clyk_43UL_8M9L_6JiTtPC2TyU0; n_mh=vrLGYVtwqutbPLOGNTDUGahwaD9AyYjn4iVvAO2Xt0s; sso_uid_tt=92e014dfb6653bdc319ecc6a6ceea870; sso_uid_tt_ss=92e014dfb6653bdc319ecc6a6ceea870; toutiao_sso_user=d0bd8d5cc0f75420799903572941ce83; toutiao_sso_user_ss=d0bd8d5cc0f75420799903572941ce83; passport_auth_status=5c576b088f4a19448eb4efd7aaeb7c5e,; passport_auth_status_ss=5c576b088f4a19448eb4efd7aaeb7c5e,; uid_tt=564215aecc985785d033c9e4c9d00fc4; uid_tt_ss=564215aecc985785d033c9e4c9d00fc4; sid_tt=f14390d924c81856fde84b1cd534bf09; sessionid=f14390d924c81856fde84b1cd534bf09; sessionid_ss=f14390d924c81856fde84b1cd534bf09; odin_tt=0aa1c100d17bf3541dce9e8dd62c6353302b8abaaa0a5998d5c437313feb245d8f7b6391a69772e4afa7d3c718878837; passport_assist_user=CjwC3fi9JyApG4DN-HiFI6n5FcGAdzNDT29nR-nSDJYAVfqh2BYI77qdTN2GRfgagkYLRi1wxNp1akHBwGcaSAo8XDkNT-UWnkFmc_0eXMYCb8OIh4G_YnH8pylwwdfS-7PCTekX3trj0JyENUVWLWFxnKuG5HhSS4FB2CtxEJ7yrg0Yia_WVCIBA9bY7IU=; sid_ucp_sso_v1=1.0.0-KDc0NmY3NzA5ZWFhNzI2YzMyOWMxMDMwNjAwMDg3YzRjYzg3ZjlhODcKHQjG-7zT9QEQ5dv9oQYY7zEgDDCL_7nMBTgGQPQHGgJscSIgZDBiZDhkNWNjMGY3NTQyMDc5OTkwMzU3Mjk0MWNlODM; ssid_ucp_sso_v1=1.0.0-KDc0NmY3NzA5ZWFhNzI2YzMyOWMxMDMwNjAwMDg3YzRjYzg3ZjlhODcKHQjG-7zT9QEQ5dv9oQYY7zEgDDCL_7nMBTgGQPQHGgJscSIgZDBiZDhkNWNjMGY3NTQyMDc5OTkwMzU3Mjk0MWNlODM; publish_badge_show_info="0,0,0,1681878505305"; LOGIN_STATUS=1; store-region=cn-sc; store-region-src=uid; sid_guard=f14390d924c81856fde84b1cd534bf09|1681878504|5183998|Sun,+18-Jun-2023+04:28:22+GMT; sid_ucp_v1=1.0.0-KGY5OGQ3OTQ4YmVkYzczODgzYzM0MmJmOWYxMzhkMDliMTc5NGI3NjMKGQjG-7zT9QEQ6Nv9oQYY7zEgDDgGQPQHSAQaAmxmIiBmMTQzOTBkOTI0YzgxODU2ZmRlODRiMWNkNTM0YmYwOQ; ssid_ucp_v1=1.0.0-KGY5OGQ3OTQ4YmVkYzczODgzYzM0MmJmOWYxMzhkMDliMTc5NGI3NjMKGQjG-7zT9QEQ6Nv9oQYY7zEgDDgGQPQHSAQaAmxmIiBmMTQzOTBkOTI0YzgxODU2ZmRlODRiMWNkNTM0YmYwOQ; download_guide="3/20230419"; pwa2="3|0"; FOLLOW_NUMBER_YELLOW_POINT_INFO="MS4wLjABAAAA-jD2lukp--I21BF8VQsmYUqJDbj3FmU-kGQTHl2y1Cw/1681920000000/0/0/1681900423333"; __ac_nonce=0644234d60042cacebbb6; __ac_signature=_02B4Z6wo00f01eZN0dAAAIDAhUcRuQz7dNHmbdVAAB3TRUC7i8VqXQejR8jv-D8UggBx1MBLH564PE.cCZf00m7Cw640CNUvcc5jJfhgn8u5FhvVndykvwbQb.HEpSfGN-8eqql7GpuGZJ8f1d; strategyABtestKey="1682060514.261"; passport_fe_beating_status=true; csrf_session_id=405b0ec4f6338a5d893a5f14f6fd1a64; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtY2xpZW50LWNlcnQiOiItLS0tLUJFR0lOIENFUlRJRklDQVRFLS0tLS1cbk1JSUNGRENDQWJxZ0F3SUJBZ0lVR1ljQ3FuQUh0UUJBZm5WWkYxQW84cUtjY2Zrd0NnWUlLb1pJemowRUF3SXdcbk1URUxNQWtHQTFVRUJoTUNRMDR4SWpBZ0JnTlZCQU1NR1hScFkydGxkRjluZFdGeVpGOWpZVjlsWTJSellWOHlcbk5UWXdIaGNOTWpNd016STNNRE15T0RBeldoY05Nek13TXpJM01URXlPREF6V2pBbk1Rc3dDUVlEVlFRR0V3SkRcblRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxWVhKa01Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERcbkFRY0RRZ0FFNmZ1Z3d0MEJnZUh5akVub1FvNWtXUS9qc2daTTV1YXBiNTQ4KytTV0dRSjMwb2lSTHNtYlVFSUZcblFIYzh3UEthZzZmdXNPTm91WncxOEdNYm5vTStwNk9CdVRDQnRqQU9CZ05WSFE4QkFmOEVCQU1DQmFBd01RWURcblZSMGxCQ293S0FZSUt3WUJCUVVIQXdFR0NDc0dBUVVGQndNQ0JnZ3JCZ0VGQlFjREF3WUlLd1lCQlFVSEF3UXdcbktRWURWUjBPQkNJRUlPV3Y3d01ZUGhoeUNPL2ZwenJGNDJNeEQ4ZGIzN0YyTDgxaW8zVTVlVFpaTUNzR0ExVWRcbkl3UWtNQ0tBSURLbForcU9aRWdTamN4T1RVQjdjeFNiUjIxVGVxVFJnTmQ1bEpkN0lrZURNQmtHQTFVZEVRUVNcbk1CQ0NEbmQzZHk1a2IzVjVhVzR1WTI5dE1Bb0dDQ3FHU000OUJBTUNBMGdBTUVVQ0lCbm9xRDBRbVdUSlNLOVNcbkFZRjJ6YkljYzBsZjFRMDVTUGxXMURDQ0FMVUpBaUVBazJFRWpKdkdFRnl0YzBWbXRoRTA5bFpGeFFkUmlGN21cbk9pdE5IZzBOZUJrPVxuLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLVxuIn0=; msToken=qSfWwAdwksuBS5wmQAvpzUsf2ovkFFKefOLSvZDKA1Z_FX7ith-wCknpVQB08kft4ISWp00GHeQBaPwV9tcWJq6xBC-mPnQKNjBVINeOQGvFtSdsfacWMtWpa8x1RJE=; FOLLOW_LIVE_POINT_INFO="MS4wLjABAAAA-jD2lukp--I21BF8VQsmYUqJDbj3FmU-kGQTHl2y1Cw/1682092800000/0/0/1682061497980"; msToken=jDwC5gjTRXV6hrFvGMG-AkOBXHGrt_Mp5NaltB1upOUm0aQnZ7sy7qlSEn2tQbGHShp2X7ayNMDQQlPekSTV9MkxBv56LR9zepTlYNOoqbH_RdjDvbl-MZDrmui3OEE=; tt_scid=hERl4ibL-B89BGXb9wUfsmVkQh-G2dvL2wI0QvEDYLooFsvwoz.q6J4ZA0WErn0Tb9fb; home_can_add_dy_2_desktop="1"'}

    import requests

    res = requests.get(user_all_mix_link, headers=headers).text
    import json
    datadict = json.loads(res)
    print(datadict["aweme_list"][0]["video"]["bit_rate"])
    print(len(datadict["aweme_list"][0]["video"]["bit_rate"]))


if __name__ == "__main__":
    # test()
    # getMusicInfo()
    # getUserAllMixInfo()
    # getMixInfo()
    # getAwemeInfo()
    # getUserInfo()
    # getLiveInfo()
    pass
