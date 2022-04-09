from functools import reduce
import pandas as pd
import numpy as np

# Price momentum score with period of 252 days
def readFile(firm):
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
            days252 = closing_price[num-var:num+1]
            rank = [sorted(days252, reverse=True).index(x) for x in days252]
            score_list.append(score[rank[var]])
        else:
            score_list.append("NaN")

    df[firm + "_Score"] = score_list
    df.drop(["Close/Last", "Volume", "Open", "High", "Low"], axis=1, inplace=True)
    df_score = pd.DataFrame(df)
    return df_score


def main():
    firms = ["AAPL", "SBUX", "MSFT", "CSCO", "QCOM", "Facebook", "AMZN", "TSLA", "AMD", "ZNGA"]
    dfs = []

    for firm in firms:
        df = readFile(firm)
        dfs.append(df)

    df_final = reduce(lambda left, right: pd.merge(left, right, how="outer", on="Date"), dfs)
    df_final.to_csv("Price_Momentum_Score252.csv", index=False)


main()
