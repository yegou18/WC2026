import os
import json
import urllib.request
from bs4 import BeautifulSoup
import re

def create_folder_structure():
    print("[*] 开始获取懂球帝世界杯球队分组信息...")
    
    url = 'https://www.dongqiudi.com/data?cid=61&tab=standings'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 找到所有的“小组赛”表格区域
    tables = soup.find_all('table')
    
    if not tables:
        print("[-] 未找到分组表格")
        return

    base_dir = "WorldCup2026_Teams"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    all_teams = []
    
    # 按照 A, B, C, D 的顺序分配组别
    group_labels = [chr(i) for i in range(ord('A'), ord('Z')+1)]
    
    for idx, table in enumerate(tables):
        group_name = f"Group_{group_labels[idx]}"
        group_dir = os.path.join(base_dir, group_name)
        
        if not os.path.exists(group_dir):
            os.makedirs(group_dir)
            
        print(f"\n[*] 处理 {group_name}:")
        
        # 提取该表格中的所有球队
        links = table.find_all('a', href=re.compile(r'/team/\d+'))
        
        for link in links:
            team_name = link.text.strip()
            team_url = "https://www.dongqiudi.com" + link['href']
            
            print(f"  - {team_name} ({team_url})")
            
            all_teams.append({
                "group": group_name,
                "name": team_name,
                "url": team_url,
                "folder": group_dir
            })

    # 将所有球队信息保存为 JSON，供主脚本调用
    with open(os.path.join(base_dir, "teams_list.json"), "w", encoding="utf-8") as f:
        json.dump(all_teams, f, ensure_ascii=False, indent=2)
        
    print(f"\n[+] 成功提取并分配 {len(all_teams)} 支球队的分组目录！")

if __name__ == "__main__":
    create_folder_structure()
