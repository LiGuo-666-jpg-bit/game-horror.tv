# 安装指南

## 环境要求

- Python 3.8 或更高版本
- 操作系统：Windows / Linux / macOS / Android（Termux）
- 无需安装任何第三方库

## 下载方式

### 方式一：Git 克隆（推荐）

```bash
git clone https://github.com/LiGuo-666-jpg-bit/game-horror.tv.git
cd game-horror.tv
```

### 方式二：下载 ZIP

1. 打开 https://github.com/LiGuo-666-jpg-bit/game-horror.tv
2. 点击绿色 `Code` 按钮 → `Download ZIP`
3. 解压后进入目录

## 运行游戏

```bash
python main.py
```

## 手机运行（Termux）

```bash
pkg install -y python git
git clone https://github.com/LiGuo-666-jpg-bit/game-horror.tv.git
cd game-horror.tv
python main.py
```

> 手机端完全支持，无需额外配置。

## 常见安装问题

| 问题 | 解决方法 |
|---|---|
| `python` 命令不存在 | 尝试 `python3` 代替 `python` |
| 中文显示乱码 | 终端设置为 UTF-8 编码 |
| Termux 中报错 | 确保已安装 `python` 和 `git` |
