<div align="center">
  <img width="158" height="158" alt="8265c08f-4abd-43f0-aeea-292b3dff568d" src="https://github.com/user-attachments/assets/4e293275-dd58-4fd0-85cf-51ba0d527826" />
  <h1> WC2026 智能辅助决策引擎</h1>
  <p><i>基于大模型与海量足球数据的赛事深度分析与推演系统</i></p>
</div>

---

## 🖥️ 系统展示

<img width="2559" height="1347" alt="image" src="https://github.com/user-attachments/assets/e0d1a323-9f31-4ba4-8c63-ab46574ef717" />

<img width="2559" height="1271" alt="d349c904-47bc-43ef-bf9e-b69331cfd213" src="https://github.com/user-attachments/assets/5204f44d-b2f2-4526-8334-66191593a268" />


---

📖 项目简介

202605
大家好又是一年世界杯，是人总想要赢点钱，这个系统是我看了德国经济学家克莱门特的分析报告来的灵感做出来的，其中AI的预测策略也参考了这位教授的报告内容，另外还有国家队球队、球员、教练、战术这些维度进行综合分析


20260616
新增了palyer玩法概念是通过玩家定额度由模型根据赔率预测结果，来决定投注策略也就是买多少你能赚钱，但是额度就这么多玩完就没了。可以和几个好朋友一起玩(这个功能还差的有点多只搭了个框)
工作原因这个系统后期也不会怎么更新
目前集成球队、球员、教练、战术这几个数据维度，其实远远不够

这个系统架构真的还可以诚心希望大家可以二次开发
1、增加赔率维度这是重中之重！！(上体彩和博彩网站爬根据赔率变化修改投注策略)今年世界杯太多爆冷资本赚钱越来越不在乎底线了，葡萄牙居然能和佛得角踢平。
2、增加球队实时的比赛数据目前系统的演算数据一大部分都是通过这些国家队的预选赛、友谊赛来的数据其实不太真实大家都在藏拙只有世界杯正赛的这些比赛才能展现真实的战术、球员数据、球队实力

值得一提
我的登录页面还做的不错这个地球转起来很好看，我调整了很久摄像机位置当时做完真的盯着看了很久。


🛠️ 技术栈

前端: Vue 3 (Composition API), Vite, Element Plus, CSS Flexbox/Grid
后端: Python, FastAPI
数据采集: Playwright (Headless Chrome), AsyncIO
数据库: PostgreSQL (pg8000/psycopg2) + JSONB 数据类型结构化
3D渲染与模型: Three.js, Sketchfab Viewer API
大模型基座: 阿里云 DashScope (Qwen-3.7-Max 文本分析, Qwen-VL-Max 视觉提取)

---

🏃 部署指南

环境要求
Python 3.10+
Node.js 18+
PostgreSQL 14+

1. 数据库与环境变量配置
请确保本地已安装 PostgreSQL。

在根目录和 `backend` 目录下创建 `.env` 文件，可参考 `.env.example`：
```env
DB_PASSWORD=您的数据库密码
QWEN_API_KEY=您的阿里云DashScope Key
```

2. 后端配置与启动
```bash
cd backend

# 安装依赖
pip install fastapi uvicorn psycopg2-binary pydantic openai python-dotenv playwright

# 安装无头浏览器依赖 (用于数据爬虫)
playwright install

# 启动服务 (默认端口 10086)
python main.py
```

3. 前端配置与启动
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

---

⚠️ 声明与免责条款

合规声明：本系统提供的各项预测、盈亏测算及策略引擎仅供内部测试、编程研究与学术参考。**严禁用于非法赌博或商业售卖。足球比赛具有极强的不可预见性，AI 推演结果不构成任何形式的投资或投注绝对依据。**
