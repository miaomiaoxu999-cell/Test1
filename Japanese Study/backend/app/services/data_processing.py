# 数据处理服务
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import mutual_info_regression
from sklearn.preprocessing import MinMaxScaler
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """数据处理服务类"""
    
    def __init__(self):
        self.scaler = MinMaxScaler()
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        """加载数据文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            加载后的数据
        """
        logger.info(f"Loading data from {file_path}")
        # 根据文件扩展名选择加载方式
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please use CSV or Excel files.")
        
        logger.info(f"Loaded {len(df)} rows of data")
        return df
    
    def detect_outliers(self, df: pd.DataFrame, column: str, method: str = 'zscore') -> pd.DataFrame:
        """异常值检测
        
        Args:
            df: 输入数据
            column: 要检测的列名
            method: 检测方法，支持 'zscore' 或 'iqr'
            
        Returns:
            标记了异常值的数据
        """
        logger.info(f"Detecting outliers in column {column} using {method} method")
        df = df.copy()
        
        if method == 'zscore':
            # 基于3σ原则检测异常值
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            df[f'{column}_is_outlier'] = z_scores > 3
        elif method == 'iqr':
            # 基于IQR方法检测异常值
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df[f'{column}_is_outlier'] = (df[column] < lower_bound) | (df[column] > upper_bound)
        else:
            raise ValueError(f"Unsupported outlier detection method: {method}")
        
        outlier_count = df[f'{column}_is_outlier'].sum()
        logger.info(f"Detected {outlier_count} outliers in column {column}")
        return df
    
    def handle_outliers(self, df: pd.DataFrame, column: str, method: str = 'remove') -> pd.DataFrame:
        """处理异常值
        
        Args:
            df: 输入数据
            column: 要处理的列名
            method: 处理方法，支持 'remove' 或 'replace'
            
        Returns:
            处理后的数据
        """
        logger.info(f"Handling outliers in column {column} using {method} method")
        df = df.copy()
        
        if method == 'remove':
            # 删除异常值
            df = df[~df[f'{column}_is_outlier']].drop(columns=[f'{column}_is_outlier'])
        elif method == 'replace':
            # 用中位数替换异常值
            median = df[~df[f'{column}_is_outlier']][column].median()
            df.loc[df[f'{column}_is_outlier'], column] = median
            df = df.drop(columns=[f'{column}_is_outlier'])
        else:
            raise ValueError(f"Unsupported outlier handling method: {method}")
        
        logger.info(f"Handled outliers in column {column}")
        return df
    
    def fill_missing_values(self, df: pd.DataFrame, column: str, method: str = 'bayesian') -> pd.DataFrame:
        """填补缺失值
        
        Args:
            df: 输入数据
            column: 要填补的列名
            method: 填补方法，支持 'bayesian'、'mean'、'median' 或 'mode'
            
        Returns:
            填补后的数据
        """
        logger.info(f"Filling missing values in column {column} using {method} method")
        df = df.copy()
        
        missing_count = df[column].isnull().sum()
        logger.info(f"Found {missing_count} missing values in column {column}")
        
        if method == 'bayesian':
            # 贝叶斯插值填补缺失值
            # 这里使用随机森林作为贝叶斯方法的近似
            df_without_missing = df.dropna(subset=[column])
            df_with_missing = df[df[column].isnull()]
            
            if len(df_with_missing) == 0:
                return df
            
            # 选择数值型特征作为输入
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            if column in numeric_columns:
                numeric_columns.remove(column)
            
            # 如果没有其他数值型特征，使用均值填补
            if not numeric_columns:
                df[column] = df[column].fillna(df[column].mean())
                return df
            
            # 训练随机森林模型
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(df_without_missing[numeric_columns], df_without_missing[column])
            
            # 预测缺失值
            df.loc[df[column].isnull(), column] = model.predict(df_with_missing[numeric_columns])
        elif method == 'mean':
            df[column] = df[column].fillna(df[column].mean())
        elif method == 'median':
            df[column] = df[column].fillna(df[column].median())
        elif method == 'mode':
            df[column] = df[column].fillna(df[column].mode()[0])
        else:
            raise ValueError(f"Unsupported missing value filling method: {method}")
        
        logger.info(f"Filled missing values in column {column}")
        return df
    
    def feature_engineering(self, df: pd.DataFrame, time_column: str) -> pd.DataFrame:
        """特征工程
        
        Args:
            df: 输入数据
            time_column: 时间列名
            
        Returns:
            处理后的数据
        """
        logger.info(f"Performing feature engineering on time column {time_column}")
        df = df.copy()
        
        # 将时间列转换为datetime类型
        df[time_column] = pd.to_datetime(df[time_column])
        
        # 提取时间特征
        df['hour'] = df[time_column].dt.hour
        df['day_of_week'] = df[time_column].dt.dayofweek
        df['day_of_month'] = df[time_column].dt.day
        df['month'] = df[time_column].dt.month
        df['quarter'] = df[time_column].dt.quarter
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        # 提取季节性特征
        df['sin_hour'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['cos_hour'] = np.cos(2 * np.pi * df['hour'] / 24)
        df['sin_month'] = np.sin(2 * np.pi * df['month'] / 12)
        df['cos_month'] = np.cos(2 * np.pi * df['month'] / 12)
        
        logger.info(f"Generated {len(df.columns) - len(df.columns.drop(['hour', 'day_of_week', 'day_of_month', 'month', 'quarter', 'is_weekend', 'sin_hour', 'cos_hour', 'sin_month', 'cos_month']))} new features")
        return df
    
    def feature_selection(self, df: pd.DataFrame, target_column: str, method: str = 'mutual_info') -> pd.DataFrame:
        """特征选择
        
        Args:
            df: 输入数据
            target_column: 目标列名
            method: 选择方法，支持 'mutual_info' 或 'random_forest'
            
        Returns:
            选择后的特征
        """
        logger.info(f"Performing feature selection for target {target_column} using {method} method")
        
        # 选择数值型特征
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        if target_column in numeric_columns:
            numeric_columns.remove(target_column)
        
        X = df[numeric_columns]
        y = df[target_column]
        
        if method == 'mutual_info':
            # 使用互信息熵进行特征选择
            mutual_info = mutual_info_regression(X, y)
            feature_importance = pd.Series(mutual_info, index=X.columns)
        elif method == 'random_forest':
            # 使用随机森林进行特征选择
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)
            feature_importance = pd.Series(model.feature_importances_, index=X.columns)
        else:
            raise ValueError(f"Unsupported feature selection method: {method}")
        
        # 选择重要性大于0的特征
        selected_features = feature_importance[feature_importance > 0].index.tolist()
        logger.info(f"Selected {len(selected_features)} features: {selected_features}")
        
        # 返回选择后的特征和目标列
        return df[selected_features + [target_column]]
    
    def normalize_data(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """数据标准化
        
        Args:
            df: 输入数据
            columns: 要标准化的列名列表
            
        Returns:
            标准化后的数据
        """
        logger.info(f"Normalizing columns: {columns}")
        df = df.copy()
        
        # 训练标准化器并转换数据
        df[columns] = self.scaler.fit_transform(df[columns])
        logger.info(f"Normalized {len(columns)} columns")
        return df
    
    def preprocess_data(self, df: pd.DataFrame, config: dict) -> pd.DataFrame:
        """完整的数据预处理流程
        
        Args:
            df: 输入数据
            config: 预处理配置
            
        Returns:
            预处理后的数据
        """
        logger.info("Starting data preprocessing pipeline")
        
        # 1. 异常值检测和处理
        if config.get('handle_outliers', False):
            for column in config.get('outlier_columns', []):
                df = self.detect_outliers(df, column, config.get('outlier_detection_method', 'zscore'))
                df = self.handle_outliers(df, column, config.get('outlier_handling_method', 'remove'))
        
        # 2. 缺失值填补
        for column in df.columns:
            if df[column].isnull().sum() > 0:
                df = self.fill_missing_values(df, column, config.get('missing_value_method', 'bayesian'))
        
        # 3. 特征工程
        if config.get('feature_engineering', False) and config.get('time_column'):
            df = self.feature_engineering(df, config.get('time_column'))
        
        # 4. 特征选择
        if config.get('feature_selection', False) and config.get('target_column'):
            df = self.feature_selection(df, config.get('target_column'), config.get('feature_selection_method', 'mutual_info'))
        
        # 5. 数据标准化
        if config.get('normalize', False) and config.get('normalize_columns'):
            df = self.normalize_data(df, config.get('normalize_columns'))
        
        logger.info(f"Data preprocessing completed. Final shape: {df.shape}")
        return df
