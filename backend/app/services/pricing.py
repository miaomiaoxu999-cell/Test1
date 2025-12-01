# 定价计算服务
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import logging

logger = logging.getLogger(__name__)


class PricingService:
    """定价计算服务类"""
    
    def calculate_cost_baseline(self, station_id: int, cost_per_kwh: float, fixed_costs: float, predicted_volume: float) -> float:
        """计算成本基准
        
        Args:
            station_id: 充电站ID
            cost_per_kwh: 每度电的变动成本
            fixed_costs: 固定成本
            predicted_volume: 预测充电量
            
        Returns:
            成本基准（元/kWh）
        """
        logger.info(f"Calculating cost baseline for station {station_id}")
        
        # 总成本 = 固定成本 + 变动成本 * 预测充电量
        total_cost = fixed_costs + cost_per_kwh * predicted_volume
        
        # 成本基准 = 总成本 / 预测充电量
        cost_baseline = total_cost / predicted_volume if predicted_volume > 0 else cost_per_kwh
        
        logger.info(f"Cost baseline calculated: {cost_baseline:.4f} 元/kWh")
        return cost_baseline
    
    def calculate_price_elasticity(self, df: pd.DataFrame, price_column: str, demand_column: str) -> float:
        """计算价格弹性系数
        
        Args:
            df: 包含价格和需求数据的数据框
            price_column: 价格列名
            demand_column: 需求列名
            
        Returns:
            价格弹性系数
        """
        logger.info(f"Calculating price elasticity using columns {price_column} and {demand_column}")
        
        # 计算价格和需求的对数变化
        df = df.copy()
        df['ln_price'] = np.log(df[price_column])
        df['ln_demand'] = np.log(df[demand_column])
        
        # 计算价格弹性系数（需求变化率 / 价格变化率）
        # 使用线性回归计算弹性系数
        from sklearn.linear_model import LinearRegression
        
        X = df['ln_price'].values.reshape(-1, 1)
        y = df['ln_demand'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        elasticity = model.coef_[0]
        
        logger.info(f"Price elasticity calculated: {elasticity:.4f}")
        return elasticity
    
    def optimize_price(self, cost_baseline: float, elasticity: float, current_price: float, current_demand: float, competitor_price: float = None) -> float:
        """计算最优定价
        
        Args:
            cost_baseline: 成本基准
            elasticity: 价格弹性系数
            current_price: 当前价格
            current_demand: 当前需求
            competitor_price: 竞品价格（可选）
            
        Returns:
            最优定价
        """
        logger.info(f"Optimizing price with cost_baseline={cost_baseline}, elasticity={elasticity}, current_price={current_price}")
        
        # 定义收益函数（负的，因为我们要最小化）
        def negative_revenue(price):
            # 价格弹性公式：ΔQ/Q = ε * ΔP/P
            # 需求变化率 = 弹性系数 * 价格变化率
            price_change_rate = (price - current_price) / current_price
            demand_change_rate = elasticity * price_change_rate
            new_demand = current_demand * (1 + demand_change_rate)
            
            # 确保需求为正
            new_demand = max(new_demand, 0)
            
            # 收益 = (价格 - 成本基准) * 需求
            revenue = (price - cost_baseline) * new_demand
            
            # 返回负收益，因为scipy.optimize.minimize最小化目标函数
            return -revenue
        
        # 设置价格范围（成本基准到当前价格的2倍）
        bounds = [(cost_baseline, current_price * 2)]
        
        # 初始猜测为当前价格
        initial_guess = [current_price]
        
        # 优化收益函数
        result = minimize(negative_revenue, initial_guess, bounds=bounds)
        
        if result.success:
            optimal_price = result.x[0]
            logger.info(f"Optimal price calculated: {optimal_price:.4f} 元/kWh")
            return optimal_price
        else:
            logger.error(f"Price optimization failed: {result.message}")
            return current_price
    
    def calculate_nash_equilibrium(self, station_cost: float, competitor_cost: float, station_elasticity: float, competitor_elasticity: float, cross_elasticity: float = 0.1) -> tuple:
        """计算纳什均衡价格
        
        Args:
            station_cost: 充电站成本
            competitor_cost: 竞品成本
            station_elasticity: 充电站价格弹性
            competitor_elasticity: 竞品价格弹性
            cross_elasticity: 交叉价格弹性
            
        Returns:
            充电站和竞品的纳什均衡价格
        """
        logger.info("Calculating Nash equilibrium prices")
        
        # 定义充电站的收益函数（负的）
        def station_negative_revenue(prices):
            station_price, competitor_price = prices
            
            # 计算充电站的需求
            # 自身价格影响 + 竞品价格影响
            station_demand = 1000 * (1 + station_elasticity * (station_price - 1) + cross_elasticity * (competitor_price - 1))
            station_demand = max(station_demand, 0)
            
            # 充电站收益
            station_revenue = (station_price - station_cost) * station_demand
            
            return -station_revenue
        
        # 定义竞品的收益函数（负的）
        def competitor_negative_revenue(prices):
            station_price, competitor_price = prices
            
            # 计算竞品的需求
            competitor_demand = 1000 * (1 + competitor_elasticity * (competitor_price - 1) + cross_elasticity * (station_price - 1))
            competitor_demand = max(competitor_demand, 0)
            
            # 竞品收益
            competitor_revenue = (competitor_price - competitor_cost) * competitor_demand
            
            return -competitor_revenue
        
        # 联合收益函数（两者之和的负数）
        def joint_negative_revenue(prices):
            return station_negative_revenue(prices) + competitor_negative_revenue(prices)
        
        # 初始猜测价格
        initial_guess = [1.0, 1.0]
        
        # 价格范围
        bounds = [(station_cost, 3.0), (competitor_cost, 3.0)]
        
        # 优化联合收益函数
        result = minimize(joint_negative_revenue, initial_guess, bounds=bounds)
        
        if result.success:
            station_eq_price, competitor_eq_price = result.x
            logger.info(f"Nash equilibrium prices calculated: station={station_eq_price:.4f}, competitor={competitor_eq_price:.4f}")
            return station_eq_price, competitor_eq_price
        else:
            logger.error(f"Nash equilibrium calculation failed: {result.message}")
            return 1.0, 1.0
    
    def predict_revenue(self, price: float, cost_baseline: float, elasticity: float, current_price: float, current_demand: float) -> float:
        """预测收益
        
        Args:
            price: 预测价格
            cost_baseline: 成本基准
            elasticity: 价格弹性系数
            current_price: 当前价格
            current_demand: 当前需求
            
        Returns:
            预测收益
        """
        logger.info(f"Predicting revenue for price={price}")
        
        # 计算需求变化
        price_change_rate = (price - current_price) / current_price
        demand_change_rate = elasticity * price_change_rate
        new_demand = current_demand * (1 + demand_change_rate)
        new_demand = max(new_demand, 0)
        
        # 计算收益
        revenue = (price - cost_baseline) * new_demand
        
        logger.info(f"Predicted revenue: {revenue:.2f} 元")
        return revenue
    
    def calculate_optimal_pricing(self, df: pd.DataFrame, config: dict) -> dict:
        """完整的最优定价计算流程
        
        Args:
            df: 输入数据
            config: 定价配置
            
        Returns:
            最优定价结果，包括定价建议和收益预测
        """
        logger.info("Starting optimal pricing calculation pipeline")
        
        # 1. 计算成本基准
        cost_per_kwh = config.get('cost_per_kwh', 0.5)
        fixed_costs = config.get('fixed_costs', 1000.0)
        predicted_volume = config.get('predicted_volume', df['charging_amount'].mean())
        
        cost_baseline = self.calculate_cost_baseline(
            config.get('station_id', 1),
            cost_per_kwh,
            fixed_costs,
            predicted_volume
        )
        
        # 2. 计算价格弹性系数
        price_column = config.get('price_column', 'electricity_price')
        demand_column = config.get('demand_column', 'charging_amount')
        elasticity = self.calculate_price_elasticity(df, price_column, demand_column)
        
        # 3. 计算当前价格和需求
        current_price = df[price_column].mean()
        current_demand = df[demand_column].mean()
        
        # 4. 计算最优定价
        competitor_price = config.get('competitor_price', None)
        optimal_price = self.optimize_price(
            cost_baseline,
            elasticity,
            current_price,
            current_demand,
            competitor_price
        )
        
        # 5. 如果有竞品价格，进行纳什均衡修正
        if competitor_price is not None:
            competitor_cost = config.get('competitor_cost', cost_per_kwh + 0.05)
            competitor_elasticity = config.get('competitor_elasticity', elasticity)
            cross_elasticity = config.get('cross_elasticity', 0.1)
            
            optimal_price, _ = self.calculate_nash_equilibrium(
                cost_baseline,
                competitor_cost,
                elasticity,
                competitor_elasticity,
                cross_elasticity
            )
        
        # 6. 预测收益
        predicted_revenue = self.predict_revenue(
            optimal_price,
            cost_baseline,
            elasticity,
            current_price,
            current_demand
        )
        
        # 7. 计算价格浮动区间（基于成本基准和市场情况）
        lower_bound = cost_baseline * 1.05  # 最低价格为成本基准的1.05倍
        upper_bound = optimal_price * 1.15  # 最高价格为最优价格的1.15倍
        
        logger.info("Optimal pricing calculation completed")
        
        return {
            'optimal_price': optimal_price,
            'cost_baseline': cost_baseline,
            'elasticity': elasticity,
            'predicted_revenue': predicted_revenue,
            'price_range': {
                'lower': lower_bound,
                'upper': upper_bound
            },
            'current_price': current_price,
            'current_demand': current_demand
        }
