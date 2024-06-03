class Investor:
    def __init__(self, cliff, tge_unlock, vesting, investors_supply, monthly_sell_percentage):
        self.cliff = cliff  # Період, протягом якого інвестори не можуть продавати свої токени
        self.tge_unlock = tge_unlock  # Відсоток токенів, який розблоковується під час генерації токенів.
        self.vesting = vesting  # Період поступового розблокування токенів після cliff періоду

        self.started_investors_supply = investors_supply  # Початкова кількість токенів виділена інвесторам загалом
        self.investors_supply = investors_supply  # Кількість токенів виділена інвесторам загалом
        self.token_holdings = tge_unlock * investors_supply  # Наявна кількість токенів
        self.tokens_sold = 0  # Кількість вже проданих токенів

        self.monthly_sell_percentage = monthly_sell_percentage  # Відсоток токенів, які продають інвестори щомісяця
        self.months_passed = 0  # Лічильник місяців, що пройшли
        # Кількість токенів, які розблоковують щомісяця після cliff періоду
        self.monthly_get_after_cliff = (1 - tge_unlock) * investors_supply / vesting

        self.realized_profit = 0  # Реалізований прибуток
        self.unrealized_profit = 0  # Нереалізований прибуток

    def update_token_holdings(self):
        if self.months_passed > self.cliff:
            self.token_holdings += self.monthly_get_after_cliff
            self.investors_supply -= self.monthly_get_after_cliff

    def update_profits(self, liquidity_pool, ammount_to_sell):
        # Реалізований прибуток: добуток кількості вже проданих токенів на теперішню ціну
        self.realized_profit += ammount_to_sell * liquidity_pool.current_price

        # Нереалізований прибуток: добуток кількості ще не проданих токенів (включаючі заблоковані) на теперішню ціну
        self.unrealized_profit = (self.started_investors_supply - self.tokens_sold) * liquidity_pool.current_price + self.realized_profit

    def sell_tokens(self, liquidity_pool):
        self.months_passed += 1

        if self.investors_supply >= self.monthly_get_after_cliff:
            self.update_token_holdings()
        else:
            print("All tokens from investors supply were given")

        if self.months_passed <= self.cliff:
            print("Cliff period for investor: tokens cannot be sold.")
            return

        amount_to_sell = self.token_holdings * self.monthly_sell_percentage
        stable_coins_to_receive = amount_to_sell * liquidity_pool.current_price

        print(f"Stable coins to receive: {stable_coins_to_receive}")
        print(f"Token holdings before sale: {self.token_holdings}")

        if liquidity_pool.update_pool(stable_coins_to_receive, is_addition=False):
            self.token_holdings -= amount_to_sell
            self.tokens_sold += amount_to_sell

        print(f"Token holdings after sale: {self.token_holdings}")
        print(f"Realized profit: {self.realized_profit}")

        self.update_profits(liquidity_pool, amount_to_sell)
