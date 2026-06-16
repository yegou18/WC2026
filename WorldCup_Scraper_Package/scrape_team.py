import asyncio
import json
import base64
import os
import sys
import shutil
import time
import subprocess
import urllib.request
from playwright.async_api import async_playwright
from openai import AsyncOpenAI

# ---------------- 配置区 ----------------
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "YOUR_API_KEY_HERE")
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen-vl-max"
CDP_PORT = 9222

client = AsyncOpenAI(api_key=QWEN_API_KEY, base_url=QWEN_BASE_URL)

def get_or_clone_chrome_profile():
    src = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
    dst = os.path.join(os.getcwd(), "chrome_cloned_profile")
    
    if os.path.exists(dst):
        print(f"  [+] 检测到已存在可复用的 Chrome 缓存副本: {dst}")
        return dst
        
    print("[*] 初次运行，正在全量克隆 Chrome 用户配置...")
    try:
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns('Cache', 'Code Cache', 'Media Cache'))
    except Exception as e:
        pass
    return dst

async def ensure_chrome_ready():
    # 核心：获取克隆的非默认目录
    cloned_user_data_dir = get_or_clone_chrome_profile()
    
    # 检查端口是否已经在使用
    try:
        proxy_handler = urllib.request.ProxyHandler({}) 
        opener = urllib.request.build_opener(proxy_handler)
        opener.open(f"http://127.0.0.1:{CDP_PORT}/json/version", timeout=1)
        print("[*] 检测到 Chrome CDP 端口已在运行，复用现有实例。")
        return True
    except Exception:
        pass
        
    print("[*] 正在启动克隆配置的 Chrome 并开启 CDP 端口...")
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
    ]
    chrome_exe = next((p for p in chrome_paths if os.path.exists(p)), None)
    if not chrome_exe:
        print("[!] 找不到 Chrome 浏览器！")
        return False
        
    cmd = [
        chrome_exe, 
        f'--user-data-dir={cloned_user_data_dir}', 
        '--profile-directory=Default',  # 强制指定默认配置目录，跳过配置选择页面
        f'--remote-debugging-port={CDP_PORT}', 
        '--hide-crash-restore-bubble',
        '--no-first-run', 
        '--no-default-browser-check'
    ]
    
    subprocess.Popen(cmd)
    
    print("[*] 等待 Chrome 调试端口就绪...")
    for _ in range(15):
        try:
            time.sleep(1)
            proxy_handler = urllib.request.ProxyHandler({}) 
            opener = urllib.request.build_opener(proxy_handler)
            opener.open(f"http://127.0.0.1:{CDP_PORT}/json/version", timeout=2)
            return True
        except Exception:
            pass
            
    print("[!] 致命错误：端口依然无法绑定。请检查环境。")
    return False

async def scrape_team_info(url: str, team_name: str, output_dir: str = "."):
    print(f"[*] 正在处理球队: {team_name} - {url}")
    
    if not await ensure_chrome_ready():
        return
        
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            # 使用现有页面或者打开新页面
            if len(context.pages) > 0:
                page = context.pages[0]
            else:
                page = await context.new_page()
                
            # 强制带上前台可见标志
            await page.bring_to_front()
                
            try:
                print(f"[*] 正在访问球队主页: {url}")
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(2)
            except Exception as e:
                print(f"[!] 访问页面超时或失败，尝试继续: {e}")
            
            # 第一阶段：基础信息和主页长图
            print("[*] 等待 DOM 加载...")
            await page.wait_for_load_state("domcontentloaded")
            await asyncio.sleep(2)
            # 滚到底部确保加载
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(1)
            await page.evaluate("window.scrollTo(0, 0)")
            await asyncio.sleep(1)
            
            ss_main = await page.screenshot(full_page=True, type="jpeg", quality=80)
            b64_main = base64.b64encode(ss_main).decode('utf-8')
            
            # 点击“阵容”标签页
            print("[*] 正在切换到【阵容】标签页...")
            b64_squad = None
            player_screenshots = []
            
            try:
                await page.locator("button.tp-tab:has-text('阵容')").click(timeout=3000)
                await asyncio.sleep(2)
                try:
                    await page.wait_for_selector(".tp-roster-row", timeout=5000)
                except:
                    pass
                    
                # 首先截取完整的阵容页面图作为备份和教练/整体数据提取
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(1)
                await page.evaluate("window.scrollTo(0, 0)")
                await asyncio.sleep(1)
                ss_squad = await page.screenshot(full_page=True, type="jpeg", quality=80)
                b64_squad = base64.b64encode(ss_squad).decode('utf-8')
                print("[+] 成功截取阵容页面长图！")
                
                # --- 新逻辑：捕获点击弹出的新标签页获取球员详情 ---
                print("[*] 开始逐个点击球员进入详情页提取数据...")
                
                # 设置新页面监听器
                new_pages_queue = asyncio.Queue()
                def on_page(new_page):
                    new_pages_queue.put_nowait(new_page)
                context.on("page", on_page)
                
                players = page.locator(".tp-roster-row")
                count = await players.count()
                print(f"[*] 发现 {count} 个可点击的球员/教练项")
                
                # 防止异常页面导致内存溢出，设置一个合理的安全上限
                count = min(count, 45)
                
                for i in range(count):
                    try:
                        print(f"  [>] 正在点击第 {i+1}/{count} 项...")
                        
                        # 在每次点击前清空队列，防止上一次的残留页面影响本次捕获
                        while not new_pages_queue.empty():
                            try:
                                stale_page = new_pages_queue.get_nowait()
                                await stale_page.close()
                            except:
                                pass
                                
                        # 确保元素可见并点击
                        await players.nth(i).scroll_into_view_if_needed()
                        await asyncio.sleep(0.5)
                        
                        # 使用物理点击触发新标签页
                        box = await players.nth(i).bounding_box()
                        if box:
                            await page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)
                            
                            # 等待新标签页弹出 (最多等3秒)
                            try:
                                new_page = await asyncio.wait_for(new_pages_queue.get(), timeout=3.0)
                                print(f"      [+] 成功打开详情页: {new_page.url}")
                                
                                try:
                                    await new_page.wait_for_load_state("domcontentloaded", timeout=10000)
                                    await asyncio.sleep(1.5) # 等待数据加载
                                    
                                    # 滚动确保内容加载
                                    await new_page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                                    await asyncio.sleep(0.5)
                                    
                                    # 截图
                                    ss_player = await new_page.screenshot(full_page=True, type="jpeg", quality=60)
                                    player_screenshots.append({
                                        "url": new_page.url,
                                        "b64": base64.b64encode(ss_player).decode('utf-8')
                                    })
                                except Exception as inner_e:
                                    print(f"      [-] 详情页加载或截图失败: {inner_e}")
                                finally:
                                    try:
                                        await new_page.close()
                                    except:
                                        pass
                                
                            except asyncio.TimeoutError:
                                print("      [-] 点击未触发新页面 (可能是纯文本教练行，无详情)")
                    except Exception as e:
                        print(f"      [-] 点击第 {i+1} 项时发生错误: {e}")
                        
                # 移除监听器
                context.remove_listener("page", on_page)
                
            except Exception as e:
                print(f"[-] 切换阵容页或抓取详情失败: {e}")
                
            # 点击“赛程”标签页
            print("[*] 正在切换到【赛程】标签页...")
            b64_schedule = None
            try:
                await page.locator("button.tp-tab:has-text('赛程')").click(timeout=3000)
                await asyncio.sleep(2)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(1)
                ss_schedule = await page.screenshot(full_page=True, type="jpeg", quality=80)
                b64_schedule = base64.b64encode(ss_schedule).decode('utf-8')
            except Exception as e:
                print(f"[-] 切换赛程页失败: {e}")
                
        except Exception as e:
            print(f"[!] 抓取过程发生异常: {e}")
            return
        finally:
            try:
                # 只关闭页面，不关闭 browser 以便 CDP 保持开启
                await page.close()
            except:
                pass
            
    print("[*] 基础截图完成，正在调用 Qwen 进行提取...")
    
    prompt_base = f"""
    你是一个专业的数据挖掘专家。请分析这几张来自懂球帝球队主页（{team_name}）的截图（包含球队信息、阵容页、赛程页）。
    
    请提取以下具体信息，并严格返回 JSON 格式：
    
    1. team_info: 对象，包含球队的基本信息（如英文名、城市、成立时间、主场、容量、市值等）。
    2. schedule: 数组，包含球队的赛程信息。每场比赛是一个对象，包含：date(日期/时间)、competition(赛事名称)、home_team(主队)、away_team(客队)、score(比分，如果是未开赛则填null)。
    
    必须返回合法的 JSON，不要包含 markdown 标记块和额外说明文字。
    """
    
    user_content_base = [{"type": "text", "text": prompt_base}]
    if b64_main: user_content_base.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_main}"}})
    if b64_schedule: user_content_base.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_schedule}"}})
        
    final_result = {"team_info": {}, "squad": [], "schedule": []}
    
    try:
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": user_content_base}],
            response_format={"type": "json_object"}
        )
        base_data = json.loads(response.choices[0].message.content)
        final_result["team_info"] = base_data.get("team_info", {})
        final_result["schedule"] = base_data.get("schedule", [])
    except Exception as e:
        print(f"[!] 基础信息提取出错: {e}")
        
    # --- 逐个处理球员数据，注重精准度 ---
    if player_screenshots:
        print(f"[*] 开始逐个解析 {len(player_screenshots)} 名球员的详细数据，这将花费一些时间，请耐心等待...")
        
        for idx, p in enumerate(player_screenshots):
            print(f"  [>] 正在由 AI 深度解析第 {idx+1}/{len(player_screenshots)} 个人员数据: {p['url']}")
            
            prompt_player = f"""
            你是一个资深的足球数据分析师。我将提供一张懂球帝球员个人主页的高清截图。
            请极致精确地提取该人员的所有详细数据，并严格返回一个 JSON 对象。
            
            你需要提取以下字段（如果截图里没有该项数据，请填 null）：
            - name: 姓名
            - number: 球衣号码
            - position: 场上位置（如 前锋, 中场, 后卫, 门将, 教练）
            - age: 年龄
            - height: 身高
            - weight: 体重
            - preferred_foot: 惯用脚
            - value: 身价
            - birth_date: 出生日期
            - nationality: 国籍
            - overall_rating: 综合能力评分（通常是一个大数字）
            - stats: 对象，包含具体的各项能力值（如 速度、射门、传球、盘带、防守、力量 等评分）
            - recent_matches: 数组，提取【本赛季比赛】或【近期比赛】列表。每场比赛包含：date(日期), match(对阵信息), score(比分), rating(评分), status(胜/平/负，如 W/D/L)
            
            必须返回合法的 JSON，不要包含任何额外的 markdown 代码块标记。
            """
            
            user_content_player = [
                {"type": "text", "text": prompt_player},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{p['b64']}"}}
            ]
                
            try:
                p_resp = await client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": user_content_player}],
                    response_format={"type": "json_object"}
                )
                p_data = json.loads(p_resp.choices[0].message.content)
                p_data["source_url"] = p['url'] # 附加上原始链接以便追溯
                
                # 更新或者合并到现有的 squad 中
                found = False
                for existing_p in final_result["squad"]:
                    if existing_p.get("name") == p_data.get("name") or (existing_p.get("name") and p_data.get("name") and existing_p.get("name") in p_data.get("name")):
                        existing_p.update(p_data)
                        found = True
                        break
                
                if not found:
                    final_result["squad"].append(p_data)
                    
                print(f"      [+] 成功解析: {p_data.get('name', '未知')}")
                
                # 每解析完一个，就实时保存一次
                filename = os.path.join(output_dir, f"{team_name}.json")
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(final_result, f, ensure_ascii=False, indent=2)
                    
            except Exception as e:
                print(f"      [-] 解析失败: {e}")
            
    filename = os.path.join(output_dir, f"{team_name}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(final_result, f, ensure_ascii=False, indent=2)
        
    print(f"\n[+] 球队 {team_name} 完整数据已保存到 {filename}")

if __name__ == "__main__":
    if sys.platform == "win32":
        # Playwright 在 Windows 上使用 async 必须设置 ProactorEventLoop
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
    target_url = "https://www.dongqiudi.com/team/1278"
    team_name = "墨西哥"
    out_dir = "."
    
    if len(sys.argv) >= 3:
        target_url = sys.argv[1]
        team_name = sys.argv[2]
    if len(sys.argv) >= 4:
        out_dir = sys.argv[3]
        
    asyncio.run(scrape_team_info(target_url, team_name, out_dir))