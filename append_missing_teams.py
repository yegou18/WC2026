import json
import psycopg2

def sync_missing_teams():
    db_password = os.getenv("DB_PASSWORD", "postgres")
    conn = psycopg2.connect(user="postgres", password=db_password, host="127.0.0.1", port=5432, database="postgres")
    cur = conn.cursor()

    # 读取球队信息.json
    with open('球队信息.json', 'r', encoding='utf-8') as f:
        teams_data = json.load(f)
        
    missing_team_names = ['葡萄牙', '挪威', '苏格兰', '突尼斯', '伊朗']
    
    for team in teams_data:
        team_name = team.get("球队名称", "")
        if team_name not in missing_team_names:
            continue
            
        print(f"正在录入缺失球队数据: {team_name}")
        
        # 1. 获取数据库中的 team_id
        cur.execute("SELECT id FROM teams WHERE name = %s", (team_name,))
        row = cur.fetchone()
        if not row:
            print(f"数据库中未找到球队 {team_name}，跳过")
            continue
        team_id = row[0]
        
        # 2. 清理旧的球员数据（虽然是空的，以防万一）
        cur.execute("DELETE FROM players_detailed WHERE team_id = %s", (team_id,))
        
        # 3. 录入球员数据
        players_dict = team.get("球员名单", {})
        starters = team.get("预计首发阵容", {})
        
        # 解析首发名单中的球员名字片段
        starter_names = []
        for pos, names_str in starters.items():
            # 简单按照 、、，等分割
            names = names_str.replace('、', ',').split(',')
            for n in names:
                starter_names.append(n.strip())
        
        def is_starter(player_name):
            for sn in starter_names:
                if sn in player_name:
                    return True
            return False

        # 遍历所有位置录入
        for position, player_list in players_dict.items():
            for p_info in player_list:
                # p_info格式如: "扬·索默（拜仁慕尼黑）" 或 "马塞尔·萨比策（多特蒙德，队长）"
                name_club = p_info.split('（')
                p_name = name_club[0].strip()
                club = ""
                if len(name_club) > 1:
                    club = name_club[1].replace('）', '').replace(',队长', '').replace('，队长', '').strip()
                
                # 简单估算综合评分 (仅为占位)
                rating = 80 if is_starter(p_name) else 75
                
                cur.execute("""
                    INSERT INTO players_detailed (
                        team_id, name, position, club, is_starter, overall_rating
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (team_id, p_name, position, club, is_starter(p_name), rating))
        
        conn.commit()
        print(f"球队 {team_name} 录入完成")

    cur.close()
    conn.close()

if __name__ == "__main__":
    sync_missing_teams()
