import dash
from dash import html
from dash import dcc
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import yfinance as yf

########### Define your variables

#Site parameters
tabtitle='$$$'
myheading='The Prospector'
githublink='https://github.com/t-boeck/prospector'

#Data parameters
ticker = 'aapl'
period = '1d'
interval = '1m'
mov_avg_window=21

#Download data
data = yf.download(tickers=ticker, period=period, interval=interval,
                       progress=False, show_errors=False)

# if data.empty:
#     with out_pl: print(f"{ticker} data failed to download, please try again.")
#     return

data.index = data.index.tz_convert('America/Los_Angeles')

#Calculate Moving Average and Ballinger Bands
mov_avg_title = str(mov_avg_window) + 'd Moving Avg'
data[mov_avg_title] = data['Close'].rolling(window=mov_avg_window).mean()
data['Upper Band'] = data[mov_avg_title] + 1.96*data['Close'].rolling(window=mov_avg_window).std()
data['Lower Band'] = data[mov_avg_title] - 1.96*data['Close'].rolling(window=mov_avg_window).std()

#declare figure
fig = go.Figure()

fig.add_trace(go.Scatter(x=data.index, y= data[mov_avg_title],
                         line=dict(color='blue', width=.7),
                         name = mov_avg_title))
fig.add_trace(go.Scatter(x=data.index, y= data['Upper Band'],
                         line=dict(color='red', width=1.5),
                         name = 'Upper Band (Sell)'))
fig.add_trace(go.Scatter(x=data.index, y= data['Lower Band'],
                         line=dict(color='green', width=1.5),
                         name = 'Lower Band (Buy)'))

#Candlestick
fig.add_trace(go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'], name = 'market data'))

# Add titles
fig.update_layout(
    title=ticker.upper(),
    yaxis_title='Stock Price')

# X-Axes
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=15, label="15m", step="minute", stepmode="backward"),
            dict(count=45, label="45m", step="minute", stepmode="backward"),
            dict(count=3, label="3h", step="hour", stepmode="backward"),
            dict(label=period, step="all")
        ])
    )
)

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading),
    dcc.Graph(
        id='stocks',
        figure=fig
    ),
    html.A('Code on Github', href=githublink),
    ]
)

if __name__ == '__main__':
    app.run_server()
