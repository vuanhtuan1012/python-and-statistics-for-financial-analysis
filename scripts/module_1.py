"""
Building a simple trading strategy
"""

import logging

import pandas as pd
from matplotlib import pyplot as plt

from common import DATA_DIR, get_logger


def read_csv(filename: str, logger: logging.Logger) -> pd.DataFrame:
    """
    Returns DataFrame read from CSV file in the data directory
    """
    df = pd.read_csv(
        DATA_DIR.joinpath(filename), index_col="Date", parse_dates=["Date"]
    )
    logger.info("read successfully CSV file %s.", filename)
    return df


def get_column_name(window: int) -> str:
    """
    Returns column name of a signal
    """
    return f"MA{window}"


def add_signal(df: pd.DataFrame, window: int, logger: logging.Logger):
    """
    Adds signal column to DataFrame

    Rows contain missing values will be droped
    """
    col_name = get_column_name(window)

    if col_name in df.columns:
        logger.info("signal column `%s` already exists in DataFrame.", col_name)
        return

    df[col_name] = df["Close"].rolling(window).mean()
    df.dropna(inplace=True)
    logger.info("signal column `%s` was added successfully.", col_name)


def execute_long_one_share_trade(
    df: pd.DataFrame, fast_window: int, slow_window: int, logger: logging.Logger
):
    """
    Executes the long one-share stock trading strategy
    """
    # add fast and slow signal columns
    add_signal(df, fast_window, logger)
    add_signal(df, slow_window, logger)

    # follow the long one-share stock trading strategy:
    # buy 1 if fast > slow, otherwise, do nothing
    fast_col = get_column_name(fast_window)
    slow_col = get_column_name(slow_window)
    df["Shares"] = [
        1 if df.loc[idx, fast_col] > df.loc[idx, slow_col] else 0 for idx in df.index
    ]
    logger.info("number of shares is stored in the `Shares` column.")


def calculate_daily_profit(df: pd.DataFrame, logger: logging.Logger):
    """
    Calculates daily profit
    """
    df["CloseTomorrow"] = df["Close"].shift(-1)
    df.dropna(inplace=True)
    df["Profit"] = [
        (
            df.loc[idx, "CloseTomorrow"] - df.loc[idx, "Close"]
            if df.loc[idx, "Shares"] == 1
            else 0
        )
        for idx in df.index
    ]
    logger.info("daily profit is stored in the `Profit` column.")


def calculate_wealth(df: pd.DataFrame, logger: logging.Logger):
    """
    Calculates the accumulated wealth over the period
    """
    df["Wealth"] = df["Profit"].cumsum()
    logger.info("accumulated wealth is stored in the `Wealth` column.")


def display_profit(df: pd.DataFrame, company: str):
    """
    Displays the graph of daily profit
    """
    df["Profit"].plot()
    plt.axhline(y=0, color="red")
    plt.ylabel("Profit")
    plt.title(f"{company} Daily Profit")
    plt.show()


def display_wealth(df: pd.DataFrame, company: str):
    """
    Displays the graph of accumulated wealth
    """
    df["Wealth"].plot()
    plt.ylabel("Wealth")
    plt.title(
        f"{company}: total money win = ${round(df.loc[df.index[-1], "Wealth"], 2)}"
    )
    plt.show()


def trade_and_analyse(company: str, data_file: str, logger: logging.Logger):
    """
    Executes the long one-share stock trading strategy
    """
    logger.info("Trade %s stock.", company)
    df = read_csv(data_file, logger)
    execute_long_one_share_trade(df, 10, 50, logger)
    calculate_daily_profit(df, logger)
    display_profit(df, company)
    calculate_wealth(df, logger)
    display_wealth(df, company)


def main():
    """
    Main function
    """
    logger = get_logger()
    trade_and_analyse("Facebook", "facebook.csv", logger)
    trade_and_analyse("Microsoft", "microsoft.csv", logger)


if __name__ == "__main__":
    main()
