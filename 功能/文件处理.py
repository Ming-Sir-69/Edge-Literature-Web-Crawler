import os

def open_result():
    result_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '搜索结果')
    result_files = [f for f in os.listdir(result_dir) if f.startswith('result') and f.endswith('.txt')]
    if result_files:
        latest_result = max(result_files, key=lambda f: os.path.getctime(os.path.join(result_dir, f)))
        os.startfile(os.path.join(result_dir, latest_result))
    else:
        print("没有找到搜索结果文件")
