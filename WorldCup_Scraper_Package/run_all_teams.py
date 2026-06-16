import os
import json
import asyncio
import subprocess
from scrape_team import scrape_team_info

async def run_all_teams():
    # 读取第一步生成的 JSON 列表
    teams_file = os.path.join("WorldCup2026_Teams", "teams_list.json")
    if not os.path.exists(teams_file):
        print(f"[!] 找不到 {teams_file}，请先运行 create_groups.py")
        return
        
    with open(teams_file, "r", encoding="utf-8") as f:
        teams = json.load(f)
        
    print(f"[*] 共加载了 {len(teams)} 支球队信息，准备开始批量抓取...")
    
    # 确保 Windows 下的 asyncio 策略
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
    # 为了防止中途崩溃，增加一个进度记录机制
    for idx, team in enumerate(teams):
        team_name = team['name']
        team_url = team['url']
        out_dir = team['folder']
        
        expected_file = os.path.join(out_dir, f"{team_name}.json")
        if os.path.exists(expected_file):
            print(f"[+] 跳过 {team_name}，文件已存在: {expected_file}")
            continue
            
        print(f"\n=======================================================")
        print(f"[*] 进度: {idx+1}/{len(teams)}")
        print(f"[*] 开始处理: {team_name} ({team['group']})")
        print(f"=======================================================\n")
        
        try:
            # 调用 scrape_team.py 中的异步抓取逻辑
            await scrape_team_info(team_url, team_name, out_dir)
            print(f"[+] {team_name} 处理完成。")
        except Exception as e:
            print(f"[-] 处理 {team_name} 时发生异常: {e}")
            print(f"[-] 将跳过该队，继续下一支队伍。")
            
        # 给一点缓冲时间，防止被平台风控
        await asyncio.sleep(5)
        
    print("\n[+] 所有 48 支球队批量抓取任务结束！")

if __name__ == "__main__":
    asyncio.run(run_all_teams())
