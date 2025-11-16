import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

class ChartRenderer:
    def __init__(self):
        self.theme = "plotly_dark"
        self.colors = {
            'primary': '#00d4aa',
            'secondary': '#ff6b6b',
            'accent': '#4ecdc4',
            'background': '#0e1117',
            'surface': '#262730'
        }
    
    def create_price_chart(self, data, symbol):
        """Create candlestick price chart"""
        try:
            fig = go.Figure()
            
            # Candlestick chart
            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                name=symbol,
                increasing_line_color=self.colors['primary'],
                decreasing_line_color=self.colors['secondary']
            ))
            
            fig.update_layout(
                title=f"{symbol} - Price Chart",
                xaxis_title="Date",
                yaxis_title="Price ($)",
                template=self.theme,
                height=500,
                hovermode='x unified',
                xaxis_rangeslider_visible=False
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating price chart: {str(e)}")
            return go.Figure()
    
    def create_volume_chart(self, data, symbol):
        """Create volume chart"""
        try:
            fig = go.Figure()
            
            # Volume bars
            colors = ['red' if close < open else 'green' 
                     for close, open in zip(data['close'], data['open'])]
            
            fig.add_trace(go.Bar(
                x=data.index,
                y=data['volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.7
            ))
            
            fig.update_layout(
                title=f"{symbol} - Volume Analysis",
                xaxis_title="Date",
                yaxis_title="Volume",
                template=self.theme,
                height=300,
                hovermode='x unified'
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating volume chart: {str(e)}")
            return go.Figure()
    
    def create_technical_chart(self, data, symbol, show_ma=True, show_bollinger=True, 
                             show_rsi=True, show_macd=True, show_stoch=False, show_williams=False):
        """Create comprehensive technical analysis chart"""
        try:
            # Determine number of subplots
            subplot_count = 1  # Main price chart
            if show_rsi:
                subplot_count += 1
            if show_macd:
                subplot_count += 1
            if show_stoch:
                subplot_count += 1
            if show_williams:
                subplot_count += 1
            
            # Create subplot titles
            subplot_titles = [f"{symbol} - Technical Analysis"]
            if show_rsi:
                subplot_titles.append("RSI")
            if show_macd:
                subplot_titles.append("MACD")
            if show_stoch:
                subplot_titles.append("Stochastic")
            if show_williams:
                subplot_titles.append("Williams %R")
            
            # Create subplots
            fig = make_subplots(
                rows=subplot_count,
                cols=1,
                shared_xaxes=True,
                subplot_titles=subplot_titles,
                row_heights=[0.6] + [0.4/(subplot_count-1)]*(subplot_count-1) if subplot_count > 1 else [1.0],
                vertical_spacing=0.05
            )
            
            # Main candlestick chart
            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                name=symbol,
                increasing_line_color=self.colors['primary'],
                decreasing_line_color=self.colors['secondary']
            ), row=1, col=1)
            
            # Moving averages
            if show_ma:
                if 'sma_20' in data.columns:
                    fig.add_trace(go.Scatter(
                        x=data.index,
                        y=data['sma_20'],
                        mode='lines',
                        name='SMA 20',
                        line=dict(color='orange', width=1)
                    ), row=1, col=1)
                
                if 'sma_50' in data.columns:
                    fig.add_trace(go.Scatter(
                        x=data.index,
                        y=data['sma_50'],
                        mode='lines',
                        name='SMA 50',
                        line=dict(color='blue', width=1)
                    ), row=1, col=1)
            
            # Bollinger Bands
            if show_bollinger and 'bb_upper' in data.columns:
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['bb_upper'],
                    mode='lines',
                    name='BB Upper',
                    line=dict(color='gray', width=1, dash='dash'),
                    showlegend=False
                ), row=1, col=1)
                
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['bb_lower'],
                    mode='lines',
                    name='BB Lower',
                    line=dict(color='gray', width=1, dash='dash'),
                    fill='tonexty',
                    fillcolor='rgba(128,128,128,0.1)',
                    showlegend=False
                ), row=1, col=1)
            
            current_row = 2
            
            # RSI
            if show_rsi and 'rsi' in data.columns:
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['rsi'],
                    mode='lines',
                    name='RSI',
                    line=dict(color=self.colors['primary'], width=2)
                ), row=current_row, col=1)
                
                # RSI levels
                fig.add_hline(y=70, line_dash="dash", line_color="red", 
                             annotation_text="Overbought", row=current_row)
                fig.add_hline(y=30, line_dash="dash", line_color="green", 
                             annotation_text="Oversold", row=current_row)
                
                current_row += 1
            
            # MACD
            if show_macd and 'macd' in data.columns:
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['macd'],
                    mode='lines',
                    name='MACD',
                    line=dict(color='blue', width=2)
                ), row=current_row, col=1)
                
                if 'macd_signal' in data.columns:
                    fig.add_trace(go.Scatter(
                        x=data.index,
                        y=data['macd_signal'],
                        mode='lines',
                        name='Signal',
                        line=dict(color='red', width=1)
                    ), row=current_row, col=1)
                
                if 'macd_histogram' in data.columns:
                    fig.add_trace(go.Bar(
                        x=data.index,
                        y=data['macd_histogram'],
                        name='Histogram',
                        marker_color='green',
                        opacity=0.5
                    ), row=current_row, col=1)
                
                current_row += 1
            
            # Stochastic
            if show_stoch and 'stoch_k' in data.columns:
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['stoch_k'],
                    mode='lines',
                    name='%K',
                    line=dict(color='blue', width=2)
                ), row=current_row, col=1)
                
                if 'stoch_d' in data.columns:
                    fig.add_trace(go.Scatter(
                        x=data.index,
                        y=data['stoch_d'],
                        mode='lines',
                        name='%D',
                        line=dict(color='red', width=1)
                    ), row=current_row, col=1)
                
                current_row += 1
            
            # Williams %R
            if show_williams and 'williams_r' in data.columns:
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['williams_r'],
                    mode='lines',
                    name='Williams %R',
                    line=dict(color='purple', width=2)
                ), row=current_row, col=1)
                
                fig.add_hline(y=-20, line_dash="dash", line_color="red", row=current_row)
                fig.add_hline(y=-80, line_dash="dash", line_color="green", row=current_row)
            
            fig.update_layout(
                template=self.theme,
                height=200 * subplot_count + 100,
                hovermode='x unified',
                xaxis_rangeslider_visible=False
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating technical chart: {str(e)}")
            return go.Figure()
