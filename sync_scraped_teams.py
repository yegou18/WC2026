import os
import json
import psycopg2
import glob

def sync_scraped_teams():
    db_password = os.getenv("DB_PASSWORD", "postgres")
    conn = psycopg2.connect(user="postgres", password=db_password, host="127.0.0.1", port=5432, database="postgres")
    cur = conn.cursor()
    
    missing_teams = ['葡萄牙', '挪威', '苏格兰', '突尼斯', '伊朗']
    
    for team_name in missing_teams:
        # Find the JSON file
        pattern = f"E:/工作/系统开发/sjb/WorldCup2026_Teams/**/{team_name}.json"
        files = glob.glob(pattern, recursive=True)
        if not files:
            print(f"未找到 {team_name} 的 JSON 文件，可能还在抓取中")
            continue
            
        json_file = files[0]
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        squad = data.get("squad", [])
        if not squad:
            print(f"{team_name} 的阵容数据为空")
            continue
            
        print(f"正在同步 {team_name} 的球员数据到数据库 (共 {len(squad)} 人)...")
        
        cur.execute("SELECT id FROM teams WHERE name = %s", (team_name,))
        row = cur.fetchone()
        if not row:
            continue
        team_id = row[0]
        
        # 清除旧数据
        cur.execute("DELETE FROM players_detailed WHERE team_id = %s", (team_id,))
        
        for player in squad:
            name = player.get("name") or "未知"
            position = player.get("position") or "未知"
            club = player.get("club") or ""
            # default to not starter, and average rating
            is_starter = False
            rating = player.get("overall_rating") or 75
            
            cur.execute("""
                INSERT INTO players_detailed (
                    team_id, name, position, club, is_starter, overall_rating
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (team_id, name, position, club, is_starter, rating))
            
    conn.commit()
    cur.close()
    conn.close()
    print("数据库同步完成。")

if __name__ == "__main__":
    sync_scraped_teams()
