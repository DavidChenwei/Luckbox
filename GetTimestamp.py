import urllib.request


def get_page(url):
    res = urllib.request.urlopen(url)
    content = res.read().decode()
    return content


def get_TimeStamp(args):
    room_id = args
    str_url = 'https://egame.qq.com/' + str(room_id)
    res = urllib.request.urlopen(str_url)
    content = res.read().decode()
    arr_1 = content.split('"pid":"' + str(room_id) + '_')
    str_timestamp = arr_1[1][0:10]
    # print(content)
    # print(arr_1[1][0:10])
    return str_timestamp
