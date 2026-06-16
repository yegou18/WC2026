# 懂球帝 世界杯48支球队全量数据采集系统

该系统是专为抓取“懂球帝”网页端（PC）的 2026 世界杯 48 支球队及全量球员详细数据而设计的纯自动化工具。
核心原理采用了**“基于 CDP 的 Playwright 原生浏览器接管” + “大模型(Qwen)视觉提取”**的双重架构。

## 为什么采用这种架构？
1. **防风控与验证码规避：** 不使用传统的 HTTP `requests` 或纯 Headless 浏览器（极易被平台盾拦截），而是通过复用本机日常登录过的真实 Chrome 浏览器用户缓存目录（User Data），完全模拟真实人类环境。
2. **突破网页端的数据阉割：** 懂球帝 PC 网页端阉割了球员详情页的入口（点击球员没反应）。我们通过截取完整的长图，并利用 AI 视觉大模型强大的结构化能力，直接“看图说话”，一次性将整支球队所有球员的身价、年龄、出场数据等精准转为 JSON。
3. **断点续传与高容错：** 架构自带重试与容错机制，某个球队抓取异常不会导致整个批次崩溃。

## 文件结构说明

整个数据采集包包含以下三个核心文件，必须按顺序执行：

### 1. `create_groups.py` (球队发现与初始化建库)
- **作用：** 自动访问懂球帝的世界杯数据中心，解析当前的积分榜/分组榜表格，提取出全部 48 支球队的名称和 URL。
- **产出：** 
  - 自动创建 `WorldCup2026_Teams` 文件夹。
  - 在其中创建 `Group_A` 到 `Group_L` 的 12 个子文件夹。
  - 生成 `teams_list.json` 文件（作为后续抓取的任务索引库）。

### 2. `scrape_team.py` (单支球队底层抓取与 AI 提取引擎)
- **作用：** 这是整个系统的核心驱动文件，包含了浏览器接管、长图截取、Prompt 构建和调用大模型的逻辑。
- **机制：** 
  - 它会全量克隆本机的 Chrome 缓存到 `chrome_cloned_profile`。
  - 以非默认目录拉起 Chrome，并绑定 `9222` CDP 调试端口。
  - Playwright 接入后，自动控制页面滚动，确保懒加载图片全部渲染。
  - 截取“阵容”标签页的高清长图，发送给 Qwen 视觉大模型。
  - 大模型将其解析为层级极度规范的 JSON（包含 `team_info`, `squad` 数组等）。
- **注意：** 此文件通常不需要单独运行，它会被主脚本调用。

### 3. `run_all_teams.py` (全局自动化调度器)
- **作用：** 批处理控制器。
- **机制：** 
  - 读取 `teams_list.json` 中的 48 支球队列表。
  - 采用 `for` 循环依次调用 `scrape_team_info()` 方法。
  - **断点续传：** 如果发现在某个组（如 `Group_C`）下已经存在 `巴西.json`，则会自动跳过，继续下一支队伍。
  - **防封禁：** 每次抓完一支球队，会强制 `sleep(5)` 冷却，防止被懂球帝服务器拉黑 IP。

## 运行环境与依赖准备

1. **Python 环境：** Python 3.9+ 
2. **必要库安装：**
   ```bash
   pip install playwright aiohttp beautifulsoup4 openai
   playwright install chromium
   ```
3. **AI 大模型密钥：**
   在 `scrape_team.py` 的头部，配置好您的阿里云百炼大模型 Key：
   ```python
   QWEN_API_KEY = "您的_API_KEY"
   QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
   MODEL_NAME = "qwen-vl-max"
   ```
4. **原生浏览器要求：**
   请确保电脑上安装了正常的 Google Chrome，脚本会自动寻找 `C:\Program Files\Google\Chrome\Application\chrome.exe` 等常见路径。

## 启动操作流程

1. **生成任务清单与目录结构：**
   ```bash
   python create_groups.py
   ```
   *检查 `WorldCup2026_Teams` 文件夹是否成功生成。*

2. **开始全自动化批处理挂机采集：**
   ```bash
   python run_all_teams.py
   ```
   *终端会打印进度，并在各自的 Group 文件夹下逐一生成极度规范的球队 JSON 数据，可直接用于对接 PostgreSQL 等关系型或文档型数据库。*
