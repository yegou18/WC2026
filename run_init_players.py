import psycopg2
import os

def execute_sql():
    try:
        db_password = os.getenv("DB_PASSWORD", "postgres")
        conn = psycopg2.connect(user='postgres', password=db_password, host='127.0.0.1', port=5432, database='postgres')
        cur = conn.cursor()
        
        with open('init_players.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
            
        cur.execute(sql)
        conn.commit()
        
        cur.close()
        conn.close()
        print("数据库脚本执行成功！")
    except Exception as e:
        print(f"数据库执行失败: {e}")

if __name__ == "__main__":
    execute_sql()
