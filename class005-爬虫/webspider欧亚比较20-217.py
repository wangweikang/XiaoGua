import os
from pprint import pprint
import csv
from collections import Counter
import json
import time
import xlrd

import requests
from pyquery import PyQuery as pq
import re
from urllib import request
from urllib import error
from urllib import parse
from http import cookiejar
import datetime
from tkinter import *
import time
import threading
from tkinter import filedialog


def csv_save(data, path, header=None):
    """
    将数据data，保存为.csv文件，注意在写入的时候，
    open函数中newline=''，才能保证隔行没有空行

    """
    with open(path, "a+", newline='') as f:
        f_csv = csv.writer(f)
        if header:
            f_csv.writerow(header)
        if data is not None:
            f_csv.writerows(data)
        # f_csv.writerows(map(lambda x: [x], data))


def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'a', encoding='utf-8') as f:
        # log('save', path, s, data)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        # log('load', s)
        return json.loads(s)


def calc_salary(data):
    s = data[0].split("-")
    s_low = float(s[0])
    s_high = float(s[1])
    s_model = ((s_high - s_low) * 0.4 + s_low)
    return s_model


class Model():
    """
    基类, 用来显示类的信息
    """

    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class Main_Window:
    def __init__(self):
        self.spider = ZCSpider()
        window = Tk()
        window.title("lotterry_spider")
        # 添加一个多选按钮和单选按钮到frame1
        # 添加一个label、entry、button和message到frame2
        frame1 = Frame(window)
        frame1.pack()

        frame2 = LabelFrame(frame1, text="开赔公司选择: ")
        self.zcspider = ZCSpider()
        self.gs_list = []
        self.companyid_list = []
        self.gameid = StringVar()
        label_gameid = Label(frame2, text="输入比赛ID号:")
        label_gameid.grid(row=5, column=1)
        self.companyid = StringVar()
        label_companyid = Label(frame2, text="输入公司ID:")
        label_companyid.grid(row=6, column=1)
        input_gameid = Entry(frame2, textvariable=self.gameid)
        input_gameid.grid(row=5, column=2)
        input_companyid = Entry(frame2, textvariable=self.companyid)
        input_companyid.grid(row=6, column=2)
        self.btAddcompany = Button(frame2, text="添加公司id", command=self.addcompanyButton)

        self.btGrubData = Button(frame2, text="开始抓取数据", command=self.grubdataButton)
        frame2.grid(row=1, column=1)
        self.btLoadFile = Button(frame2, text="加载公司id文件", command=self.load_file)

        hit_frame1 = LabelFrame(frame1, text="开赔公司id列表: ")
        hit_frame1.grid(row=2, column=1)

        # 添加一个text
        self.text = Text(hit_frame1)
        self.text.pack()
        self.btGrubData.grid(row=8, column=1)
        self.btAddcompany.grid(row=6, column=3)
        self.btLoadFile.grid(row=7, column=1)

        self.frame3 = Frame(window)
        self.frame3.pack()

        window.mainloop()

    def load_file(self):
        self.gs_file_list = []
        filename = filedialog.askopenfilename()
        print(filename)
        if filename != '':
            data = xlrd.open_workbook(filename)  # 打开excel
            table = data.sheets()[0]
            for i in range(table.nrows):
                self.gs_list.append(int(table.row_values(i)[0]))
                self.text.insert(END, str(int(table.row_values(i)[0])) + ",")

    def loginButton(self):
        self.text.insert(END,
                         "登陆成功,用户名:{},密码:{}，验证码:{}".format(self.user.get(), self.password.get(), self.authnum.get()))
        self.spider.login(self.user.get(), self.password.get(), self.authnum.get())

    def addcompanyButton(self):
        self.gs_list.append(self.companyid.get())
        self.text.insert(END, self.companyid.get() + ",")

    def grubdataButton(self):
        self.btAddcompany['state'] = DISABLED
        game_id = self.gameid.get()
        if game_id == "":
            pass
        if len(self.companyid_list) < 1:
            pass
        csv_save(None, "data/game_data.csv", self.spider.csv_header)
        grub_time = datetime.datetime.now()
        if self.gs_list is None:
            return
        for i in range(216):
            self.zcspider.grub_data(game_id, self.gs_list, grub_time - i * datetime.timedelta(minutes=20))

    def add_check(self, frame, check_list, gs_list):
        for i, gs in enumerate(gs_list):
            win = IntVar()
            check_num = Checkbutton(frame, text="{}".format(gs), variable=win)
            check_num.deselect()
            check_num.grid(row=int(i / 7), column=i % 7)
            check_list.append(win)


class ZCSpider(Model):
    """
    51 job 网站爬虫类
    """

    def __init__(self):
        self.game_list = []
        self.diedainums = 0
        # # 澳客网其实爬取url
        self.main_url = "http://www.okooo.com"
        self.pankou_num = {
            "平手": 0,
            "平手/半球": -0.25,
            "半球": -0.5,
            "半球/一球": -0.75,
            "一球": -1,
            "一球/球半": -1.25,
            "球半": -1.5,
            "球半/两球": -1.75,
            "两球": -2.0,
            "两球/两球半": -2.25,
            "两球半": -2.5,
            "两球半/三球": -2.75,
            "三球": -3.0,
            "受平手/半球": 0.25,
            "受半球": 0.5,
            "受半球/一球": 0.75,
            "受一球": 1,
            "受一球/球半": 1.25,
            "受球半": 1.5,
            "受球半/两球": 1.75,
            "受两球": 2.0,
            "受两球/两球半": 2.25,
            "受两球半": 2.5,
            "受两球半/三球": 2.75,
            "受三球": 3.0,
        }

        self.pankou_url_tmplate = "http://www.okooo.com/soccer/match/{}/{}/change/{}/"  # 查看盘口分析的url模版
        # 利用opener保存cookie
        self.opener = None
        self.text = ""
        self.headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"

        }
        # 设置csv文件的首行
        self.csv_header = ['时间', '主胜赔率', '平局赔率', '客胜赔率', '赔率个数', '时间', '主水位', '盘口', '客水位', '水位个数']

    # 向headers中添加referer，这样才能顺利访问子网页
    def add_refer_header(self, refer):
        if refer:
            header = headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
                'referer': refer,
            }
        return header

    def grub_data(self, game_id, company_idlist, grub_time=datetime.datetime.now()):

        time_show = str(grub_time).split(".")[0]
        game_data = []

        oupan_list = []
        for company_id in company_idlist:
            oupan_url = self.pankou_url_tmplate.format(game_id, "odds", company_id)
            req = requests.get(oupan_url, headers=self.add_refer_header(self.main_url))
            content = req.content.decode("gbk")
            e = pq(content)
            tr_list = e("tr")
            if len(tr_list) < 4:
                break
            for tr in tr_list[2:]:
                try:
                    e = pq(tr)
                    td_list = e("td")
                    if len(td_list) < 5:
                        continue

                    time_str = pq(td_list[0]).text()
                    if "(" in time_str:
                        time_str = time_str.split("(")[0]

                    time_format = time.strptime(time_str, "%Y/%m/%d %H:%M")

                    time_day = time_format.tm_mday
                    time_hour = time_format.tm_hour
                    time_min = time_format.tm_min
                    print(grub_time.day, grub_time.hour, grub_time.minute, time_day, time_hour, time_min)

                    zusheng_odds_str = pq(td_list[2]).text()
                    zusheng_odds = float(self.delete_str(zusheng_odds_str))
                    ping_odds_str = pq(td_list[3]).text()
                    ping_odds = float(self.delete_str(ping_odds_str))
                    kesheng_odds_str = pq(td_list[4]).text()
                    kesheng_odds = float(self.delete_str(kesheng_odds_str))
                except:
                    continue
                if grub_time.day == time_day:
                    if grub_time.hour == time_hour:
                        if grub_time.minute >= time_min:
                            oupan_list.append([time_show, zusheng_odds, ping_odds, kesheng_odds])
                            break

                    elif grub_time.hour > time_hour:
                        oupan_list.append([time_show, zusheng_odds, ping_odds, kesheng_odds])
                        break
                elif grub_time.day > time_day:
                    oupan_list.append([time_show, zusheng_odds, ping_odds, kesheng_odds])
                    break
            print(oupan_list)
            sum_num_1 = len(oupan_list)
            zusheng_oupan_sum = 0
            ping_oupan_sum = 0
            kesheng_oupan_sum = 0
            sum_1 = 1
            if sum_num_1 == 0:
                sum_1 = 1
            else:
                sum_1 = sum_num_1
            for oupan_data in oupan_list:
                zusheng_oupan_sum += oupan_data[1]
                ping_oupan_sum += oupan_data[2]
                kesheng_oupan_sum += oupan_data[3]

        yapan_list = []
        for company_id in company_idlist:
            yapan_url = self.pankou_url_tmplate.format(game_id, "ah", company_id)
            req = requests.get(yapan_url, headers=self.add_refer_header(self.main_url))
            content = req.content.decode("gbk")
            e = pq(content)

            tr_list = e("tr")
            if len(tr_list) < 4:
                break
            for tr in tr_list[2:]:
                try:
                    e = pq(tr)
                    td_list = e("td")
                    if len(td_list) < 3:
                        continue
                    time_str = pq(td_list[0]).text()
                    if "(" in time_str:
                        time_str = time_str.split("(")[0]


                    time_format = time.strptime(time_str, "%Y/%m/%d %H:%M")

                    time_day = time_format.tm_mday
                    time_hour = time_format.tm_hour
                    time_min = time_format.tm_min
                    print(grub_time.day, grub_time.hour, grub_time.minute, time_day, time_hour, time_min)

                    zushui_odds_str = pq(td_list[2]).text()
                    zushui_odds = float(self.delete_str(zushui_odds_str))
                    pankou = pq(td_list[3]).text()
                    pankou_num = self.pankou_num[pankou]

                    keshui_odds_str = pq(td_list[4]).text()
                    keshui_odds = float(self.delete_str(keshui_odds_str))
                except :
                    continue

                if grub_time.day == time_day:
                    if grub_time.hour == time_hour:
                        if grub_time.minute >= time_min:
                            yapan_list.append([time_show, zushui_odds, pankou_num, keshui_odds])
                            break

                    elif grub_time.hour > time_hour:
                        yapan_list.append([time_show, zushui_odds, pankou_num, keshui_odds])
                        break

                elif grub_time.day > time_day:
                    yapan_list.append([time_show, zushui_odds, pankou_num, keshui_odds])
                    break

        print(yapan_list)
        zushui_yapan_sum = 0
        pankou_num_sum = 0
        keshui_yapan_sum = 0
        sum_2 = 1
        sum_num_2 = len(yapan_list)
        if sum_num_2 == 0:
            sum_2 = 1
        else:
            sum_2 = sum_num_2
        for yapan_data in yapan_list:
            zushui_yapan_sum += yapan_data[1]
            pankou_num_sum += yapan_data[2]
            keshui_yapan_sum += yapan_data[3]

        game_data.append([time_show, round(zusheng_oupan_sum / sum_1, 2), round(ping_oupan_sum / sum_1, 2),
                          round(kesheng_oupan_sum / sum_1, 2), sum_num_1, time_show, round(zushui_yapan_sum / sum_2, 2),
                          round(pankou_num_sum / sum_2, 2), round(keshui_yapan_sum / sum_2, 2), sum_num_2])
        csv_save(game_data, "data/game_data.csv")
        # self.diedainums +=1
        # if self.diedainums == 216:
        #     return
        # self.grub_data(game_id, company_idlist, grub_time -  datetime.timedelta(minutes=20))

    def delete_str(self, float_str):
        if "↑" in float_str or "↓" in float_str:
            return float_str[:-1]
        return float_str

    def time_cmp(self, time):
        return int(time.strftime("%Y/%m/%d %H:%M", time))


def main():
    # spider = ZCSpider()
    # spider.grub_data(1017826, 27)
    # spider.get_authnum()
    # spider.login("185023companyid40105", "AKWgaogao1005", "sda")
    # spider.game_by_date(1)
    Main_Window()


if __name__ == "__main__":
    main()
