-- MySQL数据库建表语句
-- 充电站智能预测平台

-- 创建数据库
CREATE DATABASE IF NOT EXISTS charging_station_forecast;
USE charging_station_forecast;

-- 充电站表
CREATE TABLE IF NOT EXISTS stations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    total_piles INT NOT NULL,
    capacity FLOAT NOT NULL,
    cost_per_kwh FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 历史充电数据表
CREATE TABLE IF NOT EXISTS historical_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    station_id INT NOT NULL,
    time_slot DATETIME NOT NULL,
    charging_amount FLOAT NOT NULL COMMENT '充电量(kWh)',
    electricity_price FLOAT NOT NULL COMMENT '电价(元/kWh)',
    charging_duration FLOAT NOT NULL COMMENT '充电时长(h)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE CASCADE
);

-- 变量数据表
CREATE TABLE IF NOT EXISTS variable_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    station_id INT NOT NULL,
    time_slot DATETIME NOT NULL,
    temperature FLOAT COMMENT '温度(℃)',
    humidity FLOAT COMMENT '湿度(%)',
    traffic_flow INT COMMENT '车流量(辆)',
    competitor_price FLOAT COMMENT '竞品价格(元/kWh)',
    user_behavior_score FLOAT COMMENT '用户行为评分',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE CASCADE
);

-- 模型配置参数表
CREATE TABLE IF NOT EXISTS model_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    station_id INT NOT NULL,
    name VARCHAR(100) NOT NULL COMMENT '配置名称',
    monte_carlo_times INT DEFAULT 10000 COMMENT '蒙特卡洛模拟次数',
    lstm_hidden_layers INT DEFAULT 3 COMMENT 'LSTM隐藏层数量',
    price_elasticity FLOAT DEFAULT -0.5 COMMENT '价格弹性系数',
    confidence_level FLOAT DEFAULT 0.95 COMMENT '置信度阈值',
    is_default BOOLEAN DEFAULT FALSE COMMENT '是否为默认配置',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE CASCADE
);

-- 预测结果表
CREATE TABLE IF NOT EXISTS predict_result (
    id INT AUTO_INCREMENT PRIMARY KEY,
    station_id INT NOT NULL,
    time_slot DATETIME NOT NULL,
    predicted_amount_mean FLOAT NOT NULL COMMENT '预测充电量均值(kWh)',
    predicted_amount_lower FLOAT NOT NULL COMMENT '预测充电量下限(kWh)',
    predicted_amount_upper FLOAT NOT NULL COMMENT '预测充电量上限(kWh)',
    suggested_price_mean FLOAT NOT NULL COMMENT '建议价格均值(元/kWh)',
    suggested_price_lower FLOAT NOT NULL COMMENT '建议价格下限(元/kWh)',
    suggested_price_upper FLOAT NOT NULL COMMENT '建议价格上限(元/kWh)',
    revenue_prediction FLOAT NOT NULL COMMENT '收益预测(元)',
    model_config_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE CASCADE,
    FOREIGN KEY (model_config_id) REFERENCES model_config(id) ON DELETE CASCADE
);

-- 实际回流数据表
CREATE TABLE IF NOT EXISTS actual_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    station_id INT NOT NULL,
    time_slot DATETIME NOT NULL,
    actual_amount FLOAT NOT NULL COMMENT '实际充电量(kWh)',
    actual_price FLOAT NOT NULL COMMENT '实际定价(元/kWh)',
    user_feedback TEXT COMMENT '用户反馈',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE CASCADE
);

-- 定价策略表
CREATE TABLE IF NOT EXISTS pricing_strategy (
    id INT AUTO_INCREMENT PRIMARY KEY,
    station_id INT NOT NULL,
    name VARCHAR(100) NOT NULL COMMENT '策略名称',
    description TEXT COMMENT '策略描述',
    is_active BOOLEAN DEFAULT FALSE COMMENT '是否激活',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE CASCADE
);

-- 时段定价表
CREATE TABLE IF NOT EXISTS time_slot_pricing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    strategy_id INT NOT NULL,
    time_slot VARCHAR(20) NOT NULL COMMENT '时段(如:00:00-01:00)',
    price FLOAT NOT NULL COMMENT '定价(元/kWh)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (strategy_id) REFERENCES pricing_strategy(id) ON DELETE CASCADE
);

-- 索引优化
CREATE INDEX idx_historical_data_station_time ON historical_data(station_id, time_slot);
CREATE INDEX idx_variable_data_station_time ON variable_data(station_id, time_slot);
CREATE INDEX idx_predict_result_station_time ON predict_result(station_id, time_slot);
CREATE INDEX idx_actual_data_station_time ON actual_data(station_id, time_slot);

-- 插入示例数据
INSERT INTO stations (name, location, total_piles, capacity, cost_per_kwh) VALUES
('示例充电站1', '北京市朝阳区', 10, 120, 0.5),
('示例充电站2', '上海市浦东新区', 15, 180, 0.55);

INSERT INTO model_config (station_id, name, monte_carlo_times, lstm_hidden_layers, price_elasticity, confidence_level, is_default) VALUES
(1, '默认配置', 10000, 3, -0.5, 0.95, TRUE),
(2, '默认配置', 10000, 3, -0.45, 0.95, TRUE);