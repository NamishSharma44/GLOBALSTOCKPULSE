# 🌐 Global Stock Market Analyzer

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.46+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)


**A comprehensive AI-powered financial analysis platform supporting 8 global markets with real-time data, technical analysis, and intelligent investment recommendations.**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-tech-stack) • [Contributing](#-contributing)

</div>

---

## 🎯 Overview

**Global Stock Market Analyzer** is an advanced, AI-enhanced financial analysis platform built with Python and Streamlit. It provides comprehensive stock market analysis across 8 major global markets, combining real-time data visualization, technical indicators, fundamental analysis, news sentiment tracking, and AI-powered investment recommendations.

### Why This Tool?

- 🌍 **Multi-Market Support**: Analyze stocks from US, India, China, Europe, Hong Kong, Japan, Canada, and Australia
- 🤖 **AI-Powered Insights**: Leverage Google's Gemini AI for intelligent investment recommendations
- 📊 **Comprehensive Analysis**: Technical indicators, fundamental metrics, news sentiment, and performance analytics
- 💱 **Multi-Currency**: Automatic currency conversion (USD, INR, CNY, EUR, HKD, JPY, CAD, AUD)
- 🎨 **Modern UI**: Beautiful dark-themed interface with interactive charts
- 🚀 **Production Ready**: Robust fallback mechanisms ensure 100% uptime

---

## ✨ Features

### 📈 Technical Analysis
- **20+ Technical Indicators**: RSI, MACD, Bollinger Bands, Stochastic Oscillator, Williams %R, ADX
- **Moving Averages**: SMA (20, 50) and EMA (12, 26)
- **Support & Resistance**: Automated level detection
- **Interactive Charts**: Candlestick patterns with Plotly visualization
- **Custom Timeframes**: 1 month to 2 years analysis periods

### 🏢 Fundamental Analysis
- **Financial Metrics**: P/E, P/B, P/S ratios, EV/EBITDA, PEG ratio
- **Company Information**: Sector, industry, market cap, employee count
- **Profitability Metrics**: Revenue, gross profit, operating margins, ROA, ROE
- **Financial Health**: Debt-to-equity, current ratio, beta
- **Dividend Information**: Dividend rate and yield
- **Analyst Recommendations**: Target prices and consensus ratings

### 📰 News & Sentiment Analysis
- **Multi-Source Aggregation**: NewsAPI, MarketAux, Alpha Vantage, Finnhub, Yahoo Finance
- **Global RSS Feeds**: CNBC, Bloomberg, Reuters, regional financial news
- **Sentiment Analysis**: TextBlob-powered sentiment scoring
- **Smart Conclusions**: AI-generated market sentiment summaries
- **Key Themes Detection**: Automatic identification of earnings, growth, market trends
- **Trading Implications**: Actionable insights based on news sentiment

### 🤖 AI Investment Advisor
- **Intelligent Recommendations**: Buy/Sell/Hold signals with confidence levels
- **Risk Assessment**: Multi-factor risk analysis (Low/Medium/High)
- **Price Targets**: AI-calculated target prices with timeframes
- **Entry/Exit Strategies**: Specific price levels and timing recommendations
- **Interactive Chatbot**: Ask questions about stocks and get AI-powered answers
- **Fallback Analysis**: Sophisticated rule-based system when AI unavailable

### ⚖️ Stock Comparison
- **Side-by-Side Analysis**: Compare 2-3 stocks simultaneously
- **Comprehensive Metrics**: Returns, volatility, Sharpe ratio, technical indicators
- **AI Rankings**: Intelligent scoring and ranking system
- **Visual Comparisons**: Risk-return scatter plots, performance charts
- **Investment Recommendations**: Clear winner identification with reasoning

### 📊 Performance Metrics
- **Return Analysis**: Total return, annualized return, daily/monthly returns
- **Risk Metrics**: Volatility, Sharpe ratio, max drawdown, downside volatility
- **Statistical Analysis**: VaR, skewness, kurtosis
- **Price Positioning**: 52-week high/low analysis
- **Volume Analysis**: Average volume, volume ratios

---

## 🎥 Demo

### Main Dashboard
![Dashboard](https://via.placeholder.com/800x400?text=Dashboard+Screenshot)

### Technical Analysis
![Technical Analysis](https://via.placeholder.com/800x400?text=Technical+Analysis+Screenshot)

### AI Advisor
![AI Advisor](https://via.placeholder.com/800x400?text=AI+Advisor+Screenshot)

### Stock Comparison
![Comparison](https://via.placeholder.com/800x400?text=Stock+Comparison+Screenshot)

---

## 🛠 Tech Stack

### Core Technologies
- **Python 3.11+**: Primary programming language
- **Streamlit 1.46+**: Web application framework
- **Pandas 2.3+**: Data manipulation and analysis
- **NumPy**: Numerical computations

### Data & APIs
- **yFinance 0.2.64**: Yahoo Finance data retrieval
- **Google Gemini AI**: AI-powered analysis and recommendations
- **NewsAPI**: Financial news aggregation
- **MarketAux**: Alternative news source
- **Alpha Vantage**: News sentiment data
- **Finnhub**: Company news feed

### Visualization
- **Plotly 6.2+**: Interactive charts and graphs
- **Streamlit Option Menu 0.4+**: Enhanced navigation

### NLP & Analysis
- **TextBlob 0.19+**: Sentiment analysis
- **BeautifulSoup4 4.13+**: Web scraping
- **Feedparser 6.0+**: RSS feed parsing
- **Trafilatura 2.0+**: Content extraction

### Development
- **python-dotenv 1.1+**: Environment variable management
- **requests 2.32+**: HTTP requests

---

## 🏗 Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                       │
│  ┌──────────┬──────────┬──────────┬──────────┬────────────┐ │
│  │Overview  │Technical │Fundamental│Performance│News/AI    │ │
│  └──────────┴──────────┴──────────┴──────────┴────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Core Components Layer                     │
│  ┌────────────────┬─────────────────┬────────────────────┐  │
│  │ Data Fetcher   │ Tech Analyzer   │ AI Advisor         │  │
│  │ Chart Renderer │ News Renderer   │ Fund Analyzer      │  │
│  │ Comparison     │ Currency Helper │ Styling            │  │
│  └────────────────┴─────────────────┴────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Data Sources                     │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │Yahoo     │Gemini AI │NewsAPI   │MarketAux │RSS Feeds │  │
│  │Finance   │          │          │          │          │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow
1. **User Input** → Market & symbol selection
2. **Data Retrieval** → Multi-source data fetching with fallbacks
3. **Processing** → Technical indicators, sentiment analysis
4. **AI Analysis** → Gemini AI processing (with fallback)
5. **Visualization** → Interactive charts and dashboards
6. **Caching** → Intelligent caching (5min-1hr based on data type)

---



### Basic Workflow

1. **Select Market**: Choose from 8 global markets in the sidebar
2. **Enter Symbol**: Input stock ticker (e.g., AAPL, RELIANCE, TSLA)
3. **Choose Timeframe**: Select analysis period (1 month to 2 years)
4. **Analyze**: Click "Analyze Stock" button
5. **Explore Tabs**: Navigate through different analysis views

### Advanced Features

#### Stock Comparison
1. Navigate to "Compare Stocks" tab
2. Select 2-3 stocks with their markets
3. Use quick presets or custom selection
4. View comprehensive side-by-side analysis

#### AI Chat
1. Go to "AI Advisor" tab
2. Ask questions in the chat interface
3. Get intelligent, context-aware responses
4. View chat history for reference

---


## 🌍 Supported Markets

| Market | Code | Currency | Exchange | Example Stocks |
|--------|------|----------|----------|----------------|
| 🇺🇸 United States | US | USD ($) | NASDAQ, NYSE | AAPL, MSFT, GOOGL |
| 🇮🇳 India | IN | INR (₹) | NSE, BSE | RELIANCE, TCS, INFY |
| 🇨🇳 China | CN | CNY (¥) | SSE, SZSE | BABA, TCEHY |
| 🇪🇺 Europe | EU | EUR (€) | Multiple | SAP, ASML |
| 🇭🇰 Hong Kong | HK | HKD (HK$) | HKEX | 0700, 0941 |
| 🇯🇵 Japan | JP | JPY (¥) | TSE | 7203, 9984 |
| 🇨🇦 Canada | CA | CAD (C$) | TSX | SHOP, RY |
| 🇦🇺 Australia | AU | AUD (A$) | ASX | BHP, CBA |

---

## 📁 Project Structure
```
global-stock-analyzer/
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (create this)
├── .gitignore                     # Git ignore file
├── README.md                      # This file
│
├── .streamlit/
│   └── config.toml                # Streamlit configuration
│
├── utils/                         # Core utility modules
│   ├── __init__.py
│   ├── data_fetcher.py           # Stock data retrieval
│   ├── technical_analysis.py     # Technical indicators
│   ├── ai_advisor.py             # AI analysis & recommendations
│   ├── currency_helper.py        # Multi-currency support
│   └── styling.py                # Custom CSS styling
│
├── components/                    # UI components
│   ├── __init__.py
│   ├── charts.py                 # Interactive visualizations
│   ├── news.py                   # News aggregation & sentiment
│   ├── fundamental.py            # Fundamental analysis
│   └── comparison.py             # Stock comparison tool
│
└── docs/                          # Documentation (optional)
    ├── architecture.md
    ├── api_reference.md
    └── user_guide.md
```

---

## 🎨 Features Showcase

### Technical Indicators
- **RSI (14)**: Momentum oscillator (0-100 scale)
- **MACD**: Trend-following momentum indicator
- **Bollinger Bands**: Volatility indicator with upper/lower bands
- **Stochastic Oscillator**: Momentum indicator comparing closing price
- **Williams %R**: Momentum indicator showing overbought/oversold
- **ADX**: Trend strength indicator

### AI Capabilities
- **Multi-Model Support**: Automatically tries gemini-1.5-flash, gemini-1.5-flash-8b, gemini-2.0-flash-exp
- **Intelligent Fallback**: Sophisticated rule-based system when AI unavailable
- **Context-Aware**: Considers technical, fundamental, and sentiment data
- **Risk Scoring**: 12+ factor analysis for comprehensive recommendations

### News Sources
- **Global Coverage**: 15+ RSS feeds from major financial publishers
- **Market-Specific**: Tailored news for each geographic market
- **Sentiment Scoring**: -1 to +1 scale with keyword boosting
- **Deduplication**: Smart removal of similar articles
