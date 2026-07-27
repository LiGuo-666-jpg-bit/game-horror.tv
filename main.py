# -*- coding: utf-8 -*-
"""📺 电视模拟恐怖 v5.0 - 主程序"""
import random,time,sys,os

try: from trailer import show_trailer
except: def show_trailer(): pass

# 颜色
R="\033[91m";G="\033[92m";Y="\033[93m";C="\033[96m";W="\033[97m";B="\033[1m";D="\033[2m";BL="\033[5m";RT="\033[0m";BG="\033[41m"

def clr(): os.system('cls' if os.name=='nt' else 'clear')
def col(t,c): return f"{c}{t}{RT}"
def cnt(t,w=50): return t.center(w)
def slp(t): time.sleep(t)

# 游戏状态
class G:
    def __init__(s):
        s.run=True;s.tv=False;s.ch=0;s.vol=5;s.san=100
        s.tm=0;s.fl=False;s.door=False;s.win=False
        s.phone=False;s.foot=0;s.evt=0;s.watch=0
        s.clues=0;s.diary=False;s.mute=False
        s.inv=0;s.dch=set();s.ach=[];s.wk=1;s.mem=0
        s.ph=0;s.last="";s.bear=1;s.candle=0
        s.med=0;s.tea=0;s.mirror=0;s.tape=0
        s.diary_n=0;s.tape_on=False;s.tape_tm=0
        s.c013=0

g=G()

def sbar(v,mx,ch='█'):
    f=int(v/mx*10);return col("["+ch*f+"░"*(10-f)+"]","\033[92m" if v>60 else "\033[93m" if v>30 else "\033[91m")+f" {v}%"

def rnd(t): print(t);sys.stdout.flush()
def tv(c):
    clr()
    w=46;print(col("╔"+"═"*w+"╗","\033[2m"))
    for l in c.strip().split("\n"):print(col("║","\033[2m")+l[:w].center(w)+col("║","\033[2m"))
    print(col("╚"+"═"*w+"╝","\033[2m"))
    print();print(col(f"  📺 CH{str(g.ch).zfill(2)} | {sbar(g.san,100)} | {sbar(g.vol,10)}",D))
    if g.last:print(col(f"  ⚡ {g.last}","\033[93m"))

# 频道
def ch_cont(ch):
    if ch==0: return "\n".join("".join(random.choice("░▒▓█ ")for _ in range(44))for _ in range(10))
    if ch==1: return "\n\n  天气预报\n\n  明日气温: 零下"+random.choice(["5","12","永远"])+"度\n  风力: 未知\n  \"今晚不要出门\""
    if ch==2: return "\n\n  🎬 深夜电影\n\n  "+("██ 她在往后爬 ██" if g.san<50 else "正在播放...\n画面有些模糊")
    if ch==3: return "\n\n  📰 紧急新闻\n\n  "+random.choice(["又一人失踪\n最后出现在家中看电视","警方:深夜请锁好门窗","广播塔发出异常信号"])
    if ch==4: return "\n\n  📖 教育频道\n\n  1978年废弃广播塔\n  位置: 你家楼下\n  状态: 从未拆除"
    if ch==5: return "\n\n  🧽 午夜卡通\n\n  "+("██ 他的脸裂开了 ██" if g.san<40 else "海绵宝宝深夜篇\n他笑着就不笑了")
    if ch==6: return "\n\n  🛒 午夜购物\n\n  \"拨打 666-6666\"\n  我们上门服务\n  ██ 请勿拨打 ██"
    if ch==7: return "\n\n  📺 测试图案\n\n  "+col('"你锁门了吗？"',"\033[93m+\033[5m")
    if ch==8: return "\n\n  📡 纪录片\n\n  信号来自地下六米\n  1953年广播塔\n  \"有人在下面\""
    if ch==9: return "\n\n  🎵 午夜旋律\n\n  正在播放\n  "+random.choice(["《生日快乐》","《两只老虎》","《小星星》"])
    if ch==10: return "\n\n  📢 深夜广告\n\n  夜守者门锁\n  你家装的正是这款\n  \"它能保护你吗\""
    if ch==11: return "\n\n  🚔 警方频道\n\n  警察在讨论\"那个房子\"\n  地址说的就是你家"
    if ch==12: return "\n\n  🧸 儿童频道\n\n  睡前故事:\n  \"他再也没有醒来\"\n  \"晚安\""
    if ch==13:
        g.san=max(0,g.san-15);g.evt+=1;g.c013+=1
        return f"\n\n  {col('???','\033[91m+\033[1m+\033[5m')}\n\n  ██████████████████████\n  ██  {col('他就在你身后','\033[91m+\033[5m')}  ██\n  ██████████████████████\n\n  \"你终于看见我了\""
    if ch==14:
        g.san=max(0,g.san-20);g.evt+=1
        return f"\n\n  {col('???','\033[91m+\033[1m+\033[5m')}\n\n  ██████████████████████\n  ██  {col('直播:你的房间','\033[93m+\033[5m')}  ██\n  ██████████████████████"
    if ch==15:
        g.san=max(0,g.san-25);g.evt+=1
        return f"\n\n  {col('???','\033[41m+\033[97m+\033[1m+\033[5m')}\n\n  ██  {col('I AM HERE','\033[97m+\033[1m')}  ██"
    if ch==16:
        g.san=max(0,g.san-30);g.evt+=1
        return f"\n\n  {col('???','\033[41m+\033[97m+\033[1m+\033[5m')}\n\n  ██  {col('I AM YOUR NEXT','\033[97m+\033[1m'])}  ██"
    return "  [无信号]"

# 物品效果
def use_item(name):
    eff={"🕯️ 蜡烛":(15,"你点燃了蜡烛。","暗处有东西在盯着你..."),
         "🧸 泰迪熊":(20,"你抱紧泰迪熊。","放下后熊在另一个位置看你。"),
         "📖 日记本":(25 if g.diary_n==0 else 5,"翻开日记...","字迹越来越潦草"),
         "📻 收音机":(10,"收音机里传来歌声。","信号里夹杂低语..."),
         "💊 安眠药":(30,"你吞下安眠药。","时间快进60分钟。"),
         "🍵 热茶":(12,"热茶温暖了胃。",""),
         "🪞 镜子":(15,"镜子里的人对你笑了。","电视闪烁了一下。"),
         "📼 录像带":(20,"插入录像带。白噪音。","锁定3分钟。")}
    if name not in eff: return "无效物品"
    s,m,side=eff[name]
    if name=="📖 日记本":g.diary=True;g.diary_n+=1;g.clues+=1
    elif name=="💊 安眠药":g.tm+=60;g.med=max(0,g.med-1)
    elif name=="🕯️ 蜡烛":g.candle=max(0,g.candle-1)
    elif name=="🧸 泰迪熊":pass
    g.san=min(100,g.san+s);g.last=m
    if side:g.last=side
    return m

# 操作
def act(k):
    if k=='t':
        g.tv=not g.tv
        g.ch=1 if g.tv else 0
        g.last="电视已"+"打开" if g.tv else "关闭"
    elif k in('w','up'):
        if g.tv:g.ch=(g.ch+1)%17;g.dch.add(g.ch);g.tm+=1;g.watch+=1
    elif k in('s','down'):
        if g.tv:g.ch=(g.ch-1)%17;g.dch.add(g.ch);g.tm+=1;g.watch+=1
    elif k in('d','right'):g.vol=min(10,g.vol+1)
    elif k in('a','left'):g.vol=max(0,g.vol-1);g.mute=g.vol==0
    elif k=='l':
        g.san=max(0,g.san-5);g.evt+=1
        g.last=random.choice(["客厅一片漆黑。","衣柜门开了一条缝。","窗帘在动。","手机亮了一下。","你背后有呼吸声。"])
    elif k=='f':g.fl=not g.fl;g.last="手电筒"+"打开" if g.fl else "关闭"
    elif k=='o':g.door=not g.door;g.last="门锁上了" if g.door else "门解锁了"
    elif k=='v':
        g.win=not g.win
        g.san=max(0,g.san-(10 if g.win else -5))
        g.last="窗户打开了" if g.win else "窗户关上了"
    elif k=='p':g.phone=not g.phone;g.last="电话响了" if g.phone else "电话停了"
    elif k=='m':g.mute=not g.mute;g.last="静音" if g.mute else "取消静音"
    elif k=='i':
        clr()
        rnd(col("🎒 物品栏:","\033[1m"))
        items=[("🕯️ 蜡烛",g.candle),("🧸 泰迪熊","∞"),("📖 日记本","∞"),("📻 收音机","∞"),("💊 安眠药",g.med),("🍵 热茶",g.tea),("🪞 镜子",g.mirror),("📼 录像带",g.tape)]
        for n,c in items:rnd(f"  {n} (x{c})")
        rnd(f"\n  理智: {sbar(g.san,100)}")
        rnd(f"  存活: {g.tm}分钟 | 频道: {len(g.dch)}/17")
        try:ch=input(col("\n  输入物品名使用 (或0返回): ","\033[96m")).strip()
        except:return
        if ch!='0':
            for n,_ in items:
                if ch in n or n in ch:
                    rnd(col("  "+use_item(n),"\033[92m"));time.sleep(1.5);return
            rnd(col("  未找到该物品","\033[91m"));time.sleep(1)
    elif k=='c':
        clr()
        rnd(col("📡 频道列表:","\033[1m"))
        for i in range(17):
            m="★" if i in g.dch else "?"
            d=" ☠️" if i>=13 else ""
            rnd(f"  CH{i:02d} {m} {d}")
        rnd(f"\n  已发现: {len(g.dch)}/17")
        try:input(col("\n  回车返回...","\033[2m"))
        except:pass
    elif k in('h','?'):
        clr()
        hlp="w/↑上一台 s/↓下一台 d/→音量+ a/←音量-\nt开关 l环顾 f手电 o门锁 v窗户\np电话 i物品 m静音 c列表 q退出"
        rnd(col("🎮 操作:\n\n  "+hlp.replace(" ","\n  "),"\033[1m"))
        try:input(col("\n  回车返回...","\033[2m"))
        except:pass

# 随机
def rand_evt():
    if random.randint(1,100)>35:return
    if not g.tv and random.randint(1,100)<=15:g.tv=True;g.ch=random.choice([1,3,7]);g.last="📺 电视自己开了"
    if g.tv and g.ch!=13 and random.randint(1,100)<=8:g.ch=13;g.last="📺 频道跳到了CH13"
    if not g.door and random.randint(1,100)<=20:g.foot+=1;g.last="🚪 门外有脚步声"
    if g.fl and random.randint(1,100)<=10:g.last="🔦 手电筒闪了一下"
    if random.randint(1,100)<=12:g.san=max(0,g.san-random.randint(2,6));g.last="🧠 你感到眩晕"

# 死亡
def check_die():
    if g.san<=0:return end_scene("💀 理智归零","他走出来坐在你旁边\"终于可以聊聊了\"","\033[91m")
    if g.foot>=12:return end_scene("🚪 破门而入","门锁被撞开\"我来找你了\"","\033[91m")
    if g.evt>=10:return end_scene("👁️ 被标记","无论逃到哪里他都知道\"跑不掉的\"","\033[91m")
    if g.win and g.san<40:return end_scene("🪟 渗透","一只苍白的手搭上窗台\"谢谢没关窗\"","\033[91m")
    if g.watch>=120 and not g.diary:return end_scene("📺 收视率","你成了下一个\"录制完成\"","\033[91m")
    if g.tm>=500:return end_scene("🌅 天亮","阳光照进客厅\"今晚还会再来\"","\033[92m",True)
    return False

def end_scene(ttl,desc,clr_code,good=False):
    clr()
    bar="╔══════════════════════════════════════╗"
    rnd(col(bar,"\033[91m"))
    rnd(col(f"║  {ttl}  ".center(36)+"║","\033[91m+\033[1m"))
    rnd(col(bar,"\033[91m"))
    rnd("\n  "+desc.replace("\n","\n  "))
    rnd(col("\n\n  [GAME OVER]","\033[91m+\033[1m"))
    g.run=False;return True

# 阶段
def phase():
    np=min(4,g.tm//60)
    if np>g.ph:
        g.ph=np
        clr()
        ps=["序章:你以为只是普通夜晚","第一章:电视播放不该播的","第二章:现实与电视模糊","第三章:它在靠近","终章:黎明前最后黑暗"]
        rnd(col("\n  📖 "+ps[g.ph]+"\n","\033[95m+\033[1m"));time.sleep(2)

# 主循环
def loop():
    while g.run:
        if g.tv:tv(ch_cont(g.ch))
        else:
            clr()
            rnd(col("  📺 电视已关闭","\033[2m"));print()
            rnd(col(f"  理智:{sbar(g.san,100)} | 时间:23:{47+g.tm%60:02d} | 脚步:{g.foot} | 事件:{g.evt}","\033[2m"))
            if g.last:rnd(col(f"  ⚡ {g.last}","\033[93m"))
        rand_evt();phase()
        if check_die():break
        try:cmd=input(col("  > ","\033[96m")).strip().lower()
        except:g.run=False;break
        if cmd in('q','quit'):g.run=False
        else:act(cmd)

# 主入口
def main():
    show_trailer()
    clr()
    story=f"\n{col('╔══════════════════════════════════════╗','\033[91m')}\n{col('║      序 章 · 深 夜 来 电      ║','\033[91m+\033[1m')}\n{col('╚══════════════════════════════════════╝','\033[91m')}\n\n{col('2024年11月15日,周五,23:30','\033[97m')}\n\nyi个人住在这栋老公寓的{col('13楼','\033[91m')}。\n昨晚{col('电视自己开了','\033[91m')}。\n\n你拔掉了电源。\n但你感觉{col('它还会回来','\033[91m')}。\n\n今晚你决定{col('不再逃避','\033[91m')}。\n\n{col('但是你忘了检查衣柜。','\033[93m')}\n\n{col('游戏开始。','\033[91m+\033[1m')}\n{col('按回车继续...','\033[96m')}\n"
    rnd(story)
    try:input()
    except:pass
    loop()
    clr()
    rnd(col("\n  感谢游玩 📺 电视模拟恐怖\n  github.com/LiGuo-666-jpg-bit/game-trailer\n","\033[2m"))

if __name__=='__main__':main()
