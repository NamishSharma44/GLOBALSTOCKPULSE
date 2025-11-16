import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.currency_helper import CurrencyHelper

class FundamentalAnalyzer:
    def __init__(self):
        pass
    
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def get_fundamental_data(_self, symbol, market_code):
        """Fetch fundamental data from Yahoo Finance"""
        try:
            # Add market suffix if needed
            market_suffixes = {
                "US": "",
                "IN": ".NS",
                "CN": ".SS",
                "EU": ".PA",
                "HK": ".HK",
                "JP": ".T",
                "CA": ".TO",
                "AU": ".AX"
            }
            
            full_symbol = symbol + market_suffixes.get(market_code, "")
            ticker = yf.Ticker(full_symbol)
            
            # Get company info
            info = ticker.info
            
            if not info or 'symbol' not in info:
                return None
                
            return info
            
        except Exception as e:
            st.error(f"Error fetching fundamental data: {str(e)}")
            return None
    
    def render_fundamental_analysis(self, fundamental_data, market_code="US"):
        """Render fundamental analysis with proper currency"""
        try:
            if not fundamental_data:
                st.warning("⚠️ Fundamental data not available")
                return
            
            currency_symbol = CurrencyHelper.get_currency_symbol(market_code)
            currency_code = CurrencyHelper.get_currency_code(market_code)
            
            # Company Overview
            st.markdown("### 🏢 Company Overview")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Company Name:** {fundamental_data.get('longName', 'N/A')}")
                st.markdown(f"**Sector:** {fundamental_data.get('sector', 'N/A')}")
                st.markdown(f"**Industry:** {fundamental_data.get('industry', 'N/A')}")
                st.markdown(f"**Country:** {fundamental_data.get('country', 'N/A')}")
                st.markdown(f"**Exchange:** {fundamental_data.get('exchange', 'N/A')}")
            
            with col2:
                market_cap = fundamental_data.get('marketCap', 0)
                if market_cap:
                    if market_cap >= 1e12:
                        market_cap_display = f"{currency_symbol}{market_cap/1e12:.2f}T"
                    elif market_cap >= 1e9:
                        market_cap_display = f"{currency_symbol}{market_cap/1e9:.2f}B"
                    elif market_cap >= 1e6:
                        market_cap_display = f"{currency_symbol}{market_cap/1e6:.2f}M"
                    else:
                        market_cap_display = f"{currency_symbol}{market_cap:,.0f}"
                else:
                    market_cap_display = "N/A"
                
                st.markdown(f"**Market Cap:** {market_cap_display}")
                st.markdown(f"**Employees:** {fundamental_data.get('fullTimeEmployees', 'N/A'):,}" if fundamental_data.get('fullTimeEmployees') else "**Employees:** N/A")
                st.markdown(f"**Website:** [{fundamental_data.get('website', 'N/A')}]({fundamental_data.get('website', '#')})" if fundamental_data.get('website') else "**Website:** N/A")
                st.markdown(f"**Currency:** {currency_code}")
            
            # ... rest of the code, update all price displays with currency_symbol
            
            # Key Financial Metrics section
            st.markdown("### 💰 Key Financial Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                current_price = fundamental_data.get('currentPrice', fundamental_data.get('regularMarketPrice', 0))
                st.metric("Current Price", CurrencyHelper.format_price(current_price, market_code) if current_price else "N/A")
                
                previous_close = fundamental_data.get('previousClose', 0)
                if previous_close and current_price:
                    change = current_price - previous_close
                    change_pct = (change / previous_close) * 100
                    st.metric("Previous Close", 
                            CurrencyHelper.format_price(previous_close, market_code), 
                            f"{CurrencyHelper.format_price(change, market_code, 2)} ({change_pct:+.2f}%)")
            
            with col2:
                day_high = fundamental_data.get('dayHigh', 0)
                day_low = fundamental_data.get('dayLow', 0)
                st.metric("Day High", CurrencyHelper.format_price(day_high, market_code) if day_high else "N/A")
                st.metric("Day Low", CurrencyHelper.format_price(day_low, market_code) if day_low else "N/A")
            
            with col3:
                week_52_high = fundamental_data.get('fiftyTwoWeekHigh', 0)
                week_52_low = fundamental_data.get('fiftyTwoWeekLow', 0)
                st.metric("52W High", CurrencyHelper.format_price(week_52_high, market_code) if week_52_high else "N/A")
                st.metric("52W Low", CurrencyHelper.format_price(week_52_low, market_code) if week_52_low else "N/A")
            
            with col4:
                volume = fundamental_data.get('volume', 0)
                avg_volume = fundamental_data.get('averageVolume', 0)
                st.metric("Volume", f"{volume:,}" if volume else "N/A")
                st.metric("Avg Volume", f"{avg_volume:,}" if avg_volume else "N/A")
            
            # Valuation Metrics
            st.markdown("### 📊 Valuation Metrics")
            
            valuation_data = {}
            
            # P/E Ratio
            pe_ratio = fundamental_data.get('trailingPE', fundamental_data.get('forwardPE'))
            valuation_data['P/E Ratio'] = f"{pe_ratio:.2f}" if pe_ratio else "N/A"
            
            # P/B Ratio
            pb_ratio = fundamental_data.get('priceToBook')
            valuation_data['P/B Ratio'] = f"{pb_ratio:.2f}" if pb_ratio else "N/A"
            
            # P/S Ratio
            ps_ratio = fundamental_data.get('priceToSalesTrailing12Months')
            valuation_data['P/S Ratio'] = f"{ps_ratio:.2f}" if ps_ratio else "N/A"
            
            # EV/EBITDA
            ev_ebitda = fundamental_data.get('enterpriseToEbitda')
            valuation_data['EV/EBITDA'] = f"{ev_ebitda:.2f}" if ev_ebitda else "N/A"
            
            # PEG Ratio
            peg_ratio = fundamental_data.get('pegRatio')
            valuation_data['PEG Ratio'] = f"{peg_ratio:.2f}" if peg_ratio else "N/A"
            
            # Display valuation metrics in table
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Valuation Ratios:**")
                for metric, value in list(valuation_data.items())[:3]:
                    st.markdown(f"• **{metric}:** {value}")
            
            with col2:
                st.markdown("**Additional Metrics:**")
                for metric, value in list(valuation_data.items())[3:]:
                    st.markdown(f"• **{metric}:** {value}")
            
            # Financial Performance
            st.markdown("### 📈 Financial Performance")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Profitability:**")
                
                # Revenue
                revenue = fundamental_data.get('totalRevenue')
                if revenue:
                    if revenue >= 1e9:
                        revenue_display = f"${revenue/1e9:.2f}B"
                    elif revenue >= 1e6:
                        revenue_display = f"${revenue/1e6:.2f}M"
                    else:
                        revenue_display = f"${revenue:,.0f}"
                    st.markdown(f"• **Revenue (TTM):** {revenue_display}")
                
                # Gross Profit
                gross_profit = fundamental_data.get('grossProfits')
                if gross_profit:
                    if gross_profit >= 1e9:
                        gross_profit_display = f"${gross_profit/1e9:.2f}B"
                    elif gross_profit >= 1e6:
                        gross_profit_display = f"${gross_profit/1e6:.2f}M"
                    else:
                        gross_profit_display = f"${gross_profit:,.0f}"
                    st.markdown(f"• **Gross Profit:** {gross_profit_display}")
                
                # Profit Margins
                gross_margin = fundamental_data.get('grossMargins')
                if gross_margin:
                    st.markdown(f"• **Gross Margin:** {gross_margin*100:.2f}%")
                
                operating_margin = fundamental_data.get('operatingMargins')
                if operating_margin:
                    st.markdown(f"• **Operating Margin:** {operating_margin*100:.2f}%")
                
                profit_margin = fundamental_data.get('profitMargins')
                if profit_margin:
                    st.markdown(f"• **Profit Margin:** {profit_margin*100:.2f}%")
            
            with col2:
                st.markdown("**Financial Health:**")
                
                # Debt to Equity
                debt_to_equity = fundamental_data.get('debtToEquity')
                if debt_to_equity:
                    st.markdown(f"• **Debt-to-Equity:** {debt_to_equity:.2f}")
                
                # Current Ratio
                current_ratio = fundamental_data.get('currentRatio')
                if current_ratio:
                    st.markdown(f"• **Current Ratio:** {current_ratio:.2f}")
                
                # Return on Assets
                roa = fundamental_data.get('returnOnAssets')
                if roa:
                    st.markdown(f"• **ROA:** {roa*100:.2f}%")
                
                # Return on Equity
                roe = fundamental_data.get('returnOnEquity')
                if roe:
                    st.markdown(f"• **ROE:** {roe*100:.2f}%")
                
                # Beta
                beta = fundamental_data.get('beta')
                if beta:
                    st.markdown(f"• **Beta:** {beta:.2f}")
            
            # Dividend Information
            dividend_rate = fundamental_data.get('dividendRate')
            dividend_yield = fundamental_data.get('dividendYield')
            
            if dividend_rate or dividend_yield:
                st.markdown("### 💵 Dividend Information")
                col1, col2 = st.columns(2)
                
                with col1:
                    if dividend_rate:
                        st.metric("Annual Dividend", f"${dividend_rate:.2f}")
                
                with col2:
                    if dividend_yield:
                        st.metric("Dividend Yield", f"{dividend_yield*100:.2f}%")
            
            # Analyst Recommendations
            recommendation = fundamental_data.get('recommendationKey')
            target_price = fundamental_data.get('targetMeanPrice')
            
            if recommendation or target_price:
                st.markdown("### 🎯 Analyst Recommendations")
                col1, col2 = st.columns(2)
                
                with col1:
                    if recommendation:
                        rec_color = "green" if recommendation in ["buy", "strong_buy"] else "red" if recommendation in ["sell", "strong_sell"] else "orange"
                        st.markdown(f"**Recommendation:** <span style='color: {rec_color}'>{recommendation.replace('_', ' ').title()}</span>", unsafe_allow_html=True)
                
                with col2:
                    if target_price:
                        current_price = fundamental_data.get('currentPrice', 0)
                        if current_price:
                            upside = ((target_price / current_price) - 1) * 100
                            st.metric("Target Price", f"${target_price:.2f}", f"{upside:+.1f}% upside")
                        else:
                            st.metric("Target Price", f"${target_price:.2f}")
                            
        except Exception as e:
            st.error(f"Error rendering fundamental analysis: {str(e)}")
