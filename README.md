# 🌐 GlobalStockPulse

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://globalstockpulse.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Gemini AI](https://img.shields.io/badge/Powered%20by-Gemini%20AI-orange.svg)](https://ai.google.dev/)

**🚀 Live Demo: [https://globalstockpulse.streamlit.app/](https://globalstockpulse.streamlit.app/)**

An AI-powered comprehensive stock market analysis platform supporting **8 global markets** with real-time data, advanced technical analysis, fundamental metrics, news sentiment tracking, and intelligent investment recommendations powered by Google's Gemini AI.

---

## ✨ Features

### 📊 Multi-Market Support
Analyze stocks from 8 major global markets:
| Market | Exchange | Currency |
|--------|----------|----------|
| 🇺🇸 United States | NYSE, NASDAQ | USD ($) |
| 🇮🇳 India | NSE, BSE | INR (₹) |
| 🇨🇳 China | SSE, SZSE | CNY (¥) |
| 🇪🇺 Europe | Euronext | EUR (€) |
| 🇭🇰 Hong Kong | HKEX | HKD (HK$) |
| 🇯🇵 Japan | TSE | JPY (¥) |
| 🇨🇦 Canada | TSX | CAD (C$) |
| 🇦🇺 Australia | ASX | AUD (A$) |

### 📈 Technical Analysis
- **20+ Technical Indicators**: RSI, MACD, Bollinger Bands, Stochastic Oscillator, Williams %R, ADX
- **Moving Averages**: SMA (20, 50) and EMA (12, 26)
- **Support & Resistance**: Automated level detection
- **Interactive Charts**: Candlestick patterns with Plotly visualization
- **Custom Timeframes**: 1 month to 2 years analysis periods

### 🏢 Fundamental Analysis
- **Valuation Metrics**: P/E, P/B, P/S ratios, EV/EBITDA, PEG ratio
- **Company Profile**: Sector, industry, market cap, employee count
- **Profitability**: Revenue, gross profit, operating margins, ROA, ROE
- **Financial Health**: Debt-to-equity, current ratio, beta
- **Dividends**: Dividend rate and yield information
- **Analyst Ratings**: Target prices and consensus recommendations

### 📰 News & Sentiment Analysis
- **Multi-Source Aggregation**: Alpha Vantage, Finnhub, Yahoo Finance, Global RSS Feeds
- **Real-time Sentiment**: TextBlob-powered sentiment scoring
- **Visual Analytics**: Sentiment distribution charts
- **Key Theme Detection**: Automatic identification of market trends
- **Trading Implications**: Actionable insights based on news sentiment

### 🤖 AI Investment Advisor (Powered by Gemini)
- **Smart Recommendations**: Buy/Sell/Hold signals with confidence levels
- **Risk Assessment**: Multi-factor risk analysis (Low/Medium/High)
- **Price Targets**: AI-calculated target prices with timeframes
- **Entry/Exit Strategies**: Specific price levels and timing
- **Interactive Chatbot**: Ask questions and get AI-powered answers
- **Fallback Analysis**: Rule-based system when AI unavailable

### ⚖️ Stock Comparison
- **Side-by-Side Analysis**: Compare 2-3 stocks simultaneously
- **Comprehensive Metrics**: Returns, volatility, Sharpe ratio, technical indicators
- **AI Rankings**: Intelligent scoring and ranking system
- **Visual Comparisons**: Risk-return scatter plots, normalized performance charts
- **Quick Presets**: Pre-configured comparisons (Tech Giants, Indian Banks, etc.)

### 📊 Performance Metrics
- **Return Analysis**: Total return, annualized return, daily/monthly returns
- **Risk Metrics**: Volatility, Sharpe ratio, max drawdown, VaR
- **Statistical Analysis**: Skewness, kurtosis, win rate
- **Price Positioning**: 52-week high/low analysis

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Gemini API Key (free at [Google AI Studio](https://aistudio.google.com/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/NamishSharma44/GlobalStockPulse.git
cd GlobalStockPulse
```

2. **Create virtual environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
NEWS_API_KEY=your_news_api_key (optional)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key (optional)
FINNHUB_API_KEY=your_finnhub_key (optional)
MARKETAUX_API_KEY=your_marketaux_key (optional)
```

5. **Run the application**
```bash
streamlit run app.py
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Frontend** | Streamlit, Plotly, HTML/CSS |
| **Backend** | Python 3.11+ |
| **AI/ML** | Google Gemini AI, TextBlob |
| **Data Sources** | Yahoo Finance (yfinance), Alpha Vantage, Finnhub |
| **Analysis** | Pandas, NumPy |
| **Deployment** | Streamlit Cloud |

---

## 📁 Project Structure

```
GlobalStockPulse/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (local)
├── components/
│   ├── charts.py            # Chart rendering (Plotly)
│   ├── comparison.py        # Stock comparison module
│   ├── fundamental.py       # Fundamental analysis
│   └── news.py              # News & sentiment analysis
└── utils/
    ├── ai_advisor.py        # Gemini AI integration
    ├── currency_helper.py   # Multi-currency support
    ├── data_fetcher.py      # Yahoo Finance data fetching
    ├── styling.py           # Custom CSS styling
    └── technical_analysis.py # Technical indicators
```

---

## 🔑 API Keys

| API | Purpose | Required | Get Key |
|-----|---------|----------|---------|
| **Gemini AI** | AI analysis & chatbot | ✅ Yes | [Google AI Studio](https://aistudio.google.com/) |
| **Alpha Vantage** | News sentiment | Optional | [alphavantage.co](https://www.alphavantage.co/support/#api-key) |
| **Finnhub** | Company news | Optional | [finnhub.io](https://finnhub.io/) |
| **NewsAPI** | News articles | Optional | [newsapi.org](https://newsapi.org/) |
| **MarketAux** | Financial news | Optional | [marketaux.com](https://www.marketaux.com/) |




-
---

<p align="center">
  Made with ❤️ using Streamlit & Gemini AI
</p>
