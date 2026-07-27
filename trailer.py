# -*- coding: utf-8 -*-
"""
📺 电视模拟恐怖 - 预告片模块 v5.0
可单独运行: python trailer.py
可被主程序调用: from trailer import show_trailer
"""

import time
import sys
import os

# ========== 颜色工具 ==========
def _c(text, color=""):
    if not color:
        return text
    codes = {
        "red": "\033[91m", "yellow": "\033[93m", "cyan": "\033[96m",
        "white": "\033[97m", "dim": "\033[2m", "bold": "\033[1m",
        "blink": "\033[5m", "reset": "\033[0m",
    }
    result = ""
    for part in color.split("+"):
        result += codes.get(part, "")
    return f"{result}{text}{codes['reset']}"

def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def _center(text, width=52):
    return text.center(width)

# ========== 预告片主体 ==========
def show_trailer():
    """电影级预告片 - 播完自动返回"""
    try:
        _clear()
    except:
        pass

    # 第一幕：标题闪烁
    for _ in range(3):
        try:
            print(_center(_c("📺  电 视 模 拟 恐 怖  📺", "red+bold+blink")))
            time.sleep(0.4)
            _clear()
            time.sleep(0.2)
        except:
            pass

    try:
        print(_center(_c("TV SIMULATOR HORROR", "dim")))
        time.sleep(1.0)
        _clear()
    except:
        pass

    # 第二幕：制作名单
    credits = [
        ("一部关于 电视 的电影", "white"),
        ("", ""),
        ("导演: 你的大脑", "dim"),
        ("主演: 你", "dim"),
        ("特别出演: 频道13", "red"),
        ("摄影: 你手机的前置摄像头", "dim"),
        ("音效: 你家的电路", "dim"),
        ("技术支持: 1953年的广播塔", "dim"),
    ]
    for text, color in credits:
        try:
            print(_center(_c(text, color)))
            time.sleep(0.6)
        except:
            pass
    time.sleep(1.0)

    # 第三幕：警告
    try:
        _clear()
        print(_center(_c("⚠ 以下画面可能引起不适 ⚠", "yellow+bold")))
        time.sleep(0.8)
        print(_center(_c("建议佩戴耳机 · 暗光环境体验", "dim")))
        time.sleep(0.6)
        print(_center(_c("未满18岁请在家长陪同下游玩", "dim")))
        time.sleep(1.5)
    except:
        pass

    # 第四幕：预告片段
    scenes = [
        "2024年11月15日",
        "周五 深夜 23:47",
        "你独自在家",
        "",
        '"你关掉了电视"',
        '"但你还是听到了笑声"',
        "",
        ('「频道13」← 它不是电视台播的', "red+bold"),
        ('「是上一任观众录的」', "red+bold"),
        "",
        ('他在你身后', "blink+red"),
        ('他在门后', "blink+red"),
        ('他在衣柜里', "blink+red"),
        ('他在电视里', "blink+red"),
        "",
        ('「不要相信电视里说的话」', "yellow+bold"),
        ('「手电筒是命」', "yellow+bold"),
        '"遥控器也在发抖"',
        '"另外5个频道...是给你看的"',
        '"每次死亡都会回到今晚"',
        '"8种结局，你能在天亮前逃出去吗？"',
    ]

    for scene in scenes:
        try:
            _clear()
            if isinstance(scene, tuple):
                print(_center(_c(scene[0], scene[1])))
            else:
                c = "cyan" if scene.startswith('"') else "white"
                print(_center(_c(scene, c)))
            time.sleep(0.35)
        except:
            pass

    # 第五幕：倒计时
    for i in [3, 2, 1]:
        try:
            _clear()
            print(_center(_c(str(i), "red+bold+blink")))
            time.sleep(0.8)
        except:
            pass

    # 第六幕：最终标题
    try:
        _clear()
        print()
        print(_center(_c("📺  电 视 模 拟 恐 怖  📺", "red+bold")))
        print()
        print(_center(_c("press enter to begin", "dim")))
        print(_center(_c("（输入 q 可跳过预告片）", "dim")))
        print()

        try:
            choice = input().strip().lower()
            if choice == 'q':
                return
        except (EOFError, KeyboardInterrupt):
            pass
    except:
        pass

# ========== 独立运行入口 ==========
if __name__ == "__main__":
    try:
        show_trailer()
    except KeyboardInterrupt:
        _clear()
        print("\n  " + _c("预告片被中断", "dim"))
