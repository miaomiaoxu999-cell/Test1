# 预测模型服务
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import logging

logger = logging.getLogger(__name__)


class PredictionService:
    """预测模型服务类"""
    
    def __init__(self):
        self.lstm_model = None
        self.prophet_model = None
    
    def prepare_lstm_data(self, df: pd.DataFrame, target_column: str, look_back: int = 24) -> tuple:
        """准备LSTM模型的数据
        
        Args:
            df: 输入数据
            target_column: 目标列名
            look_back: 时间窗口大小
            
        Returns:
            训练数据和标签
        """
        logger.info(f"Preparing LSTM data with look_back={look_back}")
        
        # 选择数值型特征
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        if target_column not in numeric_columns:
            numeric_columns.append(target_column)
        
        data = df[numeric_columns].values
        X, y = [], []
        
        for i in range(len(data) - look_back):
            X.append(data[i:(i + look_back), :])
            y.append(data[i + look_back, numeric_columns.index(target_column)])
        
        X = np.array(X)
        y = np.array(y)
        
        logger.info(f"Prepared LSTM data with shape X: {X.shape}, y: {y.shape}")
        return X, y
    
    def build_lstm_model(self, input_shape: tuple, hidden_layers: int = 3, units: int = 64, dropout_rate: float = 0.2) -> Sequential:
        """构建LSTM模型
        
        Args:
            input_shape: 输入数据形状
            hidden_layers: 隐藏层数量
            units: 每个隐藏层的单元数
            dropout_rate: Dropout率
            
        Returns:
            构建好的LSTM模型
        """
        logger.info(f"Building LSTM model with {hidden_layers} hidden layers, {units} units per layer")
        
        model = Sequential()
        
        # 添加第一个LSTM层
        model.add(LSTM(units=units, return_sequences=True, input_shape=input_shape))
        model.add(Dropout(dropout_rate))
        
        # 添加中间LSTM层
        for _ in range(hidden_layers - 2):
            model.add(LSTM(units=units, return_sequences=True))
            model.add(Dropout(dropout_rate))
        
        # 添加最后一个LSTM层
        model.add(LSTM(units=units))
        model.add(Dropout(dropout_rate))
        
        # 添加输出层
        model.add(Dense(1))
        
        # 编译模型
        model.compile(optimizer='adam', loss='mean_squared_error')
        
        logger.info("LSTM model built successfully")
        return model
    
    def train_lstm(self, X: np.array, y: np.array, epochs: int = 100, batch_size: int = 32, hidden_layers: int = 3) -> tuple:
        """训练LSTM模型
        
        Args:
            X: 训练数据
            y: 训练标签
            epochs: 训练轮数
            batch_size: 批次大小
            hidden_layers: 隐藏层数量
            
        Returns:
            训练好的模型和训练历史
        """
        logger.info(f"Training LSTM model for {epochs} epochs with batch_size={batch_size}")
        
        # 构建模型
        self.lstm_model = self.build_lstm_model(X.shape[1:], hidden_layers=hidden_layers)
        
        # 训练模型
        history = self.lstm_model.fit(X, y, epochs=epochs, batch_size=batch_size, validation_split=0.2, verbose=1)
        
        logger.info("LSTM model trained successfully")
        return self.lstm_model, history
    
    def predict_lstm(self, model: Sequential, X: np.array) -> np.array:
        """使用LSTM模型进行预测
        
        Args:
            model: 训练好的LSTM模型
            X: 输入数据
            
        Returns:
            预测结果
        """
        logger.info(f"Making LSTM predictions for {len(X)} samples")
        predictions = model.predict(X)
        logger.info("LSTM predictions completed")
        return predictions
    
    def train_prophet(self, df: pd.DataFrame, ds_column: str, y_column: str) -> Prophet:
        """训练Prophet模型
        
        Args:
            df: 输入数据
            ds_column: 日期列名
            y_column: 目标列名
            
        Returns:
            训练好的Prophet模型
        """
        logger.info(f"Training Prophet model with ds={ds_column}, y={y_column}")
        
        # 准备Prophet所需的数据格式
        prophet_df = df[[ds_column, y_column]].rename(columns={ds_column: 'ds', y_column: 'y'})
        
        # 初始化并训练Prophet模型
        self.prophet_model = Prophet(daily_seasonality=True, weekly_seasonality=True, yearly_seasonality=True)
        self.prophet_model.fit(prophet_df)
        
        logger.info("Prophet model trained successfully")
        return self.prophet_model
    
    def predict_prophet(self, model: Prophet, future_periods: int) -> pd.DataFrame:
        """使用Prophet模型进行预测
        
        Args:
            model: 训练好的Prophet模型
            future_periods: 预测未来的天数
            
        Returns:
            预测结果
        """
        logger.info(f"Making Prophet predictions for {future_periods} periods")
        
        # 创建未来日期
        future = model.make_future_dataframe(periods=future_periods, freq='H')
        
        # 进行预测
        forecast = model.predict(future)
        
        logger.info("Prophet predictions completed")
        return forecast
    
    def ensemble_predictions(self, lstm_preds: np.array, prophet_preds: np.array, weights: tuple = (0.5, 0.5)) -> np.array:
        """融合LSTM和Prophet的预测结果
        
        Args:
            lstm_preds: LSTM预测结果
            prophet_preds: Prophet预测结果
            weights: 融合权重
            
        Returns:
            融合后的预测结果
        """
        logger.info(f"Ensembling predictions with weights: LSTM={weights[0]}, Prophet={weights[1]}")
        
        # 确保预测结果形状一致
        if len(lstm_preds.shape) > 1:
            lstm_preds = lstm_preds.flatten()
        if len(prophet_preds.shape) > 1:
            prophet_preds = prophet_preds.flatten()
        
        # 加权融合
        ensemble_preds = weights[0] * lstm_preds + weights[1] * prophet_preds
        
        logger.info("Prediction ensemble completed")
        return ensemble_preds
    
    def monte_carlo_simulation(self, predictions: np.array, std_dev: float, n_simulations: int = 10000, confidence_level: float = 0.95) -> tuple:
        """蒙特卡洛模拟生成置信区间
        
        Args:
            predictions: 点预测结果
            std_dev: 预测标准差
            n_simulations: 模拟次数
            confidence_level: 置信水平
            
        Returns:
            模拟结果的均值、下限和上限
        """
        logger.info(f"Running Monte Carlo simulation with {n_simulations} simulations, confidence_level={confidence_level}")
        
        # 生成模拟数据
        simulations = np.zeros((n_simulations, len(predictions)))
        
        for i in range(n_simulations):
            # 为每个预测点生成随机误差
            errors = np.random.normal(0, std_dev, len(predictions))
            simulations[i] = predictions + errors
        
        # 计算置信区间
        lower_bound = np.percentile(simulations, (1 - confidence_level) / 2 * 100, axis=0)
        upper_bound = np.percentile(simulations, (1 + confidence_level) / 2 * 100, axis=0)
        mean_pred = np.mean(simulations, axis=0)
        
        logger.info("Monte Carlo simulation completed")
        return mean_pred, lower_bound, upper_bound
    
    def calculate_metrics(self, y_true: np.array, y_pred: np.array) -> dict:
        """计算预测指标
        
        Args:
            y_true: 真实值
            y_pred: 预测值
            
        Returns:
            包含各种指标的字典
        """
        logger.info("Calculating prediction metrics")
        
        # 确保输入形状一致
        if len(y_true.shape) > 1:
            y_true = y_true.flatten()
        if len(y_pred.shape) > 1:
            y_pred = y_pred.flatten()
        
        metrics = {
            'mae': mean_absolute_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'r2': r2_score(y_true, y_pred),
            'mape': np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        }
        
        logger.info(f"Metrics calculated: {metrics}")
        return metrics
    
    def predict_charging_amount(self, df: pd.DataFrame, config: dict) -> dict:
        """完整的充电量预测流程
        
        Args:
            df: 输入数据
            config: 预测配置
            
        Returns:
            预测结果，包括点预测和置信区间
        """
        logger.info("Starting charging amount prediction pipeline")
        
        # 1. 准备数据
        target_column = config.get('target_column', 'charging_amount')
        time_column = config.get('time_column', 'time_slot')
        look_back = config.get('look_back', 24)
        
        # 2. 训练LSTM模型
        X, y = self.prepare_lstm_data(df, target_column, look_back)
        lstm_model, _ = self.train_lstm(X, y, hidden_layers=config.get('lstm_hidden_layers', 3))
        
        # 3. LSTM预测
        lstm_preds = self.predict_lstm(lstm_model, X)
        
        # 4. 训练Prophet模型
        prophet_model = self.train_prophet(df, time_column, target_column)
        
        # 5. Prophet预测
        future_periods = config.get('future_periods', 24)
        prophet_forecast = self.predict_prophet(prophet_model, future_periods)
        prophet_preds = prophet_forecast['yhat'].values[-future_periods:]
        
        # 6. 融合预测结果
        ensemble_preds = self.ensemble_predictions(lstm_preds[-future_periods:], prophet_preds)
        
        # 7. 蒙特卡洛模拟生成置信区间
        std_dev = config.get('std_dev', np.std(df[target_column]))
        mean_pred, lower_bound, upper_bound = self.monte_carlo_simulation(
            ensemble_preds,
            std_dev,
            n_simulations=config.get('monte_carlo_times', 10000),
            confidence_level=config.get('confidence_level', 0.95)
        )
        
        # 8. 计算预测指标
        metrics = self.calculate_metrics(y[-future_periods:], ensemble_preds)
        
        logger.info("Charging amount prediction completed")
        
        return {
            'predictions': mean_pred,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'metrics': metrics,
            'config': config
        }
