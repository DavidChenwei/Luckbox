# -*- coding:utf-8 -*-
import requests, time
import json

from CalculateDiamond import isgift, caldiamond
from GetTimestamp import get_TimeStamp
from Search_list import time_search, id_search
import globalvar as gl

url = 'https://game.egame.qq.com/cgi-bin/pgg_async_fcgi'
ls = []

# str2 = get_TimeStamp(545319777)
time_list = []  # 用来存住已经存在的时间戳
id_list = []  # 用来存放已经存在的msg ID
Total_Diamond = 0  # 礼物的总钻石数

room_id = ''
time_id = ''
gl.set_value("num_mdx", 0)
gl.set_value("num_mtl", 0)
gl.set_value('Total_Diamond', 0)
gl.set_value('RMB_value', 0)


def grab_info(self):
    global room_id
    global time_id
    global Total_Diamond
    global time_list
    global id_list

    while True:
        try:
            room_id = gl.get_value('roomId')
            time_id = gl.get_value('time_stamp')
            price_mdx = gl.get_value('price_mdx')
            price_mtl = gl.get_value('price_mtl')
            if room_id is not None and time_id is not None and price_mdx is not None and price_mtl is not None:
                break
        except Exception as e:
            print(e)
    str_info = str(room_id) + "_" + str(time_id)
    # temp = str1 + '_' + str2
    # print(temp)
    try:
        timestamp = int(time.time())
        data = {
            '_t': timestamp,
            'g_tk': room_id,
            'p_tk': '',
            'param': '{"key":{"module":"pgg_live_barrage_svr","method":"get_barrage","param":{"anchor_id":' + str(
                room_id) + ','
                           '"vid":' + '"%s"' % str_info + ',"scenes":4096,"last_tm":5}}}',
            'app_info': '{"platform":4,"terminal_type":2,"egame_id":"egame_official","version_code":"9.9.9",'
                        '"version_name":"9.9.9"}',
            'tt': '1'
        }
        response = requests.get(url, params=data)
        response = response.text
        msg_list = json.loads(response)
        msg_list = msg_list['data']['key']['retBody']['data']['msg_list']
        # response.encoding = 'utf-8'
        # msg_list = response.json()['data']['key']['retBody']['data']['msg_list']
        # msg_list = response.json()
        if not msg_list:
            i = 1
			
        for i in msg_list:
            msg_id = i['msgid']
            username = i['nick']
            content = i['content']
            time_stamp = i['tm']
            #
            if content == 'pk':
                continue
            # '{0}' 去掉可以拿到夺宝信息
            if '{0}' in content:
                continue
            if msg_id in ls:
                continue
            if len(ls) <= 10:
                ls.append(msg_id)
            else:
                ls.pop(0)
                ls.append(msg_id)
            time_stamp_int = int(time_stamp)
            timeArray = time.localtime(time_stamp_int / 1000)
            otherStyleTime = time.strftime("%H:%M:%S", timeArray)
            if '梦幻盒子 变幻出' in content or '梦幻盒子 爆出' in content:  # 第一个if是用来判断不管是飘屏还是房间里的弹幕是否和梦幻盒子有关
                # print(username,content)
                # print(msg_list)
                bln_time = time_search(time_list, time_stamp)
                bln_id = id_search(id_list, msg_id)
                if '的直播间 赠送' in content:  # 第二个if, 如果带有直播间证明是飘屏，需要单独处理成弹幕的格式在计算
                    str_arr_1 = content.split(' 在 ')
                    username = str_arr_1[0]
                    str_arr_2 = str_arr_1[1].split(' 的直播间 赠送')
                    room_name = str_arr_2[0]
                    # print(room_name)
                    # print(username)
                    print(msg_list)
                    if room_name == '王子非非常欧' or room_name == '王子非的臭妹妹':  # 第三个if, 判断是否在指定的直播间出货
                        if bln_time and bln_id:  # 第四个if, 用时间戳和msg_id来判断是否重复内容
                            time_list.append(int(time_stamp))
                            id_list.append(msg_id)
                            content = username + ' 赠送 ' + str_arr_2[1]
                            print(otherStyleTime, username + '的消息：\t' + '\033[1;34m' + content + '\033[0m')
                            if '梦幻盒子 爆出 BUFF' in content:
                                content = content.replace('梦幻盒子 爆出 BUFF', '梦幻盒子 变幻出 ')
                            diamond = caldiamond(content, username, otherStyleTime, msg_id)
                            Total_Diamond = Total_Diamond + diamond
                            # print("当前钻石总计:", Total_Diamond)
                            RMB_value = Total_Diamond / 10 * 0.6025
                            gl.set_value('Total_Diamond', Total_Diamond)
                            gl.set_value('RMB_value', RMB_value)
                            # print('当前RMB总计:', RMB_value)
                            print("------------------------------------------------------------------------")
                    # else:
                    #     print("重复内容不显示")
                        # content = username + ' 赠送 ' + str_arr_2[1]
                        # print(otherStyleTime, username + '的消息：\t' + '\033[1;34m' + content + '\033[0m')
                else:
                    bln_gift = isgift(username, content)
                    bln_name = '梦幻摩天轮' not in content and '梦幻迷迭香' not in content
                    if bln_gift and bln_time and bln_id and bln_name:
                        time_list.append(int(time_stamp))
                        id_list.append(msg_id)
                        # print(msg_list)
                        print(otherStyleTime, username + '的消息：\t' + '\033[1;34m' + content + '\033[0m')
                        diamond = caldiamond(content, username, otherStyleTime, msg_id)
                        Total_Diamond = Total_Diamond + diamond
                        # print("当前钻石总计:", Total_Diamond)
                        RMB_value = Total_Diamond / 10 * 0.6025
                        gl.set_value('Total_Diamond', Total_Diamond)
                        gl.set_value('RMB_value', RMB_value)
                        # print('当前RMB总计:', RMB_value)
                        print("------------------------------------------------------------------------")
            time.sleep(0.1)
    except Exception as e:
        print(e)
