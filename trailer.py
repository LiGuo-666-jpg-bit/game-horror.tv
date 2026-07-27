# -*- coding: utf-8 -*-
"""📺 电视模拟恐怖 - 预告片模块"""
import time,sys,os

def _c(t,c=""):
    if not c:return t
    m={"r":"\033[91m","y":"\033[93m","c":"\033[96m","w":"\033[97m","d":"\033[2m","b":"\033[1m","bl":"\033[5m","rt":"\033[0m","bg":"\033[41m"}
    return "".join(m.get(p,"") for p in c.split("+"))+t+"\033[0m"

def _clr():
    try:os.system('cls' if os.name=='nt' else 'clear')
    except:pass

def show_trailer():
    try:
        for _ in range(3):
            _clr();print(_c("📺  电 视 模 拟 恐 怖  📺","r+b+bl"));time.sleep(0.4)
            _clr();time.sleep(0.2)
        print(_c("TV SIMULATOR HORROR","d"));time.sleep(1);_clr()
        for t,cl in [("一部关于 电视 的电影","w"),("",""),("导演: 你的大脑","d"),("主演: 你","d"),("特别出演: 频道13","r"),("摄影: 你手机的前置摄像头","d"),("音效: 你家的电路","d"),("技术支持: 1953年的广播塔","d")]:
            print(_c(t,cl));time.sleep(0.6)
        time.sleep(1);_clr()
        print(_c("⚠ 以下画面可能引起不适 ⚠","y+b"));time.sleep(0.8)
        print(_c("建议佩戴耳机 · 暗光环境体验","d"));time.sleep(1);_clr()
        for s in ["2024年11月15日","周五 深夜 23:47","你独自在家","","\"你关掉了电视\"","\"但你还是听到了笑声\"","",_c('「频道13」← 它不是电视台播的',"r+b"),"他在你身后","他在门后","他在电视里","",_c('「手电筒是命」',"y+b"),'"8种结局，你能在天亮前逃出去吗？"']:
            _clr()
            if s.startswith("他在") or s.startswith("「手"):print(_c(s,"r+b+bl"))
            else:print(_c(s,"c" if s.startswith('"') else "w"))
            time.sleep(0.35)
        for i in [3,2,1]:
            _clr();print(_c(str(i),"r+b+bl"));time.sleep(0.8)
        _clr();print();print(_c("📺  电 视 模 拟 恐 怖  📺","r+b"));print();print(_c("press enter to begin","d"))
        try:
            if input().strip().lower()=='q':return
        except:pass
    except:pass

if __name__=='__main__':show_trailer()
