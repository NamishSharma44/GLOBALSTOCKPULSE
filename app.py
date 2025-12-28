import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from streamlit_option_menu import option_menu

# Import custom modules
from utils.data_fetcher import DataFetcher
from utils.technical_analysis import TechnicalAnalyzer
from utils.ai_advisor import AIAdvisor
from utils.styling import apply_custom_css
from components.charts import ChartRenderer
from components.news import NewsRenderer
from components.fundamental import FundamentalAnalyzer
from components.comparison import StockComparison
from utils.currency_helper import CurrencyHelper

from dotenv import load_dotenv
load_dotenv()  # Add this line if missing
# Page configuration
st.set_page_config(
    page_title="Global Stock Market Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
apply_custom_css()

# Initialize components
@st.cache_resource
def init_components():
    components = {
        'data_fetcher': DataFetcher(),
        'technical_analyzer': TechnicalAnalyzer(),
        'ai_advisor': AIAdvisor(),
        'chart_renderer': ChartRenderer(),
        'news_renderer': NewsRenderer(),
        'fundamental_analyzer': FundamentalAnalyzer()
    }
    
    # Add comparison component
    components['comparison'] = StockComparison(
        components['data_fetcher'],
        components['technical_analyzer'],
        components['ai_advisor']
    )
    
    return components

components = init_components()

# Sidebar configuration
with st.sidebar:
    st.markdown("# 🌍 Global Stock Analyzer")
    
    # Market selection
    market_options = {
        "🇺🇸 United States": "US",
        "🇮🇳 India": "IN",
        "🇨🇳 China": "CN",
        "🇪🇺 Europe": "EU",
        "🇭🇰 Hong Kong": "HK",
        "🇯🇵 Japan": "JP",
        "🇨🇦 Canada": "CA",
        "🇦🇺 Australia": "AU"
    }
    
    selected_market = st.selectbox(
        "Select Market",
        options=list(market_options.keys()),
        index=0
    )
    
    market_code = market_options[selected_market]
    
    # Stock symbol input
    symbol = st.text_input(
        "Stock Symbol",
        value="AAPL" if market_code == "US" else "RELIANCE" if market_code == "IN" else "TSLA",
        help="Enter stock symbol without market suffix"
    ).upper()
    

     # Show currency info
    currency_info = CurrencyHelper.get_currency_name(market_code)
    currency_symbol = CurrencyHelper.get_currency_symbol(market_code)
    st.caption(f"💱 Currency: {currency_symbol} {currency_info}")

    # Time period selection
    time_periods = {
        "1 Month": 30,
        "3 Months": 90,
        "6 Months": 180,
        "1 Year": 365,
        "2 Years": 730
    }
    
    selected_period = st.selectbox(
        "Time Period",
        options=list(time_periods.keys()),
        index=2
    )
    
    days = time_periods[selected_period]
    
    # Analysis button
    analyze_button = st.button("🔍 Analyze Stock", type="primary", use_container_width=True)

# Main content
if analyze_button or 'current_analysis' in st.session_state:
    if analyze_button:
        # Fetch data
        with st.spinner(f"Fetching data for {symbol} from {selected_market}..."):
            stock_data = components['data_fetcher'].get_stock_data(symbol, market_code, days)
            
            if stock_data.empty:
                st.error(f"❌ No data found for {symbol} in {selected_market} market")
                st.stop()
            
            # Store in session state
            st.session_state.current_analysis = {
                'symbol': symbol,
                'market': market_code,
                'data': stock_data,
                'days': days
            }
    
    # Get current analysis from session state
    analysis = st.session_state.current_analysis
    symbol = analysis['symbol']
    market_code = analysis['market']
    stock_data = analysis['data']
    days = analysis['days']
    
    # Main navigation
    selected_tab = option_menu(
    menu_title=None,
    options=["📊 Overview", "📈 Technical Analysis", "🏢 Fundamental Analysis", "📊 Performance Metrics", "📰 News & Sentiment", "🤖 AI Advisor", "⚖️ Compare Stocks"],
    icons=["graph-up", "bar-chart", "building", "speedometer", "newspaper", "robot", "arrows-angle-contract"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#00d4aa", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#262730",
                "background-color": "transparent",
                "color": "#fafafa"
            },
            "nav-link-selected": {"background-color": "#00d4aa", "color": "#0e1117"},
        }
    )
    
    # Overview Tab
    # Overview Tab
    if selected_tab == "📊 Overview":
        st.markdown(f"## 📊 {symbol} - {selected_market} Market Overview")
        
        # Get currency for this market
        currency_symbol = CurrencyHelper.get_currency_symbol(market_code)
        currency_code = CurrencyHelper.get_currency_code(market_code)
        
        # Key metrics
        latest_price = stock_data['close'].iloc[-1]
        prev_price = stock_data['close'].iloc[-2] if len(stock_data) > 1 else latest_price
        price_change = latest_price - prev_price
        price_change_pct = (price_change / prev_price) * 100 if prev_price != 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label=f"Current Price ({currency_code})",
                value=CurrencyHelper.format_price(latest_price, market_code),
                delta=f"{CurrencyHelper.format_price(price_change, market_code, 2)} ({price_change_pct:+.2f}%)"
            )
        
        with col2:
            st.metric(
                label="Volume",
                value=f"{stock_data['volume'].iloc[-1]:,.0f}"
            )
        
        with col3:
            high_52w = stock_data['high'].max()
            st.metric(
                label="52W High",
                value=CurrencyHelper.format_price(high_52w, market_code)
            )
        
        with col4:
            low_52w = stock_data['low'].min()
            st.metric(
                label="52W Low",
                value=CurrencyHelper.format_price(low_52w, market_code)
            )
        # Price chart
        st.markdown("### 📈 Price Chart")
        price_chart = components['chart_renderer'].create_price_chart(stock_data, symbol)
        st.plotly_chart(price_chart, use_container_width=True)
        
        # Volume chart
        st.markdown("### 📊 Volume Analysis")
        volume_chart = components['chart_renderer'].create_volume_chart(stock_data, symbol)
        st.plotly_chart(volume_chart, use_container_width=True)
    
    # Technical Analysis Tab
    elif selected_tab == "📈 Technical Analysis":
        st.markdown(f"## 📈 Technical Analysis - {symbol}")
        
        # Calculate technical indicators
        with st.spinner("Calculating technical indicators..."):
            technical_data = components['technical_analyzer'].calculate_all_indicators(stock_data)
        
        # Technical indicators selection
        col1, col2 = st.columns(2)
        
        with col1:
            show_ma = st.checkbox("Moving Averages", value=True)
            show_bollinger = st.checkbox("Bollinger Bands", value=True)
            show_rsi = st.checkbox("RSI", value=True)
        
        with col2:
            show_macd = st.checkbox("MACD", value=True)
            show_stoch = st.checkbox("Stochastic", value=False)
            show_williams = st.checkbox("Williams %R", value=False)
        
        # Main technical chart
        tech_chart = components['chart_renderer'].create_technical_chart(
            technical_data, symbol, show_ma, show_bollinger, show_rsi, show_macd, show_stoch, show_williams
        )
        st.plotly_chart(tech_chart, use_container_width=True)
        
        # Technical summary
        st.markdown("### 📋 Technical Summary")
        tech_summary = components['technical_analyzer'].get_technical_summary(technical_data)
        
        # Key indicators overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("**RSI Analysis**")
            rsi_current = tech_summary.get('rsi_current', 50)
            if rsi_current > 70:
                st.error(f"Overbought: {rsi_current:.2f}")
            elif rsi_current < 30:
                st.success(f"Oversold: {rsi_current:.2f}")
            else:
                st.info(f"Neutral: {rsi_current:.2f}")
        
        with col2:
            st.markdown("**MACD Signal**")
            macd_signal = tech_summary.get('macd_signal', 'Neutral')
            if macd_signal == "Bullish":
                st.success("🟢 Bullish")
            elif macd_signal == "Bearish":
                st.error("🔴 Bearish")
            else:
                st.info("🟡 Neutral")
        
        with col3:
            st.markdown("**Trend Signal**")
            trend_signal = tech_summary.get('trend_signal', 'Neutral')
            if 'Uptrend' in trend_signal:
                st.success(f"📈 {trend_signal}")
            elif 'Downtrend' in trend_signal:
                st.error(f"📉 {trend_signal}")
            else:
                st.info(f"↔️ {trend_signal}")
        
        with col4:
            st.markdown("**Volume Analysis**")
            volume_signal = tech_summary.get('volume_signal', 'Normal Volume')
            if 'High' in volume_signal:
                st.success(f"🔊 {volume_signal}")
            elif 'Low' in volume_signal:
                st.warning(f"🔉 {volume_signal}")
            else:
                st.info(f"🔈 {volume_signal}")
        
        # Detailed technical analysis
        st.markdown("### 📊 Detailed Analysis")
        
        # Create detailed summary text
        detailed_summary = f"""
        **Current Market Position:**
        - **Price Trend:** {tech_summary.get('trend_signal', 'Unknown')}
        - **Momentum:** {tech_summary.get('momentum_signal', 'Unknown')}
        - **Volume Activity:** {tech_summary.get('volume_signal', 'Unknown')}
        - **Bollinger Band Position:** {tech_summary.get('bollinger_position', 'Unknown')}
        
        **Key Technical Levels:**
        """
        
        # Add support and resistance levels if available
        if not technical_data.empty and 'support' in technical_data.columns:
            latest_support = technical_data['support'].iloc[-1]
            latest_resistance = technical_data['resistance'].iloc[-1]
            current_price = technical_data['close'].iloc[-1]
            
            detailed_summary += f"""
        - **Current Price:** ${current_price:.2f}
        - **Support Level:** ${latest_support:.2f}
        - **Resistance Level:** ${latest_resistance:.2f}
        - **Distance to Support:** {((current_price - latest_support) / current_price * 100):.2f}%
        - **Distance to Resistance:** {((latest_resistance - current_price) / current_price * 100):.2f}%
            """
        
        # Add trading signals
        detailed_summary += f"""
        
        **Trading Signals:**
        - **RSI Signal:** {'Overbought (Consider Selling)' if rsi_current > 70 else 'Oversold (Consider Buying)' if rsi_current < 30 else 'Neutral'}
        - **MACD Signal:** {macd_signal}
        - **Overall Recommendation:** {tech_summary.get('overall_signal', 'Hold - Wait for clearer signals')}
        """
        
        st.markdown(detailed_summary)
        
        # Technical indicator values table
        if not technical_data.empty:
            st.markdown("### 📈 Current Indicator Values")
            latest_data = technical_data.iloc[-1]
            
            indicator_data = {
                'Indicator': ['RSI (14)', 'MACD', 'MACD Signal', 'Bollinger Upper', 'Bollinger Lower', 'Williams %R', 'ADX'],
                'Value': [
                    f"{latest_data.get('rsi', 0):.2f}",
                    f"{latest_data.get('macd', 0):.4f}",
                    f"{latest_data.get('macd_signal', 0):.4f}",
                    f"${latest_data.get('bb_upper', 0):.2f}",
                    f"${latest_data.get('bb_lower', 0):.2f}",
                    f"{latest_data.get('williams_r', 0):.2f}",
                    f"{latest_data.get('adx', 0):.2f}"
                ],
                'Signal': [
                    'Overbought' if latest_data.get('rsi', 50) > 70 else 'Oversold' if latest_data.get('rsi', 50) < 30 else 'Neutral',
                    'Bullish' if latest_data.get('macd', 0) > latest_data.get('macd_signal', 0) else 'Bearish',
                    'Rising' if latest_data.get('macd_signal', 0) > 0 else 'Falling',
                    'Resistance' if latest_data.get('close', 0) < latest_data.get('bb_upper', 0) else 'Breakout',
                    'Support' if latest_data.get('close', 0) > latest_data.get('bb_lower', 0) else 'Breakdown',
                    'Overbought' if latest_data.get('williams_r', -50) > -20 else 'Oversold' if latest_data.get('williams_r', -50) < -80 else 'Neutral',
                    'Strong Trend' if latest_data.get('adx', 0) > 25 else 'Weak Trend'
                ]
            }
            
            df_indicators = pd.DataFrame(indicator_data)
            st.table(df_indicators)
    
    # Fundamental Analysis Tab
    elif selected_tab == "🏢 Fundamental Analysis":
        st.markdown(f"## 🏢 Fundamental Analysis - {symbol}")
        
        with st.spinner("Fetching fundamental data..."):
            fundamental_data = components['fundamental_analyzer'].get_fundamental_data(symbol, market_code)
        
        if fundamental_data:
            components['fundamental_analyzer'].render_fundamental_analysis(fundamental_data, market_code)
        else:
            st.warning("❌ Fundamental data not available for this stock")
    
    # Performance Metrics Tab
    elif selected_tab == "📊 Performance Metrics":
        st.markdown(f"## 📊 Performance Metrics - {symbol}")
        
        with st.spinner("Calculating performance metrics..."):
            # Calculate returns
            stock_data['daily_returns'] = stock_data['close'].pct_change()
            
            # Performance calculations
            total_return = ((stock_data['close'].iloc[-1] / stock_data['close'].iloc[0]) - 1) * 100
            volatility = stock_data['daily_returns'].std() * (252 ** 0.5) * 100  # Annualized
            sharpe_ratio = (stock_data['daily_returns'].mean() / stock_data['daily_returns'].std()) * (252 ** 0.5) if stock_data['daily_returns'].std() != 0 else 0
            
            # Max drawdown calculation
            rolling_max = stock_data['close'].expanding().max()
            drawdown = (stock_data['close'] - rolling_max) / rolling_max
            max_drawdown = drawdown.min() * 100
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Return", f"{total_return:.2f}%")
            with col2:
                st.metric("Volatility (Annual)", f"{volatility:.2f}%")
            with col3:
                st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
            with col4:
                st.metric("Max Drawdown", f"{max_drawdown:.2f}%")
            
            # Performance chart
            st.markdown("### 📈 Cumulative Returns")
            cumulative_returns = (1 + stock_data['daily_returns']).cumprod()
            
            performance_fig = go.Figure()
            performance_fig.add_trace(go.Scatter(
                x=stock_data.index,
                y=cumulative_returns,
                mode='lines',
                name='Cumulative Returns',
                line=dict(color='#00d4aa', width=2)
            ))
            
            performance_fig.update_layout(
                title=f"{symbol} - Cumulative Returns",
                xaxis_title="Date",
                yaxis_title="Cumulative Return",
                template="plotly_dark",
                hovermode='x unified'
            )
            
            st.plotly_chart(performance_fig, use_container_width=True)
            
            # Risk-Return Analysis
            st.markdown("### ⚖️ Risk-Return Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Return Metrics:**")
                st.write(f"• Daily Average Return: {stock_data['daily_returns'].mean()*100:.4f}%")
                st.write(f"• Best Day: {stock_data['daily_returns'].max()*100:.2f}%")
                st.write(f"• Worst Day: {stock_data['daily_returns'].min()*100:.2f}%")
                st.write(f"• Positive Days: {(stock_data['daily_returns'] > 0).sum()}/{len(stock_data['daily_returns'])}")
            
            with col2:
                st.markdown("**Risk Metrics:**")
                st.write(f"• Daily Volatility: {stock_data['daily_returns'].std()*100:.4f}%")
                st.write(f"• VaR (95%): {stock_data['daily_returns'].quantile(0.05)*100:.2f}%")
                st.write(f"• Skewness: {stock_data['daily_returns'].skew():.4f}")
                st.write(f"• Kurtosis: {stock_data['daily_returns'].kurtosis():.4f}")
    
    # News & Sentiment Tab
    elif selected_tab == "📰 News & Sentiment":
        st.markdown(f"## 📰 News & Sentiment Analysis - {symbol}")
        
        with st.spinner("Fetching latest news and analyzing sentiment..."):
            news_data = components['news_renderer'].get_news_data(symbol, market_code)
        
        # Always render news analysis - the renderer will handle empty data gracefully
        components['news_renderer'].render_news_analysis(news_data, symbol)
    
    # AI Advisor Tab
    elif selected_tab == "🤖 AI Advisor":
        st.markdown(f"## 🤖 AI Investment Advisor - {symbol}")
        
        # Cache key for AI analysis
        analysis_cache_key = f"ai_analysis_{symbol}_{market_code}_{days}"
        
        # Check if we have cached analysis
        if analysis_cache_key not in st.session_state:
            with st.spinner("Generating AI analysis..."):
                # Get technical data for AI analysis
                technical_data = components['technical_analyzer'].calculate_all_indicators(stock_data)
                tech_summary = components['technical_analyzer'].get_technical_summary(technical_data)
                
                # Get news sentiment
                news_data = components['news_renderer'].get_news_data(symbol, market_code)
                news_sentiment = "neutral"
                if news_data:
                    avg_sentiment = sum(article.get('sentiment_score', 0) for article in news_data) / len(news_data)
                    if avg_sentiment > 0.1:
                        news_sentiment = "positive"
                    elif avg_sentiment < -0.1:
                        news_sentiment = "negative"
                
                # Generate AI analysis
                ai_analysis = components['ai_advisor'].generate_analysis(
                    symbol, stock_data, tech_summary, news_sentiment, market_code
                )
                
                # Cache the analysis
                st.session_state[analysis_cache_key] = {
                    'analysis': ai_analysis,
                    'tech_summary': tech_summary
                }
        else:
            # Use cached analysis
            ai_analysis = st.session_state[analysis_cache_key]['analysis']
            tech_summary = st.session_state[analysis_cache_key]['tech_summary']
        
        # Add refresh button
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("🔄 Refresh", key="refresh_ai_analysis"):
                if analysis_cache_key in st.session_state:
                    del st.session_state[analysis_cache_key]
                st.rerun()
        
        if ai_analysis:
            components['ai_advisor'].render_analysis(ai_analysis, symbol, stock_data, tech_summary, market_code)
        else:
            st.error("❌ Unable to generate AI analysis at this time")
            
            # Still show chatbot even if main analysis fails
            st.markdown("---")
            st.markdown("### 🤖 Ask the AI Advisor")
            st.markdown("Ask any questions about this stock or general investment topics.")
            
            if f"chat_history_{symbol}" not in st.session_state:
                st.session_state[f"chat_history_{symbol}"] = []
            
            # Use a form to prevent page reloads
            with st.form(key=f"fallback_chat_form_{symbol}", clear_on_submit=True):
                user_question = st.text_input(
                    "Your question:", 
                    placeholder=f"e.g., What factors might affect {symbol}'s price?",
                    key=f"fallback_chat_input_{symbol}"
                )
                ask_button = st.form_submit_button("Ask")
            
            if ask_button and user_question.strip():
                with st.spinner("AI is thinking..."):
                    tech_summary = components['technical_analyzer'].get_technical_summary(
                        components['technical_analyzer'].calculate_all_indicators(stock_data)
                    )
                    response = components['ai_advisor'].generate_chat_response(user_question, symbol, stock_data, tech_summary)
                    st.session_state[f"chat_history_{symbol}"].append({
                        "question": user_question,
                        "answer": response,
                        "timestamp": datetime.now().strftime("%H:%M")
                    })
            
            # Display chat history
            if st.session_state[f"chat_history_{symbol}"]:
                st.markdown("### 💬 Chat History")
                for i, chat in enumerate(reversed(st.session_state[f"chat_history_{symbol}"][-5:])):
                    with st.expander(f"Q: {chat['question'][:50]}{'...' if len(chat['question']) > 50 else ''} ({chat['timestamp']})", expanded=(i==0)):
                        st.markdown(f"**Question:** {chat['question']}")
                        st.markdown(f"**Answer:** {chat['answer']}")
                    

    # Compare Stocks Tab
    # Compare Stocks Tab
    # Compare Stocks Tab
    elif selected_tab == "⚖️ Compare Stocks":
        st.markdown("## ⚖️ Compare Stocks")
        
        st.markdown("""
        Compare 2-3 stocks side-by-side to identify the best investment opportunity.
        The AI will analyze returns, risk, technical indicators, and provide a recommendation.
        """)
        
        # Comparison inputs
        col1, col2 = st.columns(2)
        
        with col1:
            num_stocks = st.radio("Number of stocks to compare:", [2, 3], horizontal=True)
        
        with col2:
            comp_period = st.selectbox(
                "Comparison Period:",
                options=list(time_periods.keys()),
                index=2,
                key="comp_period"
            )
        
        comp_days = time_periods[comp_period]
        
        # Quick presets
        st.markdown("### 🚀 Quick Comparison Presets")
        
        preset_options = {
            "Custom Selection": None,
            "🏦 Tech Giants (AAPL vs MSFT vs GOOGL)": {
                'symbols': ['AAPL', 'MSFT', 'GOOGL'],
                'markets': ['US', 'US', 'US']
            },
            "🏦 Indian Banks (HDFC vs ICICI vs SBI)": {
                'symbols': ['HDFCBANK', 'ICICIBANK', 'SBIN'],
                'markets': ['IN', 'IN', 'IN']
            },
            "💻 Indian IT (TCS vs Infosys vs Wipro)": {
                'symbols': ['TCS', 'INFY', 'WIPRO'],
                'markets': ['IN', 'IN', 'IN']
            },
            "🚗 EV Leaders (Tesla vs Rivian)": {
                'symbols': ['TSLA', 'RIVN'],
                'markets': ['US', 'US']
            },
            "📱 Social Media (META vs SNAP)": {
                'symbols': ['META', 'SNAP'],
                'markets': ['US', 'US']
            },
            "🛒 E-Commerce (AMZN vs BABA)": {
                'symbols': ['AMZN', 'BABA'],
                'markets': ['US', 'US']
            }
        }
        
        selected_preset = st.selectbox(
            "Choose a preset or select Custom:",
            options=list(preset_options.keys()),
            index=0
        )
        
        # Stock inputs
        st.markdown("### 📊 Stock Selection")
        
        if selected_preset == "Custom Selection":
            # Manual entry
            compare_cols = st.columns(num_stocks)
            compare_symbols = []
            compare_markets = []
            
            for i, col in enumerate(compare_cols):
                with col:
                    st.markdown(f"**Stock {i+1}**")
                    
                    comp_market = st.selectbox(
                        "Market",
                        options=list(market_options.keys()),
                        index=0,  # Default to US
                        key=f"comp_market_{i}"
                    )
                    
                    selected_market_code = market_options[comp_market]
                    
                    default_symbols = ["AAPL", "MSFT", "GOOGL"]
                    
                    comp_symbol = st.text_input(
                        "Symbol",
                        value=default_symbols[i] if i < len(default_symbols) else "AAPL",
                        key=f"comp_symbol_{i}"
                    ).upper()
                    
                    compare_symbols.append(comp_symbol)
                    compare_markets.append(selected_market_code)
            
            st.info("💡 **Important:** Ensure each stock is paired with its correct market:\n- US stocks (AAPL, MSFT, GOOGL, etc.) → 🇺🇸 United States\n- Indian stocks (RELIANCE, TCS, etc.) → 🇮🇳 India")
        
        else:
            # Use preset
            preset_data = preset_options[selected_preset]
            compare_symbols = preset_data['symbols'][:num_stocks]
            compare_markets = preset_data['markets'][:num_stocks]
            
            # Pad if needed
            while len(compare_symbols) < num_stocks:
                compare_symbols.append('AAPL')
                compare_markets.append('US')
            
            # Display selected stocks
            st.success(f"✅ Selected: {' vs '.join(compare_symbols)}")
            
            # Show markets
            market_display = " | ".join([f"{sym} ({mkts})" for sym, mkts in zip(compare_symbols, compare_markets)])
            st.caption(f"Markets: {market_display}")
        
        compare_button = st.button("🔍 Compare Stocks", type="primary", use_container_width=True)
        
        if compare_button:
            # Validate inputs
            if len(set(compare_symbols)) != len(compare_symbols):
                st.error("❌ Please select different stocks for comparison")
            elif any(not s.strip() for s in compare_symbols):
                st.error("❌ Please enter valid stock symbols")
            else:
                with st.spinner(f"Analyzing {', '.join(compare_symbols)}..."):
                    # Fetch comparison data
                    comparison_data = components['comparison'].fetch_comparison_data(
                        compare_symbols, compare_markets, comp_days
                    )
                    
                    if len(comparison_data) < 2:
                        st.error("❌ Could not fetch data for at least 2 stocks.")
                        st.markdown("**Troubleshooting:**")
                        st.markdown("1. Verify stock symbols are correct")
                        st.markdown("2. Check that markets match the stocks")
                        st.markdown("3. Try using one of the Quick Presets above")
                        
                        # Show which stocks failed
                        st.markdown("**Fetch Results:**")
                        for sym, mkt in zip(compare_symbols, compare_markets):
                            if sym in comparison_data:
                                st.success(f"✅ {sym} ({mkt}) - Success")
                            else:
                                st.error(f"❌ {sym} ({mkt}) - Failed")
                    else:
                        st.success(f"✅ Successfully fetched data for {len(comparison_data)} stocks")
                        
                        # Generate AI comparison
                        comparison_analysis = components['comparison'].generate_comparison_analysis(
                            list(comparison_data.keys()), comparison_data
                        )
                        
                        # Render comparison
                        components['comparison'].render_comparison(
                            list(comparison_data.keys()), comparison_data, comparison_analysis
                        )
                    
    

else:
    # Welcome screen
    st.markdown("""
    # 🌍 Welcome to Global Stock Market Analyzer
    
    ## Features:
    - **📊 Multi-Market Support**: Analyze stocks from 8 global markets
    - **📈 Technical Analysis**: Comprehensive technical indicators and charts
    - **🏢 Fundamental Analysis**: Company financials and valuation metrics
    - **📊 Performance Metrics**: Risk-return analysis and portfolio metrics
    - **📰 News & Sentiment**: Real-time news aggregation with sentiment analysis
    - **🤖 AI Advisor**: AI-powered investment insights and recommendations
    
    ## Supported Markets:
    - 🇺🇸 United States (NASDAQ, NYSE)
    - 🇮🇳 India (NSE, BSE)
    - 🇨🇳 China (SSE, SZSE)
    - 🇪🇺 Europe (Multiple exchanges)
    - 🇭🇰 Hong Kong (HKEX)
    - 🇯🇵 Japan (TSE)
    - 🇨🇦 Canada (TSX)
    - 🇦🇺 Australia (ASX)
    
    Select a market and enter a stock symbol to get started!
    """)
