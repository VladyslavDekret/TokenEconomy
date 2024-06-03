import matplotlib.pyplot as plt
import pandas as pd
import os
from liquidity_pool import LiquidityPool
from investor import Investor
from user import User
from others import Others


def main():
    all_data_stable_coins = []
    all_data_demand = []
    all_data_stable_coins_and_demand = []

    os.makedirs('graphics/stable_coins', exist_ok=True)
    os.makedirs('graphics/demand', exist_ok=True)
    os.makedirs('graphics/stable_coins_and_demand', exist_ok=True)

    initial_stable_coins_values = [1.5 * 1000 * 1000, 2.0 * 1000 * 1000, 2.5 * 1000 * 1000, 3.5 * 1000 * 1000, 4.5 * 1000 * 1000]
    demand_values = [0.01 * 1000 * 1000, 0.03 * 1000 * 1000, 0.05 * 1000 * 1000, 0.07 * 1000 * 1000, 0.1 * 1000 * 1000]

    for initial_stable_coins in initial_stable_coins_values:
        liquidity_pool = LiquidityPool(stable_coins=initial_stable_coins, liquidity_supply=initial_stable_coins * 10)
        investors = create_investors()
        user = User(demand=0.05 * 1000 * 1000, demand_growth_rate=0.3)
        others = Others(cliff=6, tge_unlock=0.1, vesting=18, others_supply=(80 * 1000 * 1000) - (initial_stable_coins * 10), monthly_sell_percentage=0.1)
        data = simulate_monthly_changes(36, liquidity_pool, investors, user, others)
        df = pd.DataFrame(data)
        df["initial_stable_coins"] = initial_stable_coins
        all_data_stable_coins.append(df)

    plot_token_price_over_time(all_data_stable_coins, "token_price_stable_coins", "Ціна токену для різних значень Stable Coins", x_label="month", group_label="initial_stable_coins", folder="stable_coins")
    plot_combined_graph(all_data_stable_coins, "stable_changes_combined", "Зміни стейбл коінів для різних значень Stable Coins", x_label='month', y_label='Кількість стейбл коінів', value_label='stable_coins', group_label='initial_stable_coins', folder='stable_coins')
    plot_combined_graph(all_data_stable_coins, "token_changes_combined", "Зміни токенів для різних значень Stable Coins", x_label='month', y_label='Кількість токенів', value_label='liquidity_supply', group_label='initial_stable_coins', folder='stable_coins')

    for initial_stable_coins in initial_stable_coins_values:
        plot_investor_profits(all_data_stable_coins, f'investors_realized_profit_stable_coins_{initial_stable_coins/1000000}M', f'Реалізований прибуток інвесторів для початкового значення Stable Coins: {initial_stable_coins/1000000}M', x_label='month', investor_type='realized', filter_value=initial_stable_coins, filter_type='initial_stable_coins', folder='stable_coins', investors=create_investors())
        plot_investor_profits(all_data_stable_coins, f'investors_unrealized_profit_stable_coins_{initial_stable_coins/1000000}M', f'Нереалізований прибуток інвесторів для початкового значення Stable Coins: {initial_stable_coins/1000000}M', x_label='month', investor_type='unrealized', filter_value=initial_stable_coins, filter_type='initial_stable_coins', folder='stable_coins', investors=create_investors())

    for demand in demand_values:
        liquidity_pool = LiquidityPool(stable_coins=1.5 * 1000 * 1000, liquidity_supply=15 * 1000 * 1000)
        investors = create_investors()
        user = User(demand=demand, demand_growth_rate=0.3)
        others = Others(cliff=6, tge_unlock=0.1, vesting=18, others_supply=65 * 1000 * 1000, monthly_sell_percentage=0.1)
        data = simulate_monthly_changes(36, liquidity_pool, investors, user, others)
        df = pd.DataFrame(data)
        df["demand"] = demand
        all_data_demand.append(df)

    plot_token_price_over_time(all_data_demand, "token_price_demand", "Ціна токену для різних значень Demand", x_label="month", group_label="demand", folder="demand")
    plot_combined_graph(all_data_demand, "stable_changes_combined", "Зміни стейбл коінів для різних значень Demand", x_label='month', y_label='Кількість стейбл коінів', value_label='stable_coins', group_label='demand', folder='demand')
    plot_combined_graph(all_data_demand, "token_changes_combined", "Зміни токенів для різних значень Demand", x_label='month', y_label='Кількість токенів', value_label='liquidity_supply', group_label='demand', folder='demand')

    for demand in demand_values:
        plot_investor_profits(all_data_demand, f'investors_realized_profit_demand_{demand/1000000}M', f'Реалізований прибуток інвесторів для значення Demand: {demand/1000000}M', x_label='month', investor_type='realized', filter_value=demand, filter_type='demand', folder='demand', investors=create_investors())
        plot_investor_profits(all_data_demand, f'investors_unrealized_profit_demand_{demand/1000000}M', f'Нереалізований прибуток інвесторів для значення Demand: {demand/1000000}M', x_label='month', investor_type='unrealized', filter_value=demand, filter_type='demand', folder='demand', investors=create_investors())

    for initial_stable_coins in initial_stable_coins_values:
        data_for_current_stable_coin = []
        for demand in demand_values:
            liquidity_pool = LiquidityPool(stable_coins=initial_stable_coins, liquidity_supply=initial_stable_coins * 10)
            investors = create_investors()
            user = User(demand=demand, demand_growth_rate=0.3)
            others = Others(cliff=6, tge_unlock=0.1, vesting=18, others_supply=(80 * 1000 * 1000) - (initial_stable_coins * 10), monthly_sell_percentage=0.1)
            data = simulate_monthly_changes(36, liquidity_pool, investors, user, others)
            df = pd.DataFrame(data)
            df["initial_stable_coins"] = initial_stable_coins
            df["demand"] = demand
            data_for_current_stable_coin.append(df)
            all_data_stable_coins_and_demand.append(df)

        plot_token_price_over_time(data_for_current_stable_coin, f"token_price_stable_coins_{initial_stable_coins/1000000}M", f"Ціна токену для початкового значення Stable Coins: {initial_stable_coins/1000000}M", x_label="month", group_label="demand", folder="stable_coins_and_demand")
        plot_combined_graph(data_for_current_stable_coin, f"stable_changes_combined_{initial_stable_coins/1000000}M", f"Зміни стейбл коінів для початкового значення Stable Coins: {initial_stable_coins/1000000}M", x_label='month', y_label='Кількість стейбл коінів', value_label='stable_coins', group_label='demand', folder='stable_coins_and_demand')
        plot_combined_graph(data_for_current_stable_coin, f"token_changes_combined_{initial_stable_coins/1000000}M", f"Зміни токенів для початкового значення Stable Coins: {initial_stable_coins/1000000}M", x_label='month', y_label='Кількість токенів', value_label='liquidity_supply', group_label='demand', folder='stable_coins_and_demand')


def create_investors():
    return [
        Investor(cliff=6, tge_unlock=0.1, vesting=18, investors_supply=4 * 1000 * 1000, monthly_sell_percentage=0.05),
        Investor(cliff=6, tge_unlock=0.1, vesting=18, investors_supply=4 * 1000 * 1000, monthly_sell_percentage=0.1),
        Investor(cliff=6, tge_unlock=0.1, vesting=18, investors_supply=4 * 1000 * 1000, monthly_sell_percentage=0.2),
        Investor(cliff=6, tge_unlock=0.1, vesting=18, investors_supply=4 * 1000 * 1000, monthly_sell_percentage=0.3),
        Investor(cliff=6, tge_unlock=0.1, vesting=18, investors_supply=4 * 1000 * 1000, monthly_sell_percentage=0.4)
    ]


def simulate_monthly_changes(months, liquidity_pool, investors, user, others):
    data = []

    for month in range(1, months + 1):
        user.buy_tokens(liquidity_pool=liquidity_pool)
        user.update_demand(month)
        for investor in investors:
            investor.sell_tokens(liquidity_pool=liquidity_pool)
        others.sell_tokens(liquidity_pool=liquidity_pool)

        pool_state = liquidity_pool.get_pool_state()
        pool_state["month"] = month
        for i, investor in enumerate(investors):
            pool_state[f'investor_{i+1}_realized_profit'] = investor.realized_profit
            pool_state[f'investor_{i+1}_unrealized_profit'] = investor.unrealized_profit
            pool_state[f'investor_{i+1}_monthly_sell_percentage'] = investor.monthly_sell_percentage
        data.append(pool_state)

    return data


def plot_token_price_over_time(all_data, graphic_file_name, graphic_name, x_label, group_label, folder=""):
    plt.figure(figsize=(10, 6))

    for df in all_data:
        plt.plot(df[x_label], df["current_price"], marker='o', linestyle='-',
                 label=f'{group_label.capitalize()}: {df[group_label].iloc[0]:,.0f}')

    plt.title(graphic_name)
    plt.xlabel("Місяць")
    plt.ylabel("Ціна токену")
    plt.legend()
    plt.grid(True)
    plt.savefig(f'graphics/{folder}/{graphic_file_name}.png')
    plt.close()


def plot_combined_graph(all_data, graphic_file_name, graphic_name, x_label, y_label, value_label, group_label, folder=""):
    plt.figure(figsize=(10, 6))

    for df in all_data:
        plt.plot(df[x_label], df[value_label], marker='o', linestyle='-', label=f'{group_label.capitalize()}: {df[group_label].iloc[0]:,.0f}')

    plt.title(graphic_name)
    plt.xlabel(x_label.capitalize())
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True)
    plt.savefig(f'graphics/{folder}/{graphic_file_name}.png')
    plt.close()


def plot_investor_profits(all_data, graphic_file_name, graphic_name, x_label, investor_type, filter_value, filter_type, folder="", investors=None):
    plt.figure(figsize=(10, 6))

    for df in all_data:
        if df[filter_type].iloc[0] == filter_value:
            for i, investor in enumerate(investors):
                plt.plot(df[x_label], df[f'investor_{i+1}_{investor_type}_profit'], marker='o', linestyle='-',
                         label=f'Інвестор {i+1} ({investor.monthly_sell_percentage * 100}%)')

    plt.title(graphic_name)
    plt.xlabel("Місяць")
    plt.ylabel("Прибуток")
    plt.legend()
    plt.grid(True)
    plt.savefig(f'graphics/{folder}/{graphic_file_name}.png')
    plt.close()


if __name__ == "__main__":
    main()
