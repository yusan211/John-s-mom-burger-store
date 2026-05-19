# 🍔 John’s Mom Burger Store  
**Python 期末大作业 – 模拟经营小游戏**

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)  
![Pygame](https://img.shields.io/badge/pygame-2.5.0-green.svg)  
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

## 📖 项目简介  
一款模拟汉堡店经营的交互式游戏。玩家需根据顾客订单，依次添加食材制作汉堡，在顾客耐心耗尽前完成并上餐，以赚取金钱和声誉。每日随机生成 5~8 位顾客，支持购买食材库存，游戏难度随天数逐步提升。

---

## 🎮 游戏玩法  
| 操作 | 说明 |
|------|------|
| 🥩 食材按钮 | 点击按钮，按顺序堆叠汉堡层 |
| 🧹 Clear 按钮 | 清空当前正在制作的汉堡 |
| 🍽️ Serve 按钮 | 汉堡与订单完全匹配且完成后，点击出餐 |
| 🛒 Buy Stock | 花费 $50 为所有食材增加 5 个库存 |
| 📅 Next Day | 结束当天营业，进入新的一天（自动刷新顾客） |

- 顾客头上会显示**想要的汉堡名称**和**食谱顺序**（如 Bun → Patty → Cheese → Bun）。
- 耐心条：绿色（充足）→ 橙色（紧张）→ 红色（愤怒）。耐心归零则顾客离开，声誉下降。
- 快速完成可获得额外 **$5 奖金**。

---
> 💡 **注**：本项目主要使用代码动态绘制图形，未依赖外部图片资源。

---

## 运行指南

### 1️⃣ 环境准备
确保已安装 Python 3.8+ 与 Pygame 库：
### 2️⃣ 启动游戏
<img width="2004" height="1364" alt="ac9a4b1a12ca48c634f6ce5dab7e49bf" src="https://github.com/user-attachments/assets/e976bfc7-c615-49df-9d19-8ba1106c8e6a" />

## 开源地址

📌 **GitHub 仓库**：  
https://github.com/yusan211/John-s-mom-burger-store

---

## 总结与心得

通过本次项目，我深入理解了 **Pygame 的事件驱动机制** 与 **游戏主循环结构**，并在实践中掌握了：
- 面向对象思想在游戏开发中的应用
- UI 交互与状态管理的实现方式
- 简单 AI 行为（顾客耐心倒计时）的设计方法

该项目不仅巩固了 Python 基础知识，也提升了综合编程与问题解决能力，是一次非常有意义的课程实践。

---

*© 2026John's Mom Burger Store Project — 卢雨晴*
