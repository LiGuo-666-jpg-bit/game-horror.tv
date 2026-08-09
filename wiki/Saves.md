# 存档说明

## 存档位置

存档文件保存在游戏目录下的 `saves/` 文件夹中。

```
game-horror.tv/
└── saves/
    ├── player1.json
    ├── player2.json
    └── ...
```

## 存档格式

每个存档是一个 JSON 文件，包含以下字段：

```json
{
  "username": "玩家名称",
  "sanity": 100,
  "time": 0,
  "channel": 1,
  "volume": 5,
  "items": {},
  "week": 1,
  "clears": 0,
  "achievements": [],
  "discovered_channels": []
}
```

## 手动修改存档

你可以用任何文本编辑器打开存档文件，手动修改数值：

- `sanity`：理智值（0–100）
- `time`：游戏内时间（分钟）
- `week`：周目数
- `clears`：通关次数

> 修改存档前请备份原文件。过度修改可能影响游戏体验。

## 多账号隔离

不同登录账号的存档互不干扰。游客模式无法存档。
