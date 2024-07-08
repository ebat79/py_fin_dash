import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

@st.cache_resource(ttl=300, show_spinner=True)
def fetch_options_data(symbol):
    """ Fetch options data for an ETF symbol from Yahoo Finance. """
    etf = yf.Ticker(symbol)
    try:
        expiration_dates = etf.options
        options_info = []
        for expiration_date in expiration_dates:
            options_chain = etf.option_chain(expiration_date)
            puts = options_chain.puts
            calls = options_chain.calls
            options_info.append({
                'Expiration Date': expiration_date,
                'Puts Count': len(puts),
                'Calls Count': len(calls)
            })
        return options_info
    except Exception as e:
        st.error(f"Could not fetch options data for {symbol}: {e}")
        return []

def format_assets(assets):
    """ Format large numbers into a readable string with appropriate units. """
    if assets >= 1e9:
        return f"{assets / 1e9:.2f}B"
    elif assets >= 1e6:
        return f"{assets / 1e6:.2f}M"
    return assets

@st.cache_data(show_spinner=True)
def fetch_data(symbol):
    """ Fetch financial data and metrics for ETFs from Yahoo Finance. """
    etf = yf.Ticker(symbol)
    info = etf.info
    options_info = fetch_options_data(symbol)
    return {
        'Name': info.get('longName', 'N/A'),
        'Latest Price': f"${info.get('previousClose', np.nan)}",
        '52W High': f"${info.get('fiftyTwoWeekHigh', np.nan)}",
        '52W Low': f"${info.get('fiftyTwoWeekLow', np.nan)}",
        '1 Year Return': f"{info.get('ytdReturn', np.nan) * 100:.2f}%" if info.get('ytdReturn') is not None else np.nan,
        '3 Year Return': f"{info.get('threeYearAverageReturn', np.nan) * 100:.2f}%" if info.get('threeYearAverageReturn') is not None else np.nan,
        '5 Year Return': f"{info.get('fiveYearAverageReturn', np.nan) * 100:.2f}%" if info.get('fiveYearAverageReturn') is not None else np.nan,
        'Total Assets': format_assets(info.get('totalAssets', np.nan)),
        'Dividend Yield': f"{info.get('yield', np.nan) * 100:.2f}%" if info.get('yield') is not None else np.nan,
        'Average Volume': info.get('averageVolume', np.nan),
        'Options Detail': "; ".join([f"Exp: {opt['Expiration Date']}, Puts: {opt['Puts Count']}, Calls: {opt['Calls Count']}" for opt in options_info]),
    }

def app():
    """ Streamlit app entry point for displaying ETF analysis. """
    st.title("ETF Analysis")
    refresh_button = st.button("Refresh Data")

    if refresh_button:
        st.experimental_rerun()

    file_path = "etfs.txt"
    try:
        with open(file_path, 'r') as file:
            symbols = [line.strip().upper() for line in file.readlines()]
            data = [fetch_data(symbol) for symbol in symbols]
            df = pd.DataFrame(data)
            #st.table(df)
            st.dataframe(df)
    except FileNotFoundError:
        st.error("ETF symbols file not found. Please ensure 'etfs.txt' is available in your directory.")

if __name__ == "__main__":
    app()
