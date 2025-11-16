import json
import os
import streamlit as st
from datetime import datetime
from google import genai
from google.genai import types
from utils.currency_helper import CurrencyHelper
from dotenv import load_dotenv

load_dotenv()

class AIAdvisor:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key or api_key == "default_key" or api_key == "your_actual_api_key_here":
            st.error("⚠️ Gemini API key not configured. Please add GEMINI_API_KEY to your .env file")
            self.available = False
            self.client = None
        else:
            try:
                self.client = genai.Client(api_key=api_key)
                self.available = True
            except Exception as e:
                st.error(f"Failed to initialize Gemini AI: {str(e)}")
                self.available = False
                self.client = None
    
    def generate_analysis(self, symbol, stock_data, tech_summary, news_sentiment, market_code="US"):
        """Generate comprehensive AI-powered investment analysis"""
        if not self.available or self.client is None:
            current_price = stock_data['close'].iloc[-1] if not stock_data.empty else 100.0
            return self._create_fallback_analysis(symbol, current_price, tech_summary, news_sentiment, market_code)
        
        try:

            from utils.currency_helper import CurrencyHelper



            currency_symbol = CurrencyHelper.get_currency_symbol(market_code)
            currency_code = CurrencyHelper.get_currency_code(market_code)

            # Calculate comprehensive metrics
            current_price = stock_data['close'].iloc[-1]
            price_change = ((current_price / stock_data['close'].iloc[0]) - 1) * 100
            volatility = stock_data['close'].pct_change().std() * 100
            
            # Calculate additional metrics
            avg_volume = stock_data['volume'].mean()
            current_volume = stock_data['volume'].iloc[-1]
            volume_ratio = (current_volume / avg_volume) if avg_volume > 0 else 1
            
            # Price positioning
            high_52w = stock_data['high'].max()
            low_52w = stock_data['low'].min()
            price_position = ((current_price - low_52w) / (high_52w - low_52w) * 100) if (high_52w - low_52w) > 0 else 50
            
            prompt = f"""
You are an expert financial analyst. Provide detailed investment analysis for {symbol} stock.

MARKET DATA:
- Current Price: {CurrencyHelper.format_price(current_price, market_code)} ({currency_code})
- Period Performance: {price_change:.2f}%
- Daily Volatility: {volatility:.2f}%
- Price Position (52W Range): {price_position:.1f}%
- Volume vs Average: {volume_ratio:.2f}x

TECHNICAL INDICATORS:
- RSI (14): {tech_summary.get('rsi_current', 50):.1f}
- MACD Signal: {tech_summary.get('macd_signal', 'Neutral')}
- Trend: {tech_summary.get('trend_signal', 'Neutral')}
- Volume Pattern: {tech_summary.get('volume_signal', 'Normal')}
- Bollinger Position: {tech_summary.get('bollinger_position', 'Within Bands')}

MARKET SENTIMENT:
- News Sentiment: {news_sentiment}
- Overall Signal: {tech_summary.get('overall_signal', 'Neutral')}

Provide analysis in valid JSON format:
{{
    "risk_level": "Low/Medium/High",
    "recommendation": "Strong Buy/Buy/Hold/Sell/Strong Sell",
    "confidence_level": "High/Medium/Low",
   "price_target": "{currency_symbol}XXX.XX",
    "timeframe": "3-6 months",
    "key_factors": [
        "Detailed technical analysis insight",
        "Market sentiment and news impact",
        "Volume and momentum analysis",
        "Price position and trend strength",
        "Risk-reward assessment"
    ],
    "risk_factors": [
        "Specific technical risk with probability",
        "Market volatility assessment",
        "External factors and market conditions"
    ],
    "opportunities": [
        "Growth catalyst identification",
        "Technical breakout/breakdown potential",
        "Market positioning advantages"
    ],
    "entry_strategy": "Specific entry points with price levels and timing",
    "exit_strategy": "Clear profit targets and stop-loss levels with rationale",
    "analysis_summary": "Comprehensive 4-5 sentence analysis covering technical setup, fundamental outlook, risk-reward ratio, and actionable recommendations with specific reasoning."
}}
"""
            
            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4,  # Lower temperature for more consistent analysis
                    max_output_tokens=3000,
                    top_p=0.95
                )
            )
            
            if response.text:
                clean_text = response.text.strip()
                
                # Remove markdown formatting
                if clean_text.startswith('```json'):
                    clean_text = clean_text[7:]
                if clean_text.startswith('```'):
                    clean_text = clean_text[3:]
                if clean_text.endswith('```'):
                    clean_text = clean_text[:-3]
                
                clean_text = clean_text.strip()
                analysis = json.loads(clean_text)
                
                # Validate and enhance analysis
                return self._validate_analysis(analysis, current_price, market_code)
            
            return self._create_fallback_analysis(symbol, current_price, tech_summary, news_sentiment, market_code)
            
        except Exception as e:
            st.warning(f"AI analysis encountered an issue. Using enhanced fallback analysis.")
            current_price = stock_data['close'].iloc[-1] if not stock_data.empty else 100.0
            return self._create_fallback_analysis(symbol, current_price, tech_summary, news_sentiment, market_code)
    
    def _validate_analysis(self, analysis, current_price, market_code="US"):
        """Validate and enhance AI analysis"""
        currency_symbol = CurrencyHelper.get_currency_symbol(market_code)
        # Ensure all required fields exist
        required_fields = ['risk_level', 'recommendation', 'confidence_level', 'price_target', 
                          'timeframe', 'key_factors', 'risk_factors', 'opportunities', 
                          'entry_strategy', 'exit_strategy', 'analysis_summary']
        
        for field in required_fields:
            if field not in analysis:
                analysis[field] = "Not available"
        
        # Validate price target format
        price_target = analysis['price_target']
        try:
            # Remove any currency symbols and parse
            price_val = float(''.join(c for c in price_target if c.isdigit() or c == '.'))
            analysis['price_target'] = CurrencyHelper.format_price(price_val, market_code)
        except:
            analysis['price_target'] = CurrencyHelper.format_price(current_price * 1.05, market_code)
        
        return analysis
    
    def _create_fallback_analysis(self, symbol, current_price, tech_summary, news_sentiment, market_code="US"):
        """Enhanced fallback analysis with detailed reasoning"""
        rsi = tech_summary.get('rsi_current', 50)
        trend = tech_summary.get('trend_signal', 'Neutral')
        macd = tech_summary.get('macd_signal', 'Neutral')
        volume = tech_summary.get('volume_signal', 'Normal')
        bollinger = tech_summary.get('bollinger_position', 'Within Bands')
        
        # Sophisticated scoring system
        bullish_score = 0
        bearish_score = 0
        
        # RSI analysis (weight: 2)
        if rsi < 25:
            bullish_score += 3
        elif rsi < 35:
            bullish_score += 2
        elif rsi > 75:
            bearish_score += 3
        elif rsi > 65:
            bearish_score += 2
        
        # Trend analysis (weight: 3)
        if 'Strong Uptrend' in trend:
            bullish_score += 3
        elif 'Uptrend' in trend:
            bullish_score += 2
        elif 'Strong Downtrend' in trend:
            bearish_score += 3
        elif 'Downtrend' in trend:
            bearish_score += 2
        
        # MACD analysis (weight: 2)
        if macd == 'Bullish':
            bullish_score += 2
        elif macd == 'Bearish':
            bearish_score += 2
        
        # Volume analysis (weight: 1)
        if 'High' in volume:
            if bullish_score > bearish_score:
                bullish_score += 1
            else:
                bearish_score += 1
        
        # News sentiment (weight: 1)
        if news_sentiment == 'positive':
            bullish_score += 1
        elif news_sentiment == 'negative':
            bearish_score += 1
        
        # Bollinger position
        if 'Below' in bollinger:
            bullish_score += 1
        elif 'Above' in bollinger:
            bearish_score += 1
        
        # Determine recommendation with confidence
        score_diff = abs(bullish_score - bearish_score)
        
        if bullish_score >= 6 and score_diff >= 3:
            recommendation = "Strong Buy"
            risk_level = "Medium"
            confidence = "High"
            price_target = current_price * 1.12
        elif bullish_score >= 4:
            recommendation = "Buy"
            risk_level = "Medium"
            confidence = "Medium" if score_diff >= 2 else "Low"
            price_target = current_price * 1.08
        elif bearish_score >= 6 and score_diff >= 3:
            recommendation = "Strong Sell"
            risk_level = "High"
            confidence = "High"
            price_target = current_price * 0.92
        elif bearish_score >= 4:
            recommendation = "Sell"
            risk_level = "High"
            confidence = "Medium" if score_diff >= 2 else "Low"
            price_target = current_price * 0.95
        else:
            recommendation = "Hold"
            risk_level = "Medium"
            confidence = "Medium"
            price_target = current_price * 1.03
        
        return {
            "risk_level": risk_level,
            "recommendation": recommendation,
            "confidence_level": confidence,
            "price_target": CurrencyHelper.format_price(price_target, market_code),
            "timeframe": "3-6 months",
            "key_factors": [
                f"RSI at {rsi:.1f} indicates {self._interpret_rsi(rsi)} with {self._rsi_pressure(rsi)}",
                f"Price showing {trend.lower()} pattern with {macd.lower()} MACD confirmation, indicating {self._momentum_strength(trend, macd)}",
                f"Volume analysis reveals {volume.lower()} suggesting {self._volume_interpretation(volume, trend)}",
                f"Price position {bollinger.lower()} providing {self._bollinger_opportunity(bollinger)}",
                f"News sentiment is {news_sentiment}, {self._sentiment_impact(news_sentiment, recommendation)}"
            ],
            "risk_factors": [
                f"Technical volatility risk: {self._assess_volatility_risk(rsi, trend)}",
                f"Market momentum: {self._momentum_risk(macd, trend)}",
                f"Position risk: Current setup carries {risk_level.lower()} risk with {self._risk_context(rsi, bollinger)}"
            ],
            "opportunities": [
                f"Entry opportunity: {self._entry_opportunity(rsi, trend, bollinger)}",
                f"Technical setup: {self._technical_opportunity(trend, macd, volume)}",
                f"Risk-reward profile: {self._risk_reward(recommendation, risk_level)}"
            ],
            "entry_strategy": f"Optimal entry zone: {CurrencyHelper.format_price(current_price * 0.97, market_code)} - {CurrencyHelper.format_price(current_price * 0.99, market_code)}. Wait for {self._entry_confirmation(rsi, volume)} before entering position. Consider scaling in with 50% initial position.",
            "exit_strategy": f"Primary target: {CurrencyHelper.format_price(price_target, market_code)} ({((price_target/current_price - 1)*100):.1f}% gain). Stop loss: {CurrencyHelper.format_price(current_price * 0.94, market_code)} ({((current_price * 0.94/current_price - 1)*100):.1f}% risk). Risk-reward ratio: {abs((price_target - current_price) / (current_price - current_price * 0.94)):.2f}:1",
            "analysis_summary": f"Technical analysis of {symbol} at {CurrencyHelper.format_price(current_price, market_code)} shows {trend.lower()} with RSI at {rsi:.1f} and {macd.lower()} MACD signal. {recommendation} recommendation (confidence: {confidence.lower()}) based on {bullish_score} bullish vs {bearish_score} bearish indicators. Price target {CurrencyHelper.format_price(price_target, market_code)} represents {((price_target/current_price - 1)*100):.1f}% potential {'gain' if price_target > current_price else 'loss'} over 3-6 months. {self._concluding_advice(recommendation, risk_level, confidence)}"
        }
    
    # Helper methods for better interpretations
    def _interpret_rsi(self, rsi):
        if rsi < 25: return "extremely oversold conditions"
        elif rsi < 35: return "oversold conditions"
        elif rsi > 75: return "extremely overbought conditions"
        elif rsi > 65: return "overbought conditions"
        else: return "neutral momentum"
    
    def _rsi_pressure(self, rsi):
        if rsi < 30: return "strong buying pressure expected"
        elif rsi > 70: return "potential selling pressure"
        else: return "balanced market conditions"
    
    def _momentum_strength(self, trend, macd):
        if 'Uptrend' in trend and macd == 'Bullish':
            return "strong bullish momentum alignment"
        elif 'Downtrend' in trend and macd == 'Bearish':
            return "strong bearish momentum alignment"
        else:
            return "mixed momentum signals requiring caution"
    
    def _volume_interpretation(self, volume, trend):
        if 'High' in volume:
            return "strong conviction in current trend"
        elif 'Low' in volume:
            return "weak participation, trend may lack strength"
        else:
            return "moderate market participation"
    
    def _bollinger_opportunity(self, bollinger):
        if 'Below' in bollinger:
            return "potential mean reversion opportunity"
        elif 'Above' in bollinger:
            return "caution - potential overextension"
        else:
            return "normal price action within expected range"
    
    def _sentiment_impact(self, sentiment, recommendation):
        if sentiment == 'positive' and 'Buy' in recommendation:
            return "supporting the bullish technical setup"
        elif sentiment == 'negative' and 'Sell' in recommendation:
            return "confirming the bearish technical outlook"
        else:
            return "creating mixed signals with technical analysis"
    
    def _assess_volatility_risk(self, rsi, trend):
        if rsi > 70 or rsi < 30:
            return "Extreme RSI levels suggest high volatility risk"
        else:
            return "Moderate volatility expected in current range"
    
    def _momentum_risk(self, macd, trend):
        if ('Uptrend' in trend and macd == 'Bearish') or ('Downtrend' in trend and macd == 'Bullish'):
            return "Divergence between trend and MACD suggests potential reversal risk"
        else:
            return "Momentum indicators aligned with trend direction"
    
    def _risk_context(self, rsi, bollinger):
        if rsi > 70 and 'Above' in bollinger:
            return "elevated risk due to overbought conditions"
        elif rsi < 30 and 'Below' in bollinger:
            return "attractive risk-reward for contrarian entry"
        else:
            return "balanced risk profile"
    
    def _entry_opportunity(self, rsi, trend, bollinger):
        if rsi < 35 and 'Below' in bollinger:
            return "Favorable entry zone with oversold conditions"
        elif 'Uptrend' in trend and rsi < 60:
            return "Pullback entry opportunity in established uptrend"
        else:
            return "Wait for better risk-reward entry setup"
    
    def _technical_opportunity(self, trend, macd, volume):
        if 'Uptrend' in trend and macd == 'Bullish' and 'High' in volume:
            return "Strong technical alignment with volume confirmation"
        else:
            return "Mixed technical signals suggest selective positioning"
    
    def _risk_reward(self, recommendation, risk):
        if 'Strong' in recommendation:
            return "Attractive risk-reward with high conviction setup"
        elif 'Hold' in recommendation:
            return "Neutral risk-reward, better opportunities may exist"
        else:
            return f"Moderate risk-reward appropriate for {risk.lower()} risk tolerance"
    
    def _entry_confirmation(self, rsi, volume):
        confirmations = []
        if rsi < 40:
            confirmations.append("RSI bounce above 35")
        if 'Low' in volume:
            confirmations.append("volume expansion")
        return " and ".join(confirmations) if confirmations else "price stability"
    
    def _concluding_advice(self, recommendation, risk, confidence):
        if confidence == "High":
            return f"High-confidence {recommendation.lower()} signal. Position size: 60-80% of planned allocation."
        elif confidence == "Medium":
            return f"Moderate-confidence {recommendation.lower()} signal. Position size: 40-60% of planned allocation."
        else:
            return f"Low-confidence signal. Consider smaller position (20-40%) or wait for confirmation."
    
    def generate_chat_response(self, question, symbol, stock_data, tech_summary, market_code="US"):
        """Enhanced chatbot with better context"""
        if not self.available or self.client is None:
            return "AI chatbot is currently unavailable. Please configure your GEMINI_API_KEY in the .env file."
        
        try:
            current_price = stock_data['close'].iloc[-1]
            rsi = tech_summary.get('rsi_current', 50)
            trend = tech_summary.get('trend_signal', 'Neutral')
            currency_code = CurrencyHelper.get_currency_code(market_code)
            
            prompt = f"""You are an experienced financial advisor. Answer this question about {symbol} stock professionally and concisely.

            Current Market Data:
            - Price: {CurrencyHelper.format_price(current_price, market_code)} ({currency_code})
            - RSI: {rsi:.1f}
            - Trend: {trend}
            - MACD: {tech_summary.get('macd_signal', 'Neutral')}

            User Question: {question}

            Provide a helpful answer in 2-4 paragraphs. Be specific, actionable, and educational. If discussing trading strategies, always emphasize risk management."""
            
            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=1000
                )
            )
            
            return response.text if response.text else "Unable to generate response at this time."
            
        except Exception as e:
            return f"Error processing your question. Please try rephrasing it."
    
    def render_analysis(self, analysis, symbol, stock_data, tech_summary, market_code="US"):
        """Render analysis with the existing beautiful UI"""
        # [Keep your existing render_analysis method - it's already good]
        # I'll provide the same rendering code to maintain consistency
        try:
            currency_symbol = CurrencyHelper.get_currency_symbol(market_code)
            currency_code = CurrencyHelper.get_currency_code(market_code)
            st.markdown(f"""
            <div style='background: linear-gradient(90deg, #00d4aa 0%, #1f4068 100%); 
                        padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;'>
                <h2 style='color: white; margin: 0;'>
                    AI Investment Analysis for {symbol}
                </h2>
                <p style='color: white; opacity: 0.8; margin: 5px 0 0 0; font-size: 14px;'>
                    All prices in {currency_code}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background-color: #2d3748; padding: 15px; border-radius: 8px; 
                        border-left: 4px solid #ff6b6b; margin-bottom: 20px;'>
                <p style='color: #e2e8f0; margin: 0; font-size: 14px;'>
                    <strong>Educational Purpose Disclaimer:</strong> This AI analysis is for educational and informational purposes only. 
                    It should not be considered as financial advice. Always conduct your own research 
                    and consult with qualified financial advisors before making investment decisions.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                risk_level = analysis.get('risk_level', 'Medium')
                risk_color = "#ff4757" if risk_level == "High" else "#ffa502" if risk_level == "Medium" else "#2ed573"
                st.markdown(f"""
                <div style='background-color: #1a202c; padding: 20px; border-radius: 12px; 
                           border: 2px solid {risk_color}; text-align: center; margin-bottom: 10px;'>
                    <h4 style='color: #e2e8f0; margin: 0; font-size: 16px;'>Risk Level</h4>
                    <p style='color: {risk_color}; font-size: 24px; font-weight: bold; margin: 5px 0;'>{risk_level}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                recommendation = analysis.get('recommendation', 'Hold')
                rec_color = "#2ed573" if "Buy" in recommendation else "#ff4757" if "Sell" in recommendation else "#ffa502"
                st.markdown(f"""
                <div style='background-color: #1a202c; padding: 20px; border-radius: 12px; 
                           border: 2px solid {rec_color}; text-align: center; margin-bottom: 10px;'>
                    <h4 style='color: #e2e8f0; margin: 0; font-size: 16px;'>Recommendation</h4>
                    <p style='color: {rec_color}; font-size: 24px; font-weight: bold; margin: 5px 0;'>{recommendation}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                price_target = analysis.get('price_target', 'N/A')
                st.markdown(f"""
                <div style='background-color: #1a202c; padding: 20px; border-radius: 12px; 
                           border: 2px solid #00d4aa; text-align: center; margin-bottom: 10px;'>
                    <h4 style='color: #e2e8f0; margin: 0; font-size: 16px;'>Price Target</h4>
                    <p style='color: #00d4aa; font-size: 24px; font-weight: bold; margin: 5px 0;'>{price_target}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                confidence_level = analysis.get('confidence_level', 'Medium')
                timeframe = analysis.get('timeframe', '3-6 months')
                conf_color = "#2ed573" if confidence_level == "High" else "#ffa502" if confidence_level == "Medium" else "#ff7675"
                st.markdown(f"""
                <div style='background-color: #1a202c; padding: 20px; border-radius: 12px; 
                           border: 2px solid #00d4aa; text-align: center; margin-bottom: 10px;'>
                    <h4 style='color: #e2e8f0; margin: 0; font-size: 16px;'>Timeframe</h4>
                    <p style='color: #00d4aa; font-size: 18px; font-weight: bold; margin: 5px 0;'>{timeframe}</p>
                    <p style='color: {conf_color}; font-size: 14px; margin: 0;'>Confidence: {confidence_level}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div style='background-color: #1a202c; padding: 20px; border-radius: 12px; 
                           border-left: 4px solid #2ed573; margin-bottom: 15px;'>
                    <h3 style='color: #2ed573; margin-top: 0; margin-bottom: 15px;'>Key Factors</h3>
                """, unsafe_allow_html=True)
                for factor in analysis.get('key_factors', []):
                    st.markdown(f"<p style='color: #e2e8f0; margin: 8px 0; font-size: 14px;'>• {factor}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style='background-color: #1a202c; padding: 20px; border-radius: 12px; 
                           border-left: 4px solid #ff6b6b; margin-bottom: 15px;'>
                    <h3 style='color: #ff6b6b; margin-top: 0; margin-bottom: 15px;'>Risk Factors</h3>
                """, unsafe_allow_html=True)
                for factor in analysis.get('risk_factors', []):
                    st.markdown(f"<p style='color: #e2e8f0; margin: 8px 0; font-size: 14px;'>• {factor}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style='background-color: #1a202c; padding: 20px; border-radius: 12px; 
                           border-left: 4px solid #00d4aa; margin-bottom: 15px;'>
                    <h3 style='color: #00d4aa; margin-top: 0; margin-bottom: 15px;'>Opportunities</h3>
                """, unsafe_allow_html=True)
                for opportunity in analysis.get('opportunities', []):
                    st.markdown(f"<p style='color: #e2e8f0; margin: 8px 0; font-size: 14px;'>• {opportunity}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                entry_strategy = analysis.get('entry_strategy', 'Consider market conditions')
                st.markdown(f"""
                <div style='background-color: #1a202c; padding: 20px; border-radius: 12px; 
                           border-left: 4px solid #2ed573; margin-bottom: 15px;'>
                    <h3 style='color: #2ed573; margin-top: 0; margin-bottom: 15px;'>Entry Strategy</h3>
                    <p style='color: #e2e8f0; margin: 0; font-size: 14px; line-height: 1.6;'>{entry_strategy}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                exit_strategy = analysis.get('exit_strategy', 'Set appropriate targets')
                st.markdown(f"""
                <div style='background-color: #1a202c; padding: 20px; border-radius: 12px; 
                           border-left: 4px solid #ff6b6b; margin-bottom: 15px;'>
                    <h3 style='color: #ff6b6b; margin-top: 0; margin-bottom: 15px;'>Exit Strategy</h3>
                    <p style='color: #e2e8f0; margin: 0; font-size: 14px; line-height: 1.6;'>{exit_strategy}</p>
                </div>
                """, unsafe_allow_html=True)
            
            if 'analysis_summary' in analysis:
                summary = analysis['analysis_summary']
                st.markdown(f"""
                <div style='background-color: #1a202c; padding: 25px; border-radius: 12px; 
                           border: 2px solid #00d4aa; margin: 20px 0;'>
                    <h3 style='color: #00d4aa; margin-top: 0; margin-bottom: 15px; text-align: center;'>Detailed Analysis</h3>
                    <p style='color: #e2e8f0; margin: 0; font-size: 16px; line-height: 1.8; text-align: justify;'>{summary}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### Ask the AI Advisor")
            
            if f"chat_history_{symbol}" not in st.session_state:
                st.session_state[f"chat_history_{symbol}"] = []
            
            user_question = st.text_input(
                "Your question:", 
                placeholder=f"e.g., What factors might affect {symbol}'s price?",
                key=f"chat_input_{symbol}"
            )
            
            col1, col2 = st.columns([1, 5])
            with col1:
                ask_button = st.button("Ask", key=f"ask_btn_{symbol}")
            with col2:
                clear_chat = st.button("Clear Chat", key=f"clear_btn_{symbol}")
            
            if clear_chat:
                st.session_state[f"chat_history_{symbol}"] = []
                st.rerun()
            
            if ask_button and user_question.strip():
                with st.spinner("AI is thinking..."):
                    response = self.generate_chat_response(user_question, symbol, stock_data, tech_summary, market_code)
                    st.session_state[f"chat_history_{symbol}"].append({
                        "question": user_question,
                        "answer": response,
                        "timestamp": datetime.now().strftime("%H:%M")
                    })
                st.rerun()
            
            if st.session_state[f"chat_history_{symbol}"]:
                st.markdown("### Chat History")
                for i, chat in enumerate(reversed(st.session_state[f"chat_history_{symbol}"][-5:])):
                    with st.expander(f"Q: {chat['question'][:50]}... ({chat['timestamp']})", expanded=(i==0)):
                        st.markdown(f"**Question:** {chat['question']}")
                        st.markdown(f"**Answer:** {chat['answer']}")
                
        except Exception as e:
            st.error(f"Error rendering analysis: {str(e)}")