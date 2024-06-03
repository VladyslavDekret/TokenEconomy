from liquidity_pool import LiquidityPool


class User:
    def __init__(self, demand, demand_growth_rate=0):
        self.demand = demand  # Кількість стейбл коінів, на яку купують користувачі щомісяця
        self.token_holdings = 0  # Кількість токенів, якими володіють користувачі
        self.demand_growth_rate = demand_growth_rate  # Темп зростання попиту

    def update_demand(self, month):
        if month <= 12:  # Зміна попиту тільки для перших 12 місяців
            self.demand *= (1 + self.demand_growth_rate)

    def buy_tokens(self, liquidity_pool: LiquidityPool):
        amount_to_spend = self.demand
        tokens_to_buy = amount_to_spend / liquidity_pool.current_price
        if liquidity_pool.update_pool(amount_to_spend, is_addition=True):
            self.token_holdings += tokens_to_buy
        else:
            print("Failed to buy tokens: Not enough stable coins in the liquidity pool.")
