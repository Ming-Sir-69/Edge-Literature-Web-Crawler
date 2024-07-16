import tkinter as tk
import os
import webbrowser
import time
from 功能.爬虫 import BaiduXueshuAutomatic

def wd_split_dou(wd, num=1):
    wd_new = ''
    if ',' in wd:
        wd_lis = wd.split(',')
    elif '，' in wd:
        wd_lis = wd.split('，')
    else:
        return f'("{wd}")'

    if num == 1:
        for i in range(len(wd_lis)):
            if i == 0:
                wd_new = f'"{wd_lis[i].strip()}"'
            else:
                wd_new = wd_new + ' + '+ f'"{wd_lis[i].strip()}"'

    elif num == 2:
        wd_lis.reverse()
        for i in range(len(wd_lis)):
            if i == 0:
                wd_new = wd_lis[i].strip()
            else:
                wd_new = wd_new + ' | '+ wd_lis[i].strip()

    return f'({wd_new})'


def reg(e_keyword1, e_keyword2, e_pos, e_year, e_path1, e_fpath2, l_msg):
    wd1 = e_keyword1.get()
    wd2 = e_keyword2.get()

    if wd1:
        wd = wd_split_dou(wd1, num=1)
    elif wd2:
        wd = wd_split_dou(wd2, num=2)
    else:
        wd = '("氢能+供应链")'

    pos = e_pos.get()
    if pos:
        pos = int(pos)
    else:
        pos = 0

    year = e_year.get()
    if not year:
        year = '2021'

    edge_driver_path = e_path1.get()
    edge_driver_path = fr'{edge_driver_path}'
    if not edge_driver_path:
        dir = os.path.dirname(os.path.abspath(__file__))
        edge_driver_path = os.path.join(dir, 'msedgedriver.exe')
    else:
        edge_driver_path = os.path.join(edge_driver_path, 'msedgedriver.exe')

    now_time = str(time.strftime("%H_%M_%S", time.localtime(time.time())))
    fpath = e_fpath2.get()
    fpath = fr'{fpath}'

    print(f'\n如果路径无用，检查路径，{fpath}是否存在\n')
    if not fpath:
        dir = os.path.dirname(os.path.abspath(__file__))
        fpath = os.path.join(dir, f'result_{now_time}.txt')
    else:
        fpath = os.path.join(fpath, f'result_{now_time}.txt')

    page_num = 999
    try:
        d = BaiduXueshuAutomatic(edge_driver_path=edge_driver_path)
    except Exception as e:
        print(f'{edge_driver_path} 目录下没有msedgedriver.exe\n')
        print('停止运行，请看软件视频（文本）使用指南，下载（更新）Edge浏览器，并配置msedgedriver.exe的正确路径\n')
        print(f'错误信息：{e}\n')
        return

    time.sleep(1)
    try:
        code = d.run(wd, page_num, year, fpath, pos)
        if code == 0:
            l_msg['text'] = '成功获取所有期刊，成功使用记得打赏哦，谢谢！~\n'
        else:
            l_msg['text'] = f'异常终止，如果是手动强制停止请忽视\n'
    except KeyboardInterrupt:
        print('手动终止，可以前往软件重新输入检索词，重新运行软件\n')


def open_result(e_fpath2):
    dir = e_fpath2.get()
    latest_file = max([os.path.join(dir, f) for f in os.listdir(dir)], key=os.path.getctime)
    if os.path.exists(latest_file):
        os.startfile(latest_file)
    else:
        print(f'结果文件 {latest_file} 不存在。请检查路径是否正确。')


def open_json_cn():
    webbrowser.open("https://www.json.cn/")
