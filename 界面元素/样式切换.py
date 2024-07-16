import tkinter as tk
import json
import os

def load_style(style_file):
    with open(style_file, 'r') as file:
        style = json.load(file)
    return style

def apply_style(root, style):
    for widget in root.winfo_children():
        widget_type = widget.winfo_class()
        if widget_type in style:
            for key, value in style[widget_type].items():
                widget[key] = value

def switch_style():
    current_style = '默认模式.json' if switch_style.current_style == '暗夜模式.json' else '暗夜模式.json'
    style_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '资源', '风格配置', current_style)
    style = load_style(style_file)
    apply_style(tk._default_root, style)
    switch_style.current_style = current_style

switch_style.current_style = '默认模式.json'
