import streamlit as st
from pages import commodities, cryptos, etfs_value, underpriced_stocks

# Dictionary of pages
pages = {
    "Commodities": commodities,
    "Cryptos": cryptos,
    "ETFs Value": etfs_value,
    "Underpriced Stocks": underpriced_stocks
}

st.sidebar.title('Navigation')
choice = st.sidebar.radio("Choose a page:", list(pages.keys()))

page = pages[choice] # type: ignore
page.app()  # Assuming each module has an app function to run its page