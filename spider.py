import requests
from google.protobuf.json_format import MessageToJson
import dm_pb2 as Danmaku  # 需要自己编译
import json
import time
import pandas as pd
import os
from lxml import etree
# cid 825556746
# 输入你想爬取视频的BV号
"""
比亚迪：
BV11G4y127LW
BV1nW4y1579E
BV1UG411g7Hb
"""
BV = input("请输入想要爬取视频的BV号（如 BV1MN4y177PB）：")
# month_time_list = ["2022-07"]
month_time = input("请输入想要爬取的月份（如 2022-08）：")

# 存入csv/excel的表头
header_list = ['弹幕id', '弹幕所处位置', '弹幕发送时间', '弹幕内容']
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "referer": "https://www.bilibili.com/video/{}".format(BV),
    "cookie": "i-wanna-go-back=-1; buvid_fp_plain=undefined; CURRENT_BLACKGAP=0; blackside_state=0; is-2022-channel=1; LIVE_BUVID=AUTO6716594126471015; fingerprint3=5221c0bb7d4cce4fc7402bf3fc44c185; DedeUserID=631856860; DedeUserID__ckMd5=409cc17662ce50a7; rpdid=|(u)~Rll)Ruk0J'uYY)Ym~~)u; buvid4=C111D406-E152-B1DC-6B85-05659B3843DC80536-022041512-%2BFtf0v0oD5Im5HVg5PMl3Q%3D%3D; SESSDATA=b05e13fa%2C1686463097%2C2aef4%2Ac2; bili_jct=04106aa1faed1b5ed4b2841cff67c620; sid=6i6ncbfi; buvid3=BBB031C7-7444-69F6-879E-1E4DCF6BD47051104infoc; b_nut=1676888651; hit-new-style-dyn=1; CURRENT_PID=c98bbde0-cd36-11ed-b682-b9df3e25cc10; CURRENT_FNVAL=4048; _uuid=FBA75B2A-F72B-10E79-FD6A-8D1565D101E2197092infoc; nostalgia_conf=-1; b_ut=5; hit-dyn-v2=1; fingerprint=63291dae4f58a393538aa578b6797838; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; buvid_fp=ffeb0473ac88278a6015999237a5f8f6; CURRENT_QUALITY=64; home_feed_column=4; bp_video_offset_631856860=801874714921271400; b_lsid=6C106134E_18876829EC6; PVID=1; browser_resolution=1006-611",
    "origin": "https://www.bilibili.com"
}


def change_time(ctime):
    """
    :param ctime: 时间戳
    :return: 对应的日期和时间
    参考：https://www.runoob.com/python3/python-timstamp-str.html
    """
    timeArray = time.localtime(int(ctime))
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return str(otherStyleTime)


def ms_to_s(ms):
    """
    :param ms: 毫秒
    :return: 转成 分钟:秒数 xx:xx
    """
    sec = ms // 1000
    mins = sec // 60
    secs = sec % 60
    if secs < 10 and mins < 10:
        return "0{}:0{}".format(mins, secs)
    elif secs < 10 and mins >= 10:
        return "{}:0{}".format(mins, secs)
    elif secs >= 10 and mins < 10:
        return "0{}:{}".format(mins, secs)
    else:
        return "{}:{}".format(mins, secs)


def get_web_message(BV, cid):
    """
    :param BV: 视频的BV号
    :param cid: 视频的cid号
    :return: 视频的页面数据，如播放量、点赞量等
    """
    web_url = "https://www.bilibili.com/video/{}".format(BV)
    # 请求这个网址不需要cookie
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    }
    resp = requests.get(web_url, headers=headers).text
    html = etree.HTML(resp)

    title_item = html.xpath('//h1/text()')[0].strip()  # 视频标题
    up_name = html.xpath(
        '//div[@class="up-detail-top"]/a[1]/text()')[0].strip()  # up主名字
    view_item = html.xpath(
        '//span[@class="view item"]/text()')[0].strip()  # 播放量
    dm_item = html.xpath('//span[@class="dm item"]/text()')[0].strip()  # 弹幕数
    pudate_item = html.xpath(
        '//span[@class="pudate-text"]/text()')[0].strip()  # 发布时间
    like_item = html.xpath(
        '//span[@class="video-like-info video-toolbar-item-text"]/text()')[0].strip()  # 点赞量
    coin_item = html.xpath(
        '//span[@class="video-coin-info video-toolbar-item-text"]/text()')[0].strip()  # 投币量
    collect_item = html.xpath(
        '//span[@class="video-fav-info video-toolbar-item-text"]/text()')[0].strip()  # 收藏量
    human_item = get_human_online(BV, cid)  # 当前观看人数

    print('-----------------------')
    print('【标题】\t', title_item)
    print('【UP主】\t', up_name)
    print('【发布时间】\t', pudate_item)
    print('【播放量】\t', view_item)
    print('【弹幕数】\t', dm_item)
    print('【当前观看人数】\t', human_item)
    print('【点赞量】\t', like_item)
    print('【投币量】\t', coin_item)
    print('【收藏量】\t', collect_item)
    print('-----------------------')
    return title_item


def get_human_online(BV, cid):
    """
    :param BV: 视频的BV号
    :param cid: 视频的cid号
    :return: 当前视频观看人数
    当前观看人数数据通过JS进行渲染
    https://api.bilibili.com/x/player/online/total?aid=644506240&cid=804898938&bvid=BV1YY4y1c72e&ts=55368474
    aid和ts都是可选参数
    """
    online_url = "https://api.bilibili.com/x/player/online/total"
    params = {
        "cid": cid,
        "bvid": BV
    }
    human_online_resp = requests.get(url=online_url, params=params)
    human_online_data = human_online_resp.json()
    human_online = human_online_data['data']['total']
    return human_online


def get_cid(BV):
    """
    :param BV: 视频的BV号
    :return: 视频的cid号
    """
    cid_url = "https://api.bilibili.com/x/player/pagelist"
    params = {
        "bvid": BV,
        "jsonp": 'jsonp'
    }
    # 请求这个网址不需要cookie
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    }
    resp = requests.get(cid_url, params=params, headers=headers)
    cid_data = resp.json()
    cid = cid_data['data'][0]['cid']
    print('cid：', cid)
    return cid


def get_date(cid, month_time, headers=headers):
    """
    :param cid: 视频的cid号 唯一
    :param headers: requests请求头
    :return: 有弹幕的日期 列表形式
    """
    date_url = "https://api.bilibili.com/x/v2/dm/history/index"
    params = {
        "type": 1,
        "oid": cid,  # 注意：这里参数是oid oid和cid实际上是一个东西
        "month": month_time,
    }
    resp = requests.get(date_url, params=params, headers=headers)

    # date：日期；data：数据
    date_data = resp.json()
    date_data_list = date_data["data"]
    print("爬取日期：", date_data_list)
    return date_data_list


def get_danmu(cid, date, headers=headers):
    """
    :param cid: 指定视频cid号
    :param date: 指定日期
    :param headers: requests请求头
    :return: 弹幕具体数据
    B站提供了一个获取弹幕的API：https://api.bilibili.com/x/v2/dm/web/history/seg.so
    有关protobuf使用参考：https://github.com/SocialSisterYi/bilibili-API-collect
    """
    danmu_api_url = "https://api.bilibili.com/x/v2/dm/web/history/seg.so"
    # https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={}&date={}
    params = {
        "type": 1,
        "oid": cid,
        "date": date
    }
    # 发送请求，获取数据
    print("正在爬取{}的弹幕".format(date))
    resp = requests.get(danmu_api_url, params=params, headers=headers)
    danmu_data = resp.content
    # 利用protobuf处理seg.so格式文件
    danmaku_seg = Danmaku.DmSegMobileReply()
    danmaku_seg.ParseFromString(danmu_data)
    data_dir = json.loads(MessageToJson(danmaku_seg))

    # data_dir里存放的是dir类型的数据；data_dir里以列表形式存放每条弹幕的详细信息
    data_list = data_dir['elems']

    dm_id_list = []
    dm_progress_list = []
    dm_time_list = []
    dm_content_list = []

    for i in range(len(data_list)):
        # 弹幕的id 唯一
        dm_id = 'A' + data_list[i]['id']
        # 弹幕所处位置，以毫秒计
        dm_progress = ms_to_s(data_list[i].get('progress', 0))
        dm_time = change_time(data_list[i]['ctime'])
        dm_content = data_list[i]['content']

        dm_id_list.append(dm_id)
        dm_progress_list.append(dm_progress)
        dm_time_list.append(dm_time)
        dm_content_list.append(dm_content)

    df = pd.DataFrame(
        data={'弹幕id': dm_id_list, '弹幕所处位置': dm_progress_list, '弹幕发送时间': dm_time_list, '弹幕内容': dm_content_list})

    # 如果文件夹不存在
    if not os.path.exists('data'):
        os.mkdir('data')
    # 如果文件不存在或文件为空，则写入表头，否则不写入表头
    if (not os.path.exists(filename)) or (not os.path.getsize(filename)):
        # 采用GB18030编码格式 保证用excel打开不会出现乱码
        df.to_csv(filename, header=True, index=False,
                  mode='a', encoding='GB18030', sep=',')
    else:
        df.to_csv(filename, header=False, index=False,
                  mode='a', encoding='GB18030', sep=',')
    print("共{}条数据".format(len(dm_id_list)))
    print("成功保存数据！")


def remove_duplicates(filename, sub, new_filename):
    """
    去重，避免重复弹幕
    :param filename: 文件名
    :param sub: 根据该行进行去重操作
    :return: 无返回值，保存新文件
    """
    frame = pd.read_csv(filename, encoding='GB18030')
    data = frame.drop_duplicates(subset=[sub], keep='first', inplace=False)
    data.to_csv(new_filename, encoding='GB18030',
                index=False, header=header_list)


if __name__ == "__main__":
    cid = get_cid(BV)
    title = get_web_message(BV, cid)
    date_list = get_date(cid, month_time)

    filename = "data/{}.csv".format(BV)
    newfilename = "data/new_{}.csv".format(BV)

    for date in date_list:
        get_danmu(cid, date=date)
        time.sleep(2)
        print('*******************')

    # 对保存弹幕文件进行去重操作
    remove_duplicates(filename, '弹幕id', newfilename)
