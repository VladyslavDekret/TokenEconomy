class Others:
    def __init__(self, cliff, tge_unlock, vesting, others_supply, monthly_sell_percentage):
        self.cliff = cliff  # Період, протягом якого інвестори не можуть продавати свої токени
        self.tge_unlock = tge_unlock  # Відсоток токенів, який розблоковується під час генерації токенів.
        self.vesting = vesting  # Період поступового розблокування токенів після cliff періоду
        self.investors_supply = others_supply  # Кількість токенів виділена інвесторам загалом
        self.token_holdings = tge_unlock * others_supply  # Наявна кількість токенів
        self.monthly_sell_percentage = monthly_sell_percentage  # Відсоток токенів, які продають інвестори щомісяця
        self.months_passed = 0  # Лічильник місяців, що пройшли

        # Кількість токенів, які розблоковують щомісяця після cliff періоду
        self.monthly_get_after_cliff = (1 - tge_unlock) * others_supply / vesting

    def update_token_holdings(self):
        if self.months_passed > self.cliff:
            self.token_holdings += self.monthly_get_after_cliff

    def sell_tokens(self, liquidity_pool):
        self.months_passed += 1

        self.update_token_holdings()

        if self.months_passed <= self.cliff:
            print("Cliff period for others: tokens cannot be sold.")
            return

        available_to_sell = self.token_holdings
        amount_to_sell = available_to_sell * self.monthly_sell_percentage
        stable_coins_to_receive = amount_to_sell * liquidity_pool.current_price

        print(f"Stable coins to receive: {stable_coins_to_receive}")

        if liquidity_pool.update_pool(stable_coins_to_receive, is_addition=False):
            self.token_holdings -= amount_to_sell
        else:
            print("Failed to sell tokens: Not enough stable coins in the liquidity pool.")
