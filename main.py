# -*- coding: utf-8 -*-
"""电视模拟恐怖 v10.5 - game-horror.tv"""
import random, time, sys, os, json

RESET = "\033[0m"
COLOR = {"R":"\033[91m","G":"\033[92m","Y":"\033[93m","C":"\033[96m","W":"\033[97m","B":"\033[1m","D":"\033[2m","BL":"\033[5m"}

def clr(): os.system("cls" if os.name=="nt" else "clear")
def col(t,c=""):
    if not c: return t
    return "".join(COLOR.get(x,"") for x in c.split("+"))+t+RESET
def out(t): print(t); sys.stdout.flush()
def slp(s): time.sleep(s)

class Game:
    def __init__(self):
        self.running=True; self.tv_on=False; self.channel=0; self.volume=5
        self.sanity=100; self.time=0; self.door=False; self.win=False
        self.foot=0; self.evt=0; self.watched=0; self.clues=0
        self.diary=False; self.mute=False; self.disc=set(); self.week=1
        self.clears=0; self.last=""; self.con=False; self.tend=False
        self.saved=False; self.dn=0; self.cheat=False; self.mem=0
        self.ach=[]; self.phone=False
        self.items={"candle":99,"bear":99,"diary":99,"radio":99,"drug":99,"tea":99,"mirror":99,"tape":99}
        self.item_name={"candle":"🕯️蜡烛","bear":"🧸泰迪熊","diary":"📖日记本","radio":"📻收音机","drug":"💊安眠药","tea":"🍵热茶","mirror":"🪞镜子","tape":"📼录像带"}
        self.username="guest"; self.login_status="guest"; self.is_author=False
        self.already_logged_in=False
    def sanity_bar(self):
        f=int(self.sanity/10); bar="█"*f+"░"*(10-f)
        c="\033[91m" if self.sanity<30 else "\033[93m" if self.sanity<60 else "\033[92m"
        return c+"["+bar+"] "+str(self.sanity)+"%"
    def vol_bar(self):
        bar="█"*self.volume+"░"*(10-self.volume)
        return "\033[96m["+bar+"] "+str(self.volume)+"/10"+RESET

SAVE_DIR="./saves"
def ensure_dir():
    if not os.path.exists(SAVE_DIR): os.makedirs(SAVE_DIR)
def save_path(n): return SAVE_DIR+"/"+n+".json"
def save_game(g):
    if g.username.startswith("guest"): return
    ensure_dir()
    d={"week":g.week,"clears":g.clears,"fragments":g.mem,"achievements":g.ach,"true_end":g.tend,"saved":g.saved,"discovered":list(g.disc),"clues":g.clues,"last_played":time.strftime("%Y-%m-%d %H:%M")}
    try:
        with open(save_path(g.username),"w",encoding="utf-8") as f: json.dump(d,f,indent=2,ensure_ascii=False)
    except: pass
def load_game(g):
    ensure_dir(); p=save_path(g.username)
    if os.path.exists(p):
        try:
            with open(p,"r",encoding="utf-8") as f: d=json.load(f)
            g.week=d.get("week",1); g.clears=d.get("clears",0); g.mem=d.get("fragments",0)
            g.ach=d.get("achievements",[]); g.tend=d.get("true_end",False); g.saved=d.get("saved",False)
            g.disc=set(d.get("discovered",[])); g.clues=d.get("clues",0)
            clr(); out(col("  📂 存档已加载: "+g.username,"G"))
            out(col("  周目"+str(g.week)+" | 通关"+str(g.clears)+"次","C"))
            if g.clears>=2: out(col("  🏆 怀旧档已就绪","Y+B"))
            slp(2)
        except: out(col("  ⚠️ 存档损坏","Y")); slp(1)

def login(g):
    if g.already_logged_in: return True
    clr()
    out(col("╔══════════════════════════════════════╗","C"))
    out(col("║  🔐 电视模拟恐怖 · 登录              ║","C+B"))
    out(col("╠══════════════════════════════════════╣","C"))
    out(col("║  输入密码解锁对应账号                ║","W"))
    out(col("║  直接回车 → 游客模式                ║","D"))
    out(col("╚══════════════════════════════════════╝","C"))
    ACCOUNTS={"tvhorror2024":("作者_本地",True),"liguo666":("LiGuo",True),"player2":("小明",False),"guest123":("访客",False)}
    try: pwd=input(col("\n  密码: ","C")).strip()
    except: pwd=""
    if pwd in ACCOUNTS:
        name,is_author=ACCOUNTS[pwd]
        g.username=name; g.login_status="author" if is_author else "user"; g.is_author=is_author
        if is_author: g.cheat=True; g.sanity=120; [g.items.__setitem__(k,99) for k in g.items]
        clr(); out(col("✅ 欢迎 "+name,"G")); slp(1.5)
    elif pwd=="":
        g.username="guest_"+str(random.randint(1000,9999))
        clr(); out(col("👤 游客模式","Y")); slp(1)
    else:
        g.username="guest_"+str(random.randint(1000,9999))
        clr(); out(col("❌ 密码错误 → 游客","Y")); slp(1)
    g.already_logged_in=True; load_game(g); return True

def get_channel(ch,g):
    if ch==0: return "\n".join("".join(random.choice("░▒▓█ ") for _ in range(46)) for _ in range(10))
    if ch==1: return "\n\n  天气预报\n  零下十二度 · 今晚不要出门"
    if ch==2: return "\n\n  🎬 深夜电影\n  《午夜凶铃》倒放版"
    if ch==3: return "\n\n  📰 紧急新闻\n  本市又一人失踪于家中电视前"
    if ch==4: return "\n\n  📡 教育频道\n  1953年废弃广播塔"
    if ch==5: return "\n\n  🧽 午夜卡通\n  海绵宝宝的脸裂开了"
    if ch==6: return '\n\n  🛒 午夜购物\n  "拨打 666-6666"'
    if ch==7: return '\n\n  📺 测试图案\n  '+col('"你锁门了吗？"',"Y+BL")
    if ch==8: return "\n\n  📼 纪录片\n  信号来自地下六米"
    if ch==9: return "\n\n  🎵 午夜旋律\n  《生日快乐》变成了你的名字"
    if ch==10: return "\n\n  📢 深夜广告\n  夜守者门锁"
    if ch==11: return "\n\n  🚔 警方频道\n  地址说的就是你家"
    if ch==12: return '\n\n  🧸 儿童频道\n  "他再也没有醒来"'
    if ch==13: g.sanity=max(0,g.sanity-15); g.evt+=1; return "\n\n  "+col("???","R+B+BL")+"\n  ███ 他就在你身后 ███"
    if ch==14: g.sanity=max(0,g.sanity-20); g.evt+=1; return "\n\n  "+col("???","R+B+BL")+"\n  ███ 直播：你的房间 ███"
    if ch==15: g.sanity=max(0,g.sanity-25); g.evt+=1; return "\n\n  "+col("???","R+B+BL")+"\n  ███ I AM HERE ███"
    if ch==16: g.sanity=max(0,g.sanity-30); g.evt+=1; return "\n\n  "+col("???","R+B+BL")+"\n  ███ I AM YOUR NEXT ███"
    if ch==777:
        if not g.tend and not g.saved: return "\n\n  📡 CH-777\n  ░▒▓█ 信号被干扰"
        return "\n\n  📡 CH-777 拯救者频道\n  拨打 777-777-7777\n  按 1 拨打"
    return "  [无信号]"

def render_tv(g):
    clr(); w=46
    print(col("╔"+"═"*w+"╗","D"))
    for line in get_channel(g.channel,g).strip().split("\n"):
        print(col("║","D")+line[:w].center(w)+col("║","D"))
    print(col("╚"+"═"*w+"╝","D"))
    print("\n  📺CH"+str(g.channel).zfill(2)+"  音量:"+g.vol_bar()+"  理智:"+g.sanity_bar())
    print(col("  🕐23:"+str(47+g.time%60).zfill(2)+"  脚步:"+str(g.foot)+"  事件:"+str(g.evt),"D"))
    if g.last: print(col("  ⚡"+g.last,"Y"))

def use_item(g,k):
    E={"candle":(15,"点燃蜡烛","暗处在动"),"bear":(20,"抱住泰迪熊","熊在盯着你"),"diary":(25 if g.dn==0 else 5,"翻开日记本","字迹潦草"),"radio":(10,"收音机音乐","低语声"),"drug":(30,"吞安眠药","跳60分钟"),"tea":(12,"热茶","温暖"),"mirror":(15,"镜子里的人笑了","电视闪烁"),"tape":(20,"录像带白噪音","无法换台")}
    if k not in g.items: return
    e=E[k]; g.sanity=min(120 if g.cheat else 100, g.sanity+e[0]); g.last=e[1]
    if k=="diary": g.diary=True; g.dn+=1; g.clues+=1
    elif k=="drug" and g.items[k]>0: g.time+=60; g.items[k]-=1
    elif k=="candle" and g.items[k]>0: g.items[k]-=1

def show_items(g):
    while True:
        clr(); out(col("🎒 物品栏\n","B"))
        keys=list(g.items.keys())
        for i,k in enumerate(keys,1): out("  "+str(i)+"."+g.item_name[k]+"(x"+("∞" if k in("bear","diary","radio") else str(g.items[k]))+")")
        out("\n0.返回")
        try: c=input(col("\n  > ","C")).strip()
        except: break
        if c=="0": break
        try:
            idx=int(c)-1
            if 0<=idx<len(keys): use_item(g, keys[idx])
            clr(); out(col("  "+g.last,"G")); slp(1)
        except: pass

def toggle_tv(g):
    if g.tv_on: g.tv_on=False; g.channel=0; clr(); out(col("📺 电视已关闭","D"))
    else: g.tv_on=True; g.channel=1; g.disc.add(1); clr(); out(col("📺 电视启动","D"))
    slp(0.8)
def change_ch(g,d):
    if not g.tv_on: return
    mx=17 if(g.tend or g.saved)else 16
    if d=="up": g.channel=(g.channel+1)%(mx+1)
    else: g.channel=(g.channel-1)%(mx+1)
    g.disc.add(g.channel); g.time+=1; g.watched+=1
def look_around(g):
    g.sanity=max(0,g.sanity-5); g.evt+=1
    for k,pct in [("candle",15),("drug",8),("tea",20),("mirror",10)]:
        if random.randint(1,100)<=pct and g.items[k]==0: g.items[k]=1; g.last="发现"+g.item_name[k]; break
    else: g.last=random.choice(["客厅一片漆黑","衣柜门开了一条缝","窗帘在动","背后有呼吸声","手机亮了"])
    out(col("👁️ "+g.last,"Y")); slp(1.2)
def toggle_door(g):
    g.door=not g.door; g.last="锁上了" if g.door else "解锁了"
    out(col("🔒"+g.last,"G" if g.door else "Y")); slp(0.8)
def toggle_win(g):
    if not g.win: g.win=True; g.sanity=max(0,g.sanity-10); g.last="窗户打开"; out(col("🪟 "+g.last,"R"))
    else: g.win=False; g.last="窗户关上"; out(col("🪟 "+g.last,"Y"))
    slp(1)

def dial_pad(g):
    g.phone=True; buf=""
    while True:
        clr(); out(col("📞 拨号\n","C")); out("  > "+buf+"_\n")
        out("  [1][2][3]  [4][5][6]  [7][8][9]  [*/0/#]")
        out("  666-6666 / 777-777-7777")
        try: k=input(col("\n  > ","C")).strip().lower()
        except: break
        if k in"0123456789": buf=(buf+k)[:12]
        elif k=="#": check_dial(g,buf); return
        elif k in("q","c"): g.phone=False; return

def check_dial(g,num):
    raw=num.replace("-","")
    if raw=="6666666":
        clr(); out(col("📞 666-6666...","C")); slp(2)
        out(col("📞 对面: 今晚我们会去你家。","R+B")); slp(2)
        g.sanity=max(0,g.sanity-10); g.evt+=1; g.last="666已拨打"; slp(2)
    elif raw=="7777777777":
        if not g.tend and not g.saved: out(col("📞 先活下来一次再说","Y")); slp(2)
        else: play_exorcism(g)
    else: out(col("📞 空号","Y")); slp(1)
    g.phone=False

def play_exorcism(g):
    g.saved=True; clr()
    for s in ["📞 777已接通","📞 对面: 驱鬼热线","⏳ 等待...","🔔 门铃响","🏠 三位大师到了","🔥 符咒贴满电视","💀 眼睛消失","✨ 烟雾散去"]:
        clr(); out(col("\n  "+s,"W")); slp(2)
    clr()
    out(col("╔══════════════════════════════════════╗","G"))
    out(col("║     🌟 隐藏结局：拯救者 🌟         ║","G+B"))
    out(col("╚══════════════════════════════════════╝","G"))
    out("\n  【🌟 拯救者已解锁】\n  【📺 CH-777 已开放】")
    slp(3)

def random_event(g):
    if random.randint(1,100)>35: return
    if not g.tv_on and random.randint(1,100)<=15: g.tv_on=True; g.channel=random.choice([1,3,7]); g.last="📺 电视自己开了"
    elif g.tv_on and g.channel!=13 and random.randint(1,100)<=8: g.channel=13; g.last="📺 跳到CH13"
    elif not g.door and random.randint(1,100)<=20: g.foot+=1; g.last="🚪 门外脚步声"
    else: g.sanity=max(0,g.sanity-random.randint(2,6)); g.last="🧠 眩晕"

def check_death(g):
    if g.sanity<=0: save_game(g); return ending(g,"💀 理智归零","他走了出来。\"终于可以聊聊了。\"")
    if g.foot>=12 and not g.door: save_game(g); return ending(g,"🚪 破门而入","门锁被撞开了。")
    if g.foot>=12 and g.door: g.foot=0; g.last="🚪 撞了一下没撞开"; return None
    if g.evt>=10: save_game(g); return ending(g,"👁️ 被标记","电视里的人记住了你。")
    if g.win and g.sanity<40: save_game(g); return ending(g,"🪟 渗透","苍白的手搭上窗台。")
    if g.watched>=120 and not g.diary: save_game(g); return ending(g,"📺 收视率","你成了下一个上一任观众。")
    if g.time>=500:
        g.tend=True
        if g.clears<2: g.clears+=1
        g.week+=1; save_game(g)
        return ending(g,"🌅 真结局","第一缕阳光照进客厅。\n你活下来了。","true")
    return None

def ending(g,title,desc,true=False):
    clr()
    c="\033[92m" if true else "\033[91m"
    print(c+"╔══════════════════════════════════════╗")
    print("║  "+title.center(30)+"  ║")
    print("╚══════════════════════════════════════╝"+RESET)
    print("\n  "+desc+"\n\n  [游戏结束]")
    return True

def console(g):
    g.con=True
    while True:
        clr(); out(col("🔧 控制台 [全权限]","G+B"))
        out("1.真结局 2.CH777 3.满血 4.物品x99 5.驱鬼 6.跳天亮 7.清脚步 8.全频道 9.无敌 0.退出")
        try: c=input(col("\n  > ","Y")).strip()
        except: break
        if c=="0": break
        if c=="1": g.tend=True
        if c=="2": g.tend=True; g.saved=True
        if c=="3": g.sanity=120
        if c=="4": [g.items.__setitem__(k,99) for k in g.items]
        if c=="5": play_exorcism(g)
        if c=="6": g.time=500
        if c=="7": g.foot=0; g.evt=0
        if c=="8": [g.disc.add(i) for i in range(18)]; g.tend=True
        if c=="9": g.sanity=999; g.foot=0; g.evt=0; g.win=False
        out(col("  ✅","G")); slp(0.4)

def homepage(g):
    if not login(g): return False
    while True:
        clr(); out(col("📺  电 视 模 拟 恐 怖  📺","R+B+BL")); out(col("TV ANALOG HORROR v10.5","D"))
        out(""); out(col("  "+g.username+" ["+( "作者" if g.is_author else "游客")+"]","G" if g.is_author else "Y"))
        out(""); out(col("  press enter 开始  (q退出)","W"))
        try: c=input(col("  > ","C")).strip().lower()
        except: return False
        if c=="": return True
        if c=="q": return False

def main_menu(g):
    while True:
        clr()
        out(col("  ╔══════════════════════════╗","D"))
        out(col("  ║      主 菜 单             ║","W+B"))
        out(col("  ╠══════════════════════════╣","D"))
        out(col("  ║  [1] 开始新游戏          ║","W"))
        out(col("  ║  [2] 多周目              ║","W"))
        out(col("  ║  [3] 设置                ║","W"))
        out(col("  ║  [4] 帮助                ║","W"))
        out(col("  ║  [5] 关于                ║","W"))
        out(col("  ║  [6] 退出                ║","W"))
        out(col("  ╚══════════════════════════╝","D"))
        if g.clears>=2: out(col("  🏆 怀旧档 | 通关"+str(g.clears)+"次","Y+B"))
        else: out(col("  第"+str(g.week)+"周目 | 通关"+str(g.clears)+"次","D"))
        try: c=input(col("\n  > ","C")).strip()
        except: return False
        if c=="1": return True
        if c=="2":
            if g.clears>=2:
                clr(); out(col("🏆 怀旧档\n这里你已经被通关过了\n这是怀旧档","Y+B")); slp(2)
                g.cheat=True; g.sanity=120; [g.items.__setitem__(k,99) for k in g.items]; [g.disc.add(i) for i in range(18)]; g.tend=True; g.saved=True
                return True
            elif g.clears>=1: return True
            else: out(col("❌ 先通关一次","R")); slp(1)
        if c=="3":
            clr(); out("  [1]登出 [2]重置存档 [0]返回")
            try: cc=input(col("\n  > ","C")).strip()
            except: cc=""
            if cc=="1": save_game(g); g.already_logged_in=False; return homepage(g)
            if cc=="2": g.mem=0; g.ach=[]; g.week=1; g.clears=0; g.tend=False; g.saved=False; [g.items.__setitem__(k,99) for k in g.items]; save_game(g); out(col("✅ 重置","G")); slp(0.8)
        if c=="4": clr(); out("目标:活到天亮(500分)\n门锁挡破门 安眠药+30跳60\n通关2次=怀旧档"); input(col("\n回车返回","D"))
        if c=="5": clr(); out("📺 电视模拟恐怖 v10.5\ngame-horror.tv"); input(col("\n回车返回","D"))
        if c=="6": return False

def loop(g):
    while g.running:
        if g.tv_on: render_tv(g)
        else:
            clr(); out(col("📺 电视已关闭","D"))
            out(col(" 理智:"+g.sanity_bar()+" 时间:23:"+str(47+g.time%60).zfill(2),"D"))
            if g.last: out(col(" ⚡"+g.last,"Y"))
        random_event(g)
        d=check_death(g)
        if d: g.running=False; break
        try: cmd=input(col("\n  > ","C")).strip().lower()
        except: g.running=False; break
        if cmd=="~~": console(g); continue
        if cmd=="q": g.running=False
        elif cmd in("w","↑"): change_ch(g,"up")
        elif cmd in("s","↓"): change_ch(g,"down")
        elif cmd in("d","→"): g.volume=min(10,g.volume+1)
        elif cmd in("a","←"): g.volume=max(0,g.volume-1)
        elif cmd=="t": toggle_tv(g)
        elif cmd=="l": look_around(g)
        elif cmd=="o": toggle_door(g)
        elif cmd=="v": toggle_win(g)
        elif cmd=="i": show_items(g)
        elif cmd=="p": dial_pad(g)
        elif cmd=="1" and g.channel==777 and(g.tend or g.saved): play_exorcism(g)

def main():
    g=Game()
    try: from trailer import play as play_trailer
    except ImportError: play_trailer=lambda: None
    if not homepage(g): return
    if not main_menu(g): return
    play_trailer()
    clr(); out(col("╔══════════════════════════╗","R+B"))
    out(col("║      序 章 · 深 夜 来 电      ║","R+B"))
    out(col("╚══════════════════════════╝","R+B"))
    out("\n13楼公寓。电视刚刚自己关上。镜子里没有你的倒影。\n今晚你决定不再逃避。")
    out(col("\n按回车开始...","C"))
    try: input()
    except: pass
    loop(g)
    save_game(g)
    clr(); out(col("📺 结算\n","R+B"))
    out(" 存活"+str(g.time)+"分 | 脚步"+str(g.foot)+" | 事件"+str(g.evt))
    out(" | 周目"+str(g.week)+" | 通关"+str(g.clears)+"次")
    if g.clears>=2: out(col("\n🏆 怀旧档就绪","Y+B"))
    out("\n\n restart重来 / 回车退出:")
    try:
        a=input().strip().lower()
        if a in("restart","r"): main()
    except: pass

if __name__=="__main__": main()