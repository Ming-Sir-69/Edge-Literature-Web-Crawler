import re
import requests
import json
import os
import urllib
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
import threading

stop_flag = threading.Event()

class BaiduXueshuAutomatic:

    def __init__(self, edge_driver_path: str) -> None:
        self.edge_driver_path = edge_driver_path
        self.browser: webdriver.Edge
        self._init_browser()

    def _init_browser(self) -> None:
        options = EdgeOptions()
        options.add_argument('window-size=1920x1080')  # 设置窗口大小
        options.add_argument('--disable-extensions')  # 禁用扩展
        options.add_argument('--disable-gpu')  # 禁用GPU
        options.add_argument('--no-sandbox')  # 无沙盒模式
        options.add_argument('--blink-settings=imagesEnabled=false')  # 禁用图片
        options.add_argument('--disable-javascript')  # 禁用JavaScript
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        self.browser = webdriver.Edge(service=EdgeService(executable_path=self.edge_driver_path), options=options)
        self.browser.implicitly_wait(3)  # 设置隐式等待时间
        self.wait = WebDriverWait(self.browser, 15)
        self.ac = ActionChains(self.browser)

    def _wait_by_xpath(self, pattern):
        self.wait.until(EC.presence_of_element_located((By.XPATH, pattern)))

    def is_contain_chinese(self, check_str):
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def run(self, wd, exact_wd, year=2021, fpath='result.txt', pos=0):
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        }

        first_paper = ''
        count = 0
        paper_count = 0
        con_count = 0
        chinese_count = 0
        english_count = 0

        all_dic = {
            'all_paper_num': 0,
            'English Journal': {},
            'Chinese Journal': {},
            'Conference': {},
        }

        if not os.path.exists(os.path.dirname(fpath)):
            os.makedirs(os.path.dirname(fpath))

        while count <= 999 and not stop_flag.is_set():
            if pos == 0:
                url = f'https://xueshu.baidu.com/s?wd=intitle:{wd}&wd={exact_wd}&pn={count}0&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&filter=sc_year%3D%7B{year}%2C%2B%7D&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&bcp=2&sc_hit=1'
            elif pos == 1:
                url = f'https://xueshu.baidu.com/s?wd={wd}&wd={exact_wd}&pn={count}0&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&filter=sc_year%3D%7B{year}%2C%2B%7D&sc_f_para=sc_tasktype%3D%7BfirstAdvancedSearch%7D&bcp=2&sc_hit=1'
            else:
                print('检索词只能是位于标题或者文章内，只能填0或1，按ctrl+c终止终端可重新查询\n')
                return

            url = urllib.request.quote(url, safe=";/?:@&=+$,", encoding="utf-8")

            try:
                self.browser.get(url)
            except:
                print(f'Edge浏览器被异常关闭，按ctrl+c终止终端可重新进入软件点击运行\n')
                break

            print(f'百度学术搜索第{count + 1}页（无搜索结果可以复制粘贴链接去浏览器查看）:\n {url}\n')

            try:
                first_urls = self.browser.find_elements(By.XPATH, '/html/body/div[1]/div[4]/div[3]/div[2]/div/div[@class="result sc_default_result xpath-log"]')
            except:
                print('请检查软件打开的浏览器是否被人为（异常）终止，是的话，按ctrl+c，重新运行软件，期间不要关闭浏览器。\n')
                continue

            if not first_urls:
                print(f'没有搜索结果，提前结束，按ctrl+c终止终端可重新查询\n')
                with open(fpath, 'w', encoding='utf8') as fw:
                    fw.write(json.dumps(all_dic, ensure_ascii=False))
                    fw.flush()
                return

            for ii, first_url in enumerate(first_urls):
                if stop_flag.is_set():
                    break

                if count == 0 and ii == 0:
                    with open(fpath, 'w', encoding='utf8') as fw:
                        fw.write(json.dumps(all_dic, ensure_ascii=False))
                        fw.flush()
                else:
                    with open(fpath, 'r', encoding='utf8') as fr:
                        all_dic = json.loads(fr.read())
                try:
                    paper_name = first_url.find_element(By.XPATH, 'div[1]/h3/a')
                    paper_link = paper_name.get_attribute("href")
                    paper_name = paper_name.text
                except:
                    print('请检查软件打开的Edge浏览器是否被人为（异常）终止，程序运行期间不要关闭Edge浏览器，谢谢配合。\n')
                    break

                if paper_link == first_paper:
                    count = 9999
                    break

                if ii == 0:
                    first_paper = paper_link

                try:
                    res1 = requests.get(paper_link, headers=headers).text
                except:
                    print(f'百度禁掉了你的网络，等一会，按ctrl+c终止终端可重新查询\n')
                    break

                journal_name = re.findall('<a class="journal_title".*?>(.*?)</a>', res1, re.S)

                if not journal_name:
                    continue
                journal_name = journal_name[0]

                paper_count += 1

                print(f'第{paper_count}篇论文')
                print(f'文献标题: {paper_name}')
                print(f'文献链接: {paper_link}')
                print(f'期刊名称: {journal_name}')

                if ': ' in journal_name:
                    journal_name = journal_name.split(': ')[0]

                if '&amp;' in journal_name:
                    journal_name = journal_name.replace('&amp;', '&')

                if '&#039;' in journal_name:
                    journal_name = journal_name.replace('&#039;', "'")

                if self.is_contain_chinese(journal_name):
                    print("Chinese journal don't check.")
                    journal_name = f'{journal_name}'
                    print(paper_name)
                    print(paper_link)
                    print(journal_name)
                    print('\n')

                    if not all_dic['Chinese Journal'].get(journal_name):
                        all_dic['Chinese Journal'][journal_name] = []

                    all_dic['Chinese Journal'][journal_name].append({paper_name: paper_link})

                    chinese_count += 1

                    all_dic['all_paper_num'] = {
                        'all_count': paper_count,
                        'English Journal count': english_count,
                        'Chinese Journal count': chinese_count,
                        'Conference count': con_count
                    }

                    for i in list(all_dic['Chinese Journal'].keys()):
                        if '共'in all_dic['Chinese Journal'][i][0]:
                            all_dic['Chinese Journal'][i][0] = f'共{len(all_dic["Chinese Journal"][i])-1}篇'
                        else:
                            all_dic['Chinese Journal'][i].insert(0, f"共1篇")

                    all_dic['Chinese Journal'] = {key: all_dic['Chinese Journal'][key] for key, value in sorted(all_dic['Chinese Journal'].items(), key=lambda x: x[1][0], reverse=True)}

                    all_dic = json.dumps(all_dic, ensure_ascii=False)
                    with open(fpath, 'w', encoding='utf8') as fw:
                        fw.write(all_dic)
                        fw.flush()

                    continue

                if 'Conference'in journal_name:
                    print("Conference don't check.")
                    journal_name = f'{journal_name}'
                    print(paper_name)
                    print(paper_link)
                    print(journal_name)
                    print('\n')

                    if not all_dic['Conference'].get(journal_name):
                        all_dic['Conference'][journal_name] = []

                    all_dic['Conference'][journal_name].append({paper_name: paper_link})

                    con_count += 1

                    all_dic['all_paper_num'] = {
                        'all_count': paper_count,
                        'English Journal count': english_count,
                        'Chinese Journal count': chinese_count,
                        'Conference count': con_count
                    }

                    for i in list(all_dic['Conference'].keys()):
                        if '共'in all_dic['Conference'][i][0]:
                            all_dic['Conference'][i][0] = f'共{len(all_dic["Conference"][i])-1}篇'
                        else:
                            all_dic['Conference'][i].insert(0, f"共1篇")

                    all_dic['Conference'] = {key: all_dic['Conference'][key] for key, value in sorted(all_dic['Conference'].items(), key=lambda x: x[1][0], reverse=True)}

                    all_dic = json.dumps(all_dic, ensure_ascii=False)
                    with open(fpath, 'w', encoding='utf8') as fw:
                        fw.write(all_dic)
                        fw.flush()

                    continue

                status_code = True
                cite_score = ''
                journal_split = ''
                journal_date = ''

                while status_code:
                    try:
                        post_dic = {'searchname': journal_name, 'searchsort': 'relevance'}
                        search_url = 'http://www.letpub.com.cn/index.php?page=journalapp&view=search'
                        res = requests.post(search_url, post_dic, headers=headers)
                    except Exception as e:
                        print(f'letpub禁掉了你的网络，等一会，按ctrl+c终止终端可重新查询\n{e}')
                        break

                    if res.status_code == 200:
                        status_code = False
                    else:
                        print(f'letpub禁掉了你的网络，等一会，{journal_name}')
                        break

                    second_search = re.findall('</style>.*?<tr>(.*?)</tr>', res.text, re.S)[0]
                    cite_score = re.findall('CiteScore:(\d+.\d+)', second_search, re.S)
                    journal_split = re.findall('(\d区)</td>', second_search, re.S)

                    journal_date = ''
                    fourth_search = re.findall('(<td.*?</td>)', second_search, re.S)
                    for i in fourth_search:
                        l = ['月', '周', 'eeks']
                        for j in l:
                            if j in i:
                                journal_date = re.findall('>(.*?)</td>', i, re.S)
                                break

                if cite_score and journal_split and journal_date:
                    journal_name = f'{journal_split[0]} Citescore:{cite_score[0]} 审稿周期:{journal_date[0]} {journal_name}'
                elif cite_score and journal_split:
                    journal_name = f'{journal_split[0]} Citescore:{cite_score[0]} 审稿周期:无记录 {journal_name}'
                elif cite_score:
                    journal_name = f'未收录 Citescore:{cite_score[0]} 审稿周期:无记录 {journal_name}'
                else:
                    journal_name = f'未收录 无Citescore 审稿周期:无记录 {journal_name}'

                print(f'文献标题: {paper_name}')
                print(f'文献链接: {paper_link}')
                print(f'期刊名称: {journal_name}\n')

                if not all_dic['English Journal'].get(journal_name):
                    all_dic['English Journal'][journal_name] = []

                all_dic['English Journal'][journal_name].append({paper_name: paper_link})

                english_count += 1

                all_dic['all_paper_num'] = {
                    'all_count': paper_count,
                    'English Journal count': english_count,
                    'Chinese Journal count': chinese_count,
                    'Conference count': con_count
                }

                all_dic['English Journal'] = {key: all_dic['English Journal'][key] for key in sorted(all_dic['English Journal'].keys())}

                for i in list(all_dic['English Journal'].keys()):
                    if '共'in all_dic['English Journal'][i][0]:
                        all_dic['English Journal'][i][0] = f'共{len(all_dic["English Journal"][i])-1}篇'
                    else:
                        all_dic['English Journal'][i].insert(0, f"共1篇")

                all_dic = json.dumps(all_dic, ensure_ascii=False)
                with open(fpath, 'w', encoding='utf8') as fw:
                    fw.write(all_dic)
                    fw.flush()

            count += 1

        print('成功获取所有期刊，成功使用记得打赏哦，谢谢！~')
        return 0

# 执行爬取任务
if __name__ == '__main__':
    edge_driver_path = 'path/to/msedgedriver.exe'  # Edge浏览器驱动路径
    wd = "绿氢，供应链"
    exact_wd = "氢能输送"
    year = 2021
    fpath = r'E:\你铭哥的联想拯救者\Desktop\找期刊文章（放桌面运行）\edge铭铭版\搜索结果\results_{time.strftime("%Y%m%d_%H%M%S")}.json'
    pos = 0  # 0表示检索词位于标题，1表示检索词位于全文

    crawler = BaiduXueshuAutomatic(edge_driver_path)
    try:
        crawler.run(wd, exact_wd, year, fpath, pos)
    except Exception as e:
        print(f'爬取过程中发生异常: {e}')
        with open(fpath, 'w', encoding='utf8') as fw:
            fw.write(json.dumps(crawler.all_dic, ensure_ascii=False))
            fw.flush()
        print(f'部分结果已保存到 {fpath}')
