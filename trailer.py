# -*- coding: utf-8 -*-
"""电视模拟恐怖 - 预告片 v10.5"""
import time, os

def clr():
    os.system("cls" if os.name == "nt" else "clear")

def play():
    try:
        for _ in range(3):
            clr()
            print("📺  电 视 模 拟 恐 怖  ".center(50))
            time.sleep(0.4)
            clr()
            time.sleep(0.2)
        print("TV ANALOG HORROR".center(50))
        time.sleep(1)
        for t in ["一部关于电视的电影","","导演: 你的大脑","主演: 你","特别出演: 频道十三","1953年废弃广播塔","","仓库: game-horror.tv"]:
            print(t.center(50))
            time.sleep(0.5)
        time.sleep(0.8)
        clr()
        print("⚠ 以下画面可能引起不适 ".center(50))
        time.sleep(0.8)
        for s in ["2024年11月15日","周五 深夜 23:47","你独自在家",'"你关掉了电视"','"但你还是听到了笑声"',"「频道十三」← 不是电视台播的","「是上一任观众录制的」","他在你身后","他在门后","他在衣柜里","他在电视里",'「不要相信电视里说的话」','「手电筒是命」','"遥控器也在发抖"','"8种结局，天亮前逃出去？"']:
            clr()
            print(s.center(50))
            time.sleep(0.35)
        for i in [3,2,1]:
            clr()
            print(str(i).center(50))
            time.sleep(0.7)
        clr()
        print("")
        print("📺  电 视 模 拟 恐 怖  ".center(50))
        print("")
        print("按回车开始 (输入 q 跳过)".center(50))
        try:
            if input().strip().lower()=="q": return
        except: pass
    except: pass