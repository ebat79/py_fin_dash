import streamlit as st
import yfinance as yf
import pandas as pd

# Constants for API access

@st.cache_resource(show_spinner=True)
def fetch_sp500_tickers():
    """
    Fetches the current S&P 500 constituent tickers using an API.
    """
    url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    try:
        tables = pd.read_html(url, attrs={'id':"constituents"}, converters={'CIK': str}) # type: ignore
        constituents = tables[0]
        constituents_df = pd.DataFrame(constituents)
        # Convert the date column to date format
        constituents_df["Date added"] = pd.to_datetime(constituents_df["Date added"])
        return constituents_df
    except Exception as e:
        st.error(f"Request failed: {e}")
        return []

@st.cache_data(show_spinner=True)
def fetch_stock_data(tickers):
    """
    Fetches stock data for given tickers using Yahoo Finance and calculates if the stocks are underpriced.
    """
    data = []
    for symbol in tickers:
        stock = yf.Ticker(symbol)
        try:
            info = stock.info
            if 'currentPrice' in info and 'trailingEps' in info:
                shortName = info['shortName']
                industry = info['industry']
                current_price = info['currentPrice']
                eps = info['trailingEps']
                pe_ratio = info.get('trailingPE', float('inf'))  # Use trailing P/E if available

                # Assume a target P/E ratio
                target_pe = 15
                fair_value = eps * target_pe

                underpriced = current_price < fair_value
                price_gap = ((fair_value - current_price) / current_price) * 100 if current_price else 0

                data.append({
                    'Symbol': symbol,
                    'Name': shortName,
                    'Industry': industry,
                    'Current Price': current_price,
                    'EPS': eps,
                    'P/E Ratio': pe_ratio,
                    'Fair Market Value': fair_value,
                    'Underpriced': 'Yes' if underpriced else 'No',
                    'Price Gap (%)': round(price_gap, 2)
                })
        except Exception as e:
            print(f"Failed to fetch data for {symbol}: {e}")

    return pd.DataFrame(data)

def app():
    """
    Streamlit app for displaying S&P 500 stocks and their underpriced status.
    """
    st.title("S&P 500 Stock Analysis")

    refresh_button = st.button("Refresh Data")

    if refresh_button:
        st.experimental_rerun()

    constituents = fetch_sp500_tickers()
    tickers = constituents['Symbol'].tolist() # type: ignore

    if tickers:
        st.write("Loaded tickers for S&P 500 companies.")
        df = fetch_stock_data(tickers)
        if not df.empty:
            st.dataframe(df)
        else:
            st.write("No data found for the provided tickers.")
    else:
        st.write("Unable to load stock tickers. Please check API settings and network connection.")

if __name__ == "__main__":
    app()
