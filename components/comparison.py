import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
from utils.currency_helper import CurrencyHelper

class StockComparison:
    def __init__(self, data_fetcher, technical_analyzer, ai_advisor):
        self.data_fetcher = data_fetcher
        self.technical_analyzer = technical_analyzer
        self.ai_advisor = ai_advisor
    
    def fetch_comparison_data(self, symbols, market_codes, days):
        """Fetch data for multiple stocks with better error handling"""
        comparison_data = {}
        
        for symbol, market_code in zip(symbols, market_codes):
            try:
                st.info(f"Fetching data for {symbol} from {market_code} market...")
                
                # Use the same method as main app
                stock_data = self.data_fetcher.get_stock_data(symbol, market_code, days)
                
                if stock_data is None or stock_data.empty:
                    st.warning(f"⚠️ No data available for {symbol}")
                    continue
                
                st.success(f"✅ Successfully fetched {len(stock_data)} days of data for {symbol}")
                
                # Calculate technical indicators
                technical_data = self.technical_analyzer.calculate_all_indicators(stock_data)
                tech_summary = self.technical_analyzer.get_technical_summary(technical_data)
                
                comparison_data[symbol] = {
                    'data': stock_data,
                    'technical': technical_data,
                    'summary': tech_summary,
                    'market': market_code
                }
                
            except Exception as e:
                st.error(f"❌ Error fetching {symbol}: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
                continue
        
        return comparison_data
    
    def calculate_metrics(self, stock_data):
        """Calculate key performance metrics with error handling"""
        try:
            if stock_data.empty or len(stock_data) < 2:
                return None
            
            current_price = stock_data['close'].iloc[-1]
            start_price = stock_data['close'].iloc[0]
            
            # Returns
            total_return = ((current_price / start_price) - 1) * 100 if start_price != 0 else 0
            
            # Volatility
            returns = stock_data['close'].pct_change().dropna()
            
            if len(returns) < 2:
                volatility = 0
                sharpe = 0
            else:
                volatility = returns.std() * (252 ** 0.5) * 100
                
                # Sharpe ratio
                risk_free_rate = 0.02
                excess_returns = returns - (risk_free_rate / 252)
                sharpe = (excess_returns.mean() / returns.std() * (252 ** 0.5)) if returns.std() != 0 else 0
            
            # Max drawdown
            if len(returns) > 0:
                cumulative = (1 + returns).cumprod()
                rolling_max = cumulative.expanding().max()
                drawdown = (cumulative / rolling_max) - 1
                max_drawdown = drawdown.min() * 100
            else:
                max_drawdown = 0
            
            # Price position
            high_52w = stock_data['high'].max()
            low_52w = stock_data['low'].min()
            price_range = high_52w - low_52w
            price_position = ((current_price - low_52w) / price_range * 100) if price_range > 0 else 50
            
            # Volume metrics
            avg_volume = stock_data['volume'].mean()
            current_volume = stock_data['volume'].iloc[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            
            return {
                'current_price': current_price,
                'total_return': total_return,
                'volatility': volatility,
                'sharpe_ratio': sharpe,
                'max_drawdown': max_drawdown,
                'high_52w': high_52w,
                'low_52w': low_52w,
                'price_position': price_position,
                'avg_volume': avg_volume,
                'volume_ratio': volume_ratio
            }
        except Exception as e:
            st.error(f"Error calculating metrics: {str(e)}")
            return None
    
    def generate_comparison_analysis(self, symbols, comparison_data):
        """Generate AI-powered comparison analysis"""
        if not self.ai_advisor.available:
            return self._generate_fallback_comparison(symbols, comparison_data)
        
        try:
            # Prepare comparison data for AI
            analysis_text = f"Compare these {len(symbols)} stocks and recommend which to invest in:\n\n"
            
            for symbol in symbols:
                if symbol in comparison_data:
                    data = comparison_data[symbol]
                    metrics = self.calculate_metrics(data['data'])
                    
                    if metrics is None:
                        continue
                    
                    summary = data['summary']
                    
                    analysis_text += f"{symbol}:\n"
                    analysis_text += f"- Current Price: ${metrics['current_price']:.2f}\n"
                    analysis_text += f"- Total Return: {metrics['total_return']:.2f}%\n"
                    analysis_text += f"- Volatility: {metrics['volatility']:.2f}%\n"
                    analysis_text += f"- Sharpe Ratio: {metrics['sharpe_ratio']:.2f}\n"
                    analysis_text += f"- Max Drawdown: {metrics['max_drawdown']:.2f}%\n"
                    analysis_text += f"- RSI: {summary.get('rsi_current', 50):.1f}\n"
                    analysis_text += f"- Trend: {summary.get('trend_signal', 'Neutral')}\n"
                    analysis_text += f"- MACD: {summary.get('macd_signal', 'Neutral')}\n\n"
            
            prompt = f"""{analysis_text}

Provide a comprehensive comparison in JSON format:
{{
    "best_choice": "SYMBOL",
    "best_choice_reasons": [
        "Specific reason with data points",
        "Another compelling reason with metrics",
        "Third supporting factor with evidence"
    ],
    "rankings": [
        {{"symbol": "SYMBOL1", "rank": 1, "score": 85, "rationale": "Strong returns with low volatility"}},
        {{"symbol": "SYMBOL2", "rank": 2, "score": 70, "rationale": "Moderate performance"}}
    ],
    "risk_comparison": "Detailed risk analysis comparing volatility, drawdown, and stability across all stocks",
    "return_comparison": "Return potential comparison highlighting winners and explaining performance differences",
    "technical_comparison": "Technical setup comparison covering trends, momentum, and entry opportunities",
    "recommendation": "Specific actionable recommendation with allocation percentages",
    "summary": "4-5 sentence comprehensive comparison explaining why the best choice wins and what makes it superior"
}}"""
            
            from google.genai import types
            
            # Use the retry method from ai_advisor
            response_text = self.ai_advisor._call_model_with_retry(prompt, temperature=0.4, max_tokens=2500)
            
            if response_text:
                import json
                clean_text = response_text.strip()
                
                if clean_text.startswith('```json'):
                    clean_text = clean_text[7:]
                if clean_text.startswith('```'):
                    clean_text = clean_text[3:]
                if clean_text.endswith('```'):
                    clean_text = clean_text[:-3]
                
                clean_text = clean_text.strip()
                analysis = json.loads(clean_text)
                return analysis
            
            return self._generate_fallback_comparison(symbols, comparison_data)
            
        except Exception as e:
            st.warning(f"AI analysis unavailable, using fallback analysis")
            return self._generate_fallback_comparison(symbols, comparison_data)
    
    def _generate_fallback_comparison(self, symbols, comparison_data):
        """Generate fallback comparison when AI unavailable"""
        scores = {}
        
        for symbol in symbols:
            if symbol not in comparison_data:
                continue
            
            score = 50  # Base score
            data = comparison_data[symbol]
            metrics = self.calculate_metrics(data['data'])
            
            if metrics is None:
                scores[symbol] = 50
                continue
            
            summary = data['summary']
            
            # Score based on returns (max 25 points)
            if metrics['total_return'] > 30:
                score += 25
            elif metrics['total_return'] > 20:
                score += 20
            elif metrics['total_return'] > 10:
                score += 15
            elif metrics['total_return'] > 0:
                score += 10
            elif metrics['total_return'] > -10:
                score += 5
            else:
                score -= 5
            
            # Score based on risk-adjusted returns (max 20 points)
            if metrics['sharpe_ratio'] > 2.0:
                score += 20
            elif metrics['sharpe_ratio'] > 1.5:
                score += 15
            elif metrics['sharpe_ratio'] > 1.0:
                score += 10
            elif metrics['sharpe_ratio'] > 0.5:
                score += 5
            
            # Score based on technical indicators (max 15 points)
            rsi = summary.get('rsi_current', 50)
            if 45 < rsi < 55:
                score += 10
            elif 40 < rsi < 60:
                score += 7
            elif 30 < rsi < 70:
                score += 3
            
            trend_signal = summary.get('trend_signal', '')
            if 'Strong Uptrend' in trend_signal:
                score += 5
            elif 'Uptrend' in trend_signal:
                score += 3
            elif 'Downtrend' in trend_signal:
                score -= 3
            
            # Score based on volatility (max 15 points - lower is better)
            if metrics['volatility'] < 15:
                score += 15
            elif metrics['volatility'] < 20:
                score += 10
            elif metrics['volatility'] < 30:
                score += 5
            elif metrics['volatility'] < 40:
                score += 2
            
            # Score based on drawdown (max 10 points - smaller drawdown is better)
            if metrics['max_drawdown'] > -10:
                score += 10
            elif metrics['max_drawdown'] > -15:
                score += 7
            elif metrics['max_drawdown'] > -20:
                score += 5
            elif metrics['max_drawdown'] > -30:
                score += 2
            
            # Score based on MACD (max 5 points)
            if summary.get('macd_signal') == 'Bullish':
                score += 5
            elif summary.get('macd_signal') == 'Bearish':
                score -= 2
            
            scores[symbol] = max(0, min(100, score))  # Ensure score is between 0-100
        
        # Rank stocks
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        if not ranked:
            return self._get_default_analysis(symbols)
        
        best_choice = ranked[0][0]
        
        rankings = []
        for i, (symbol, score) in enumerate(ranked):
            data = comparison_data[symbol]
            metrics = self.calculate_metrics(data['data'])
            summary = data['summary']
            
            if metrics:
                rationale = f"Overall Score: {score}/100. Return: {metrics['total_return']:.1f}%, Volatility: {metrics['volatility']:.1f}%, Sharpe: {metrics['sharpe_ratio']:.2f}, Trend: {summary.get('trend_signal', 'Neutral')}"
            else:
                rationale = f"Score: {score}/100. Limited data available."
            
            rankings.append({
                'symbol': symbol,
                'rank': i + 1,
                'score': int(score),
                'rationale': rationale
            })
        
        best_data = comparison_data[best_choice]
        best_metrics = self.calculate_metrics(best_data['data'])
        best_summary = best_data['summary']
        
        if not best_metrics:
            return self._get_default_analysis(symbols)
        
        # Build best choice reasons
        reasons = []
        reasons.append(f"Highest overall score ({int(scores[best_choice])}/100) based on comprehensive analysis of returns, risk, and technical factors")
        
        if best_metrics['total_return'] > 0:
            reasons.append(f"Superior return performance with {best_metrics['total_return']:.1f}% total return over the analysis period")
        else:
            reasons.append(f"Best risk-adjusted performance with Sharpe ratio of {best_metrics['sharpe_ratio']:.2f}")
        
        if best_metrics['sharpe_ratio'] > 0.5:
            reasons.append(f"Excellent risk-reward profile demonstrated by Sharpe ratio of {best_metrics['sharpe_ratio']:.2f} and maximum drawdown of only {best_metrics['max_drawdown']:.1f}%")
        else:
            reasons.append(f"Favorable technical setup with {best_summary.get('trend_signal', 'stable trend')} and RSI at {best_summary.get('rsi_current', 50):.1f}")
        
        # Compare with second best
        if len(ranked) > 1:
            second_symbol = ranked[1][0]
            second_data = comparison_data[second_symbol]
            second_metrics = self.calculate_metrics(second_data['data'])
            
            if second_metrics:
                if best_metrics['total_return'] > second_metrics['total_return']:
                    reasons.append(f"Outperforms {second_symbol} by {(best_metrics['total_return'] - second_metrics['total_return']):.1f}% in total returns")
                elif best_metrics['volatility'] < second_metrics['volatility']:
                    reasons.append(f"Lower volatility ({best_metrics['volatility']:.1f}%) compared to {second_symbol} ({second_metrics['volatility']:.1f}%), indicating more stable performance")
        
        return {
            'best_choice': best_choice,
            'best_choice_reasons': reasons[:4],  # Top 4 reasons
            'rankings': rankings,
            'risk_comparison': f"Risk analysis shows {best_choice} offers the optimal balance with {best_metrics['volatility']:.1f}% volatility and {best_metrics['max_drawdown']:.1f}% maximum drawdown. The Sharpe ratio of {best_metrics['sharpe_ratio']:.2f} indicates superior risk-adjusted returns compared to alternatives.",
            'return_comparison': f"{best_choice} demonstrates the strongest performance with {best_metrics['total_return']:.1f}% total return. " + (f"This significantly outpaces {ranked[1][0]} which gained {self.calculate_metrics(comparison_data[ranked[1][0]]['data'])['total_return']:.1f}%." if len(ranked) > 1 else ""),
            'technical_comparison': f"Technical analysis favors {best_choice} with {best_summary.get('trend_signal', 'neutral trend')}, {best_summary.get('macd_signal', 'neutral')} MACD signal, and RSI at {best_summary.get('rsi_current', 50):.1f}. The technical setup suggests {('continued upward momentum' if 'Uptrend' in best_summary.get('trend_signal', '') else 'stable price action')}.",
            'recommendation': f"Primary recommendation: Allocate 60-70% to {best_choice} as core holding due to superior risk-adjusted returns and favorable technical setup. " + (f"Consider 30-40% allocation to {ranked[1][0]} for diversification." if len(ranked) > 1 else "Maintain cash reserves for entry opportunities."),
            'summary': f"Comprehensive analysis across {len(symbols)} stocks identifies {best_choice} as the superior investment choice. With {best_metrics['total_return']:.1f}% returns, {best_metrics['volatility']:.1f}% volatility, and a Sharpe ratio of {best_metrics['sharpe_ratio']:.2f}, {best_choice} demonstrates the optimal combination of performance and risk management. The technical setup shows {best_summary.get('trend_signal', 'neutral trend').lower()} with RSI at {best_summary.get('rsi_current', 50):.1f}, indicating {('strong momentum' if 'Uptrend' in best_summary.get('trend_signal', '') else 'stable conditions')}. Based on {int(scores[best_choice])}/100 overall score, {best_choice} represents the best risk-reward opportunity among the compared stocks."
        }
    
    def _get_default_analysis(self, symbols):
        """Return default analysis when data is insufficient"""
        return {
            'best_choice': symbols[0] if symbols else "N/A",
            'best_choice_reasons': [
                "Insufficient data available for comprehensive analysis",
                "Please try different stock symbols or time periods",
                "Ensure stock symbols are valid for their respective markets"
            ],
            'rankings': [{'symbol': s, 'rank': i+1, 'score': 50, 'rationale': 'Insufficient data'} for i, s in enumerate(symbols)],
            'risk_comparison': "Unable to perform risk comparison due to insufficient data",
            'return_comparison': "Unable to compare returns due to insufficient data",
            'technical_comparison': "Unable to perform technical comparison due to insufficient data",
            'recommendation': "Please select different stocks or verify that symbols are correct",
            'summary': "Analysis could not be completed due to insufficient data. Please verify stock symbols and try again."
        }
    
    def render_comparison(self, symbols, comparison_data, comparison_analysis):
        """Render comparison visualization with proper currencies"""
        try:
            # Header
            st.markdown(f"""
            <div style='background: linear-gradient(90deg, #00d4aa 0%, #667eea 100%); 
                        padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;'>
                <h2 style='color: white; margin: 0;'>
                    📊 Stock Comparison Analysis
                </h2>
                <p style='color: white; opacity: 0.9; margin: 5px 0 0 0;'>
                    Comparing {len(symbols)} stocks: {', '.join(symbols)}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # AI Recommendation Summary
            best_choice = comparison_analysis['best_choice']
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #2ed57315 0%, #2ed57305 100%);
                        padding: 25px; border-radius: 12px; border-left: 5px solid #2ed573; margin-bottom: 25px;'>
                <h3 style='color: #2ed573; margin-top: 0; margin-bottom: 15px;'>
                    🏆 Recommended Choice: {best_choice}
                </h3>
                <p style='color: #e2e8f0; font-size: 16px; line-height: 1.8;'>
                    {comparison_analysis['summary']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Rankings
            st.markdown("### 🥇 Stock Rankings")
            
            for rank_data in comparison_analysis['rankings']:
                symbol = rank_data['symbol']
                rank = rank_data['rank']
                score = rank_data['score']
                

                market = comparison_data[symbol]['market']
                currency_code = CurrencyHelper.get_currency_code(market)
                current_price = self.calculate_metrics(comparison_data[symbol]['data'])['current_price']

                if rank == 1:
                    color = "#2ed573"
                    medal = "🥇"
                elif rank == 2:
                    color = "#ffa502"
                    medal = "🥈"
                else:
                    color = "#ff4757"
                    medal = "🥉"
                
                st.markdown(f"""
            <div style='background-color: #1a202c; padding: 15px; border-radius: 8px; 
                       border-left: 4px solid {color}; margin-bottom: 10px;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <h4 style='color: {color}; margin: 0;'>{medal} Rank #{rank} - {symbol}</h4>
                        <p style='color: #94a3b8; margin: 2px 0; font-size: 12px;'>
                            {CurrencyHelper.format_price(current_price, market)} ({currency_code})
                        </p>
                        <p style='color: #e2e8f0; margin: 5px 0 0 0; font-size: 14px;'>{rank_data['rationale']}</p>
                    </div>
                    <div style='text-align: right;'>
                        <p style='color: {color}; font-size: 24px; font-weight: bold; margin: 0;'>{score}</p>
                        <p style='color: #94a3b8; font-size: 12px; margin: 0;'>Score</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Key Metrics Comparison Table
            st.markdown("### 📊 Key Metrics Comparison")
            
            metrics_data = []
            for symbol in symbols:
                if symbol in comparison_data:
                    metrics = self.calculate_metrics(comparison_data[symbol]['data'])
                    if metrics:
                        summary = comparison_data[symbol]['summary']
                        market = comparison_data[symbol]['market']
                        currency_symbol = CurrencyHelper.get_currency_symbol(market)
                        currency_code = CurrencyHelper.get_currency_code(market)
                        metrics_data.append({
                            'Symbol': symbol,
                            'Market': market,
                            'Currency': currency_code,
                            'Price': CurrencyHelper.format_price(metrics['current_price'], market),
                            'Return': f"{metrics['total_return']:.2f}%",
                            'Volatility': f"{metrics['volatility']:.2f}%",
                            'Sharpe': f"{metrics['sharpe_ratio']:.2f}",
                            'Max DD': f"{metrics['max_drawdown']:.2f}%",
                            'RSI': f"{summary.get('rsi_current', 50):.1f}",
                            'Trend': summary.get('trend_signal', 'Neutral')
                        })
            
            if metrics_data:
                df_metrics = pd.DataFrame(metrics_data)
                st.dataframe(df_metrics, use_container_width=True, hide_index=True)
            else:
                st.warning("Unable to display metrics table due to data issues")
            
            # Price Performance Chart
            st.markdown("### 📈 Price Performance Comparison")
            
            fig = go.Figure()
            
            colors = ['#00d4aa', '#667eea', '#ffa502', '#ff6b6b']
            
            for i, symbol in enumerate(symbols):
                if symbol in comparison_data:
                    data = comparison_data[symbol]['data']
                    if not data.empty and len(data) > 1:
                        # Normalize to base 100
                        normalized = (data['close'] / data['close'].iloc[0]) * 100
                        
                        fig.add_trace(go.Scatter(
                            x=data.index,
                            y=normalized,
                            mode='lines',
                            name=symbol,
                            line=dict(width=3 if symbol == best_choice else 2, color=colors[i % len(colors)])
                        ))
            
            fig.update_layout(
                title="Normalized Price Performance (Base 100)",
                xaxis_title="Date",
                yaxis_title="Normalized Price",
                template="plotly_dark",
                height=500,
                hovermode='x unified',
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk-Return Scatter
            st.markdown("### ⚖️ Risk-Return Analysis")
            
            fig_scatter = go.Figure()
            
            for symbol in symbols:
                if symbol in comparison_data:
                    metrics = self.calculate_metrics(comparison_data[symbol]['data'])
                    if metrics:
                        color = '#2ed573' if symbol == best_choice else '#94a3b8'
                        size = 25 if symbol == best_choice else 18
                        
                        fig_scatter.add_trace(go.Scatter(
                            x=[metrics['volatility']],
                            y=[metrics['total_return']],
                            mode='markers+text',
                            name=symbol,
                            text=[symbol],
                            textposition='top center',
                            textfont=dict(size=14, color=color),
                            marker=dict(
                                size=size, 
                                color=color,
                                line=dict(width=2, color='white')
                            ),
                            hovertemplate=f'<b>{symbol}</b><br>Risk: %{{x:.2f}}%<br>Return: %{{y:.2f}}%<extra></extra>'
                        ))
            
            fig_scatter.update_layout(
                title="Risk vs Return (Higher Return + Lower Risk = Better)",
                xaxis_title="Volatility (Risk) %",
                yaxis_title="Total Return %",
                template="plotly_dark",
                height=500,
                showlegend=False
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Detailed Analysis Sections
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div style='background-color: #1a202c; padding: 20px; border-radius: 12px; margin-bottom: 15px;'>
                    <h4 style='color: #00d4aa; margin-top: 0;'>🛡️ Risk Analysis</h4>
                    <p style='color: #e2e8f0; line-height: 1.6; font-size: 14px;'>{comparison_analysis['risk_comparison']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style='background-color: #1a202c; padding: 20px; border-radius: 12px;'>
                    <h4 style='color: #00d4aa; margin-top: 0;'>💰 Return Analysis</h4>
                    <p style='color: #e2e8f0; line-height: 1.6; font-size: 14px;'>{comparison_analysis['return_comparison']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style='background-color: #1a202c; padding: 20px; border-radius: 12px; margin-bottom: 15px;'>
                    <h4 style='color: #00d4aa; margin-top: 0;'>📊 Technical Analysis</h4>
                    <p style='color: #e2e8f0; line-height: 1.6; font-size: 14px;'>{comparison_analysis['technical_comparison']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style='background-color: #1a202c; padding: 20px; border-radius: 12px;'>
                    <h4 style='color: #2ed573; margin-top: 0;'>💡 Investment Recommendation</h4>
                    <p style='color: #e2e8f0; line-height: 1.6; font-size: 14px;'>{comparison_analysis['recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Why Best Choice
            st.markdown(f"### 🎯 Why {best_choice}?")
            
            for i, reason in enumerate(comparison_analysis['best_choice_reasons'], 1):
                st.markdown(f"""
                <div style='background-color: #2ed57310; padding: 15px; border-radius: 8px; 
                           border-left: 3px solid #2ed573; margin-bottom: 10px;'>
                    <p style='color: #e2e8f0; margin: 0; font-size: 15px;'>
                        <strong style='color: #2ed573;'>{i}.</strong> {reason}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Disclaimer
            st.markdown("---")
            st.markdown("""
            <div style='background-color: #2d3748; padding: 15px; border-radius: 8px; 
                        border-left: 4px solid #ffa502; margin-top: 20px;'>
                <p style='color: #e2e8f0; margin: 0; font-size: 13px;'>
                    <strong>⚠️ Disclaimer:</strong> This comparison is for educational and directive purposes only and should not be considered fully financial advice. 
                    Past performance does not guarantee future results. Always conduct your own research and consult with qualified financial advisors 
                    before making investment decisions.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error rendering comparison: {str(e)}")
            import traceback
            st.code(traceback.format_exc())