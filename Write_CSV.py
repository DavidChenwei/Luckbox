import csv
import time

str_time = time.strftime("%Y-%m-%d", time.localtime())
file_name = "Box_Data_" + str_time + ".csv"


def writeExecl(info: str):
    with open(file_name, "a+", newline="") as fw:
        writer = csv.writer(fw)
        info_arr = info.split(",")
        writer.writerow(info_arr)

    fw.close()
