# 计算一共收了多少钱
import re
import globalvar as gl
from Write_CSV import writeExecl

gl._init()
Dict_Mtl = {"摩天轮统计": 00000}
Dict_Mdx = {"迷迭香统计": 00000}
gl.set_value("dict_Mdx", Dict_Mdx)
gl.set_value("dict_Mtl", Dict_Mtl)

num_mdx = 0
num_mtl = 0
num_row = 0

# 判断收集到的信息是否是和礼物有关的
def isgift(username: str, content: str):
    bln = False
    bln_add = False
    bln_add_1 = False
    if '撮佸嚭' in content:
        bln_add = True
    if '挱闂磋' in content:
        bln_add_1 = True
    # print('传到这个里的用户名是'+username)
    # print('传到这个里的内容是' + content)
    length = len(username)
    # print('截取的内容是' + content[0:length])
    if username == content[0:length] and bln_add == False and username != '' and bln_add_1 == False:
        bln_1 = '分享' in content
        if not bln_1:
            length_1 = len(content)
            info = content[length:length_1]
            # print(info)
            # 这里只抓梦幻系的礼物，其他都是false, 只有梦幻系的是true
            res = '梦幻花环' in info or '梦幻情书' in info or '梦幻迷迭香' in info or '梦幻摩天轮' in info
            if res:
                bln = True
    return bln


# 计算礼物金额，上面有露掉的内容，这里需要再过滤一遍
def caldiamond(content: str, username: str, time_stamp: int, msg_id : str):
    global num_mdx, num_mtl
    global Dict_Mdx, Dict_Mtl
    global num_row
    number_Dapao = gl.get_value('number_Dapao')
    Diamond = 0
    length = len(content)
    length_name = len(username)
    info = content[length_name:length]
    # print(info)
    arry_1 = info.split(" 变幻出 ")
    # print(arry_1)
    str_temp = arry_1[1].split("x")
    # print(str_temp)
    # 获取礼物名称
    NameGift = str_temp[0]
    # 获取礼物个数
    str_temp_1 = str_temp[1].split("个")
    account = int(str_temp_1[0][0:1])
    # print('收到了', account, '个', NameGift)
    # Total_Account += account
    # gl.set_value('TotalAccount', Total_Account)

    if '闪电超跑' in NameGift:
        Diamond = 1880
    if '要抱抱' in NameGift:
        Diamond = 1
    if '666' in NameGift:
        Diamond = 1
    if '大炮' in NameGift and '黄金' not in content:
        number_Dapao = number_Dapao + account
        Diamond = 100
        gl.set_value('number_Dapao', number_Dapao)
        # print('收到 ' + number_Dapao + " 个大炮")
    if '爱你一万年' in NameGift:
        Diamond = 1314
    if '黄金大炮' in NameGift:
        Diamond = 100
    if '比心' in NameGift:
        Diamond = 2
    if '盛典葱鸭' in NameGift:
        Diamond = 1
    if '守护主播' in NameGift:
        Diamond = 60
    if '银河战机' in NameGift:
        Diamond = 5000
    if '至尊王者' in NameGift:
        Diamond = 20000
    if '幸运星' in NameGift:
        Diamond = 10
    if '海洋之心' in NameGift:
        Diamond = 520
    if '告白气球' in NameGift:
        Diamond = 9999
    if '么么哒' in NameGift:
        Diamond = 520
    if '喜欢你' in NameGift:
        Diamond = 99
    if '打call' in NameGift:
        Diamond = 52
    if '你最棒' in NameGift:
        Diamond = 6
    if '盛典冲锋机' in NameGift:
        Diamond = 1000
    if '梦幻花环' in NameGift:
        Diamond = 60
        str_info = str(time_stamp) + "," + username + "," + NameGift + "," + str(account) + "," + str(Diamond * account) + "," +msg_id
        gl.set_value(num_row, str_info)
        try:
            writeExecl(str_info)
        except Exception as e:
            print(e)
        num_row += 1

    if '梦幻情书' in NameGift:
        Diamond = 660
        str_info = str(time_stamp) + "," + username + "," + NameGift + "," + str(account) + "," + str(Diamond * account) + "," + msg_id
        gl.set_value(num_row, str_info)
        try:
            writeExecl(str_info)
        except Exception as e:
            print(e)
        num_row += 1

    if '梦幻迷迭香' in NameGift:
        Diamond = 1000
        str_info = str(time_stamp) + "," + username + "," + NameGift + "," + str(account) + "," + str(Diamond * account) + "," + msg_id
        try:
            writeExecl(str_info)
        except Exception as e:
            print(e)
        gl.set_value(num_row, str_info)
        num_row += 1
        try:
            if Dict_Mdx.__contains__(username):
                last_account = Dict_Mdx.get(username)
                total = account + int(last_account)
                Dict_Mdx.update({username: total})
            else:
                Dict_Mdx[username] = account
            gl.set_value("dict_Mdx", Dict_Mdx)

            # print(Dict_Mdx)
        except Exception as e:
            print(e)
        num_mdx = num_mdx + account
        gl.set_value('num_mdx', num_mdx)
    if '梦幻摩天轮' in NameGift:
        Diamond = 10000
        str_info = str(time_stamp) + "," + username + "," + NameGift + "," + str(account) + "," + str(Diamond * account) + "," + msg_id
        try:
            writeExecl(str_info)
        except Exception as e:
            print(e)
        gl.set_value(num_row, str_info)
        num_row += 1

        try:
            if Dict_Mtl.__contains__(username):
                last_account = Dict_Mtl.get(username)
                total = account + int(last_account)
                Dict_Mtl.update({username: total})
            else:
                Dict_Mtl[username] = account
            gl.set_value("dict_Mtl", Dict_Mtl)
        except Exception as e:
            print(e)
        num_mtl = num_mtl + account
        # print(Dict_Mtl)
        gl.set_value('num_mtl', num_mtl)
    return Diamond * account
