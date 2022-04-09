import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def score252(firm):
    filename = "./Data/" + firm
    df = pd.read_csv(filename + ".csv", sep=",", header=0)
    score_list = []

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by="Date", ascending=True)
    df["Close/Last"] = df["Close/Last"].str.replace("$", "", regex=False).astype(float)
    closing_price = df["Close/Last"].tolist()

    period = 252
    var = period - 1
    score = np.around(np.linspace(100, 0, period, endpoint=True), 2)

    for num in range(len(closing_price)):
        if num >= var:
            days252 = closing_price[num - var:num + 1]
            rank = [sorted(days252, reverse=True).index(x) for x in days252]
            score_list.append(score[rank[var]])
        else:
            score_list.append("NaN")

    df[firm + "_Score"] = score_list
    df_252 = pd.DataFrame(df)
    return df_252


def score126(firm):
    filename = "./Data/" + firm
    df = pd.read_csv(filename + ".csv", sep=",", header=0)
    score_list = []

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by="Date", ascending=True)
    df["Close/Last"] = df["Close/Last"].str.replace("$", "", regex=False).astype(float)
    closing_price = df["Close/Last"].tolist()

    period = 126
    var = period - 1
    score = np.around(np.linspace(100, 0, period, endpoint=True), 2)

    for num in range(len(closing_price)):
        if num >= var:
            days252 = closing_price[num - var:num + 1]
            rank = [sorted(days252, reverse=True).index(x) for x in days252]
            score_list.append(score[rank[var]])
        else:
            score_list.append("NaN")

    df[firm + "_Score"] = score_list
    df_126 = pd.DataFrame(df)
    return df_126


def score63(firm):
    filename = "./Data/" + firm
    df = pd.read_csv(filename + ".csv", sep=",", header=0)
    score_list = []

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by="Date", ascending=True)
    df["Close/Last"] = df["Close/Last"].str.replace("$", "", regex=False).astype(float)
    closing_price = df["Close/Last"].tolist()

    period = 63
    var = period - 1
    score = np.around(np.linspace(100, 0, period, endpoint=True), 2)

    for num in range(len(closing_price)):
        if num >= var:
            days252 = closing_price[num - var:num + 1]
            rank = [sorted(days252, reverse=True).index(x) for x in days252]
            score_list.append(score[rank[var]])
        else:
            score_list.append("NaN")

    df[firm + "_Score"] = score_list
    df_63 = pd.DataFrame(df)
    return df_63


def ema20(firm):
    filename = "./Data/" + firm
    df = pd.read_csv(filename + ".csv", sep=",", header=0)
    ema_list = []

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by="Date", ascending=True)
    df["Close/Last"] = df["Close/Last"].str.replace("$", "", regex=False).astype(float)
    closing_price = df["Close/Last"].tolist()

    period = 20
    wm = 2 / (period + 1)
    sma = sum(closing_price[:period]) / period
    ema_initial = np.around(((closing_price[period] * wm) + (sma * (1 - wm))), 2)
    ema_list.append(ema_initial)
    counter = 0

    for price in range(period + 1, len(closing_price), 1):
        ema_today = np.around(((closing_price[price] * wm) + (ema_list[counter] * (1 - wm))), 2)
        ema_list.append(ema_today)
        counter += 1

    # Delete the oldest data that cannot have EMA
    df.drop(labels=range(len(closing_price) - period, len(closing_price)), axis=0, inplace=True)
    df[firm + "_EMA"] = ema_list
    df_ema = pd.DataFrame(df)
    return df_ema


def main():
    # Use only one stock to compare scores with different periods (252, 126, and 63) and exponential moving average
    # with period of 20 days (Using a plot and bar graphs)
    amazon252 = score252("AMZN")
    amazon252 = amazon252.drop(amazon252.index[0:1887], axis=0)

    amazon126 = score126("AMZN")
    amazon126 = amazon126.drop(amazon126.index[0:1887], axis=0)

    amazon63 = score63("AMZN")
    amazon63 = amazon63.drop(amazon63.index[0:1887], axis=0)

    amazon_EMA = ema20("AMZN")
    amazon_EMA = amazon_EMA.drop(amazon_EMA.index[0:1887], axis=0)

    # 4 Data Subplots
    plt.figure(figsize=(30, 20))

    # 1st, Close/Last price
    ax1 = plt.subplot(5, 1, 1)
    plt.plot(amazon252["Date"], amazon252["Close/Last"], linestyle="solid", linewidth=1, color="C4")

    # 2nd, Price momentum score with period of 252 days
    ax2 = plt.subplot(5, 1, 2)
    plt.bar(amazon252["Date"], amazon252["AMZN_Score"], linestyle="dashed", linewidth=1, color="C2")
    ax2.set_ylim(0, 120)

    # 3rd, Price momentum score with period of 126 days
    ax3 = plt.subplot(5, 1, 3)
    plt.bar(amazon126["Date"], amazon126["AMZN_Score"], linestyle="dashed", linewidth=1, color="C2")
    ax3.set_ylim(0, 120)

    # 4th, Price momentum score with period of 63 days
    ax4 = plt.subplot(5, 1, 4)
    plt.bar(amazon63["Date"], amazon63["AMZN_Score"], linestyle="dashed", linewidth=1, color="C2")
    ax4.set_ylim(0, 120)

    # 5th, Exponential moving average with period of 20 days
    ax5 = plt.subplot(5, 1, 5)
    plt.bar(amazon_EMA["Date"], amazon_EMA["AMZN_EMA"], linestyle="dashed", linewidth=1, color="C2")
    ax5.set_ylim(0, 4500)

    plt.show()


main()
