CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'player',
    balance DECIMAL(10,2) DEFAULT 0.00
);

CREATE TABLE IF NOT EXISTS bets (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    bet_type VARCHAR(50), -- 'match', 'champion'
    description TEXT,
    amount DECIMAL(10,2),
    status VARCHAR(20), -- 'pending', 'won', 'lost'
    profit DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 清空旧数据以防止重复插入（如果是重新运行）
TRUNCATE TABLE bets CASCADE;
TRUNCATE TABLE users CASCADE;

-- 插入玩家数据
-- player1: 管理员, 余额为 42.5(盈利) + 20(本金返还) = 62.5
INSERT INTO users (id, username, password, role, balance) VALUES 
(1, 'player1', '123456', 'admin', 62.50);

-- player2: 玩家, 余额为 100(未投注本金) + 100(本金返还) + 212.5(盈利) = 412.5
INSERT INTO users (id, username, password, role, balance) VALUES 
(2, 'player2', '123456', 'player', 412.50);

-- 重置序列
SELECT setval('users_id_seq', 2, true);

-- 插入 player1 的投注记录
INSERT INTO bets (user_id, bet_type, description, amount, status, profit) VALUES
(1, 'champion', '冠军预测', 50.00, 'pending', 0.00),
(1, 'match', '第一场预测 (揭幕战)', 20.00, 'won', 42.50);

-- 插入 player2 的投注记录
INSERT INTO bets (user_id, bet_type, description, amount, status, profit) VALUES
(2, 'match', '第一场预测 (揭幕战)', 100.00, 'won', 212.50),
(2, 'champion', '冠军预测', 50.00, 'pending', 0.00);
