from functools import reduce
import pandas as pd
import numpy as np


def readFile(firm, period):
    filename = "./Data/" + firm + ".csv"
    df = pd.read_csv(filename, sep=",", header=0)
    ema_list = []

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by="Date", ascending=True)
    df["Close/Last"] = df["Close/Last"].str.replace("$", "", regex=False).astype(float)
    closing_price = df["Close/Last"].tolist()

    # Calculate exponential moving average with period of 20 days
    wm = 2/(period+1)
    sma = sum(closing_price[:period])/period
    ema_initial = np.around(((closing_price[period]*wm) + (sma*(1-wm))), 2)
    ema_list.append(ema_initial)
    counter = 0

    for price in range(period+1, len(closing_price), 1):
        ema_today = np.around(((closing_price[price]*wm) + (ema_list[counter]*(1-wm))), 2)
        ema_list.append(ema_today)
        counter += 1

    # Delete the oldest data that cannot have EMA
    df.drop(labels=range(len(closing_price)-period, len(closing_price)), axis=0, inplace=True)
    df.drop(["Close/Last", "Volume", "Open", "High", "Low"], axis=1, inplace=True)
    df[firm + "_EMA"] = ema_list
    df_ema = pd.DataFrame(df)
    return df_ema


def main():
    firms = ["AAPL", "SBUX", "MSFT", "CSCO", "QCOM", "Facebook", "AMZN", "TSLA", "AMD", "ZNGA"]
    dfs = []

    for firm in firms:
        df = readFile(firm, 20)
        dfs.append(df)

    df_final = reduce(lambda left, right: pd.merge(left, right, how="outer", on="Date"), dfs)
    df_final.to_csv("Exponential_Moving_Average20.csv", index=False)


main()
