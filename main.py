# -*- coding: utf-8 -*-
# ============================================================
#   📺 电视模拟恐怖 · 终极中文版 v4.0
#   纯 Python 标准库 | 零外部依赖 | 手机/电脑通用
#   运行: python main.py
# ============================================================

import random
import time
import sys
import os

# ── 导入预告片模块 ──
try:
    from trailer import show_trailer
except ImportError:
    # 如果 trailer.py 不存在，定义空函数跳过
    def show_trailer():
        pass


# ═══════════════════════════════════════════════════════════
#  颜色系统（全部内联字符串，不存在属性缺失问题）
# ═══════════════════════════════════════════════════════════
BLACK   = "\033[30m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
GRAY    = "\033[90m"
BRED    = "\033[91m"
BGREEN  = "\033[92m"
BYELLOW = "\033[93m"
BBLUE   = "\033[94m"
BMAGENTA= "\033[95m"
BCYAN   = "\033[96m"
BWHITE  = "\033[97m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
BLINK   = "\033[5m"
RESET   = "\033[0m"

# ═══════════════════════════════════════════════════════════
#  屏幕工具
# ═══════════════════════════════════════════════════════════
def cls():
    print("\033[2J\033[H", end="", flush=True)

def hide_cur():
    print("\033[?25l", end="")

def show_cur():
    print("\033[?25h", end="")

def slow(text, delay=0.03):
    """逐字输出，营造氛围"""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def center(text, width=40):
    """简单居中"""
    raw = text
    for code in [BLACK,RED,GREEN,YELLOW,BLUE,MAGENTA,CYAN,WHITE,
                 GRAY,BRED,BGREEN,BYELLOW,BBLUE,BMAGENTA,BCYAN,BWHITE,
                 BOLD,DIM,BLINK,RESET]:
        raw = raw.replace(code, "")
    pad = (width - len(raw)) // 2
    return " " * max(0, pad) + text

def progress_bar(val, maxv, w=10):
    filled = int(w * val / maxv) if maxv > 0 else 0
    if val / maxv > 0.6: c = GREEN
    elif val / maxv > 0.3: c = YELLOW
    else: c = RED
    return "".join(f"{c}█{RESET}" if i < filled else f"{GRAY}░{RESET}" for i in range(w))

# ═══════════════════════════════════════════════════════════
#  雪花/噪点
# ═══════════════════════════════════════════════════════════
def static_line(w=40):
    chars = " .-+*xX#%@░▒▓█"
    return "".join(random.choice(chars) for _ in range(w))

def full_static(h=8, w=40):
    return [f"{DIM}{static_line(w)}{RESET}" for _ in range(h)]

# ═══════════════════════════════════════════════════════════
#  电视边框
# ═══════════════════════════════════════════════════════════
def draw_tv(content, w=44, h=10):
    out = []
    out.append(f"{GRAY}╔{'═' * w}╗{RESET}")
    out.append(f"{GRAY}║{RESET}{DIM}▌▌▌▌{RESET}{GRAY}┌{'─' * (w-12)}┐{RESET}{DIM}▌▌▌▌{RESET}{GRAY}║{RESET}")
    for i in range(h):
        if i < len(content):
            line = content[i]
            if len(line) > w - 12: line = line[:w-12]
            else: line = line + " " * (w - 12 - len(line))
            if i % 3 == 0: line = f"{DIM}{line}{RESET}"
            out.append(f"{GRAY}║{RESET}{DIM}▌▌▌▌{RESET} {line} {RESET}{DIM}▌▌▌▌{RESET}{GRAY}║{RESET}")
        else:
            out.append(f"{GRAY}║{RESET}{DIM}▌▌▌▌{RESET}{' ' * (w-8)}{DIM}▌▌▌▌{RESET}{GRAY}║{RESET}")
    out.append(f"{GRAY}║{RESET}{DIM}▌▌▌▌{RESET}{GRAY}└{'─' * (w-12)}┘{RESET}{DIM}▌▌▌▌{RESET}{GRAY}║{RESET}")
    out.append(f"{GRAY}╚{'═' * w}╝{RESET}")
    out.append(f"  {GRAY}╲{' ' * (w-8)}╱{RESET}")
    out.append(f"    {GRAY}╲{' ' * (w-12)}╱{RESET}")
    return "\n".join(out)

# ═══════════════════════════════════════════════════════════
#  频道系统（全中文内容）
# ═══════════════════════════════════════════════════════════
class 频道:
    """所有频道内容生成器"""

    @staticmethod
    def 获取(编号, 游戏=None):
        映射 = {
            0: 频道.雪花, 1: 频道.天气, 2: 频道.老电影,
            3: 频道.新闻, 4: 频道.教育, 5: 频道.卡通,
            6: 频道.购物, 7: 频道.测试图, 8: 频道.纪录片,
            9: 频道.音乐, 10: 频道.广告, 11: 频道.警方,
            12: 频道.儿童, 13: 频道.频道13, 14: 频道.频道14,
            15: 频道.频道15, 16: 频道.频道16,
        }
        return 映射.get(编号, 频道.雪花)(游戏)

    # ── 各频道内容 ─────────────────────────────────────

    @staticmethod
    def 雪花(g): return full_static()

    @staticmethod
    def 天气(g):
        return [
            f"{BYELLOW}{BOLD}  【天气预报】{RESET}",
            f"{GRAY}{'─'*38}{RESET}",
            f"  今晚: 大雾，能见度{BRED}极低{RESET}",
            f"  气温: 16°C → {BRED}4°C{RESET}",
            f"  风力: 无风",
            f"",
            f"  {YELLOW}⚠ 特别提醒:{RESET}",
            f"  夜间请勿独自外出",
            f"  如听到敲门声请立即报警",
            f"  锁好门窗，拉好窗帘",
            f"  不要回应任何自称维修人员的人",
        ]

    @staticmethod
    def 老电影(g):
        # 理智越低，电影越恐怖
        if g and g.理智 < 50:
            return [
                f"  {DIM}--- 深夜放映 ---{RESET}",
                f"",
                f"  {RED}男人: \"亲爱的，我马上回来\"{RESET}",
                f"  {RED}女人: \"我等你...永远等你...\"{RESET}",
                f"",
                f"  {BRED}{BLINK}画面定格。女人的脸开始腐烂。{RESET}",
                f"  {BRED}她对着镜头笑。{RESET}",
                f"  {BRED}她知道你在看。{RESET}",
            ]
        elif g and g.理智 < 75:
            return [
                f"  {DIM}--- 深夜放映 ---{RESET}",
                f"",
                f"  男人: \"我很快就回来\"",
                f"  女人: \"我等你\"",
                f"",
                f"  {DIM}[画面开始倒放]{RESET}",
                f"  {RED}...来...回...不...会...我...\"{RESET}",
                f"  {RED}[倒放的笑声]{RESET}",
            ]
        return [
            f"  {DIM}--- 经典老电影 ---{RESET}",
            f"",
            f"  男人: \"亲爱的，我很快就回来\"",
            f"  女人: \"我等你...\"",
            f"",
            f"  {DIM}[胶片卡住了]{RESET}",
            f"  {DIM}[声音在回响]{RESET}",
        ]

    @staticmethod
    def 新闻(g):
        故事 = [
            [
                f"{BYELLOW}{BOLD}  【紧急新闻】{RESET}",
                f"{GRAY}{'─'*38}{RESET}",
                f"  本市连续发生失踪案",
                f"  受害者均为独居者",
                f"  最后活动痕迹:",
                f"  ── 在家中看电视 ──",
                f"",
                f"  {BRED}※ 以下内容无法播出 ※{RESET}",
                f"  {BRED}████████████████████{RESET}",
            ],
            [
                f"{BYELLOW}{BOLD}  【本市新闻】{RESET}",
                f"{GRAY}{'─'*38}{RESET}",
                f"  警方通报: 近期有不明人物",
                f"  深夜在居民区活动",
                f"  特征: 穿旧式电视维修制服",
                f"  背着老式显像管电视机",
                f"  {YELLOW}如有人敲门自称修电视{RESET}",
                f"  {YELLOW}请立即报警，切勿开门{RESET}",
                f"",
                f"  {RED}该嫌疑人最后出现地点:",
                f"  {RED}── 距离你家 200 米 ──{RESET}",
            ],
            [
                f"{BYELLOW}{BOLD}  【深夜连线】{RESET}",
                f"{GRAY}{'─'*38}{RESET}",
                f"  记者: \"我们现在在广播塔遗址\"",
                f"  记者: \"信号塔从午夜开始...\"",
                f"  记者: \"...自发播放一段频率\"",
                f"  {RED}...能听到吗...{RESET}",
                f"  {RED}...它在通过电视说话...{RESET}",
                f"  {BRED}{BLINK}── 连线中断 ──{RESET}",
            ],
        ]
        return random.choice(故事)

    @staticmethod
    def 教育(g):
        return [
            f"{BCYAN}  📖 深夜教育频道{RESET}",
            f"{GRAY}{'─'*38}{RESET}",
            f"  课程: 现代都市传说研究",
            f"",
            f"  案例七: '电视机里的房客'",
            f"  {DIM}─────────────{RESET}",
            f"  1978年，一栋公寓楼里",
            f"  每个房间的电视都在午夜",
            f"  自动调到同一个频道",
            f"  第二天早上",
            f"  {BRED}所有住户消失了{RESET}",
            f"  {BRED}电视还开着{RESET}",
            f"  {BRED}画面里有人在笑{RESET}",
            f"",
            f"  {DIM}[课件被强制关闭]{RESET}",
        ]

    @staticmethod
    def 卡通(g):
        if g and g.理智 < 35:
            return [
                f"  {BRED}{BOLD}???{RESET}",
                f"",
                f"      ▲",
                f"    {BRED}◉ ▲ ◉{RESET}",
                f"    ╲___╱",
                f"",
                f"  {BRED}{BOLD}\"你还在看吗?\"{RESET}",
                f"  {BRED}{BLINK}\"我一直都在看着你\"{RESET}",
                f"",
                f"  {RED}它伸出手{RESET}",
                f"  {RED}从屏幕里{RESET}",
            ]
        elif g and g.理智 < 65:
            return [
                f"  {BRED}???{RESET}",
                f"",
                f"     \\o/",
                f"      {BRED}◉◉◉{RESET}",
                f"     /   \\",
                f"",
                f"  {YELLOW}♪ 快来陪我玩...♪{RESET}",
                f"  {YELLOW}♪ 永远...永远...♪{RESET}",
                f"",
                f"  {YELLOW}⚠ 画面被修改过{RESET}",
            ]
        return [
            f"  🐰 快乐兔子乐园 🐰",
            f"",
            f"     \\o/",
            f"      ○○○",
            f"     /   \\",
            f"",
            f"  ♪ 啦啦啦 快乐的一天 ♪",
            f"",
            f"  [广告即将开始...]",
        ]

    @staticmethod
    def 购物(g):
        return [
            f"{BMAGENTA}  🛒 午夜购物频道{RESET}",
            f"{GRAY}{'─'*38}{RESET}",
            f"  今晚特惠!",
            f"",
            f"  🔪 银质餐刀套装 - ¥99",
            f"  🪞 古董穿衣镜 - ¥299",
            f"  📻 复古收音机   - ¥199",
            f"  🧸  vintage 泰迪熊 - ¥49",
            f"",
            f"  {BRED}订购热线: 666-6666{RESET}",
            f"  {RED}（请勿在午夜拨打）{RESET}",
            f"",
            f"  {DIM}...这家公司去年就倒闭了{RESET}",
        ]

    @staticmethod
    def 测试图(g):
        return [
            f"{BWHITE}  SMPTE 测试图案{RESET}",
            f"",
            f"  {RED}██████{GREEN}██████{BLUE}██████{YELLOW}██████{RESET}",
            f"  {CYAN}██████{MAGENTA}██████{WHITE}██████{GRAY}██████{RESET}",
            f"",
            f"    ○────○────○",
            f"    │         │",
            f"    ○    ●    ○",
            f"    │         │",
            f"    ○────○────○",
            f"",
            f"  {DIM}请勿靠近电视{RESET}",
            f"  {RED}请勿盯着中心点超过10秒{RESET}",
        ]

    @staticmethod
    def 纪录片(g):
        return [
            f"{BBLUE}  🎬 深夜纪录片{RESET}",
            f"{GRAY}{'─'*38}{RESET}",
            f"  《被遗忘的广播塔》",
            f"",
            f"  1953年，郊区建了一座广播塔",
            f"  每晚23:00至03:00",
            f"  会自动播放一段未知信号",
            f"",
            f"  研究人员发现...",
            f"  {RED}信号源不在塔上{RESET}",
            f"  {RED}信号来自塔下{RESET}",
            f"  {BRED}信号来自地下六米处{RESET}",
            f"",
            f"  {BRED}{BLINK}[纪录片被强制中断]{RESET}",
            f"  {RED}画面切换到一个空房间{RESET}",
            f"  {RED}那就是你家{RESET}",
        ]

    @staticmethod
    def 音乐(g):
        歌单 = [
            ("摇篮曲(变奏版)", [
                "  睡吧 睡吧 乖孩子",
                "  门已经锁好了",
                "  窗也封死了",
                f"  {YELLOW}可是烟囱没有盖{RESET}",
                f"  {YELLOW}它从烟囱进来了{RESET}",
            ]),
            ("没有人回家", [
                f"  {RED}他在楼梯上{RESET}",
                f"  {RED}他在走廊里{RESET}",
                f"  {RED}他在门后面{RESET}",
                f"  {BRED}他在你床底下{RESET}",
                f"  {BRED}他在对你笑{RESET}",
            ]),
            ("第九交响曲(残章)", [
                "  ♪ 哆━━━━━瑞━━━━━",
                "  ♪ 咪━━━━━发━━━━━",
                "  ♪ 声音越来越响...",
                f"  ♪ {RED}有人在跟着哼{RESET}",
                f"  ♪ {BRED}他就在你耳边唱{RESET}",
            ]),
        ]
        名, 词 = random.choice(歌单)
        out = [f"{BMAGENTA}  ♪ 午夜旋律 FM ♪{RESET}", f"{GRAY}{'─'*38}{RESET}", f"  正在播放: {MAGENTA}{名}{RESET}", ""]
        for l in 词: out.append(f"  {l}")
        return out

    @staticmethod
    def 广告(g):
        return [
            f"{GREEN}  📺 深夜电视购物{RESET}",
            f"{GRAY}{'─'*38}{RESET}",
            f"  \"还在害怕黑暗吗?\"",
            f"",
            f"  \"试试全新 NightGuard 智能门锁!\"",
            f"  \"经过测试，能挡住...\"",
            f"  {BRED}\"...任何试图进入的东西\"{RESET}",
            f"",
            f"  \"限时优惠 ¥599\"",
            f"  {YELLOW}※ 不适用于超自然入侵{RESET}",
            f"  {DIM}...这家公司去年就倒闭了{RESET}",
            f"",
            f"  {RED}但你家装的正是这款锁{RESET}",
        ]

    @staticmethod
    def 警方(g):
        return [
            f"{BRED}{BOLD}  🚨 警方频道(未加密){RESET}",
            f"{GRAY}{'─'*38}{RESET}",
            f"  调度: \"10-4，收到\"",
            f"  7号警员: \"在广播塔附近发现...\"",
            f"  7号警员: \"...又一辆失踪者的车\"",
            f"  调度: \"地址?\"",
            f"  7号警员: \"...就是那个地址\"",
            f"  调度: \"什么地址?\"",
            f"  7号警员: \"...{BRED}他在看着我们{RESET}\"",
            f"  {BRED}{BLINK}━━ 信号中断 ━━{RESET}",
            f"",
            f"  {RED}对面楼顶有人闪灯{RESET}",
            f"  {BRED}SOS ... SOS ... SOS{RESET}",
            f"  {RED}那是你家窗户的方向{RESET}",
        ]

    @staticmethod
    def 儿童(g):
        """儿童频道 - 看似温馨实则细思极恐"""
        if g and g.理智 < 50:
            return [
                f"  {BRED}{BOLD}睡前故事时间{RESET}",
                f"",
                f"  \"从前有个小女孩...\"",
                f"  \"她每晚都锁好门窗...\"",
                f"  \"关掉电视...\"",
                f"  \"钻进被窝...\"",
                f"",
                f"  {RED}\"但是她忘了...\"{RESET}",
                f"  {BRED}\"电视从来不会自己关\"{RESET}",
                f"",
                f"  {BRED}{BLINK}\"晚安，小女孩\"{RESET}",
            ]
        return [
            f"  🧸 睡前故事频道 🧸",
            f"",
            f"  \"从前有个小女孩\"",
            f"  \"她住在一栋老房子里\"",
            f"  \"每晚她都会...\"",
            f"  {DIM}[信号不稳定]{RESET}",
            f"  \"...听到电视在叫她名字\"",
            f"",
            f"  [明日继续]",
        ]

    @staticmethod
    def 频道13(g):
        return [
            f"{BRED}{BOLD}  ██ 频道 13 ██{RESET}",
            f"{GRAY}{'─'*38}{RESET}",
            f"",
            f"  有人在看着你",
            f"  转过头去",
            f"  现在",
            f"",
            f"  {BRED}{BOLD}┌──────────────────────┐{RESET}",
            f"  {BRED}{BOLD}│   他 就 在 你 身后   │{RESET}",
            f"  {BRED}{BOLD}└──────────────────────┘{RESET}",
            f"",
            f"  {RED}信号来源: {BRED}{BLINK}你的房间{RESET}",
            f"  {RED}录制中...{RESET}",
            f"  {DIM}观看人数: 1{RESET}",
            f"  {DIM}── 就是你 ──{RESET}",
        ]

    @staticmethod
    def 频道14(g):
        return [
            f"{BRED}{BOLD}  ▶ 直播画面{RESET}",
            f"{GRAY}{'─'*38}{RESET}",
            f"",
            f"  CAM 01 - 你的卧室",
            f"  {DIM}─────────────────{RESET}",
            f"  床上: 空",
            f"  椅子: {BRED}有人坐着{RESET}",
            f"  门: {GREEN}关着{RESET}",
            f"  窗帘: {RED}在动{RESET}",
            f"  衣柜: {BRED}门开了一条缝{RESET}",
            f"",
            f"  {BRED}{BLINK}※ 正在录制 ※{RESET}",
            f"  {RED}观看人数: 1{RESET}",
            f"  ── 就是你 ──",
        ]

    @staticmethod
    def 频道15(g):
        return [
            f"{BRED}{BOLD}  ╔════════════════════╗{RESET}",
            f"{BRED}{BOLD}  ║    频 道  1 5      ║{RESET}",
            f"{BRED}{BOLD}  ╚════════════════════╝{RESET}",
            f"",
            f"  {BRED}{BLINK}我 看 见 你 了{RESET}",
            f"",
            f"  {RED}我 看 见 你 了{RESET}",
            f"",
            f"  {BRED}{BOLD}我 看 见 你 了{RESET}",
            f"",
            f"  {RED}过 来{RESET}",
            f"  {RED}靠 近{RESET}",
            f"  {RED}屏 幕{RESET}",
            f"",
            f"  {BRED}{BOLD}把 手 放 上 去{RESET}",
        ]

    @staticmethod
    def 频道16(g):
        """最终频道 - 游戏中最恐怖的存在"""
        return [
            f"{BRED}{BOLD}  ╔════════════════════════════╗{RESET}",
            f"{BRED}{BOLD}  ║                            ║{RESET}",
            f"{BRED}{BOLD}  ║     你 不 该 来 这 里      ║{RESET}",
            f"{BRED}{BOLD}  ║                            ║{RESET}",
            f"{BRED}{BOLD}  ╚════════════════════════════╝{RESET}",
            f"",
            f"  {BRED}{BLINK}I{RESET}",
            f"  {BRED}{BLINK}A{RESET}",
            f"  {BRED}{BLINK}M{RESET}",
            f"  {BRED}{BLINK} {RESET}",
            f"  {BRED}{BLINK}H{RESET}",
            f"  {BRED}{BLINK}E{RESET}",
            f"  {BRED}{BLINK}R{RESET}",
            f"  {BRED}{BLINK}E{RESET}",
            f"",
            f"  {BRED}{BOLD}╔════════════════════════════╗{RESET}",
            f"  {BRED}{BOLD}║   now playing: 你的房间   ║{RESET}",
            f"  {BRED}{BOLD}╚════════════════════════════╝{RESET}",
        ]

# ═══════════════════════════════════════════════════════════
#  频道列表（有序，用于上下切换）
# ═══════════════════════════════════════════════════════════
频道列表 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

频道名称 = {
    0:"雪花", 1:"天气预报", 2:"深夜电影", 3:"紧急新闻", 4:"教育频道",
    5:"午夜卡通", 6:"午夜购物", 7:"测试图案", 8:"纪录片",
    9:"午夜旋律", 10:"深夜广告", 11:"警方频道", 12:"儿童频道",
    13:"???", 14:"???", 15:"???", 16:"???"
}

# ═══════════════════════════════════════════════════════════
#  游戏状态
# ═══════════════════════════════════════════════════════════
class 游戏:
    def __init__(self):
        # 核心状态
        self.电视开着 = False
        self.当前频道 = 0
        self.音量 = 3
        self.理智 = 100
        self.最大理智 = 100

        # 时间
        self.时 = 23
        self.分 = 47

        # 环境
        self.停电 = False
        self.手电筒 = False
        self.门锁 = True
        self.窗户关 = True
        self.温度 = 18

        # 事件计数
        self.事件日志 = []
        self.脚步声 = 0
        self.低语声 = 0
        self.敲门声 = 0
        self.电话响 = 0
        self.环顾次数 = 0
        self.恐怖事件 = 0
        self.呼吸声 = False

        # 隐藏频道标记
        self.见过13 = False
        self.见过14 = False
        self.见过15 = False
        self.见过16 = False

        # 粘性系统
        self.存活时间 = 0          # 存活分钟数（游戏内）
        self.电视累计时长 = 0      # 看电视总时长
        self.切换次数 = 0          # 换台次数
        self.发现秘密 = 0          # 发现的隐藏要素数
        self.阅读日记 = False      # 是否读过日记
        self.结局次数 = 0          # 累计死亡次数（多周目）
        self.已知频道 = set(range(0, 13))  # 已发现的频道
        self.解锁成就 = []         # 成就系统
        self.隐藏线索 = []         # 收集的线索

        # 多周目加成
        self.周目 = 1
        self.前世记忆 = []         # 上一次死亡的遗言

        # 当前结局标记
        self.结局原因 = None

        # 游戏阶段（用于剧情推进）
        self.阶段 = "序章"  # 序章 → 第一章 → 第二章 → 第三章 → 终章

        # 静音
        self.静音 = False
        self._上次音量 = 3

        # 物品
        self.物品 = {
            "手机": {"描述": "电量67%，信号极差", "可用": True},
            "手电筒": {"描述": "电量充足", "可用": True},
            "钥匙": {"描述": "家门钥匙", "可用": True},
            "日记本": {"描述": "你的笔迹，但有些不是你写的", "可用": True},
            "泰迪熊": {"描述": "小时候的玩偶", "可用": True},
            "收音机": {"描述": "老式晶体管收音机", "可用": True},
        }

    def 时间字符串(self):
        return f"{self.时:02d}:{self.分:02d}"

    def 记录(self, 消息):
        self.事件日志.append(消息)
        if len(self.事件日志) > 6:
            self.事件日志.pop(0)

    def 推进时间(self):
        self.分 += random.randint(1, 4)
        self.存活时间 += 1
        if self.分 >= 60:
            self.分 -= 60
            self.时 += 1
            if self.时 >= 24: self.时 = 0

        # 阶段推进
        if self.存活时间 > 30 and self.阶段 == "序章": self.阶段 = "第一章"
        if self.存活时间 > 80 and self.阶段 == "第一章": self.阶段 = "第二章"
        if self.存活时间 > 150 and self.阶段 == "第二章": self.阶段 = "第三章"
        if self.存活时间 > 250 and self.阶段 == "第三章": self.阶段 = "终章"

    def 理智图标(self):
        if self.理智 > 75: return "😊"
        if self.理智 > 50: return "😟"
        if self.理智 > 25: return "😰"
        if self.理智 > 10: return "😱"
        return "💀"

    def 检查成就(self, 名称):
        if 名称 not in self.解锁成就:
            self.解锁成就.append(名称)
            self.记录(f"{BYELLOW}🏆 成就解锁: {名称}{RESET}")

# ═══════════════════════════════════════════════════════════
#  预告片（电影级开场）
# ═══════════════════════════════════════════════════════════
def 预告片():
    """游戏启动前播放的电影级预告片"""
    cls()

    # ── 第一幕：标题闪现 ──
    for _ in range(4):
        cls()
        print("\n\n\n")
        print(f"  {BRED}{BOLD}    电 视 模 拟 恐 怖{RESET}")
        print(f"  {DIM}    TV SIMULATOR HORROR{RESET}")
        time.sleep(0.15)
        cls(); print("\n\n\n"); time.sleep(0.1)

    # ── 第二幕：制作名单（快速闪过）──
    cls()
    print("\n\n")
    credits = [
        (f"{DIM}一部关于{RESET}{BRED}电视{RESET}{DIM}的电影{RESET}", 0.6),
        (f"", 0.2),
        (f"{GRAY}导演 / 编剧{RESET}", 0.5),
        (f"{WHITE}你的大脑{RESET}", 0.8),
        (f"", 0.3),
        (f"{GRAY}主演{RESET}", 0.5),
        (f"{WHITE}你{RESET}", 0.8),
        (f"{GRAY}特别出演{RESET}", 0.5),
        (f"{BRED}频道13{RESET}", 0.8),
        (f"", 0.3),
        (f"{GRAY}摄影{RESET}", 0.5),
        (f"{DIM}你手机的前置摄像头{RESET}", 0.8),
        (f"", 0.3),
        (f"{GRAY}音效{RESET}", 0.5),
        (f"{BRED}你家的电路{RESET}", 0.8),
        (f"", 0.5),
        (f"{GRAY}技术支持{RESET}", 0.5),
        (f"{DIM}1953年的广播塔{RESET}", 1.0),
    ]
    for text, delay in credits:
        print(f"  {text}")
        time.sleep(delay)

    time.sleep(0.5)
    cls(); print("\n\n")

    # ── 第三幕：警告 ──
    print(f"  {BRED}{BOLD}  ╔══════════════════════════════════════╗{RESET}")
    print(f"  {BRED}{BOLD}  ║                                            ║{RESET}")
    print(f"  {BRED}{BOLD}  ║   ⚠ 以下画面可能引起不适  ⚠          ║{RESET}")
    print(f"  {BRED}{BOLD}  ║                                            ║{RESET}")
    print(f"  {BRED}{BOLD}  ║   建议佩戴耳机 · 暗光环境体验          ║{RESET}")
    print(f"  {BRED}{BOLD}  ║   未满18岁请在家长陪同下游玩           ║{RESET}")
    print(f"  {BRED}{BOLD}  ║   本游戏纯属虚构 如有雷同纯属巧合      ║{RESET}")
    print(f"  {BRED}{BOLD}  ║                                            ║{RESET}")
    print(f"  {BRED}{BOLD}  ╚══════════════════════════════════════╝{RESET}")
    time.sleep(2.0)

    # ── 第四幕：预告片段 ──
    scenes = [
        ("", None, 0.3, False),
        (f"{GRAY}2024年11月15日{RESET}", GRAY, 1.2, False),
        (f"{GRAY}周五 深夜 23:47{RESET}", GRAY, 1.2, False),
        (f"{GRAY}你独自在家{RESET}", GRAY, 1.5, False),
        ("", None, 0.5, False),

        # 第一段
        (f"{DIM}你关掉了电视{RESET}", DIM, 1.2, False),
        (f"{DIM}你确定你关掉了{RESET}", DIM, 1.2, False),
        (f"{BRED}但你还是听到了笑声{RESET}", BRED, 1.5, False),
        ("", None, 0.5, False),

        # 第二段
        (f"{BRED}「频道13」{RESET}", BRED, 0.8, True),
        (f"{BRED}它不是电视台播的{RESET}", BRED, 1.2, False),
        (f"{BRED}是上一任观众录的{RESET}", BRED, 1.2, False),
        (f"{BRED}录给他们走之后{RESET}", BRED, 1.0, False),
        (f"{BRED}下一任观众看{RESET}", BRED, 1.5, False),
        ("", None, 0.5, False),

        # 第三段
        (f"{DIM}你环顾房间{RESET}", DIM, 1.0, False),
        (f"{YELLOW}门锁好了{RESET}", YELLOW, 0.8, False),
        (f"{YELLOW}窗户关了{RESET}", YELLOW, 0.8, False),
        (f"{YELLOW}手电筒满电{RESET}", YELLOW, 0.8, False),
        (f"{BRED}你忘了检查衣柜{RESET}", BRED, 1.5, False),
        ("", None, 0.5, False),

        # 第四段 - 警告语
        (f"{BRED}{BOLD}「不要相信电视里说的话」{RESET}", BRED, 1.5, False),
        (f"{BRED}{BOLD}「不要调到频道13」{RESET}", BRED, 1.5, False),
        (f"{BRED}{BOLD}「不要接凌晨的电话」{RESET}", BRED, 1.5, False),
        (f"{BRED}{BOLD}「手电筒是命」{RESET}", BRED, 1.5, False),
        (f"{BRED}{BOLD}「镜子可能有问题」{RESET}", BRED, 1.5, False),
        ("", None, 0.5, False),

        # 第五段 - 快切
        (f"{BRED}他在你身后{RESET}", BRED, 0.3, True),
        (f"{BRED}他在门后{RESET}", BRED, 0.3, True),
        (f"{BRED}他在衣柜里{RESET}", BRED, 0.3, True),
        (f"{BRED}他在床底下{RESET}", BRED, 0.3, True),
        (f"{BRED}他在电视里{RESET}", BRED, 0.6, True),
        ("", None, 0.3, False),

        # 第六段
        (f"{DIM}你拿起遥控器{RESET}", DIM, 1.2, False),
        (f"{DIM}你感觉......{RESET}", DIM, 1.0, False),
        (f"{BRED}遥控器也在发抖{RESET}", BRED, 1.5, False),
        ("", None, 0.5, False),

        # 第七段
        (f"{GRAY}17个频道{RESET}", GRAY, 0.8, False),
        (f"{GRAY}只有12个应该存在{RESET}", GRAY, 1.2, False),
        (f"{BRED}另外5个......{RESET}", BRED, 1.0, False),
        (f"{BRED}是给你看的{RESET}", BRED, 1.5, False),
        ("", None, 0.5, False),

        # 第八段
        (f"{DIM}每次死亡{RESET}", DIM, 0.8, False),
        (f"{DIM}都会回到今晚{RESET}", DIM, 1.0, False),
        (f"{BRED}23:47{RESET}", BRED, 0.8, True),
        (f"{BRED}同一个沙发{RESET}", BRED, 0.8, False),
        (f"{BRED}同一个遥控器{RESET}", BRED, 0.8, False),
        (f"{BRED}同一个你{RESET}", BRED, 1.5, False),
        ("", None, 0.5, False),

        # 第九段
        (f"{YELLOW}8种结局{RESET}", YELLOW, 1.0, False),
        (f"{YELLOW}你能在天亮前逃出去吗？{RESET}", YELLOW, 1.5, False),
        ("", None, 0.5, False),

        # 第十段 - 倒计时
        (f"{BRED}{BOLD}3...{RESET}", BRED, 0.8, True),
        (f"{BRED}{BOLD}2...{RESET}", BRED, 0.8, True),
        (f"{BRED}{BOLD}1...{RESET}", BRED, 0.8, True),
        ("", None, 0.3, False),
    ]

    for text, color, delay, blink in scenes:
        cls()
        print("\n\n\n")
        if blink and text:
            for _ in range(3):
                print(f"  {text}")
                time.sleep(0.08)
                cls(); print("\n\n\n"); time.sleep(0.06)
            print(f"  {text}")
        else:
            if text:
                print(f"  {text}")
        time.sleep(delay)

    # ── 第五幕：最终标题 ──
    cls()
    print("\n\n\n\n")
    for _ in range(3):
        print(f"  {BRED}{BOLD}      📺  电 视 模 拟 恐 怖  📺{RESET}")
        print(f"  {BRED}{BOLD}         TV  SIMULATOR  HORROR{RESET}")
        time.sleep(0.2)
        cls(); print("\n\n\n\n"); time.sleep(0.1)

    cls()
    print("\n\n\n")
    print(f"  {BRED}{BOLD}      📺  电 视 模 拟 恐 怖  📺{RESET}")
    print()
    print(f"  {GRAY}press enter to begin{RESET}")
    print()
    print(f"  {DIM}（输入 q 可跳过预告片）{RESET}")

    try:
        ans = input(f"  {CYAN}▶ {RESET}").strip().lower()
        if ans == 'q':
            cls()
            print(f"\n  {DIM}...你跳过了片头...{RESET}")
            print(f"  {DIM}但片头没有跳过你{RESET}")
            time.sleep(1.5)
    except (KeyboardInterrupt, EOFError):
        pass

    cls()


# ═══════════════════════════════════════════════════════════
#  输入系统（兼容手机，纯 input 方式）
# ═══════════════════════════════════════════════════════════
def 获取输入(提示="  ▶ "):
    """获取用户输入，统一小写处理"""
    try:
        return input(f"{CYAN}{提示}{RESET}").strip().lower()
    except (KeyboardInterrupt, EOFError):
        return "q"

# ═══════════════════════════════════════════════════════════
#  渲染界面
# ═══════════════════════════════════════════════════════════
def 渲染(游戏):
    cls()

    # 标题
    print(f"  {BRED}{BOLD}╔════════════════════════════════════════════════════╗{RESET}")
    print(f"  {BRED}{BOLD}║             📺  电 视 模 拟 恐 怖  📺             ║{RESET}")
    if 游戏.周目 > 1:
        print(f"  {BRED}{BOLD}║             第 {游戏.周目} 周目 · 他记得你           ║{RESET}")
    else:
        print(f"  {BRED}{BOLD}║              深夜 23:47 · 你独自在家            ║{RESET}")
    print(f"  {BRED}{BOLD}╚════════════════════════════════════════════════════╝{RESET}")
    print()

    # 电视画面
    if 游戏.电视开着 and not 游戏.停电:
        内容 = 频道.获取(游戏.当前频道, 游戏)
    elif 游戏.停电:
        内容 = ["", "", "", f"  {GRAY}(一片漆黑){RESET}", "", "", "", ""]
    else:
        内容 = ["", "", "", f"  {DIM}(电视已关闭){RESET}", "", "", "", ""]

    print(draw_tv(内容))
    print()

    # 状态栏
    电源 = f"{GREEN}●开{RESET}" if 游戏.电视开着 else f"{RED}●关{RESET}"
    名称 = 频道名称.get(游戏.当前频道, "未知")
    音量条 = progress_bar(游戏.音量, 10)
    信号 = random.randint(1,5) if 游戏.电视开着 else 0
    信号条 = progress_bar(信号, 5, 5)
    阶段色 = RED if 游戏.阶段 in ("第三章","终章") else YELLOW if 游戏.阶段 == "第二章" else CYAN

    print(f"  {电源}  频道{游戏.当前频道:02d} {MAGENTA}{名称:8s}{RESET}  "
          f"音量:{音量条}  信号:{信号条}  "
          f"{阶段色}【{游戏.阶段}】{RESET}  {GRAY}{游戏.时间字符串()}{RESET}")

    # 隐藏频道暗示
    if 游戏.当前频道 == 12 and 游戏.存活时间 > 20:
        print(f"  {DIM}...频道列表好像还差几个...{RESET}")
    if 游戏.电视累计时长 > 60 and 16 not in 游戏.已知频道:
        print(f"  {DIM}...你感觉还有一个频道存在...{RESET}")

    print()

    # 左侧房间状态 | 右侧事件日志
    理智色 = GREEN if 游戏.理智 > 70 else YELLOW if 游戏.理智 > 40 else RED
    电力色 = GREEN if not 游戏.停电 else BRED

    房间 = [
        f"{BWHITE}{BOLD}┌─ 房间状态 ─────────────┐{RESET}",
        f"│ 🕐 时间: {YELLOW}{游戏.时间字符串()}{RESET}",
        f"│ 🌡️ 温度: {CYAN}{游戏.温度}°C{RESET}",
        f"│ ⚡ 电力: {电力色}{'正常' if not 游戏.停电 else '断电!'}{RESET}",
        f"│ 📺 电视: {'开' if 游戏.电视开着 else '关'}",
        f"│ 🔦 手电: {'开' if 游戏.手电筒 else '关'}",
        f"│ 🚪 门锁: {GREEN if 游戏.门锁 else BRED}{'已锁' if 游戏.门锁 else '未锁!'}{RESET}",
        f"│ 🪟 窗户: {GREEN if 游戏.窗户关 else BRED}{'关闭' if 游戏.窗户关 else '打开!'}{RESET}",
        f"│ 👣 脚步: {YELLOW if 游戏.脚步声>3 else ''}{游戏.脚步声}次{RESET}",
        f"│ 💬 低语: {MAGENTA if 游戏.低语声>0 else ''}{游戏.低语声}次{RESET}",
        f"│ 🚪 敲门: {BRED if 游戏.敲门声>0 else ''}{游戏.敲门声}次{RESET}",
        f"│ 📞 电话: {BRED if 游戏.电话响 else ''}{'响铃' if 游戏.电话响 else '安静'}{RESET}",
        f"│ {理智色}{游戏.理智图标()} 理智: {progress_bar(游戏.理智,游戏.最大理智)}{RESET}",
        f"│ 📊 存活: {游戏.存活时间}分钟",
        f"└──────────────────────────┘",
    ]

    日志 = [f"{BWHITE}{BOLD}┌─ 事件日志 ────────────┐{RESET}"]
    for e in 游戏.事件日志:
        日志.append(f"│ {e}")
    while len(日志) < len(房间):
        日志.append(f"│")
    日志.append(f"└──────────────────────────┘")

    for i in range(max(len(房间), len(日志))):
        l = 房间[i] if i < len(房间) else ""
        r = 日志[i] if i < len(日志) else ""
        print(f"  {l}  {r}")

    # 成就行
    if 游戏.解锁成就:
        ach = "  ".join(f"{BYELLOW}🏆{RESET}" for _ in 游戏.解锁成就)
        print(f"  {ach}  {DIM}成就 {len(游戏.解锁成就)} 个{RESET}")

    print()
    print(f"  {GRAY}{'─'*58}{RESET}")

    # 操作提示（根据阶段动态调整）
    if 游戏.阶段 == "序章":
        print(f"  {CYAN}操作: w/s=换台  a/d=音量  t=开关  l=环顾  f=手电{RESET}")
        print(f"  {CYAN}      o=门锁  v=窗户  p=电话  i=物品  c=频道表  q=退出{RESET}")
    elif 游戏.阶段 == "第一章":
        print(f"  {CYAN}操作: w/s=换台  a/d=音量  t=开关  l=环顾  f=手电{RESET}")
        print(f"  {YELLOW}警告: 不要盯着屏幕太久...{RESET}")
    elif 游戏.阶段 == "第二章":
        print(f"  {CYAN}操作: w/s=换台  a/d=音量  t=开关  l=环顾  f=手电{RESET}")
        print(f"  {BRED}※ 它已经知道你在这里了 ※{RESET}")
    elif 游戏.阶段 == "第三章":
        print(f"  {CYAN}操作: w/s=换台  a/d=音量  t=开关  l=环顾  f=手电{RESET}")
        print(f"  {BRED}{BLINK}※ 不要关手电筒 ※ 不要开门 ※ 不要接电话 ※{RESET}")
    else:  # 终章
        print(f"  {BRED}{BOLD}操作: 生存 就是 一切{RESET}")
        print(f"  {BRED}{BLINK}※ 终章 · 他来了 ※{RESET}")

    print(f"  {GRAY}(手机端: 输入字母后按回车){RESET}")
    print(f"  {GRAY}{'─'*58}{RESET}")

    # 随机氛围警告
    if 游戏.理智 < 25:
        警告 = [
            f"  {BRED}{BLINK}※ 你感觉它就在你房间里 ※{RESET}",
            f"  {BRED}※ 不要关灯...绝对不要 ※{RESET}",
            f"  {YELLOW}※ 电视里的人在和你说话 ※{RESET}",
            f"  {BRED}※ 你听到自己的声音在门外笑 ※{RESET}",
            f"  {BRED}※ 镜子里的人没在呼吸 ※{RESET}",
        ]
        print(random.choice(警告))

# ═══════════════════════════════════════════════════════════
#  动作系统
# ═══════════════════════════════════════════════════════════
def 动作_开关电视(g):
    if g.停电:
        g.记录(f"{RED}停电了，电视打不开{RESET}"); return
    g.电视开着 = not g.电视开着
    if g.电视开着:
        g.记录(f"{GREEN}电视开启 - 频道{g.当前频道:02d}{RESET}")
        g.检查成就("第一次开电视")
        # 开机雪花
        for _ in range(3):
            print(f"  {DIM}{static_line(42)}{RESET}", flush=True)
            time.sleep(0.04)
    else:
        g.记录(f"{DIM}电视关闭{RESET}")
        g.检查成就("主动关电视的勇气")

def 动作_换台(g, 方向):
    """方向: +1=上一个(数字增大) -1=下一个(数字减小)"""
    if not g.电视开着:
        g.记录(f"{RED}电视没开{RESET}"); return
    if g.停电:
        g.记录(f"{RED}停电了{RESET}"); return

    idx = 频道列表.index(g.当前频道) if g.当前频道 in 频道列表 else 0
    g.当前频道 = 频道列表[(idx + 方向) % len(频道列表)]
    g.切换次数 += 1
    g.电视累计时长 += 1

    # 换台雪花
    for _ in range(3):
        print(f"  {DIM}{static_line(42)}{RESET}", flush=True)
        time.sleep(0.03)

    # 首次发现频道
    if g.当前频道 not in g.已知频道:
        g.已知频道.add(g.当前频道)
        g.发现秘密 += 1

    # 隐藏频道首次触发
    if g.当前频道 == 13 and not g.见过13:
        g.见过13 = True; g.理智 -= 12; g.恐怖事件 += 1
        g.记录(f"{BRED}{BOLD}你不该调到这个频道...{RESET}")
        g.检查成就("窥探禁忌")
    elif g.当前频道 == 14 and not g.见过14:
        g.见过14 = True; g.理智 -= 15; g.恐怖事件 += 1
        g.记录(f"{BRED}那个频道在播放...你的房间?!{RESET}")
        g.检查成就("被监视")
    elif g.当前频道 == 15 and not g.见过15:
        g.见过15 = True; g.理智 -= 20; g.恐怖事件 += 1
        g.记录(f"{BRED}{BOLD}频道15认出了你{RESET}")
        g.检查成就("被标记")
    elif g.当前频道 == 16 and not g.见过16:
        g.见过16 = True; g.理智 -= 25; g.恐怖事件 += 1
        g.记录(f"{BRED}{BOLD}频道16...你在里面{RESET}")
        g.检查成就("超越界限")
    else:
        g.记录(f"{CYAN}→ 频道{g.当前频道:02d} {频道名称.get(g.当前频道,'?')}{RESET}")

    # 换台超过50次解锁成就
    if g.切换次数 >= 50: g.检查成就("频道 surfing 大师")
    if len(g.已知频道) >= 17: g.检查成就("全频道收集")

def 动作_音量(g, 增减):
    if not g.电视开着:
        g.记录(f"{RED}电视没开{RESET}"); return
    if 增减 > 0:
        g.音量 = min(10, g.音量 + 1)
        g.记录(f"音量: {g.音量}/10 {YELLOW}▲{RESET}")
        if g.音量 >= 9: g.记录(f"{RED}太大声了...整栋楼都听得见{RESET}"); g.理智 -= 2
    else:
        g.音量 = max(0, g.音量 - 1)
        g.记录(f"音量: {g.音量}/10 {DIM}▼{RESET}")
        if g.音量 == 0: g.记录(f"{DIM}静音...但你能听到更清楚的其他声音{RESET}")

def 动作_环顾(g):
    g.环顾次数 += 1
    g.记录(f"{CYAN}你环顾四周...{RESET}")

    if g.停电 and not g.手电筒:
        g.记录(f"{RED}太暗了...什么都看不见{RESET}")
        g.理智 -= 8; return

    # 根据阶段增加恐怖程度
    恐怖倍率 = 1.0
    if g.阶段 == "第二章": 恐怖倍率 = 1.5
    if g.阶段 == "第三章": 恐怖倍率 = 2.0
    if g.阶段 == "终章": 恐怖倍率 = 3.0

    地点 = [
        ("门口", f"{GREEN}门锁完好{RESET}", f"{YELLOW}锁芯有新的划痕{RESET}", f"{BRED}门把手在缓慢转动...{RESET}"),
        ("窗户", f"{GREEN}窗户紧闭{RESET}", f"{RED}窗玻璃上有个手印...从外面{RESET}", f"{BRED}窗外贴着一张脸{RESET}"),
        ("衣柜", f"{GREEN}衣柜关着{RESET}", f"{YELLOW}门开了一条缝...里面黑{RESET}", f"{BRED}衣柜里有东西在呼吸{RESET}"),
        ("床下", f"{GREEN}什么都没有{RESET}", f"{YELLOW}床下有东西在动...{RESET}", f"{BRED}一双眼睛在床下看着你{RESET}"),
        ("天花板", f"{GREEN}天花板正常{RESET}", f"{YELLOW}天花板上传来刮擦声{RESET}", f"{BRED}天花板在渗血{RESET}"),
        ("镜子", f"{GREEN}镜子里是你{RESET}", f"{YELLOW}镜中的你慢了半秒{RESET}", f"{BRED}镜子里的人没有转身{RESET}"),
        ("电话", f"{GREEN}电话挂好了{RESET}", f"{YELLOW}通话记录里有个未知号码{RESET}", f"{BRED}电话在响...但你没碰它{RESET}"),
        ("电视", f"{GREEN}电视正常{RESET}", f"{YELLOW}屏幕有关不掉的残影{RESET}", f"{BRED}电视里有人在等你转头{RESET}"),
    ]

    基础概率 = 0.12 + g.环顾次数 * 0.06
    for 名, 安全, 中等, 恐怖 in 地点:
        r = random.random()
        if r < 基础概率 * 恐怖倍率:
            g.记录(f"  {名}: {恐怖}")
            dmg = int(random.randint(8,12) * 恐怖倍率)
            g.理智 -= dmg
            g.恐怖事件 += 1
        elif r < (基础概率 + 0.15) * 恐怖倍率:
            g.记录(f"  {名}: {中等}")
            g.理智 -= random.randint(3, 5)
        else:
            g.记录(f"  {名}: {安全}")

    # 环顾10次以上开始有额外惩罚
    if g.环顾次数 >= 10:
        g.记录(f"{BRED}{BLINK}你看了太多次了...它注意到你了{RESET}")
        g.理智 -= 5

def 动作_手电(g):
    g.手电筒 = not g.手电筒
    if g.手电筒:
        g.记录(f"{YELLOW}手电筒打开{RESET}")
        if g.停电: g.记录(f"{GREEN}至少现在能看见东西了{RESET}")
    else:
        g.记录(f"{DIM}手电筒关闭{RESET}")
        if g.停电:
            g.记录(f"{RED}黑暗重新吞噬了一切...{RESET}")
            g.理智 -= 5

def 动作_门锁(g):
    g.门锁 = not g.门锁
    if g.门锁:
        g.记录(f"{GREEN}门锁上了{RESET}")
        g.检查成就("安全意识")
    else:
        g.记录(f"{BRED}门解锁了...{RESET}")
        g.记录(f"{BRED}{BLINK}你确定要这样做吗?{RESET}")
        g.理智 -= 5

def 动作_窗户(g):
    g.窗户关 = not g.窗户关
    if g.窗户关:
        g.记录(f"{GREEN}窗户关上了{RESET}")
    else:
        g.记录(f"{BRED}窗户打开了...{RESET}")
        g.记录(f"{RED}冷风灌了进来...还有低语声{RESET}")
        g.理智 -= 7
        g.温度 -= 2

def 动作_电话(g):
    if g.电话响 == 0:
        g.记录(f"{DIM}电话没有响{RESET}"); return

    g.记录(f"{YELLOW}电话还在响...{RESET}")
    接听 = 获取输入("  接听? (y/n): ")
    if 接听 == 'y':
        g.电话响 = 0
        消息 = [
            f"{BRED}...你在看频道13对吧...{RESET}",
            f"{BRED}...门锁好了吗...我这边打不开门...{RESET}",
            f"{BRED}...别挂电话...求你了...{RESET}",
            f"{BRED}...我就在你门外...{RESET}",
            f"{BRED}...嘘...他听见了...{RESET}",
            f"{BRED}...你身后...镜子后面...{RESET}",
        ]
        # 周目越高，电话内容越恐怖
        if g.周目 >= 2:
            消息.append(f"{BRED}{BOLD}...上一世你就是在这里死的...{RESET}")
        if g.周目 >= 3:
            消息.append(f"{BRED}{BOLD}...你已经死了...这是你的遗物...{RESET}")

        msg = random.choice(消息)
        g.记录(f"📞 {msg}")
        g.理智 -= random.randint(8, 15)

        if random.random() < 0.1:
            g.记录(f"{BRED}{BOLD}...声音...是你的{RESET}")
            g.理智 -= 20
    else:
        g.记录(f"{DIM}你让电话继续响着...{RESET}")
        g.理智 -= 3

def 动作_物品(g):
    print()
    print(f"  {BWHITE}{BOLD}┌─ 物品栏 ─────────────────────────────────┐{RESET}")
    items = list(g.物品.items())
    for i, (名, info) in enumerate(items):
        print(f"  {BWHITE}{BOLD}│{RESET} [{i+1}] {名:8s} {info['描述']:30s} {BWHITE}{BOLD}│{RESET}")
    print(f"  {BWHITE}{BOLD}└────────────────────────────────────────────┘{RESET}")
    print(f"  {DIM}提示: 手机可能收到奇怪的短信{RESET}")

    c = 获取输入("  选择(1-6)或回车返回: ")

    if c == '1':  # 手机
        g.记录(f"{DIM}手机信号: 仅一格{RESET}")
        g.记录(f"{GRAY}搜索网络...找到 'TV_Horror_Net'{RESET}")
        if g.周目 >= 2:
            g.记录(f"{RED}有一条未读短信:{RESET}")
            g.记录(f"{RED}'别走和上次一样的路'{RESET}")
        g.检查成就("尝试联网")
    elif c == '2':  # 手电筒
        g.记录(f"{DIM}手电筒电量充足{RESET}")
        if g.停电: g.记录(f"{GREEN}黑暗中唯一的伙伴{RESET}")
    elif c == '3':  # 钥匙
        g.记录(f"{DIM}家门钥匙...只有一把{RESET}")
        g.记录(f"{GRAY}钥匙上有刻字...'不要复制'{RESET}")
    elif c == '4':  # 日记本
        if not g.阅读日记:
            g.阅读日记 = True
            g.检查成就("翻开真相")
        g.记录(f"{MAGENTA}翻开日记...{RESET}")
        页数 = [
            f"{DIM}\"今晚电视又自己开了\"{RESET}",
            f"{DIM}\"频道13...那个画面...\"{RESET}",
            f"{DIM}\"我已经三天没出门了\"{RESET}",
            f"{DIM}\"食物快吃完了\"{RESET}",
            f"{DIM}\"但我不饿\"{RESET}",
            f"{BRED}\"因为它一直在喂我\"{RESET}",
            f"{BRED}\"今天的日记不是我写的\"{RESET}",
            f"{BRED}\"字迹和昨天的一样\"{RESET}",
            f"{BRED}\"但昨天是我写的\"{RESET}",
            f"{BRED}{BOLD}\"我们都被困在这里\"{RESET}",
            f"{BRED}{BOLD}\"每一周目都是\"{RESET}",
        ]
        # 周目越高，解锁越多页
        可见 = 页数[:min(len(页数), 4 + g.周目 * 2)]
        for p in 可见:
            g.记录(f"  {p}")
            time.sleep(0.4)
        g.理智 = min(g.最大理智, g.理智 + 5)  # 读日记恢复一点理智（了解真相的安慰）
        g.记录(f"{GREEN}了解真相让你稍微安心了{RESET}")
    elif c == '5':  # 泰迪熊
        g.记录(f"{DIM}你拿起泰迪熊...{RESET}")
        if random.random() < 0.4 + g.周目 * 0.1:
            g.记录(f"{BRED}它对你笑了{RESET}")
            g.理智 -= 10
        else:
            g.记录(f"{GREEN}它给了你一点安慰{RESET}")
            g.理智 = min(g.最大理智, g.理智 + 3)
    elif c == '6':  # 收音机
        g.记录(f"{DIM}收音机...调频中...{RESET}")
        频率 = [
            f"{GRAY}...白噪音...{RESET}",
            f"{GRAY}...一段莫尔斯电码...{RESET}",
            f"{RED}...help... I'm trapped in the TV...{RESET}",
            f"{RED}...不要相信频道13...{RESET}",
            f"{BRED}...快跑...{RESET}",
        ]
        for _ in range(random.randint(2, 4)):
            msg = random.choice(频率)
            g.记录(f"  📻 {msg}")
            time.sleep(0.3)
        g.理智 -= random.randint(2, 5)

def 动作_静音(g):
    if not g.电视开着:
        g.记录(f"{RED}电视没开{RESET}"); return
    if g.音量 > 0:
        g._上次音量 = g.音量; g.音量 = 0
        g.记录(f"{DIM}静音{RESET}")
    else:
        g.音量 = g._上次音量
        g.记录(f"{GREEN}取消静音 → {g.音量}/10{RESET}")

def 动作_频道表(g):
    print()
    print(f"  {BWHITE}{BOLD}┌─ 频道列表 ──────────────────────────────────┐{RESET}")
    for n in 频道列表:
        if n in g.已知频道:
            mark = f"{BRED}★{RESET}" if n in (13,14,15,16) else f"{GREEN}●{RESET}"
            name = 频道名称.get(n, "?")
            extra = ""
            if n == 13: extra = f"{BRED} 危险{RESET}"
            if n == 14: extra = f"{BRED} 监控{RESET}"
            if n == 15: extra = f"{BRED} 注视{RESET}"
            if n == 16: extra = f"{BRED}{BLINK} 终焉{RESET}"
            print(f"  {BWHITE}{BOLD}│{RESET} {mark} CH{n:02d} {CYAN}{name:10s}{RESET}{extra:20s}{BWHITE}{BOLD}│{RESET}")
        else:
            print(f"  {BWHITE}{BOLD}│{RESET} {GRAY}?  CH{n:02d} {'未知':10s}{RESET}{BWHITE}{BOLD}│{RESET}")
    print(f"  {BWHITE}{BOLD}└──────────────────────────────────────────────┘{RESET}")
    print(f"  {DIM}●=已发现 ★=危险 ?=未知 已发现{len(g.已知频道)}/17个频道{RESET}")
    if len(g.已知频道) < 17:
        print(f"  {DIM}提示: 持续换台可以发现新频道{RESET}")
    获取输入("  按回车返回... ")

def 动作_帮助():
    print()
    print(f"  {CYAN}{BOLD}┌─ 操作帮助 ────────────────────────────────┐{RESET}")
    print(f"  {CYAN}{BOLD}│{RESET} w/s = 换台(上/下)  a/d = 音量(左/右) {CYAN}{BOLD}│{RESET}")
    print(f"  {CYAN}{BOLD}│{RESET} t   = 开关电视     l   = 环顾四周   {CYAN}{BOLD}│{RESET}")
    print(f"  {CYAN}{BOLD}│{RESET} f   = 手电筒       o   = 门锁       {CYAN}{BOLD}│{RESET}")
    print(f"  {CYAN}{BOLD}│{RESET} v   = 窗户         p   = 接电话     {CYAN}{BOLD}│{RESET}")
    print(f"  {CYAN}{BOLD}│{RESET} i   = 物品栏       m   = 静音       {CYAN}{BOLD}│{RESET}")
    print(f"  {CYAN}{BOLD}│{RESET} c   = 频道列表     h   = 帮助       {CYAN}{BOLD}│{RESET}")
    print(f"  {CYAN}{BOLD}│{RESET} q   = 退出                                      {CYAN}{BOLD}│{RESET}")
    print(f"  {CYAN}{BOLD}└──────────────────────────────────────────────┘{RESET}")
    print(f"  {DIM}手机端: 输入字母后按回车{RESET}")
    print(f"  {DIM}PC端: 可直接输入字母或方向键{RESET}")
    print(f"  {DIM}本游戏纯文字体验，建议暗光环境{RESET}")
    获取输入("  按回车继续... ")

# ═══════════════════════════════════════════════════════════
#  粘性系统（多周目 / 解锁 / 成就 / 隐藏要素）
# ═══════════════════════════════════════════════════════════
def 检查粘性事件(g):
    """各种隐藏解锁条件"""
    # 存活超过100分钟
    if g.存活时间 == 100: g.检查成就("百分钟生存者")
    if g.存活时间 == 200: g.检查成就("两百分忍耐")
    if g.存活时间 == 300: g.检查成就("永夜守候")

    # 不看电视超过50分钟
    if not g.电视开着 and g.存活时间 % 50 == 0 and g.存活时间 > 0:
        g.记录(f"{GREEN}你坚持不看任何电视{RESET}")
        g.检查成就("绝缘体")

    # 理智保持80以上超过100分钟
    if g.理智 > 80 and g.存活时间 > 100:
        g.检查成就("钢铁意志")

    # 收集所有线索
    if len(g.隐藏线索) >= 7 and "真相碎片" not in g.解锁成就:
        g.检查成就("真相碎片")
        g.记录(f"{BYELLOW}你拼凑出了完整的真相...{RESET}")
        g.记录(f"{BYELLOW}那座广播塔下埋着...{RESET}")
        g.记录(f"{BYELLOW}1953年失踪的所有人...{RESET}")
        g.记录(f"{BRED}他们被做成了电视节目{RESET}")

    # 特定条件解锁隐藏频道16
    if (g.见过13 and g.见过14 and g.见过15 and 16 not in g.已知频道):
        g.记录(f"{BRED}{BLINK}...你感受到了一个新的频道...{RESET}")
        g.记录(f"{BRED}...它一直在等你发现...{RESET}")

# ═══════════════════════════════════════════════════════════
#  随机事件系统（分阶段递增）
# ═══════════════════════════════════════════════════════════
def 随机事件(g):
    # 停电中的独立事件
    if g.停电:
        if random.random() < 0.25:
            事件池 = [
                (f"{YELLOW}黑暗中...走廊传来脚步声{RESET}", 5, "foot"),
                (f"{MAGENTA}黑暗里有人低语你的名字{RESET}", 5, "whisper"),
                (f"{BRED}{BLINK}你在黑暗中听到了呼吸声...就在耳边{RESET}", 10, "breath"),
                (f"{BRED}有人敲门...很轻...很慢...{RESET}", 8, "knock"),
                (f"{BRED}有人在用指甲刮门{RESET}", 12, "knock"),
                (f"{BRED}{BLINK}手电筒的光...照到了一双眼睛{RESET}", 15, "eye"),
            ]
            消息, 伤害, 类型 = random.choice(事件池)
            g.记录(消息); g.理智 -= 伤害
            if 类型 == "foot": g.脚步声 += 1
            if 类型 == "knock": g.敲门声 += 1
            if 类型 == "whisper": g.低语声 += 1
        return

    # 基础概率随阶段递增
    基础 = 0.08
    if g.阶段 == "第一章": 基础 = 0.12
    if g.阶段 == "第二章": 基础 = 0.16
    if g.阶段 == "第三章": 基础 = 0.20
    if g.阶段 == "终章": 基础 = 0.25

    r = random.random()

    if r < 基础:
        g.脚步声 += 1; g.理智 -= 3
        g.记录(f"{YELLOW}脚步声...走廊方向{RESET}")
        g.隐藏线索.append("footstep")
    elif r < 基础 + 0.05:
        g.低语声 += 1; g.理智 -= 4
        低语 = [
            "\"快来看电视...\"",
            "\"你为什么不笑...\"",
            "\"我就在你身后...\"",
            "\"你锁门了对吗...\"",
            "\"窗户也没关吧...\"",
            "\"频道13...调过去...\"",
            "\"我们都在看着你...\"",
        ]
        g.记录(f"{MAGENTA}{random.choice(低语)}{RESET}")
    elif r < 基础 + 0.08:
        g.温度 -= random.randint(1, 2)
        g.记录(f"{CYAN}温度在下降...{RESET}")
    elif r < 基础 + 0.10:
        g.理智 -= 8
        g.记录(f"{BRED}{BLINK}你听到了呼吸声...就在你耳边{RESET}")
    elif r < 基础 + 0.12:
        g.敲门声 += 1; g.理智 -= 6
        g.记录(f"{BRED}有人在敲门...{RESET}")
    elif r < 基础 + 0.135 and not g.停电:
        g.记录(f"{BRED}{BOLD}⚡ 突然停电！整个房间陷入黑暗！{RESET}")
        g.停电 = True; g.电视开着 = False
        g.检查成就("经历停电")
    elif r < 基础 + 0.15:
        g.电话响 += 1; g.理智 -= 5
        g.记录(f"{BRED}电话响了...凌晨的电话...{RESET}")
    elif r < 基础 + 0.17:
        g.恐怖事件 += 1; g.理智 -= random.randint(3, 7)
        事件 = [
            f"{RED}镜子里的你...眨了眼{RESET}",
            f"{RED}衣柜门...自己开了...{RESET}",
            f"{YELLOW}你闻到一股腐臭味...{RESET}",
            f"{RED}天花板上...有刮擦声{RESET}",
            f"{BRED}电视关了...但屏幕还亮着{RESET}",
            f"{RED}你手机亮了...没人发消息...{RESET}",
            f"{BRED}身后传来纸张翻动的声音...{RESET}",
        ]
        g.记录(f"{random.choice(事件)}")
    elif r < 基础 + 0.185:
        # 电视自动开启
        if not g.电视开着 and not g.停电:
            g.电视开着 = True
            g.记录(f"{BRED}{BLINK}电视自己打开了...{RESET}")
            g.理智 -= 5
            if g.周目 >= 2:
                g.记录(f"{BRED}...每次都一样...它总是自己开...{RESET}")

    # 看电视频道13的持续伤害
    if g.当前频道 == 13 and g.电视开着:
        g.理智 -= 1
        if random.random() < 0.10:
            g.记录(f"{BRED}频道13在蚕食你的理智...{RESET}")
    if g.当前频道 == 16 and g.电视开着:
        g.理智 -= 3
        if random.random() < 0.15:
            g.记录(f"{BRED}{BLINK}频道16在改写你的记忆...{RESET}")

    # 粘性检查
    检查粘性事件(g)

# ═══════════════════════════════════════════════════════════
#  剧情系统（开场 + 阶段推进）
# ═══════════════════════════════════════════════════════════
def 播放剧情(标题, 文本列表, 速度=0.04):
    """播放一段剧情文字"""
    cls()
    print()
    print(f"  {BRED}{BOLD}╔════════════════════════════════════════════════════╗{RESET}")
    print(f"  {BRED}{BOLD}║  {标题:^48s}  ║{RESET}")
    print(f"  {BRED}{BOLD}╚════════════════════════════════════════════════════╝{RESET}")
    print()
    for line in 文本列表:
        slow(line, 速度)
        time.sleep(0.15)
    print()
    获取输入(f"  {DIM}按回车继续...{RESET}")

def 开场剧情():
    """游戏开场剧情"""
    cls()
    hide_cur()

    # 标题画面
    for _ in range(3):
        print(f"\r  {BRED}{BOLD}    📺 电 视 模 拟 恐 怖 📺{RESET}    ", end="", flush=True)
        time.sleep(0.5)
        print(f"\r  {DIM}    📺 电 视 模 拟 恐 怖 📺{RESET}    ", end="", flush=True)
        time.sleep(0.3)
    print()

    # 开场白
    播放剧情("序 章 · 深 夜 来 电", [
        f"{GRAY}2024年11月15日，周五，23:30{RESET}",
        f"",
        f"  你一个人住在这栋老公寓的{RED}13楼{RESET}。",
        f"  今天是发薪日，但你一点也高兴不起来。",
        f"  因为昨晚......{RED}电视自己开了{RESET}。",
        f"",
        f"  你清楚地记得自己睡前关了它。",
        f"  但凌晨三点，你被{RED}声音{RESET}吵醒了。",
        f"  不是闹钟，不是手机。",
        f"  是{RED}电视里的笑声{RESET}。",
        f"",
        f"  你冲出卧室，客厅的电视正亮着。",
        f"  屏幕上是一个你从未见过的频道。",
        f"  画面很简单——{BRED}一个空房间{RESET}。",
        f"  然后镜头缓缓转向{RED}一面镜子{RESET}。",
        f"  镜子里......{BRED}没有你{RESET}。",
        f"",
        f"  你拔掉了电视的电源。",
        f"  但你感觉......{RED}它还会回来{RESET}。",
        f"",
        f"  今晚，你决定{RED}不再逃避{RESET}。",
        f"  你要搞清楚......{BRED}电视里到底有什么{RESET}。",
        f"",
        f"  你坐在沙发上，{GREEN}遥控器{RESET}就在手边。",
        f"  窗外下起了{RED}雾{RESET}。",
        f"  手机信号{RED}只有一格{RESET}。",
        f"  门锁上了。窗户关了。手电筒满电。",
        f"",
        f"  {YELLOW}但是......{RESET}",
        f"  {YELLOW}你忘了检查衣柜。{RESET}",
        f"",
        f"  {GRAY}23:47。电视屏幕反射着客厅的灯光。{RESET}",
        f"  {GRAY}你拿起遥控器。{RESET}",
        f"  {GRAY}你知道......今晚不会太平。{RESET}",
        f"",
        f"  {BRED}游戏开始。{RESET}",
    ])

def 阶段剧情(g):
    """阶段性剧情插入"""
    if g.阶段 == "第一章" and g.存活时间 == 31:
        播放剧情("第一章 · 信号", [
            f"  23:50。你看了大约三分钟电视。",
            f"  一切似乎......{GREEN}正常{RESET}。",
            f"  新闻在播报失踪案。卡通频道在播海绵宝宝。",
            f"  你甚至开始{RED}怀疑昨晚是自己记错了{RESET}。",
            f"",
            f"  然后你调到{RED}频道7{RESET}。",
            f"  测试图案。彩色条纹。",
            f"  你准备继续往下换......",
            f"  {BRED}但图案变了{RESET}。",
            f"",
            f"  条纹开始{RED}扭曲{RESET}。",
            f"  像是有什么东西在{RED}推{RESET}它们。",
            f"  然后中间出现了一行小字：",
            f"",
            f"  {BRED}{BOLD}\"你在看我吗\"{RESET}",
            f"",
            f"  你{RED}猛地按了换台键{RESET}。",
            f"  雪花屏。然后新闻。然后购物。",
            f"  你的手在{RED}发抖{RESET}。",
            f"",
            f"  {GRAY}这不是你记错了。{RESET}",
            f"  {GRAY}电视里有东西。{RESET}",
            f"  {GRAY}它在找你。{RESET}",
        ])

    if g.阶段 == "第二章" and g.存活时间 == 81:
        播放剧情("第二章 · 入侵", [
            f"  00:15。停电了一次。",
            f"  持续了大约三十秒。",
            f"  足够让你{RED}浑身冷汗{RESET}。",
            f"",
            f"  来电后电视{RED}自动打开了{RESET}。",
            f"  停在你昨晚看到的那个频道。",
            f"  空房间。镜子。",
            f"  {BRED}但这次镜子里有人{RESET}。",
            f"",
            f"  你{RED}看不清脸{RESET}。",
            f"  但你能感觉到......{BRED}他在笑{RESET}。",
            f"",
            f"  你拔了电源。这次用{RED}剪刀{RESET}剪断了线。",
            f"  然后你听到{RED}走廊有声音{RESET}。",
            f"  脚步声。停在你{RED}门口{RESET}。",
            f"",
            f"  你{RED}透过猫眼往外看{RESET}。",
            f"  {BRED}一只眼睛{RESET}。",
            f"  {BRED}正看着猫眼{RESET}。",
            f"",
            f"  你后退三步。",
            f"  门锁是{RED}NightGuard{RESET}牌的。",
            f"  广告说能挡住任何东西。",
            f"  {GRAY}但广告没说能不能挡住{RESET}",
            f"  {GRAY}......从电视里爬出来的东西。{RESET}",
        ])

    if g.阶段 == "第三章" and g.存活时间 == 151:
        播放剧情("第三章 · 真相", [
            f"  00:47。你读完了整本日记。",
            f"  不是你写的。{RED}不是你的字迹{RESET}。",
            f"  但内容......{BRED}一字不差{RESET}。",
            f"  写着你每天做的事。想的事。{RED}害怕的东西{RESET}。",
            f"",
            f"  最后一页写着：",
            f"",
            f"  {BRED}{BOLD}\"1953年，广播塔建成。\"{RESET}",
            f"  {BRED}{BOLD}\"塔下六米，埋着一台电视机。\"{RESET}",
            f"  {BRED}{BOLD}\"那不是普通的电视机。\"{RESET}",
            f"  {BRED}{BOLD}\"那是一扇门。\"{RESET}",
            f"  {BRED}{BOLD}\"每晚午夜，门会开一条缝。\"{RESET}",
            f"  {BRED}{BOLD}\"里面的东西......会爬出来。\"{RESET}",
            f"  {BRED}{BOLD}\"爬进电波里。\"{RESET}",
            f"  {BRED}{BOLD}\"爬进信号里。\"{RESET}",
            f"  {BRED}{BOLD}\"爬进......你的电视里。\"{RESET}",
            f"",
            f"  你{RED}抬头看了一眼电视{RESET}。",
            f"  插头早就剪断了。",
            f"  但屏幕......{BRED}还是亮的{RESET}。",
            f"",
            f"  画面上出现了一行字：",
            f"  {BRED}{BLINK}\"你读过日记了。现在你知道了。\"{RESET}",
            f"  {BRED}{BLINK}\"那你知道该怎么做了吧。\"{RESET}",
            f"  {BRED}{BLINK}\"调到频道16。\"{RESET}",
            f"  {BRED}{BLINK}\"那是唯一的出口。\"{RESET}",
            f"  {BRED}{BLINK}\"或者......入口。\"{RESET}",
        ])

    if g.阶段 == "终章" and g.存活时间 == 251:
        播放剧情("终 章 · 来 者", [
            f"  01:30。理智的边界早已模糊。",
            f"  你分不清{RED}现实和幻觉{RESET}。",
            f"  也许从一开始......{BRED}就没有区别{RESET}。",
            f"",
            f"  门锁被{RED}打破了{RESET}。",
            f"  不是被撬开的。是{RED}从里面{RESET}被打开的。",
            f"  像是有人在{RED}你的门后{RESET}等着。",
            f"",
            f"  电视里......{BRED}全都是你的脸{RESET}。",
            f"  不同年龄。不同表情。",
            f"  有些在{RED}笑{RESET}。有些在{RED}哭{RESET}。",
            f"  有一个......{BRED}已经死了{RESET}。",
            f"",
            f"  你终于明白{RED}频道16{RESET}是什么了。",
            f"  不是出口。不是入口。",
            f"  {BRED}是转世{RESET}。",
            f"  {BRED}是循环{RESET}。",
            f"  {BRED}是每一次你死在这里{RESET}，",
            f"  {BRED}又在这里醒来。{RESET}",
            f"",
            f"  手机震动了。一条短信：",
            f"  {BRED}{BOLD}\"欢迎来到第{g.周目+1}周目\"{RESET}",
            f"",
            f"  {GRAY}电视屏幕裂开了。{RESET}",
            f"  {GRAY}一只手伸了出来。{RESET}",
            f"  {GRAY}然后是另一只。{RESET}",
            f"  {GRAY}然后是头。{RESET}",
            f"  {GRAY}然后是......整具身体。{RESET}",
            f"",
            f"  {BRED}{BOLD}他长得和你一模一样。{RESET}",
            f"",
            f"  {GRAY}他朝你伸出手。{RESET}",
            f"  {GRAY}\"跟我来，\"他说，\"这次换你。\"{RESET}",
            f"  {GRAY}\"你去频道16。\"{RESET}",
            f"  {GRAY}\"我来坐这里。\"{RESET}",
            f"  {GRAY}\"下一轮，我们再换。\"{RESET}",
            f"",
            f"  {BRED}{BOLD}你意识到......你不是受害者。{RESET}",
            f"  {BRED}{BOLD}你是轮班的。{RESET}",
            f"  {BRED}{BOLD}每一晚，一个人进去。{RESET}",
            f"  {BRED}{BOLD}一个人出来。{RESET}",
            f"  {BRED}{BOLD}从来没有人同时见过两个人。{RESET}",
            f"  {BRED}{BOLD}因为进去的那个人......{RESET}",
            f"  {BRED}{BOLD}永远不会出来。{RESET}",
        ])

# ═══════════════════════════════════════════════════════════
#  结局系统（8个结局）
# ═══════════════════════════════════════════════════════════
def 结局画面(g, 标题, 副标题, 正文, 提示):
    cls()
    print()
    print(f"  {BRED}{BOLD}╔════════════════════════════════════════════════════╗{RESET}")
    print(f"  {BRED}{BOLD}║  {标题:^48s}  ║{RESET}")
    print(f"  {BRED}{BOLD}╚════════════════════════════════════════════════════╝{RESET}")
    print()
    print(f"  {RED}{副标题}{RESET}")
    print()
    for line in 正文:
        print(f"  {line}")
    print()
    print(f"  {GRAY}{'─'*56}{RESET}")
    print(f"  {提示}")
    print()

def 结算(g, 原因):
    g.结局次数 += 1
    g.结局原因 = 原因

    # 统计
    print()
    print(f"  {BWHITE}{BOLD}┌─ 本局统计 ──────────────────────────┐{RESET}")
    print(f"  {BWHITE}{BOLD}│{RESET} 存活时间: {YELLOW}{g.存活时间}{RESET} 分钟")
    print(f"  {BWHITE}{BOLD}│{RESET} 最终理智: {RED}{g.理智}/{g.最大理智}{RESET}")
    print(f"  {BWHITE}{BOLD}│{RESET} 换台次数: {g.切换次数} 次")
    print(f"  {BWHITE}{BOLD}│{RESET} 恐怖事件: {BRED}{g.恐怖事件}{RESET} 次")
    print(f"  {BWHITE}{BOLD}│{RESET} 发现频道: {len(g.已知频道)}/17")
    print(f"  {BWHITE}{BOLD}│{RESET} 成就解锁: {len(g.解锁成就)} 个")
    print(f"  {BWHITE}{BOLD}│{RESET} 周目次数: {g.结局次数} 次")
    print(f"  {BWHITE}{BOLD}│{RESET} 到达阶段: {RED}{g.阶段}{RESET}")
    print(f"  {BWHITE}{BOLD}└──────────────────────────────────────────┘{RESET}")

    # 解锁的成就
    if g.解锁成就:
        print(f"\n  {BYELLOW}🏆 成就列表:{RESET}")
        for a in g.解锁成就:
            print(f"    {GREEN}✓{RESET} {a}")

    print()

def 游戏结束(g, 原因):
    """8种结局分发"""
    渲染(g)  # 最后渲染一帧

    if 原因 == "insanity":
        结局画面(g,
            "💀 理 智 归 零 💀",
            "~ 结局一：同化 ~",
            [
                "你的视线开始模糊。",
                "墙壁在融化。电视的画面变成了你的脸。",
                "不......不是变成了你的脸......",
                f"{BRED}那就是你的脸。{RESET}",
                "你听到电视里的人在笑。",
                "然后你意识到——",
                f"{BRED}你就是电视里的人。{RESET}",
                f"{BRED}你一直都是。{RESET}",
                "外面的\"你\"只是......",
                "下一个轮班的。",
                "",
                f"{GRAY}你坐在沙发上，拿起遥控器。{RESET}",
                f"{GRAY}电视关了。{RESET}",
                f"{GRAY}明天会有一个新人搬进来。{RESET}",
                f"{GRAY}他会坐在同一张沙发上。{RESET}",
                f"{GRAY}他会拿起同一个遥控器。{RESET}",
                f"{GRAY}他会......{RESET}",
                f"{BRED}看到你。{RESET}",
            ],
            f"  {DIM}提示: 试着不要看频道13太久...也许下次能撑更久{RESET}"
        )
    elif 原因 == "intruder":
        结局画面(g,
            "🚪 它 进 来 了 🚪",
            "~ 结局二：破门 ~",
            [
                "门锁发出一声脆响。",
                "不是被撬开的。是{RED}被撞开的{RESET}。",
                "沉重的脚步声走进客厅。",
                "一步一步。",
                "朝着沙发。",
                "朝着你。",
                "",
                f"{BRED}你看到了它的脸。{RESET}",
                "那是一张{RED}没有五官{RESET}的脸。",
                "只有一张{RED}嘴{RESET}。",
                "它在笑。",
                "",
                f"{GRAY}你想起广告说的那句话:{RESET}",
                f"{GRAY}\"NightGuard能挡住任何东西。\"{RESET}",
                f"{BRED}任何东西。{RESET}",
                f"{BRED}除了从电视里爬出来的。{RESET}",
                "",
                f"{BRED}它坐在了你旁边。{RESET}",
                f"{BRED}拿起了遥控器。{RESET}",
                f"{BRED}\"该你了，\"它说。{RESET}",
                f"{BRED}\"你去频道16。\"{RESET}",
            ],
            f"  {DIM}提示: 手电筒在停电时是必需品...下次记得先开{RESET}"
        )
    elif 原因 == "discovered":
        结局画面(g,
            "👁️ 它 发 现 你 了 👁️",
            "~ 结局三：被标记 ~",
            [
                "你不该环顾这么多次的。",
                "现在它知道你在找它了。",
                "而它......也在找你。",
                "",
                "电视屏幕{RED}裂开了{RESET}。",
                "不是碎裂。是像皮肤一样{RED}裂开{RESET}。",
                "一只手伸了出来。",
                "然后是另一只。",
                "然后是{RED}头{RESET}。",
                "",
                f"{BRED}他长得和你一模一样。{RESET}",
                "",
                "\"你好，\"他说。\"我是上一周的你。\"",
                "\"或者说......上一个死在这里的你。\"",
                "",
                f"{GRAY}他递给你一张纸条。{RESET}",
                f"{GRAY}上面写着频道16的密码。{RESET}",
                f"{GRAY}字迹......是你的。{RESET}",
            ],
            f"  {DIM}提示: 环顾要节制...每次环顾都在增加被发现的几率{RESET}"
        )
    elif 原因 == "window":
        结局画面(g,
            "🪟 烟 囱 没 封 住 🪟",
            "~ 结局四：渗透 ~",
            [
                "你打开了窗户。",
                "但外面没有风。",
                "有什么东西{RED}顺着窗户爬了进来{RESET}。",
                "它的身体......",
                "{RED}像电视信号一样扭曲{RESET}。",
                "忽明忽暗。",
                "像是在{RED}加载{RESET}。",
                "",
                "它落地的一瞬间，信号稳定了。",
                "变成了{RED}一个完整的人形{RESET}。",
                "",
                "它看了看你。",
                "又看了看电视。",
                "\"频道16，\"它说。\"你还没去过。\"",
                "\"我帮你占好位了。\"",
                "",
                f"{GRAY}你低头看了看自己的手。{RESET}",
                f"{GRAY}你的手......{RESET}",
                f"{BRED}也在闪烁。{RESET}",
            ],
            f"  {DIM}提示: 窗户永远不要开...外面的东西比你想象的更想进来{RESET}"
        )
    elif 原因 == "phone":
        结局画面(g,
            "📞 你 不 该 接 的 📞",
            "~ 结局五：回响 ~",
            [
                "电话那头......",
                "是你自己的声音在{RED}尖叫{RESET}。",
                "然后电话安静了。",
                "你听到{RED}身后{RESET}......",
                "电话又响了。",
                "从你{RED}枕头底下{RESET}。",
                "",
                "你掀开枕头。",
                "底下有一部{RED}老式座机{RESET}。",
                "你家的客厅{RED}没有座机{RESET}。",
                "",
                "座机的屏幕上写着:",
                f"{BRED}\"转接中...频道16...\"{RESET}",
                "",
                "你听到耳边有人说话：",
                f"{BRED}\"下一班。\"{RESET}",
                f"{BRED}\"现在。\"{RESET}",
                f"{BRED}\"立刻。\"{RESET}",
            ],
            f"  {DIM}提示: 电话响时......有时候不接比接更安全{RESET}"
        )
    elif 原因 == "watched":
        结局画面(g,
            "📺 它 看 够 了 📺",
            "~ 结局六：收视率 ~",
            [
                "你看了太久的电视。",
                "频道一个接一个地换。",
                "直到你停在了{RED}频道16{RESET}。",
                "",
                "画面是一片{RED}纯白{RESET}。",
                "然后白光中出现了{RED}一行字{RESET}：",
                "",
                f"{BRED}{BOLD}\"收视率: 100%\"{RESET}",
                f"{BRED}{BOLD}\"观众: 1\"{RESET}",
                f"{BRED}{BOLD}\"节目时长: 永不完结\"{RESET}",
                "",
                "你突然意识到一件事——",
                f"{BRED}电视里那些频道......{RESET}",
                f"{BRED}不是电视台播的。{RESET}",
                f"{BRED}是上一任\"观众\"录的。{RESET}",
                f"{BRED}录给他们走之后的......{RESET}",
                f"{BRED}下一任观众看。{RESET}",
                "",
                f"{GRAY}你听到身后传来掌声。{RESET}",
                f"{GRAY}很轻。很稀疏。{RESET}",
                f"{GRAY}像是只有一个人。{RESET}",
                f"{GRAY}在鼓掌。{RESET}",
                f"{BRED}你转过头。{RESET}",
                f"{BRED}沙发的另一端。{RESET}",
                f"{BRED}坐着一个和你长得一样的人。{RESET}",
                f"{BRED}他在对你笑。{RESET}",
                f"{BRED}\"节目好看吗？\"他说。{RESET}",
            ],
            f"  {DIM}提示: 不要一直看电视...去读日记，去环顾，去了解真相{RESET}"
        )
    elif 原因 == "truth":
        结局画面(g,
            "🔑 真 相 🔑",
            "~ 结局七：破解循环（隐藏结局）~",
            [
                "你读完了所有日记。",
                "你收集了所有线索。",
                "你知道了广播塔的秘密。",
                "你知道了{RED}频道16{RESET}是什么。",
                "",
                "不是出口。不是入口。",
                "是{RED}重置按钮{RESET}。",
                "",
                "每一次死亡，都会回到今晚。",
                "23:47。同一个沙发。同一个遥控器。",
                "但每一轮，你会{RED}多记住一点点{RESET}。",
                "日记里那些{RED}不是你写的字{RESET}——",
                "是{RED}上一轮的你{RESET}留下的。",
                "",
                "这一轮，你决定{RED}不看电视{RESET}。",
                "你决定{RED}走出去{RESET}。",
                "走出公寓。走向那座{RED}广播塔{RESET}。",
                "",
                "你打开门。走廊空无一人。",
                "电梯在13楼{RED}停了{RESET}。",
                "门打开——{RED}里面坐满了人{RESET}。",
                "他们都在{RED}看电视{RESET}。",
                "电视里——",
                f"{BRED}是你。{RESET}",
                f"{BRED}坐在沙发上。{RESET}",
                f"{BRED}准备打开电视。{RESET}",
                "",
                f"{GRAY}你低头看了看自己。{RESET}",
                f"{GRAY}你的手在变{RESET}{BRED}透明{RESET}{GRAY}。{RESET}",
                f"{GRAY}你也在变成电视信号。{RESET}",
                f"{GRAY}你也在变成......{RESET}",
                f"{BRED}下一个频道。{RESET}",
            ],
            f"  {GREEN}★ 隐藏结局解锁！你发现了循环的真相{RESET}"
        )
    elif 原因 == "escape":
        结局画面(g,
            "🌅 黎 明 🌅",
            "~ 结局八：天亮了（真结局）~",
            [
                "你撑到了{RED}天亮{RESET}。",
                "凌晨四点五十七分。",
                "东方的天空出现了{RED}第一缕光{RESET}。",
                "",
                "电视屏幕{RED}变暗了{RESET}。",
                "不是关机。是{RED}信号消失了{RESET}。",
                "像是有什么东西{RED}被光赶走了{RESET}。",
                "",
                "你听到广播塔方向传来一声{RED}巨响{RESET}。",
                "像是塔{RED}塌了{RESET}。",
                "或者......像是门{RED}被关上了{RESET}。",
                "",
                f"{GRAY}你打开手机。信号满格。{RESET}",
                f"{GRAY}你拨了110。\"我家电视......\"{RESET}",
                f"{GRAY}你不知道该怎么说。{RESET}",
                f"{GRAY}\"......我家电视在说话。\"{RESET}",
                "",
                "警察来了。看了你的电视。",
                "什么都没有。正常的雪花屏。",
                "他们以为你疯了。",
                "",
                "但你看到了——",
                "警察走后，你在电视{RED}背面{RESET}发现了一行刻字：",
                f"{BRED}\"你做到了。下次帮我也逃出来。\"{RESET}",
                "",
                f"{GREEN}字迹......是上一轮你的。{RESET}",
                f"{GREEN}你不知道自己帮了多少个\"上一轮\"。{RESET}",
                f"{GREEN}但你知道......{RESET}",
                f"{GREEN}下一轮还会来。{RESET}",
                f"{GREEN}循环还没有真正打破。{RESET}",
                f"{GREEN}但今天......{RESET}",
                f"{GREEN}今天你活着看到了太阳。{RESET}",
            ],
            f"  {GREEN}★ 真结局解锁！你撑到了天亮！{RESET}"
        )

    # 结算
    结算(g, 原因)

    # 多周目提示
    if g.结局次数 < 8:
        print(f"  {BYELLOW}已发现结局: {g.结局次数}/8{RESET}")
        print(f"  {DIM}还有更多结局等待发现...{RESET}")
        print(f"  {DIM}提示: 尝试不同的选择 - 读日记/不看电视/撑到天亮/打开窗户...{RESET}")
    else:
        print(f"  {BRED}{BOLD}★ 全结局收集完成 ★{RESET}")
        print(f"  {DIM}你已经看透了所有真相...{RESET}")

    # 周目记忆
    if g.结局次数 > 0:
        print(f"\n  {MAGENTA}下一轮记忆:{RESET}")
        记忆池 = [
            "\"这次别开门\"", "\"先读日记\"", "\"频道13是陷阱\"",
            "\"手电筒=命\"", "\"镜子不对劲\"", "\"电话别接\"",
            "\"窗户是入口\"", "\"广播塔是源头\"", "\"天亮就安全了\"",
            "\"他在门后\"", "\"衣柜里有人\"", "\"泰迪熊会救你\"",
        ]
        for _ in range(min(3, g.结局次数)):
            m = random.choice(记忆池)
            print(f"  {DIM}  {m}{RESET}")
            memory_pool = [x for x in 记忆池 if x != m]

    print()
    再玩 = 获取输入(f"  {CYAN}再来一次? (y/n):{RESET} ")
    return 再玩 == 'y'

# ═══════════════════════════════════════════════════════════
#  死亡检测
# ═══════════════════════════════════════════════════════════
def 检查死亡(g):
    """返回死亡原因或None"""
    if g.理智 <= 0: return "insanity"
    if g.脚步声 >= 12: return "intruder"
    if g.恐怖事件 >= 10: return "discovered"
    if not g.窗户关 and g.理智 < 50: return "window"
    if g.电话响 >= 5: return "phone"
    if g.电视累计时长 >= 120 and not g.阅读日记: return "watched"
    # 隐藏结局条件：读过日记+收集全部线索+存活到天亮
    if g.存活时间 >= 400 and g.阅读日记 and len(g.隐藏线索) >= 7: return "truth"
    # 真结局：单纯撑到天亮（存活500分钟）
    if g.存活时间 >= 500: return "escape"
    return None

# ═══════════════════════════════════════════════════════════
#  主循环
# ═══════════════════════════════════════════════════════════
def main():
    cls()
    hide_cur()

    # 预告片（电影级开场）
    try:
        预告片()
    except KeyboardInterrupt:
        cls()
        print(f"\n  {DIM}...预告片被跳过了...{RESET}")
        print(f"  {DIM}但正片无法跳过{RESET}")
        time.sleep(1.0)

    # 开场剧情
    开场剧情()

    # 主游戏循环（支持多周目）
    while True:
        g = 游戏()

        # 前世记忆提示
        if g.结局次数 > 0:
            cls()
            print(f"\n  {MAGENTA}── 第 {g.结局次数 + 1} 次循环 ──{RESET}")
            print(f"  {DIM}你保留了上一次的某些记忆碎片...{RESET}")
            print(f"  {DIM}这次......你会做得更好吗？{RESET}")
            print()
            获取输入("  按回车开始...")

        开机 = True
        while 开机:
            渲染(g)
            阶段剧情(g)
            随机事件(g)
            g.推进时间()

            # 看电视累加时长
            if g.电视开着:
                g.电视累计时长 += 1

            # 死亡检测
            死亡 = 检查死亡(g)
            if 死亡:
                渲染(g)
                再玩 = 游戏结束(g, 死亡)
                if 再玩:
                    g.结局次数 += 1
                    g.周目 = g.结局次数 + 1
                    break  # 重新开始新周目
                else:
                    开机 = False
                    break

            # 输入
            key = 获取输入()

            # ── 按键映射 ──
            if key in ("w", "k", "up", "↑"):
                动作_换台(g, +1)
            elif key in ("s", "j", "down", "↓"):
                动作_换台(g, -1)
            elif key in ("d", "l", "right", "→"):
                动作_音量(g, +1)
            elif key in ("a", "h", "left", "←"):
                动作_音量(g, -1)
            elif key in ("t", ""):
                动作_开关电视(g)
            elif key == "l":
                动作_环顾(g)
            elif key == "f":
                动作_手电(g)
            elif key == "o":
                动作_门锁(g)
            elif key == "v":
                动作_窗户(g)
            elif key == "p":
                动作_电话(g)
            elif key == "i":
                动作_物品(g)
            elif key == "m":
                动作_静音(g)
            elif key == "c":
                动作_频道表(g)
            elif key == "h":
                动作_帮助()
            elif key == "q":
                confirm = 获取输入(f"  {YELLOW}确定退出?{RESET} {RED}(y/n):{RESET} ")
                if confirm == 'y':
                    g.记录(f"{YELLOW}你关掉了电视...但恐惧留了下来{RESET}")
                    开机 = False
                    break
            else:
                g.记录(f"{DIM}未知操作: {key} (输入h查看帮助){RESET}")

        # 内层循环结束 = 一局结束（死亡或退出）
        if not 开机:
            break

    # ═══ 最终告别画面 ═══
    cls()
    print()
    print(f"  {BRED}{BOLD}      ___           ___           ___     {RESET}")
    print(f"  {BRED}{BOLD}     /  /\\         /__/\\         /  /\\    {RESET}")
    print(f"  {BRED}{BOLD}    /  /:/_       |  |:|        /  /:/_   {RESET}")
    print(f"  {BRED}{BOLD}   /  /:/ /\\      |  |:|       /  /:/ /\\  {RESET}")
    print(f"  {BRED}{BOLD}  /  /:/ /:/_   __|  |:|      /  /:/ /:/_ {RESET}")
    print(f"  {BRED}{BOLD} /__/:/ /:/ /\\ /__/\\_|:|____ /__/:/ /:/ /\\{RESET}")
    print(f"  {BRED}{BOLD} \\  \\:\\/:/ /:/ \\  \\:\\/:::::/ \\  \\:\\/:/ /:/{RESET}")
    print(f"  {BRED}{BOLD}  \\  \\::/ /:/   \\  \\::/~~~~   \\  \\::/ /:/ {RESET}")
    print(f"  {BRED}{BOLD}   \\  \\:/:/     \\  \\:\\        \\  \\:/:/  {RESET}")
    print(f"  {BRED}{BOLD}    \\  \\::/       \\  \\:\\        \\  \\::/   {RESET}")
    print(f"  {BRED}{BOLD}     \\__\\/         \\__\\/         \\__\\/    {RESET}")
    print()
    print(f"  {BRED}{BOLD}      感 谢 游 玩 电 视 模 拟 恐 怖{RESET}")
    print()
    print(f"  {GRAY}你永远不知道频道13在播什么...{RESET}")
    print(f"  {DIM}但下次你一个人看电视的时候...{RESET}")
    print(f"  {DIM}记得检查频道列表里...有没有多出来的频道。{RESET}")
    print()
    print(f"  {BYELLOW}★ 收集全8个结局解锁完整真相 ★{RESET}")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cls()
        print()
        print(f"  {BRED}{BOLD}━━━━━ 强行退出 ━━━━━{RESET}")
        print(f"  {DIM}但有些东西...不是退出就能摆脱的。{RESET}")
        print()
        show_cur()
        sys.exit(0)
