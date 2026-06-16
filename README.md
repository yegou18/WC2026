<div align="center">
  <img src="frontend/public/favicon.svg" width="120" alt="Logo">
  <h1>🏆 WC2026 智能辅助决策引擎</h1>
  <p><i>基于大模型与海量足球数据的赛事深度分析与推演系统</i></p>
</div>

---

## 🖥️ 系统展示

![WC2026 智能大屏截图](screenshot.png)
*现代科技风格的数据大屏：包含沉浸式 3D 体育场模型、实时赛程、球队与球员数据面板。*

---

## 📖 项目简介

WC2026 智能辅助决策引擎是一款专为 2026 年美加墨世界杯打造的数据分析与AI推演系统。项目旨在通过聚合海量球队基本面数据，结合 Playwright 自动化视觉爬虫与 Qwen 大语言模型的推演能力，为赛事分析、比分预测、盈利策略提供客观、多维度的参考依据。

## 🚀 核心特性

*   **多维 AI 智能推演**: 接入阿里云 DashScope Qwen-3.7-Max 大模型，基于详细的球队/球员物理数据（年龄、身高、体重、雷达图属性），输出胜负概率、比分预测、战术克制、伤病隐患等深度报告。
*   **AI 视觉全自动爬虫底座**: 独创的自动化数据同步方案，通过 Playwright 结合视觉大模型（`qwen-vl-max`），自动解析懂球帝等专业网站的非结构化页面，抓取最详尽的球星六芒星雷达图与球队名册，实时写入 PostgreSQL。
*   **"导演视角" 3D 科幻登录交互**: 采用 Sketchfab 顶级渲染管线与高级摄影机轨道算法，实现了带有 Lissajous 随机空间漂浮感的全 3D 真实地球背景登录页（支持鼠标自由拖拽交互与坐标持久化）。
*   **模拟盈利策略引擎 (Player 机制)**: 针对不同层级的玩家（管理员/普通玩家），内置了独立的资金盘与历史预测追溯系统。系统会根据比赛赔率与玩家本金，借助 AI 生成“重仓/轻仓”等量化投注策略指导。
*   **全局淘汰赛对阵网络 (Bracket)**: 纯 CSS 弹性布局配合伪元素实现的赛博朋克风“蜘蛛网”赛事晋级图，实时同步赛程并动态匹配国家队 SVG 矢量国旗。
*   **高并发微服务架构**: 后端 AI 接口采用并发拆分设计，实现多个预测指标的异步渲染，告别大模型长文本的漫长等待。

---

## 🛠️ 技术栈

*   **前端**: Vue 3 (Composition API), Vite, Element Plus, CSS Flexbox/Grid
*   **后端**: Python, FastAPI
*   **数据采集**: Playwright (Headless Chrome), AsyncIO
*   **数据库**: PostgreSQL (pg8000/psycopg2) + JSONB 数据类型结构化
*   **3D渲染与模型**: Three.js, Sketchfab Viewer API
*   **大模型基座**: 阿里云 DashScope (Qwen-3.7-Max 文本分析, Qwen-VL-Max 视觉提取)

---

## 🏃 部署指南

### 环境要求
*   Python 3.10+
*   Node.js 18+
*   PostgreSQL 14+

### 1. 数据库与环境变量配置
请确保本地已安装 PostgreSQL。

在根目录和 `backend` 目录下创建 `.env` 文件，可参考 `.env.example`：
```env
DB_PASSWORD=您的数据库密码
QWEN_API_KEY=您的阿里云DashScope Key
```

### 2. 后端配置与启动
```bash
cd backend

# 安装依赖
pip install fastapi uvicorn psycopg2-binary pydantic openai python-dotenv playwright

# 安装无头浏览器依赖 (用于数据爬虫)
playwright install

# 启动服务 (默认端口 10086)
python main.py
```

### 3. 前端配置与启动
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

---

## ⚠️ 声明与免责条款

*   **数据安全**：本项目已将所有 API Key、数据库密码剥离至 `.env` 环境变量中，请在部署和 Fork 时妥善保管个人密钥，**切勿上传任何包含真实 Key 的代码**。
*   **合规声明**：本系统提供的各项预测、盈亏测算及策略引擎仅供内部测试、编程研究与学术参考。**严禁用于非法赌博或商业售卖。足球比赛具有极强的不可预见性，AI 推演结果不构成任何形式的投资或投注绝对依据。**
