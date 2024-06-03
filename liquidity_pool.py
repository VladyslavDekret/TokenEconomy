class LiquidityPool:
    def __init__(self, stable_coins, liquidity_supply):
        self.stable_coins = stable_coins  # Кількість стейбл коінів у пулі ліквідності
        self.liquidity_supply = liquidity_supply  # Кількість токенів у пулі ліквідності
        self.multiply_constant = stable_coins * liquidity_supply  # Константа перемноження стейбл коінів та токенів
        self.current_price = self.update_token_price()  # Ціна на токен

    def update_pool(self, amount_stable_coins, is_addition=True):
        if is_addition:
            new_stable_coins = self.stable_coins + amount_stable_coins
        else:
            new_stable_coins = self.stable_coins - amount_stable_coins
            if new_stable_coins <= 0:
                print("Not enough stable coins in the liquidity pool.")
                return False

        new_liquidity_supply = self.multiply_constant / new_stable_coins
        if new_liquidity_supply <= 0:
            print("Not enough tokens in the liquidity pool.")
            return False

        self.stable_coins = new_stable_coins
        self.liquidity_supply = new_liquidity_supply
        self.update_token_price()

        print(f"Updated pool state: {self.get_pool_state()}")

        return True

    def update_token_price(self):
        self.current_price = self.stable_coins / self.liquidity_supply
        return self.current_price

    def get_pool_state(self):
        return {
            "stable_coins": self.stable_coins,
            "liquidity_supply": self.liquidity_supply,
            "current_price": self.current_price
        }
