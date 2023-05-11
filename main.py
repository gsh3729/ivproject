import base64
from io import BytesIO

from flask import Flask, render_template

from matplotlib.figure import Figure

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

import matplotlib
matplotlib.use('agg')

app = Flask(__name__)



@app.route("/implied")
def implied():
    fig = Figure(figsize=(10,6))
    ax = fig.subplots()
    df =  pd.read_csv("./data/Implied.csv")
    ax.axis(ymin = 0, ymax = 7)
    ax.scatter(df['Year'], df['Implied_ERP'], linestyle="-", marker="o", c = "black")
    ax.plot(df['Year'], df['Implied_ERP'], c="black")
    ax.set_title("Implied Equity Risk Premium of USA")
    ax.set_xlabel("Year")
    ax.set_ylabel("Implied ERP")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    info = "The implied equity risk premium (ERP) is an estimate of the expected excess return that investors require for investing in stocks over a risk-free rate, based on the current market prices of stocks and other financial instruments. The implied ERP can be used as a gauge of investor sentiment and risk appetite for stocks."
    return render_template('result.html', data = data, info = info)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/test")
def test():
    fig = Figure()
    ax = fig.subplots()
    df =  pd.read_csv("./data/Implied.csv")
    ax.axis(ymin = 0, ymax = 7)
    ax.scatter(df['Year'], df['Implied_ERP'], linestyle="-", marker="o", c = "black")
    ax.plot(df['Year'], df['Implied_ERP'], c="black")
    ax.set_title("Implied Equity Risk Premium of USA")
    ax.set_xlabel("Year")
    ax.set_ylabel("IERP")


    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template('result.html', data = data)


@app.route("/rating")
def rating():
    fig = Figure(figsize=(20,16))
    ax = fig.subplots()
    df = pd.read_csv("./data/MoodysRatings.csv")
    df_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    df_world_teams = df_world.merge(df, how="left", left_on=['name'], right_on=['Country'])
    df_world["geometry"].boundary.plot(ax = ax)
    color_dict = {'Aaa': 'blue', 'Aa': 'orange', 'A': 'green', 'Baa': 'red', 'Ba': 'purple',  'B': 'brown', 'C': 'pink', 'ND': 'gray'}
    df_world_teams["Colors"] = df_world_teams["Moody's rating"].map(color_dict)
    print("is nan: ", df_world_teams['Colors'].isna().sum())
    df_world_teams = df_world_teams.dropna()

    df_world_teams.plot(ax = ax, color = df_world_teams["Colors"])
    custom_points = [Line2D([0], [0], marker="o", linestyle="none", markersize=10, color=color) for color in color_dict.values()]
    leg_points = ax.legend(custom_points, color_dict.keys())
    ax.add_artist(leg_points)
    ax.set_title("Moody's Country Ratings")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    info = "Moody's country rating assesses the creditworthiness of a country's government in terms of its ability to pay back its debts and the likelihood of default."
    return render_template('result.html', data = data, info = info)

@app.route("/risk")
def risk():
    fig = Figure(figsize=(20,16))
    ax = fig.subplots()
    df = pd.read_csv("./data/ERP.csv")
    df_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    df_world["geometry"].boundary.plot(ax = ax)

    df_world_teams = df_world.merge(df, how="left", left_on=['name'], right_on=['Countries'])
    df_world_teams['ERP'] = df_world_teams['ERP'].apply(lambda x: x if x <= 30 else 30)
    df_world_teams.plot(column="ERP", ax=ax, cmap='YlGnBu_r', legend=True) 
    ax.set_title("Equity Risk Premium of Countries")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    info = "The equity risk premium (ERP) for a country is the additional return that investors demand to invest in the stock market of that country compared to a risk-free investment such as government bonds."
    return render_template('result.html', data = data, info = info)


@app.route("/expected")
def expected():
    fig = Figure(figsize=(12,6))
    ax = fig.subplots()
    df = pd.read_csv("./data/Implied.csv")
    ax.bar(df['Year'], df['T_Bond_Rate'], color='b', label = "T Bond Rate")
    ax.bar(df['Year'], df['Implied_ERP'], bottom=df['T_Bond_Rate'], color='r', label = "Implied ERP")
    ax.legend(["T Bond Rate", "Implied ERP"])
    ax.set_title("Expected Return on Stocks")
    ax.set_xlabel("Year")
    ax.set_ylabel("Return")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    info = "Expected return on Stocks = T Bond Rate + Implied Equity Risk Premium"
    return render_template('result.html', data = data, info = info)

@app.route("/returns")
def returns():
    fig = Figure(figsize=(12,6))
    ax = fig.subplots()
    df = pd.read_csv("./data/Returns.csv")

    ax.plot(df['Year'], df['Gold_Return'], label ='Gold return', color = 'gold')
    ax.plot(df['Year'], df['SP_Return'], label ='SP return', color = 'red')
    # ax.plot(df['Year'], df['Ten_Return'], label ='10 Year Bond return')
    ax.set_title("Gold Vs SP 500 Returns comparison")
    ax.legend()


    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    info = "Gold Vs SP 500 returns comparison"
    return render_template('result.html', data = data, info = info)

@app.route("/gold")
def gold():
    fig = Figure(figsize=(12,6))
    ax = fig.subplots()
    df = pd.read_csv("./data/Returns.csv")

    ax.bar(df['Year'], df['Gold_Return'], color = "gold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Gold Return")
    ax.set_title("Yearly gold returns")
    

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    info = "Gold"
    return render_template('result.html', data = data, info = info)

@app.route("/sp")
def sp():
    fig = Figure(figsize=(12,6))

    ax = fig.subplots()
    df = pd.read_csv("./data/Returns.csv")

    ax.bar(df['Year'], df['SP_Return'], color = "red")
    ax.set_xlabel("Year")
    ax.set_ylabel("SP500 Return")
    ax.set_title("Yearly SP500 returns")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    info = "The S&P 500, also known as the Standard & Poor's 500, is a stock market index that tracks the performance of the 500 largest publicly traded companies in the United States."
    return render_template('result.html', data = data, info = info)

@app.route("/house")
def house():
    fig = Figure(figsize=(12,6))

    ax = fig.subplots()
    df = pd.read_csv("./data/Housing.csv")

    ax.bar(df['Year'], df['Housing_Return'], color = 'hotpink')
    ax.set_xlabel("Year")
    ax.set_ylabel("Housing Return")
    ax.set_title("Yearly Housing returns")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    info = "Housing"
    return render_template('result.html', data = data, info = info)

@app.route("/spanalysis")
def spanalysis():
    fig = Figure(figsize=(12,8))
    ax = fig.subplots()
    df = pd.read_csv("./data/Returns.csv")
    out = pd.cut(df['SP_Return_div'], bins=[-60, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 60], include_lowest=True)
    ddf = out.value_counts(sort=False).rename_axis('unique_values').reset_index(name='counts')
    ddf['positive'] = [False]*6 + [True]*6
    ddf['counts'].plot(kind='bar',ax = ax, color=ddf.positive.map({True: 'g', False: 'r'}))
    ax.set_xticklabels(ddf['unique_values'], rotation=25)
    ax.set_ylabel("Number of years")
    ax.set_xlabel("Annual Return in percentage")
    # ax.set_xticks(rotation=45)
    ax.set_title("Annual returns on SP 500 in 1928-2022")
 
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    info = "SP 500 Analysis" 
    return render_template('result.html', data = data, info = info)

@app.route("/inflation")
def inflation():
    fig = Figure(figsize=(12,6))
    ax = fig.subplots()
    df = pd.read_csv("./data/Inflation.csv")

    year = df['Year'].to_list()
    data = np.array([df['Inflation'].to_list(), df['GDP Growth'].to_list()])
    data_shape = np.shape(data)

    # Take negative and positive data apart and cumulate
    def get_cumulated_array(data, **kwargs):
        cum = data.clip(**kwargs)
        cum = np.cumsum(cum, axis=0)
        d = np.zeros(np.shape(data))
        d[1:] = cum[:-1]
        return d  

    cumulated_data = get_cumulated_array(data, min=0)
    cumulated_data_neg = get_cumulated_array(data, max=0)

    # Re-merge negative and positive data.
    row_mask = (data<0)
    cumulated_data[row_mask] = cumulated_data_neg[row_mask]
    data_stack = cumulated_data

    cols = ["r", "g"]
    l = ["Inflation rate", "Real GDP Growth"]

    for i in np.arange(0, data_shape[0]):
        ax.bar(year, data[i], bottom=data_stack[i], color=cols[i], label = l[i])

    df = pd.read_csv("./data/Implied.csv")    
    ax.plot(year, df['T_Bond_Rate'], c="black", label="10Y Bond rate", linewidth=2.5)
    ax.legend()
    ax.set_title("Inflation")
    ax.set_xlabel("Year")
    ax.set_ylabel("Return")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    info = "Inflation rate refers to the rate at which the general level of prices for goods and services in an economy is increasing over a period of time. The 10-year Treasury bond rate is the yield or interest rate of the 10-year U.S. Treasury bond, which is a debt security issued by the U.S. government. Investors may use the 10-year Treasury bond rate as an indicator of the direction of the economy and inflation expectations."
    return render_template('result.html', data = data, info = info)



    

if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()