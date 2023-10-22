import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pycoingecko import CoinGeckoAPI
import requests

# Your API key here
api_key = 'CG-i6VrFAfKTwbG9KBuJMf6SPTs'

# Set up the page
st.title('Cryptocurrency Price Viewer')

# Initialize CoinGecko API client
cg = CoinGeckoAPI()

# Define a function to get cryptocurrency data
def get_crypto_data(symbol, interval, currency, api_key):
    headers = {'X-CoinAPI-Key': api_key}
    if interval == 'daily':
        if symbol == 'btc':
            data = cg.get_coin_market_chart_by_id(symbol, currency, '30d', headers=headers)
        else:
            data = cg.get_coin_market_chart_by_id(symbol, currency, '1d', headers=headers)
    elif interval == 'weekly':
        data = cg.get_coin_market_chart_by_id(symbol, currency, '7d', headers=headers)
    elif interval == 'monthly':
        data = cg.get_coin_market_chart_by_id(symbol, currency, '1d', headers=headers)
    elif interval == 'yearly':
        data = cg.get_coin_market_chart_by_id(symbol, currency, '365d', headers=headers)
    return data

# Get the list of cryptocurrencies from CoinGecko API
crypto_list = cg.get_coins_list()

# Create a dictionary to map symbol to id
crypto_dict = {crypto['symbol']: crypto['id'] for crypto in crypto_list}

# Extract the symbols as a list
crypto_symbols = list(crypto_dict.keys())

# Set default values
default_crypto_symbol = 'btc'
default_crypto_id = crypto_dict[default_crypto_symbol]
default_interval = 'daily'
default_market_currency = 'usd'

# Create a searchable dropdown for cryptocurrency selection
selected_crypto_symbol = st.selectbox('Select Cryptocurrency', crypto_symbols, key='crypto_dropdown', index=crypto_symbols.index(default_crypto_symbol))

# Get the corresponding id
selected_crypto_id = crypto_dict[selected_crypto_symbol]

# Create a radio button to select time interval
selected_interval = st.radio('Select Time Interval', ['daily', 'weekly', 'monthly'])

# Fetch the currency data
response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
currency_data = response.json()

# Extract the top 50 currencies
top_currencies = list(currency_data['rates'].keys())[:50]

# Create a searchable dropdown for selecting currency
selected_currency = st.selectbox('Select Currency', top_currencies, key='currency_dropdown')

crypto_data = get_crypto_data(selected_crypto_id, selected_interval, selected_currency, api_key)

# Convert data to DataFrame
df = pd.DataFrame(crypto_data['prices'], columns=['time', 'price'])
df['time'] = pd.to_datetime(df['time'], unit='ms')
df.set_index('time', inplace=True)

# Get market cap data
market_cap_data = crypto_data['market_caps']
market_caps = [cap[1] for cap in market_cap_data]

# Plot the data using Plotly
fig = go.Figure()

fig.add_trace(go.Scatter(x=df.index, y=df['price'], mode='lines', name='Price'))
fig.add_trace(go.Scatter(x=df.index, y=market_caps, mode='lines', name='Market Cap'))

# Dynamic x-axis label
fig.update_xaxes(title_text='Time')

# Dynamic y-axis label
fig.update_yaxes(title_text=f'Price in {selected_currency.upper()} / Market Cap')

# Set title
fig.update_layout(title=f'{selected_crypto_symbol.upper()} Price and Market Cap Chart',
                  xaxis_title='Time',
                  yaxis_title=f'Price in {selected_currency.upper()} / Market Cap',
                  template='plotly_dark')

# Display the plot
st.plotly_chart(fig)

# Display raw data to check
# st.write(df)
