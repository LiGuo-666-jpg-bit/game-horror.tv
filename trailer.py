# -*- coding: utf-8 -*-
"""
📺 电视模拟恐怖 · 预告片模块
====================================
功能：
  - 单独运行：python trailer.py → 直接看预告片
  - 被主程序调用：from trailer import show_trailer
  - 可嵌入其他项目复用

依赖：仅 random / time / sys / os（纯标准库）
====================================
"""

import time
import sys
import os

# ═══════════════════════════════════════════════════════════
#  颜色工具
# ═══════════════════════════════════════════════════════════
RED    = "\033[91m"
BRED   = "\033[91m\033[1m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
MAGENTA= "\033[95m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"
GRAY   = "\033[90m"
DIM    = "\033[2m"
BOLD   = "\033[1m"
BLINK  = "\033[5m"
RESET  = "\033[0m"

# ═══════════════════════════════════════════════════════════
#  清屏工具
# ═══════════════════════════════════════════════════════════
def cls():
    print("\033[2J\033[H", end="", flush=True)

def hide_cur():
    print("\033[?25l", end="", flush=True)

def show_cur():
    print("\033[?25h", end="", flush=True)

# ═══════════════════════════════════════════════════════════
#  预告片主体
# ═══════════════════════════════════════════════════════════
def show_trailer():
    """电影级预告片 - 播放完毕后返回，不阻塞"""
    cls()
    hide_cur()

    # ── 第一幕：标题闪现 ──
    for _ in range(4):
        cls()
        print("\n\n\n")
        print(f"  {BRED}    电 视 模 拟 恐 怖{RESET}")
        print(f"  {DIM}    TV SIMULATOR HORROR{RESET}")
        time.sleep(0.15)
        cls(); print("\n\n\n"); time.sleep(0.1)

    # ── 第二幕：制作名单 ──
    cls()
    print("\n\n")
    credits = [
        (f"{DIM}一部关于{RESET}{RED}电视{RESET}{DIM}的电影{RESET}", 0.6),
        ("", 0.2),
        (f"{GRAY}导演 / 编剧{RESET}", 0.5),
        (f"{WHITE}你的大脑{RESET}", 0.8),
        ("", 0.3),
        (f"{GRAY}主演{RESET}", 0.5),
        (f"{WHITE}你{RESET}", 0.8),
        (f"{GRAY}特别出演{RESET}", 0.5),
        (f"{RED}频道13{RESET}", 0.8),
        ("", 0.3),
        (f"{GRAY}摄影{RESET}", 0.5),
        (f"{DIM}你手机的前置摄像头{RESET}", 0.8),
        ("", 0.3),
        (f"{GRAY}音效{RESET}", 0.5),
        (f"{RED}你家的电路{RESET}", 0.8),
        ("", 0.5),
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

        (f"{DIM}你关掉了电视{RESET}", DIM, 1.2, False),
        (f"{DIM}你确定你关掉了{RESET}", DIM, 1.2, False),
        (f"{RED}但你还是听到了笑声{RESET}", RED, 1.5, False),
        ("", None, 0.5, False),

        (f"{RED}{BOLD}「频道13」{RESET}", RED, 0.8, True),
        (f"{RED}它不是电视台播的{RESET}", RED, 1.2, False),
        (f"{RED}是上一任观众录的{RESET}", RED, 1.2, False),
        (f"{RED}录给他们走之后{RESET}", RED, 1.0, False),
        (f"{RED}下一任观众看{RESET}", RED, 1.5, False),
        ("", None, 0.5, False),

        (f"{DIM}你环顾房间{RESET}", DIM, 1.0, False),
        (f"{YELLOW}门锁好了{RESET}", YELLOW, 0.8, False),
        (f"{YELLOW}窗户关了{RESET}", YELLOW, 0.8, False),
        (f"{YELLOW}手电筒满电{RESET}", YELLOW, 0.8, False),
        (f"{RED}你忘了检查衣柜{RESET}", RED, 1.5, False),
        ("", None, 0.5, False),

        (f"{RED}{BOLD}「不要相信电视里说的话」{RESET}", RED, 1.5, False),
        (f"{RED}{BOLD}「不要调到频道13」{RESET}", RED, 1.5, False),
        (f"{RED}{BOLD}「不要接凌晨的电话」{RESET}", RED, 1.5, False),
        (f"{RED}{BOLD}「手电筒是命」{RESET}", RED, 1.5, False),
        (f"{RED}{BOLD}「镜子可能有问题」{RESET}", RED, 1.5, False),
        ("", None, 0.5, False),

        (f"{RED}他在你身后{RESET}", RED, 0.3, True),
        (f"{RED}他在门后{RESET}", RED, 0.3, True),
        (f"{RED}他在衣柜里{RESET}", RED, 0.3, True),
        (f"{RED}他在床底下{RESET}", RED, 0.3, True),
        (f"{RED}他在电视里{RESET}", RED, 0.6, True),
        ("", None, 0.3, False),

        (f"{DIM}你拿起遥控器{RESET}", DIM, 1.2, False),
        (f"{DIM}你感觉......{RESET}", DIM, 1.0, False),
        (f"{RED}遥控器也在发抖{RESET}", RED, 1.5, False),
        ("", None, 0.5, False),

        (f"{GRAY}17个频道{RESET}", GRAY, 0.8, False),
        (f"{GRAY}只有12个应该存在{RESET}", GRAY, 1.2, False),
        (f"{RED}另外5个......{RESET}", RED, 1.0, False),
        (f"{RED}是给你看的{RESET}", RED, 1.5, False),
        ("", None, 0.5, False),

        (f"{DIM}每次死亡{RESET}", DIM, 0.8, False),
        (f"{DIM}都会回到今晚{RESET}", DIM, 1.0, False),
        (f"{RED}{BOLD}23:47{RESET}", RED, 0.8, True),
        (f"{RED}同一个沙发{RESET}", RED, 0.8, False),
        (f"{RED}同一个遥控器{RESET}", RED, 0.8, False),
        (f"{RED}同一个你{RESET}", RED, 1.5, False),
        ("", None, 0.5, False),

        (f"{YELLOW}8种结局{RESET}", YELLOW, 1.0, False),
        (f"{YELLOW}你能在天亮前逃出去吗？{RESET}", YELLOW, 1.5, False),
        ("", None, 0.5, False),

        (f"{RED}{BOLD}3...{RESET}", RED, 0.8, True),
        (f"{RED}{BOLD}2...{RESET}", RED, 0.8, True),
        (f"{RED}{BOLD}1...{RESET}", RED, 0.8, True),
        ("", None, 0.3, False),
    ]

    for item in scenes:
        text, color, delay, blink = item
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
        print(f"  {BRED}      📺  电 视 模 拟 恐 怖  📺{RESET}")
        print(f"  {BRED}         TV  SIMULATOR  HORROR{RESET}")
        time.sleep(0.2)
        cls(); print("\n\n\n\n"); time.sleep(0.1)

    cls()
    print("\n\n\n")
    print(f"  {BRED}      📺  电 视 模 拟 恐 怖  📺{RESET}")
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
    show_cur()


# ═══════════════════════════════════════════════════════════
#  独立运行入口
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        show_trailer()
    except KeyboardInterrupt:
        cls()
        print("\n  " + DIM + "预告片被中断" + RESET)
        show_cur()
        sys.exit(0)
