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

#define graphing function we'll use later
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

#TSLA stock data
#Create Tesla stock ticker
TSLA = yf.Ticker("TSLA")
#extract stock information for maximum amount of time available
tesla_data= TSLA.history(period="max")
#reset the index and show first 5 rows of available data
tesla_data.reset_index(inplace=True)
tesla_data.head()

#webscraping to extract Tesla revenue data
html_data=requests.get("https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue")
#parse html data
beautiful_soup=BeautifulSoup(html_data.content,"html.parser")

#Extract table with Tesla Quarterly Revenue
tesla_revenue= pd.DataFrame(columns=["Date","Revenue"])
for row in beautiful_soup.find(text="Tesla Quarterly Revenue").find_parent("table").find("tbody").find_all("tr"):
    col=row.find_all("td")
    Date=col[0].text
    Revenue=col[1].text.replace("$", "").replace(",", "")
    tesla_revenue=tesla_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)

#Remove empty rows
tesla_revenue=tesla_revenue[tesla_revenue['Revenue']!= ""]
tesla_revenue.dropna(inplace=True)
tesla_revenue.tail()

#GME stock data
#Create GameStop ticker
GME = yf.Ticker("GME")
#extract stock information for maximum amount of time available
gme_data= GME.history(period="max")
#reset the index and show first 5 rows of available data
gme_data.reset_index(inplace=True)
gme_data.head()

#webscraping to extract GameStop revenue data
html_data=requests.get("https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue.")
#parse html data
beautiful_soup=BeautifulSoup(html_data.content,"html.parser")

#Extract table with GameStop Quarterly Revenue
gme_revenue= pd.DataFrame(columns=["Date","Revenue"])
for row in beautiful_soup.find(text = "GameStop Quarterly Revenue").find_parent("table").find("tbody").find_all("tr"):
    col=row.find_all("td")
    Date=col[0].text
    Revenue=col[1].text.replace("$", "").replace(",", "")

#Display last 5 rows of revenue data    
    gme_revenue=gme_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)
    gme_revenue.tail()

#Graphing Visulizations
make_graph(tesla_data, tesla_revenue, 'Tesla')

make_graph(gme_data, gme_revenue, 'GameStop')
