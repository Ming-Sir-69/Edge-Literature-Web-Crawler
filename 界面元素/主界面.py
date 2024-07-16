import tkinter as tk
import os
from 界面元素.按钮处理 import reg, open_result, open_json_cn

class MainInterface:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1200x850')
        self.root.title('cyd的百宝箱，B站搜索，UID383551518，水论文的程序猿,铭铭优化版')

        default_driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '资源', '驱动')
        default_result_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '搜索结果')

        l_1 = tk.Label(root, text='B站主页链接更多视频工具（点击链接可复制）\n **个人开发，供粉丝/同学免费使用，侵权盗版必究**\n')
        l_1.config(fg='blue')
        l_1.grid(row=0, sticky=tk.W)

        l_7 = tk.Text(root, height=1)
        l_7.grid(row=0, column=1, sticky=tk.W)
        l_7.insert('1.0', 'https://space.bilibili.com/383551518')

        l_keyword1 = tk.Label(root, text='包含精确检索词\n(多个检索词以逗号，分隔）：')
        l_keyword1.grid(row=1, sticky=tk.W)
        self.e_keyword1 = tk.Entry(root)
        self.e_keyword1.grid(row=1, column=1, sticky=tk.W)

        l_keyword2 = tk.Label(root, text='包含至少一个检索词\n(多个检索词以逗号，分隔）：')
        l_keyword2.grid(row=2, sticky=tk.W)
        self.e_keyword2 = tk.Entry(root)
        self.e_keyword2.grid(row=2, column=1, sticky=tk.W)

        l_pos = tk.Label(root, text='出现检索词的位置在\n（输入0为位于标题，默认为0\n输入1为位于文章任何位置）')
        l_pos.grid(row=3, sticky=tk.W)
        self.e_pos = tk.Entry(root)
        self.e_pos.grid(row=3, column=1, sticky=tk.W)

        l_year = tk.Label(root, text='多少年之后\n（默认2021年之后）：')
        l_year.grid(row=4, sticky=tk.W)
        self.e_year = tk.Entry(root)
        self.e_year.grid(row=4, column=1, sticky=tk.W)

        l_path1 = tk.Label(root, text='msedgedriver.exe保存的文件夹地址 \n（****必填****）：')
        l_path1.grid(row=5, sticky=tk.W)
        self.e_path1 = tk.Entry(root)
        self.e_path1.grid(row=5, column=1, sticky=tk.W)
        self.e_path1.insert(0, default_driver_path)

        l_fpath2 = tk.Label(root, text='结果文件存放的文件夹地址 \n（****必填****）：')
        l_fpath2.grid(row=6, sticky=tk.W)
        self.e_fpath2 = tk.Entry(root)
        self.e_fpath2.grid(row=6, column=1, sticky=tk.W)
        self.e_fpath2.insert(0, default_result_path)

        b_l = tk.Label(root, text='程序启动后不要关掉Edge浏览器\n关掉它程序会立马停止')
        b_l.config(fg='red', font=18)
        b_l.grid(row=7, sticky=tk.W)
        b_login = tk.Button(root, text='点击运行软件（运行期间程序会假死，终端会打印结果，ctrl+c 关闭终端运行即恢复）', command=lambda: reg(self.e_keyword1, self.e_keyword2, self.e_pos, self.e_year, self.e_path1, self.e_fpath2, self.l_msg))
        b_login.grid(row=7, column=1, sticky=tk.W)
        b_login.config(fg='red')

        l_5 = tk.Label(root, text='')
        l_5.grid(row=8, sticky=tk.W)

        b_open = tk.Button(root, text='打开结果', command=lambda: open_result(self.e_fpath2))
        b_open.grid(row=9, column=1, sticky=tk.W)
        b_open.config(fg='green')

        b_json = tk.Button(root, text='结构化', command=open_json_cn)
        b_json.grid(row=9, column=2, sticky=tk.W)
        b_json.config(fg='green')

        l_66 = tk.Label(root, text='使用指南视频链接（点击链接可复制）：')
        l_66.grid(row=10, sticky=tk.W)
        l_7 = tk.Text(root, height=1)
        l_7.grid(row=10, column=1, sticky=tk.W)
        l_7.insert('1.0', 'https://www.bilibili.com/video/BV1TP411U7P8')

        l_66 = tk.Label(root, text='json格式化网站链接：')
        l_66.grid(row=11, sticky=tk.W)
        l_7 = tk.Text(root, height=1)
        l_7.grid(row=11, column=1, sticky=tk.W)
        l_7.insert('1.0', 'https://www.json.cn/')

        l_66 = tk.Label(root, text='使用指南文本下载链接（点击链接可复制）：')
        l_66.grid(row=12, sticky=tk.W)
        l_7 = tk.Text(root, height=1)
        l_7.grid(row=12, column=1, sticky=tk.W)
        l_7.insert('1.0', 'https://imgmd.oss-cn-shanghai.aliyuncs.com/qikan-sousuo-zhinan.pdf')

        l_66 = tk.Label(root, text='软件问题汇总及解决方法(实时更新)：')
        l_66.grid(row=13, sticky=tk.W)
        l_7 = tk.Text(root, height=1)
        l_7.grid(row=13, column=1, sticky=tk.W)
        l_7.insert('1.0', 'https://imgmd.oss-cn-shanghai.aliyuncs.com/xk-problem-sum.pdf')

        l_msg = tk.Label(root, text='')
        l_msg.grid(row=14)
        l_msg.config(fg='red', font=35)

        self.l_msg = l_msg

def main():
    root = tk.Tk()
    app = MainInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
