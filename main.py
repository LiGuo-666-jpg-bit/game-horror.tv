# -*- coding: utf-8 -*-
"""
📺 电视模拟恐怖 v5.0 - 主程序（含理智回复系统）
依赖: trailer.py（同目录下）
运行: python main.py
"""

import random
import time
import sys
import os

# ========== 导入预告片 ==========
try:
    from trailer import show_trailer
except ImportError:
    def show_trailer():
        pass

# ========== 颜色常量 ==========
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
DIM = "\033[2m"
BLINK = "\033[5m"
RESET = "\033[0m"
BG_RED = "\033[41m"

# ========== 工具函数 ==========
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def color(text, c):
    return f"{c}{text}{RESET}"

def center(text, width=52):
    return text.center(width)

def sleep(t):
    time.sleep(t)

# ========== 游戏状态 ==========
class Game:
    def __init__(self):
        self.running = True
        self.tv_on = False
        self.channel = 0
        self.volume = 5
        self.sanity = 100
        self.time_minutes = 0
        self.flashlight_on = False
        self.door_locked = False
        self.window_open = False
        self.phone_ringing = False
        self.phone_answer_count = 0
        self.footsteps = 0
        self.events = 0
        self.watched_minutes = 0
        self.clues_found = 0
        self.diary_read = False
        self.diary_read_count = 0
        self.muted = False
        self.discovered_channels = set()
        self.achievements = []
        self.week = 1
        self.memory_fragments = 0
        self.phase = 0
        self.last_event = ""
        self.bear_moved = False
        self.candle_active = False
        self.skip_minutes = 0
        self.vhs_active = False
        self.vhs_remaining = 0
        self.ch13_count = 0
        # 物品栏
        self.items = {
            "🕯️ 蜡烛": 0,
            "🧸 泰迪熊": 1,  # 无限使用但每次有副作用
            "📖 日记本": 1,  # 无限但后续效果递减
            "📻 收音机": 1,  # 无限
            "💊 安眠药": 0,
            "🍵 热茶": 0,
            "🪞 镜子": 0,
            "📼 空白录像带": 0,
        }

    def sanity_bar(self):
        filled = int(self.sanity / 10)
        bar = "█" * filled + "░" * (10 - filled)
        c = RED if self.sanity < 30 else YELLOW if self.sanity < 60 else GREEN
        return f"{c}[{bar}] {self.sanity}%{RESET}"

    def volume_bar(self):
        filled = self.volume
        bar = "█" * filled + "░" * (10 - filled)
        return f"{CYAN}[{bar}] {self.volume}/10{RESET}"

# ========== 渲染 ==========
def 渲染(text):
    lines = text.split("\n")
    for line in lines:
        print(line)
    sys.stdout.flush()

def 渲染电视(内容, g):
    clear()
    w = 48
    print(color("╔" + "═" * w + "╗", DIM))
    lines_content = 内容.strip().split("\n")
    for cline in lines_content:
        padded = cline[:w].center(w)
        print(color("║", DIM) + padded + color("║", DIM))
    print(color("╚" + "═" * w + "╝", DIM))
    print()
    print(color(f"  📺 CH{str(g.channel).zfill(2)} | 音量:{g.volume_bar()} | 理智:{g.sanity_bar()}", DIM))
    print(color(f"  🕐 时间: 23:{47 + g.time_minutes % 60:02d} | 脚步:{g.footsteps} | 事件:{g.events}", DIM))
    if g.vhs_active:
        print(color(f"  📼 录像带播放中... ({g.vhs_remaining}分钟)", YELLOW))
    if g.last_event:
        print(color(f"  ⚡ {g.last_event}", YELLOW))
    print()

def progress_bar(current, total, width=30):
    filled = int(width * current / total)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {current}/{total}"

# ========== 频道内容 ==========
def get_channel_content(ch, g):
    if ch == 0:
        noise = ["░", "▒", "▓", "█", " "]
        return "\n".join("".join(random.choice(noise) for _ in range(46)) for _ in range(12))

    elif ch == 1:
        temps = ["零下5度", "零下12度", "永远冻结"]
        temp = temps[g.time_minutes % len(temps)]
        return f"\n\n  天气预报\n\n  明日气温: {temp}\n  风力: 未知方向\n  降水概率: 100%\n\n  \"今晚不要出门\""

    elif ch == 2:
        titles = ["《午夜凶铃》", "《闪灵》", "《咒怨》"]
        title = titles[g.time_minutes % len(titles)]
        if g.sanity < 50:
            return f"\n\n  {title} - 倒放版\n\n  ██████████████████████\n  ██ 她 在 往 后 爬 ██\n  ██████████████████████\n\n  \"你在看什么？\""
        return f"\n\n  {title}\n\n  正在播放中...\n  画面有些模糊"

    elif ch == 3:
        news = [
            "本市又一人失踪\n最后出现在家中看电视",
            "警方提醒: 深夜请锁好门窗\n不要接陌生电话",
            "广播塔发出异常信号\n来源不明"
        ]
        return f"\n\n  📰 紧急新闻\n\n  {news[g.time_minutes % len(news)]}\n\n  \"请市民注意安全\""

    elif ch == 4:
        return "\n\n  教育频道\n\n  1978年废弃广播塔历史\n\n  位置: 就在你家楼下\n  状态: 从未拆除\n  用途: 未知"

    elif ch == 5:
        if g.sanity < 40:
            return "\n\n  🧽 午夜卡通\n\n  ██████████████████████\n  ██ 他的脸裂开了  ██\n  ██████████████████████\n\n  \"准备好笑了吗？\""
        return "\n\n  🧽 午夜卡通\n\n  海绵宝宝深夜特别篇\n  他笑着笑着就不笑了"

    elif ch == 6:
        return "\n\n  🛒 午夜购物\n\n  \"只需拨打 666-6666\"\n  \"我们上门服务\"\n  \"24小时不打烊\"\n\n  ██████████████████████\n  ██ 请勿拨打此号码 ██\n  ██████████████████████"

    elif ch == 7:
        return f"\n\n  📺 测试图案\n\n  ░▒▓█▓▒░░▒▓█▓▒░\n  ░▒▓█▓▒░░▒▓█▓▒░\n\n  \"{color('你锁门了吗？', 'blink+yellow')}\""

    elif ch == 8:
        return "\n\n  📡 纪录片\n\n  信号来自地下六米处\n  来源: 1953年广播塔\n  状态: 仍在发射\n\n  \"有人在下面\""

    elif ch == 9:
        songs = ["《生日快乐》", "《两只老虎》", "《小星星》"]
        song = songs[g.time_minutes % len(songs)]
        if g.sanity < 50:
            return f"\n\n  🎵 午夜旋律\n\n  {song}\n\n  歌词变成了你的名字\n  \"{get_username()}\""
        return f"\n\n  🎵 午夜旋律\n\n  正在播放: {song}\n  音质: 一般"

    elif ch == 10:
        return "\n\n  📢 深夜广告\n\n  推销: 夜守者门锁\n  你家装的正是这款\n\n  \"它能保护你吗？\""

    elif ch == 11:
        return "\n\n  🚔 警方频道\n\n  警察在讨论\"那个房子\"\n  地址说的就是你家\n\n  \"他还在里面\""

    elif ch == 12:
        return "\n\n  🧸 儿童频道\n\n  睡前故事:\n  \"从前有个小朋友\n  他再也没有醒来\"\n\n  \"晚安\""

    elif ch == 13:
        g.sanity = max(0, g.sanity - 15)
        g.events += 1
        g.ch13_count += 1
        return f"\n\n  {color('???', 'red+bold+blink')}\n\n  ██████████████████████\n  ██  {color('他就在你身后', 'blink+red')}  ██\n  ██████████████████████\n\n  \"你终于看见我了\""

    elif ch == 14:
        g.sanity = max(0, g.sanity - 20)
        g.events += 1
        return f"\n\n  {color('???', 'red+bold+blink')}\n\n  ██████████████████████\n  ██  {color('直播画面:', 'blink+yellow')}  ██\n  ██  {color('你的房间', 'white')}     ██\n  ██████████████████████\n\n  \"我看着你睡觉\""

    elif ch == 15:
        g.sanity = max(0, g.sanity - 25)
        g.events += 1
        return f"\n\n  {color('???', 'bg_red+white+bold+blink')}\n\n  ██████████████████████\n  ██  {color('I AM HERE', 'white+bold')}     ██\n  ██████████████████████\n\n  {color('他在你身边', 'blink+red')}"

    elif ch == 16:
        g.sanity = max(0, g.sanity - 30)
        g.events += 1
        return f"\n\n  {color('???', 'bg_red+white+bold+blink')}\n\n  ██████████████████████\n  ██  {color('I AM YOUR NEXT', 'white+bold')} ██\n  ██████████████████████\n\n  {color('游戏结束', 'blink+red')}"

    return "  [无信号]"

def get_username():
    try:
        return os.getlogin()
    except:
        return "玩家"

# ========== 开场剧情 ==========
def 开场剧情(g):
    clear()
    title = color("╔══════════════════════════════════════╗\n║      序 章 · 深 夜 来 电      ║\n╚══════════════════════════════════════╝", "red+bold")
    story = f"""
{title}

{color("2024年11月15日，周五，23:30", "white")}

你一个人住在这栋老公寓的{color("13楼", "red")}。
今天是发薪日，但你一点也高兴不起来。
因为昨晚......{color("电视自己开了", "red")}。

你清楚地记得自己睡前关了它。
但凌晨三点，你被{color("声音", "red")}吵醒了。
不是闹钟，不是手机。
是{color("电视里的笑声", "red")}。

你冲出卧室，客厅的电视正亮着。
屏幕上是一个你从未见过的频道。
画面很简单，一个空房间。
然后镜头缓缓转向一面镜子。
镜子里......{color("没有你", "red")}。

你拔掉了电视的电源。
但你感觉......{color("它还会回来", "red")}。

今晚，你决定{color("不再逃避", "red")}。
你要搞清楚......{color("电视里到底有什么", "red")}。

你坐在沙发上，{color("遥控器", "green")}就在手边。
窗外下起了雾。
手机信号{color("只有一格", "red")}。
门锁上了。窗户关了。手电筒满电。

{color("但是你忘了检查衣柜。", "yellow")}

23:47。电视屏幕反射着客厅的灯光。
你拿起遥控器。
你知道......{color("今晚不会太平", "red")}。

{color("游戏开始。", "red+bold")}
{color("按回车继续...", "cyan")}
"""
    渲染(story)
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass

# ========== 物品系统 ==========
def 使用物品(g, item_name):
    """使用物品并施加效果和副作用"""
    effects = {
        "🕯️ 蜡烛": {
            "sanity": 15, "msg": "你点燃了蜡烛。暖黄色的光驱散了一些恐惧。",
            "side": "光线昏暗，你感觉有什么东西在暗处盯着你...",
            "side_effect": lambda: setattr(g, 'candle_active', True)
        },
        "🧸 泰迪熊": {
            "sanity": 20, "msg": "你紧紧抱住泰迪熊。它很温暖。",
            "side": "你放下熊后，发现它在看你。它的眼睛转了一个角度。",
            "side_effect": lambda: setattr(g, 'bear_moved', True)
        },
        "📖 日记本": {
            "sanity": 25, "msg": "你翻开日记本...字迹越来越潦草。",
            "side": "\"不要看电视。不要相信频道13。他不是演员。\"",
            "side_effect": None
        },
        "📻 收音机": {
            "sanity": 10, "msg": "收音机里传出一首熟悉的歌。让你稍微放松了些。",
            "side": "信号里夹杂着低语声...好像在叫你的名字。",
            "side_effect": None
        },
        "💊 安眠药": {
            "sanity": 30, "msg": "你吞下安眠药。世界开始模糊...时间快进了。",
            "side": "你跳过了60分钟。但也错过了收集线索的机会。",
            "side_effect": lambda: [setattr(g, 'time_minutes', g.time_minutes + 60),
                                     setattr(g, 'skip_minutes', 60)]
        },
        "🍵 热茶": {
            "sanity": 12, "msg": "热茶温暖了你的胃。你深呼吸了一次。",
            "side": "", "side_effect": None
        },
        "🪞 镜子": {
            "sanity": 15, "msg": "你盯着镜子。镜子里的人对你笑了。你也笑了。",
            "side": "电视画面闪烁了一下，变成了镜子反射...但里面的人没动。",
            "side_effect": None
        },
        "📼 空白录像带": {
            "sanity": 20, "msg": "插入录像带。电视开始播放白噪音。很催眠。",
            "side": "录像带将持续3分钟，期间无法换台。但很安全。",
            "side_effect": lambda: [setattr(g, 'vhs_active', True),
                                     setattr(g, 'vhs_remaining', 3)]
        },
    }

    # 检查数量
    infinite = ["🧸 泰迪熊", "📖 日记本", "📻 收音机"]
    if item_name not in infinite and g.items.get(item_name, 0) <= 0:
        return "物品数量不足！", False, ""

    effect = effects[item_name]
    g.sanity = min(100, g.sanity + effect["sanity"])

    # 特殊逻辑
    if item_name == "📖 日记本":
        g.diary_read = True
        g.diary_read_count += 1
        g.clues_found += 1
        if g.diary_read_count > 1:
            # 后续递减
            g.sanity = max(0, g.sanity - 5)  # 回退部分
            actual_gain = 5
        else:
            actual_gain = 25
        effect["msg"] = f"你再次翻开日记本...又发现一条线索。(+{actual_gain} 理智)"

    if item_name == "🧸 泰迪熊" and g.bear_moved:
        effect["side"] = "熊又换了个位置。这次它在看着门。"

    if item_name == "🕯️ 蜡烛":
        g.items["🕯️ 蜡烛"] = max(0, g.items["🕯️ 蜡烛"] - 1)
    if item_name == "💊 安眠药":
        g.items["💊 安眠药"] = 0
    if item_name == "🍵 热茶":
        g.items["🍵 热茶"] = 0
    if item_name == "🪞 镜子":
        g.items["🪞 镜子"] = 0
    if item_name == "📼 空白录像带":
        g.items["📼 空白录像带"] = 0

    # 副作用执行
    if effect["side_effect"]:
        effect["side_effect"]()

    return effect["msg"], True, effect["side"]

def 动作_物品栏(g):
    while True:
        clear()
        text = color("🎒 物品栏:\n\n", "bold")
        item_list = list(g.items.keys())
        for i, item in enumerate(item_list, 1):
            count = g.items[item]
            if item in ["🧸 泰迪熊", "📖 日记本", "📻 收音机"]:
                count_str = "∞"
            else:
                count_str = str(count)
            # 理智回复提示
            hints = {
                "🕯️ 蜡烛": "+15", "🧸 泰迪熊": "+20", "📖 日记本": "+25→+5",
                "📻 收音机": "+10", "💊 安眠药": "+30", "🍵 热茶": "+12",
                "🪞 镜子": "+15", "📼 空白录像带": "+20"
            }
            hint = hints.get(item, "")
            text += f"  {i}. {item} (x{count_str}) {color(hint, 'green')}\n"

        text += f"\n  0. 返回\n"
        text += color(f"\n  当前理智: {g.sanity_bar()}\n", "white")
        text += color(f"  存活时间: {g.time_minutes} 分钟 | 已发现频道: {len(g.discovered_channels)}/17", "dim")
        渲染(text)

        try:
            choice = input(color("\n  选择物品编号使用 (0返回): ", "cyan")).strip()
        except (EOFError, KeyboardInterrupt):
            break

        if choice == '0':
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(item_list):
                msg, ok, side = 使用物品(g, item_list[idx])
                clear()
                if ok:
                    渲染(color(f"  ✅ {msg}\n", "green"))
                    if side:
                        sleep(1.0)
                        渲染(color(f"  ⚠️ {side}\n", "yellow"))
                    sleep(0.5)
                    渲染(color(f"  理智: {g.sanity_bar()}", "white"))
                    g.last_event = msg
                else:
                    渲染(color(f"  ❌ {msg}\n", "red"))
                渲染(color("\n\n  按回车继续...", "dim"))
                try:
                    input()
                except (EOFError, KeyboardInterrupt):
                    pass
            else:
                渲染(color("  无效选择！", "red"))
                sleep(1)
        except ValueError:
            渲染(color("  请输入数字！", "red"))
            sleep(1)

# ========== 操作函数 ==========
def 动作_开关电视(g):
    if g.tv_on:
        g.tv_on = False
        g.channel = 0
        clear()
        渲染(color("📺 电视已关闭。屏幕反射着微弱的月光。", "dim"))
        sleep(1)
    else:
        g.tv_on = True
        g.channel = 1
        g.discovered_channels.add(1)
        clear()
        渲染(color("📺 电视嗡的一声启动了...", "dim"))
        sleep(0.8)

def 动作_换台(g, direction):
    if not g.tv_on:
        return
    if g.vhs_active:
        渲染(color("  📼 录像带播放中，无法换台...", "yellow"))
        sleep(1)
        return
    if direction == 'up':
        g.channel = (g.channel + 1) % 17
    else:
        g.channel = (g.channel - 1) % 17
    g.discovered_channels.add(g.channel)
    g.time_minutes += 1
    if g.tv_on:
        g.watched_minutes += 1

def 动作_音量(g, direction):
    if direction == 'up' and g.volume < 10:
        g.volume += 1
    elif direction == 'down' and g.volume > 0:
        g.volume -= 1
    if g.volume == 0:
        g.muted = True
    else:
        g.muted = False

def 动作_环顾(g):
    g.sanity = max(0, g.sanity - 5)
    g.events += 1

    # 基础场景
    base_scenes = [
        "客厅一片漆黑，只有电视的光在墙上跳动。",
        "走廊尽头的衣柜门...好像开了一条缝。",
        "窗帘在动。明明窗户关着。",
        "茶几上的手机亮了一下。没有通知。",
        "你背后有呼吸声。你转身——什么都没有。",
        "厨房的水龙头在滴水。你确定关了它。",
        "天花板传来脚步声。楼上应该没人。",
    ]
    result = random.choice(base_scenes)

    # 泰迪熊移动
    if g.bear_moved:
        result += "\n\n  🧸 泰迪熊换了位置。它在看着门。"

    # 蜡烛副作用
    if g.candle_active and random.randint(1, 100) <= 25:
        result += "\n\n  🕯️ 蜡烛的光照到了衣柜后面——有什么东西缩了回去。"

    # 掉落物品
    drops = [
        ("🕯️ 蜡烛", 15),
        ("💊 安眠药", 8),
        ("🍵 热茶", 20),
        ("🪞 镜子", 10),
        ("📼 空白录像带", 5),
    ]
    for item, chance in drops:
        if random.randint(1, 100) <= chance and g.items[item] == 0:
            g.items[item] = 1
            result += f"\n\n  🎁 你发现了 {item}！"
            break

    g.last_event = result.split("\n")[0]
    渲染(color(f"👁️ 你环顾四周...\n\n  {result}", "yellow"))
    sleep(2.5)

def 动作_手电筒(g):
    if not g.flashlight_on:
        g.flashlight_on = True
        渲染(color("🔦 手电筒打开。电池: 100%", "yellow"))
        g.last_event = "手电筒已打开。"
    else:
        g.flashlight_on = False
        渲染(color("🔦 手电筒关闭。", "dim"))
        g.last_event = "手电筒已关闭。"
    sleep(1)

def 动作_门锁(g):
    if not g.door_locked:
        g.door_locked = True
        渲染(color("🔒 你锁上了门。咔嗒一声。", "green"))
        g.last_event = "门锁上了。"
    else:
        g.door_locked = False
        渲染(color("🔓 你解锁了门。你确定要这么做吗？", "yellow"))
        g.last_event = "门解锁了。"
    sleep(1)

def 动作_窗户(g):
    if not g.window_open:
        g.window_open = True
        g.sanity = max(0, g.sanity - 10)
        渲染(color("🪟 你推开了窗户。冷风灌入。\n\n  外面传来低语声...", "red"))
        g.last_event = "窗户打开。冷风+低语声。"
    else:
        g.window_open = False
        渲染(color("🪟 你关上了窗户。\n\n  玻璃内侧有一个湿漉漉的手印。", "yellow"))
        g.last_event = "窗户关上。有手印。"
    sleep(2)

def 动作_电话(g):
    if not g.phone_ringing:
        g.phone_ringing = True
        渲染(color("📞 电话突然响了！\n\n  来电: UNKNOWN\n  接听？[y/n]", "cyan"))
        g.last_event = "电话响了。"
    else:
        g.phone_ringing = False
        渲染(color("📞 电话挂断了。忙音中...", "dim"))
        g.last_event = "电话停了。"
    sleep(1.5)

def 动作_静音(g):
    g.muted = not g.muted
    if g.muted:
        渲染(color("🔇 已静音。世界安静了。太安静了。", "dim"))
        g.last_event = "静音。"
    else:
        渲染(color("🔊 取消静音。滋滋声回来了。", "cyan"))
        g.last_event = "取消静音。"
    sleep(1)

def 动作_频道列表(g):
    text = color("📡 频道列表:\n\n", "bold")
    channel_names = {
        0: "雪花屏", 1: "天气预报", 2: "深夜电影", 3: "紧急新闻",
        4: "教育频道", 5: "午夜卡通", 6: "午夜购物", 7: "测试图案",
        8: "纪录片", 9: "午夜旋律", 10: "深夜广告", 11: "警方频道",
        12: "儿童频道", 13: "???", 14: "???", 15: "???", 16: "???"
    }
    for i in range(17):
        mark = "★" if i in g.discovered_channels else "?"
        danger = " ☠️" if i >= 13 else ""
        cur = " ←" if i == g.channel and g.tv_on else ""
        text += f"  CH{i:02d} {mark} {channel_names[i]}{danger}{cur}\n"
    text += f"\n  已发现: {len(g.discovered_channels)}/17"
    text += color(f"\n\n  理智: {g.sanity_bar()}", "white")
    渲染(text)
    try:
        input(color("\n  按回车返回...", "dim"))
    except:
        pass

def 动作_帮助():
    text = color("🎮 操作指南:\n\n", "bold")
    text += "  w / ↑    上一频道          s / ↓    下一频道\n"
    text += "  d / →    音量 +            a / ←    音量 -\n"
    text += "  t          开关电视        l          环顾四周\n"
    text += "  f          手电筒          o          门锁\n"
    text += "  v          窗户            p          电话\n"
    text += "  i          物品栏(回血)    m          静音\n"
    text += "  c          频道列表        h          帮助\n"
    text += "  q          退出\n"
    text += "\n  ⚠️ 不要调到频道13。\n  ⚠️ 停电了别关手电筒。\n  ⚠️ 锁好门。\n  ⚠️ 物品栏是你唯一的生路。"
    渲染(text)
    try:
        input(color("\n  按回车返回...", "dim"))
    except:
        pass

# ========== 随机事件 ==========
def 随机事件(g):
    if random.randint(1, 100) > 35:
        return

    events = []

    if not g.tv_on and random.randint(1, 100) <= 15:
        g.tv_on = True
        g.channel = random.choice([1, 3, 7])
        g.last_event = "📺 电视自己开了。"
        events.append("电视突然自己启动了...")

    if g.tv_on and g.channel != 13 and random.randint(1, 100) <= 8:
        g.channel = 13
        g.last_event = "📺 频道自己跳到了 CH13。"
        events.append("频道不受控制地跳到了13...")

    if not g.door_locked and random.randint(1, 100) <= 20:
        g.footsteps += 1
        g.last_event = "🚪 门外有脚步声。"
        events.append("走廊传来沉重的脚步声...")

    if g.flashlight_on and random.randint(1, 100) <= 10:
        g.last_event = "🔦 手电筒闪了一下。"
        events.append("手电筒闪烁了一下...")

    if random.randint(1, 100) <= 12:
        g.sanity = max(0, g.sanity - random.randint(2, 6))
        g.last_event = "🧠 你感到一阵眩晕。"
        events.append("你感到头晕目眩...")

    # VHS 计时
    if g.vhs_active:
        g.vhs_remaining -= 1
        if g.vhs_remaining <= 0:
            g.vhs_active = False
            g.last_event = "📼 录像带播放结束。电视恢复正常。"

    if not events:
        return

    clear()
    渲染(color("⚡ 突发事件!\n", "yellow+bold"))
    for e in events:
        渲染(color(f"  • {e}", "yellow"))
    渲染("")
    g.events += len(events)
    sleep(2)

# ========== 死亡检测 ==========
def 检查死亡(g):
    if g.sanity <= 0:
        return 结局_理智归零(g)
    if g.footsteps >= 12:
        return 结局_破门而入(g)
    if g.events >= 10:
        return 结局_被标记(g)
    if g.window_open and g.sanity < 40:
        return 结局_渗透(g)
    if g.phone_ringing and g.phone_answer_count >= 5:
        return 结局_回响(g)
    if g.watched_minutes >= 120 and not g.diary_read:
        return 结局_收视率(g)
    if g.time_minutes >= 500:
        return 结局_天亮(g)
    return None

def 结局_理智归零(g):
    clear()
    text = color("╔══════════════════════════════════════╗\n║          💀 结 局 一 💀          ║\n║          理智归零                ║\n╚══════════════════════════════════════╝", "red+bold")
    text += "\n\n  你的理智耗尽了。\n\n  电视屏幕亮起。\n  他走了出来。\n  坐在你旁边的沙发上。\n  和你一起看电视。\n\n  \"终于可以好好聊聊了。\"\n\n"
    text += color("  [GAME OVER]", "red+bold")
    渲染(text)
    return True

def 结局_破门而入(g):
    clear()
    text = color("╔══════════════════════════════════════╗\n║          🚪 结 局 二 🚪          ║\n║          破门而入                ║\n╚══════════════════════════════════════╝", "red+bold")
    text += "\n\n  门锁被撞开了。\n  走廊里站着一个人形阴影。\n  他没有脸。\n\n  \"我来找你了。\"\n\n"
    text += color("  [GAME OVER]", "red+bold")
    渲染(text)
    return True

def 结局_被标记(g):
    clear()
    text = color("╔══════════════════════════════════════╗\n║          👁️ 结 局 三 👁️          ║\n║          被标记                  ║\n╚══════════════════════════════════════╝", "red+bold")
    text += "\n\n  你经历了太多恐怖事件。\n  电视里的人记住了你。\n  无论你逃到哪里...\n  他都知道。\n\n  \"跑不掉的。\"\n\n"
    text += color("  [GAME OVER]", "red+bold")
    渲染(text)
    return True

def 结局_渗透(g):
    clear()
    text = color("╔══════════════════════════════════════╗\n║          🪟 结 局 四 🪟          ║\n║          渗透                    ║\n╚══════════════════════════════════════╝", "red+bold")
    text += "\n\n  窗户开着。\n  冷风不断灌入。\n  但风里带着腐臭味。\n  一只苍白的手搭在了窗台上。\n\n  \"谢谢你没有关窗。\"\n\n"
    text += color("  [GAME OVER]", "red+bold")
    渲染(text)
    return True

def 结局_回响(g):
    clear()
    text = color("╔══════════════════════════════════════╗\n║          📞 结 局 五 📞          ║\n║          回响                    ║\n╚══════════════════════════════════════╝", "red+bold")
    text += "\n\n  你接了太多次电话。\n  每一次，对面都不说话。\n  直到最后一次——\n  你听到了自己的声音。\n\n  \"救救我。\"\n\n"
    text += color("  [GAME OVER]", "red+bold")
    渲染(text)
    return True

def 结局_收视率(g):
    clear()
    text = color("╔══════════════════════════════════════╗\n║          📺 结 局 六 📺          ║\n║          收视率                  ║\n╚══════════════════════════════════════╝", "red+bold")
    text += "\n\n  你看了太久的电视。\n  从未读过日记。\n  从未了解真相。\n  你成为了下一个\"上一任观众\"。\n\n  \"录制完成。\"\n\n"
    text += color("  [GAME OVER]", "red+bold")
    渲染(text)
    return True

def 结局_天亮(g):
    clear()
    # 检查是否达成真结局条件
    truth = g.diary_read and g.clues_found >= 3 and g.time_minutes >= 400
    if truth:
        text = color("╔══════════════════════════════════════╗\n║       🔑 真 结 局 - 真相 🔑      ║\n╚══════════════════════════════════════╝", "green+bold")
        text += "\n\n  凌晨 6:00。第一缕阳光照进客厅。\n\n  你读了日记，收集了线索，活到了天亮。\n  真相是：1953年那座广播塔...\n  不是为了发射信号。\n  是为了把什么东西封在里面。\n\n  它逃出来了。\n  通过电视信号。\n  一个接一个地找人。\n\n  你是第47个。\n  但你可能是第一个活下来的。\n\n  "
        text += color("  【你活了下来。但你知道了真相。】", "yellow+bold")
    else:
        text = color("╔══════════════════════════════════════╗\n║          🌅 结 局 八 🌅          ║\n║          天亮                    ║\n╚══════════════════════════════════════╝", "green+bold")
        text += "\n\n  凌晨 6:00。\n  第一缕阳光照进客厅。\n  电视自动关闭了。\n  门锁完好。窗户关着。\n  你活了下来。\n\n  但你知道——今晚还会再来。\n\n  "
        text += color("  【你赢了。但代价是什么？】", "yellow+bold")
    text += "\n\n  "
    text += color("  [THE END]", "green+bold")
    渲染(text)
    return True

# ========== 阶段推进 ==========
def 阶段剧情(g):
    new_phase = min(4, g.time_minutes // 60)
    if new_phase > g.phase:
        g.phase = new_phase
        clear()
        phases = [
            ("序章", "你以为这只是个普通的夜晚。"),
            ("第一章", "电视开始播放不该播的东西。"),
            ("第二章", "现实和电视的界限模糊了。"),
            ("第三章", "它在靠近。"),
            ("终章", "黎明前的最后黑暗。")
        ]
        title, desc = phases[g.phase]
        渲染(color(f"\n\n  📖 {title}\n\n  {desc}\n\n  ", "magenta+bold"))
        sleep(2)

# ========== 主循环 ==========
def 主循环(g):
    while g.running:
        阶段剧情(g)

        if g.tv_on:
            内容 = get_channel_content(g.channel, g)
            渲染电视(内容, g)
        else:
            clear()
            渲染(color("  📺 电视已关闭。", "dim"))
            print()
            渲染(color(f"  理智:{g.sanity_bar()}  |  时间: 23:{47+g.time_minutes%60:02d}  |  脚步:{g.footsteps}  |  事件:{g.events}", "dim"))
            if g.last_event:
                渲染(color(f"  ⚡ {g.last_event}", "yellow"))
            print()

        随机事件(g)

        dead = 检查死亡(g)
        if dead:
            try:
                input(color("\n  按回车退出...", "dim"))
            except:
                pass
            g.running = False
            break

        try:
            cmd = input(color("  > ", "cyan")).strip().lower()
        except (EOFError, KeyboardInterrupt):
            g.running = False
            break

        if cmd in ('q', 'quit', 'exit'):
            g.running = False
        elif cmd in ('t',):
            动作_开关电视(g)
        elif cmd in ('w', 'up'):
            动作_换台(g, 'up')
        elif cmd in ('s', 'down'):
            动作_换台(g, 'down')
        elif cmd in ('d', 'right'):
            动作_音量(g, 'up')
        elif cmd in ('a', 'left'):
            动作_音量(g, 'down')
        elif cmd in ('l',):
            动作_环顾(g)
        elif cmd in ('f',):
            动作_手电筒(g)
        elif cmd in ('o',):
            动作_门锁(g)
        elif cmd in ('v',):
            动作_窗户(g)
        elif cmd in ('p',):
            动作_电话(g)
        elif cmd in ('i',):
            动作_物品栏(g)
        elif cmd in ('m',):
            动作_静音(g)
        elif cmd in ('c',):
            动作_频道列表(g)
        elif cmd in ('h', '?'):
            动作_帮助()
        else:
            渲染(color(f"  未知命令: {cmd} (输入 h 查看帮助)", "red"))
            sleep(1)

# ========== 主入口 ==========
def main():
    show_trailer()
    g = Game()
    开场剧情(g)
    主循环(g)
    clear()
    渲染(color("\n\n  感谢游玩 📺 电视模拟恐怖 v5.0\n\n  github.com/LiGuo-666-jpg-bit/game-trailer\n\n", "dim"))

if __name__ == "__main__":
    main()
