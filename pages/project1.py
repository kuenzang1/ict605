import streamlit as st
import pandas as pd
import requests

# Function to fetch cryptocurrency data from CoinGecko API
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10000,
        "page": 1,
        "sparkline": "false"
    }
    response = requests.get(url, params=params)
    return response.json()

# Fetch crypto data
crypto_data = fetch_crypto_data()

# Create a DataFrame with selected columns
selected_columns = ['name', 'symbol', 'image', 'current_price', 'market_cap', 'high_24h', 'low_24h', 'price_change_24h']
df = pd.DataFrame(crypto_data)[selected_columns]

# Set page title and favicon
st.set_page_config(page_title="Crypto Dashboard", page_icon=":money_with_wings:")

# Add a title
st.title("Cryptocurrency Dashboard")

# Convert the 'image' column to HTML with image tags
df['image'] = df['image'].apply(lambda x: f'<img src="{x}" style="max-width:20px;">')

# Render the DataFrame as HTML
st.write(df.to_html(escape=False), unsafe_allow_html=True)
## Render the DataFrame with lazy-loading
#st.dataframe(df, height=800) ##not rendering images
# Pagination controls
page_number = st.number_input("Enter page number:", min_value=1, max_value=len(df)//100+1, value=1)
start_idx = (page_number - 1) * 100
end_idx = page_number * 100
st.write(f"Displaying rows {start_idx+1} to {min(end_idx, len(df))} of {len(df)}")
#for idx, row in df.iterrows():
 #   detail_page_url = f"streamlit run detail_page.py?id={idx}"
  #  st.markdown(f"[Details for {row['name']}](<{detail_page_url}>)", unsafe_allow_html=True)