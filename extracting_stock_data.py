!pip install yfinance
#!pip install pandas
#!pip install requests
!pip install bs4
#!pip install plotly

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
#TSLA
TSLA = yf.Ticker("TSLA")
tesla_data= TSLA.history(period="max")
tesla_data.reset_index(inplace=True)
tesla_data.head()

html_data=requests.get("https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue")
beautiful_soup=BeautifulSoup(html_data.content,"html.parser")

tesla_revenue= pd.DataFrame(columns=["Date","Revenue"])
for row in beautiful_soup.find(text="Tesla Quarterly Revenue").find_parent("table").find("tbody").find_all("tr"):
    col=row.find_all("td")
    Date=col[0].text
    Revenue=col[1].text.replace("$", "").replace(",", "")
    tesla_revenue=tesla_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)

tesla_revenue=tesla_revenue[tesla_revenue['Revenue']!= ""]
tesla_revenue.dropna(inplace=True)
tesla_revenue.tail()

#GME
GME = yf.Ticker("GME")
gme_data= GME.history(period="max")
gme_data.reset_index(inplace=True)
gme_data.head()

html_data=requests.get("https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue.")
beautiful_soup=BeautifulSoup(html_data.content,"html.parser")

gme_revenue= pd.DataFrame(columns=["Date","Revenue"])
for row in beautiful_soup.find(text = "GameStop Quarterly Revenue").find_parent("table").find("tbody").find_all("tr"):
    col=row.find_all("td")
    Date=col[0].text
    Revenue=col[1].text.replace("$", "").replace(",", "")

    gme_revenue=gme_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)
    gme_revenue.tail()

#Visulizations
make_graph(tesla_data, tesla_revenue, 'Tesla')

make_graph(gme_data, gme_revenue, 'GameStop')
