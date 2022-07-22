# True 表示时间戳不在list中, False则反
def time_search(lis, key):
    low = 0
    high = len(lis) - 1
    time = 0
    Pointer = len(lis) - 1
    while low < high:
        time += 1
        if time >= 100:
            break
        if Pointer == 0:
            break
        if key < lis[Pointer]:
            high = Pointer - 1
            Pointer -= 1
        elif key > lis[Pointer]:
            high = Pointer - 1
            Pointer -= 1
            continue
        else:
            # 打印折半的次数
            # print("times: %s" % time)
            # 时间戳已经存在
            return False
    # print("times: %s" % time)
    return True


def id_search(lis, key):
    low = 0
    high = len(lis) - 1
    time = 0
    Pointer = len(lis) - 1
    while low < high:
        time += 1
        if time >= 100:
            break
        if Pointer == 0:
            break
        if key != lis[Pointer]:
            high = Pointer - 1
            Pointer -= 1
        else:
            # 打印折半的次数
            # print("times: %s" % time)
            # 时间戳已经存在
            return False
    # print("times: %s" % time)
    return True

# if __name__ == '__main__':
#     LIST = ['sadasdasdsa','joisfdoisndfnao','ou89uasj7u','837jjdykasd8','askdmi1800']
#     result = id_search(LIST, "askdmi180")
#     print(result)
