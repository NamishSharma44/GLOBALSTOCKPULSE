import pandas as pd
import numpy as np
import streamlit as st

class TechnicalAnalyzer:
    def __init__(self):
        pass
    
    def calculate_sma(self, data, window):
        """Simple Moving Average"""
        return data.rolling(window=window).mean()
    
    def calculate_ema(self, data, window):
        """Exponential Moving Average"""
        return data.ewm(span=window).mean()
    
    def calculate_rsi(self, data, window=14):
        """Relative Strength Index"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def calculate_macd(self, data, fast=12, slow=26, signal=9):
        """MACD Indicator"""
        ema_fast = self.calculate_ema(data, fast)
        ema_slow = self.calculate_ema(data, slow)
        macd = ema_fast - ema_slow
        macd_signal = self.calculate_ema(macd, signal)
        macd_histogram = macd - macd_signal
        return macd, macd_signal, macd_histogram
    
    def calculate_bollinger_bands(self, data, window=20, num_std=2):
        """Bollinger Bands"""
        sma = self.calculate_sma(data, window)
        std = data.rolling(window=window).std()
        upper_band = sma + (std * num_std)
        lower_band = sma - (std * num_std)
        return upper_band, sma, lower_band
    
    def calculate_stochastic(self, high, low, close, k_window=14, d_window=3):
        """Stochastic Oscillator"""
        lowest_low = low.rolling(window=k_window).min()
        highest_high = high.rolling(window=k_window).max()
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=d_window).mean()
        return k_percent, d_percent
    
    def calculate_williams_r(self, high, low, close, window=14):
        """Williams %R"""
        highest_high = high.rolling(window=window).max()
        lowest_low = low.rolling(window=window).min()
        williams_r = -100 * ((highest_high - close) / (highest_high - lowest_low))
        return williams_r
    
    def calculate_adx(self, high, low, close, window=14):
        """Average Directional Index"""
        # Calculate True Range
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # Calculate Directional Movement
        dm_plus = high - high.shift()
        dm_minus = low.shift() - low
        
        dm_plus = dm_plus.where((dm_plus > dm_minus) & (dm_plus > 0), 0)
        dm_minus = dm_minus.where((dm_minus > dm_plus) & (dm_minus > 0), 0)
        
        # Calculate smoothed values
        tr_smooth = tr.rolling(window=window).mean()
        dm_plus_smooth = dm_plus.rolling(window=window).mean()
        dm_minus_smooth = dm_minus.rolling(window=window).mean()
        
        # Calculate DI+ and DI-
        di_plus = 100 * (dm_plus_smooth / tr_smooth)
        di_minus = 100 * (dm_minus_smooth / tr_smooth)
        
        # Calculate ADX
        dx = 100 * abs(di_plus - di_minus) / (di_plus + di_minus)
        adx = dx.rolling(window=window).mean()
        
        return adx
    
    def calculate_support_resistance(self, data, window=20):
        """Calculate support and resistance levels"""
        # Simple approach using rolling min/max
        support = data['low'].rolling(window=window).min()
        resistance = data['high'].rolling(window=window).max()
        return support, resistance
    
    def calculate_all_indicators(self, data):
        """Calculate all technical indicators"""
        try:
            result = data.copy()
            
            # Moving averages
            result['sma_20'] = self.calculate_sma(data['close'], 20)
            result['sma_50'] = self.calculate_sma(data['close'], 50)
            result['ema_12'] = self.calculate_ema(data['close'], 12)
            result['ema_26'] = self.calculate_ema(data['close'], 26)
            
            # RSI
            result['rsi'] = self.calculate_rsi(data['close'])
            
            # MACD
            macd, macd_signal, macd_histogram = self.calculate_macd(data['close'])
            result['macd'] = macd
            result['macd_signal'] = macd_signal
            result['macd_histogram'] = macd_histogram
            
            # Bollinger Bands
            bb_upper, bb_middle, bb_lower = self.calculate_bollinger_bands(data['close'])
            result['bb_upper'] = bb_upper
            result['bb_middle'] = bb_middle
            result['bb_lower'] = bb_lower
            
            # Stochastic
            stoch_k, stoch_d = self.calculate_stochastic(data['high'], data['low'], data['close'])
            result['stoch_k'] = stoch_k
            result['stoch_d'] = stoch_d
            
            # Williams %R
            result['williams_r'] = self.calculate_williams_r(data['high'], data['low'], data['close'])
            
            # ADX
            result['adx'] = self.calculate_adx(data['high'], data['low'], data['close'])
            
            # Support and Resistance
            support, resistance = self.calculate_support_resistance(data)
            result['support'] = support
            result['resistance'] = resistance
            
            return result
            
        except Exception as e:
            st.error(f"Error calculating technical indicators: {str(e)}")
            return data
    
    def get_technical_summary(self, technical_data):
        """Generate technical analysis summary"""
        try:
            if technical_data.empty:
                return {}
            
            latest = technical_data.iloc[-1]
            
            # RSI analysis
            rsi_current = latest.get('rsi', 50)
            if rsi_current > 70:
                rsi_signal = "Overbought"
            elif rsi_current < 30:
                rsi_signal = "Oversold"
            else:
                rsi_signal = "Neutral"
            
            # MACD analysis
            macd_current = latest.get('macd', 0)
            macd_signal_current = latest.get('macd_signal', 0)
            if macd_current > macd_signal_current:
                macd_signal = "Bullish"
            elif macd_current < macd_signal_current:
                macd_signal = "Bearish"
            else:
                macd_signal = "Neutral"
            
            # Trend analysis (using moving averages)
            price_current = latest.get('close', 0)
            sma_20 = latest.get('sma_20', 0)
            sma_50 = latest.get('sma_50', 0)
            
            if price_current > sma_20 > sma_50:
                trend_signal = "Strong Uptrend"
            elif price_current > sma_20:
                trend_signal = "Uptrend"
            elif price_current < sma_20 < sma_50:
                trend_signal = "Strong Downtrend"
            elif price_current < sma_20:
                trend_signal = "Downtrend"
            else:
                trend_signal = "Sideways"
            
            # Volume analysis
            if len(technical_data) > 1:
                avg_volume = technical_data['volume'].rolling(window=20).mean().iloc[-1]
                current_volume = latest.get('volume', 0)
                if current_volume > avg_volume * 1.5:
                    volume_signal = "High Volume"
                elif current_volume < avg_volume * 0.5:
                    volume_signal = "Low Volume"
                else:
                    volume_signal = "Normal Volume"
            else:
                volume_signal = "Normal Volume"
            
            # Bollinger Band position
            bb_upper = latest.get('bb_upper', 0)
            bb_lower = latest.get('bb_lower', 0)
            if price_current > bb_upper:
                bollinger_position = "Above Upper Band"
            elif price_current < bb_lower:
                bollinger_position = "Below Lower Band"
            else:
                bollinger_position = "Within Bands"
            
            # Overall signal
            bullish_signals = 0
            bearish_signals = 0
            
            if rsi_signal == "Oversold":
                bullish_signals += 1
            elif rsi_signal == "Overbought":
                bearish_signals += 1
            
            if macd_signal == "Bullish":
                bullish_signals += 1
            elif macd_signal == "Bearish":
                bearish_signals += 1
            
            if "Uptrend" in trend_signal:
                bullish_signals += 1
            elif "Downtrend" in trend_signal:
                bearish_signals += 1
            
            if bullish_signals > bearish_signals:
                overall_signal = "Bullish - Consider buying on dips"
            elif bearish_signals > bullish_signals:
                overall_signal = "Bearish - Consider selling on rallies"
            else:
                overall_signal = "Neutral - Wait for clearer signals"
            
            return {
                'rsi_current': rsi_current,
                'rsi_signal': rsi_signal,
                'macd_signal': macd_signal,
                'trend_signal': trend_signal,
                'volume_signal': volume_signal,
                'bollinger_position': bollinger_position,
                'momentum_signal': rsi_signal,
                'overall_signal': overall_signal
            }
            
        except Exception as e:
            st.error(f"Error generating technical summary: {str(e)}")
            return {}
