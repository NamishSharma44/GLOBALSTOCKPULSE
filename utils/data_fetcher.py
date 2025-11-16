import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

class DataFetcher:
    def __init__(self):
        self.market_suffixes = {
            "US": "",
            "IN": ".NS",
            "CN": ".SS",
            "EU": ".PA",
            "HK": ".HK",
            "JP": ".T",
            "CA": ".TO",
            "AU": ".AX"
        }
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_stock_data(_self, symbol, market, days):
        """Fetch stock data from Yahoo Finance"""
        try:
            # Add market suffix
            full_symbol = symbol + _self.market_suffixes.get(market, "")
            
            # Calculate start date
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Fetch data
            ticker = yf.Ticker(full_symbol)
            data = ticker.history(start=start_date, end=end_date)
            
            if data.empty:
                # Try alternative suffixes for some markets
                alternative_suffixes = {
                    "IN": [".BO", ".NS"],
                    "CN": [".SZ", ".SS"],
                    "EU": [".DE", ".PA", ".L"],
                }
                
                if market in alternative_suffixes:
                    for suffix in alternative_suffixes[market]:
                        alt_symbol = symbol + suffix
                        ticker = yf.Ticker(alt_symbol)
                        data = ticker.history(start=start_date, end=end_date)
                        if not data.empty:
                            break
            
            # Clean column names
            data.columns = [col.lower() for col in data.columns]
            
            return data
            
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            return pd.DataFrame()
    
    def get_company_info(self, symbol, market):
        """Get company information"""
        try:
            full_symbol = symbol + self.market_suffixes.get(market, "")
            ticker = yf.Ticker(full_symbol)
            info = ticker.info
            return info
        except Exception as e:
            st.error(f"Error fetching company info: {str(e)}")
            return {}
