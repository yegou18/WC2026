import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": "localhost",
    "port": 5432
}

def upgrade_prediction_table():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    
    print("正在扩充 match_predictions 表，加入更多分析维度...")
    cur.execute("""
        ALTER TABLE match_predictions ADD COLUMN IF NOT EXISTS tactical_restraint TEXT;
        ALTER TABLE match_predictions ADD COLUMN IF NOT EXISTS key_player_duel TEXT;
        ALTER TABLE match_predictions ADD COLUMN IF NOT EXISTS injury_impact TEXT;
        ALTER TABLE match_predictions ADD COLUMN IF NOT EXISTS possession_pace VARCHAR(200);
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("分析维度字段扩充成功！")

if __name__ == "__main__":
    upgrade_prediction_table()
