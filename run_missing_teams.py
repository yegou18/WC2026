import os
import json
import asyncio
from WorldCup_Scraper_Package.scrape_team import scrape_team_info

async def run_missing_teams():
    teams_file = os.path.join("WorldCup2026_Teams", "teams_list.json")
    with open(teams_file, "r", encoding="utf-8") as f:
        teams = json.load(f)
        
    missing_names = ['葡萄牙', '挪威', '苏格兰', '突尼斯', '伊朗']
    
    # 强制重新抓取
    for team in teams:
        if team['name'] in missing_names:
            out_dir = team['folder']
            expected_file = os.path.join(out_dir, f"{team['name']}.json")
            if os.path.exists(expected_file):
                os.remove(expected_file)
                print(f"[*] 已删除旧数据: {expected_file}")

    missing_teams = [t for t in teams if t['name'] in missing_names]
    
    for team in missing_teams:
        team_name = team['name']
        team_url = team['url']
        out_dir = team['folder']
        
        expected_file = os.path.join(out_dir, f"{team_name}.json")
            
        print(f"\n[*] 开始处理: {team_name} ({team['group']})")
        try:
            # 在抓取前确保环境绝对干净
            os.system("taskkill /F /IM chrome.exe >nul 2>&1")
            await asyncio.sleep(2)
            
            await scrape_team_info(team_url, team_name, out_dir)
            print(f"[+] {team_name} 处理完成。")
        except Exception as e:
            print(f"[-] 处理 {team_name} 时发生异常: {e}")
            
        # Kill chrome after each team to prevent context error
        os.system("taskkill /F /IM chrome.exe >nul 2>&1")
        await asyncio.sleep(3)
        
    print("\n[+] 所有缺失球队抓取完成，开始同步到数据库...")
    os.system("cd backend && python sync_new_teams_data.py")
        
if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(run_missing_teams())
