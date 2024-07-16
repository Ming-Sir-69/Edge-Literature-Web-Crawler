import threading

# 共享的停止标志
stop_flag = threading.Event()

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
