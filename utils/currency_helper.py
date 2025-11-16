class CurrencyHelper:
    """Helper class for currency formatting based on market"""
    
    MARKET_CURRENCIES = {
        "US": {"symbol": "$", "code": "USD", "name": "US Dollar"},
        "IN": {"symbol": "₹", "code": "INR", "name": "Indian Rupee"},
        "CN": {"symbol": "¥", "code": "CNY", "name": "Chinese Yuan"},
        "EU": {"symbol": "€", "code": "EUR", "name": "Euro"},
        "HK": {"symbol": "HK$", "code": "HKD", "name": "Hong Kong Dollar"},
        "JP": {"symbol": "¥", "code": "JPY", "name": "Japanese Yen"},
        "CA": {"symbol": "C$", "code": "CAD", "name": "Canadian Dollar"},
        "AU": {"symbol": "A$", "code": "AUD", "name": "Australian Dollar"}
    }
    
    @staticmethod
    def get_currency_symbol(market_code):
        """Get currency symbol for a market"""
        return CurrencyHelper.MARKET_CURRENCIES.get(market_code, {}).get("symbol", "$")
    
    @staticmethod
    def get_currency_code(market_code):
        """Get currency code for a market"""
        return CurrencyHelper.MARKET_CURRENCIES.get(market_code, {}).get("code", "USD")
    
    @staticmethod
    def get_currency_name(market_code):
        """Get currency name for a market"""
        return CurrencyHelper.MARKET_CURRENCIES.get(market_code, {}).get("name", "US Dollar")
    
    @staticmethod
    def format_price(price, market_code, decimals=2):
        """Format price with appropriate currency symbol"""
        symbol = CurrencyHelper.get_currency_symbol(market_code)
        
        # For Japanese Yen, use 0 decimals (no cents)
        if market_code == "JP":
            return f"{symbol}{price:,.0f}"
        
        return f"{symbol}{price:,.{decimals}f}"
    
    @staticmethod
    def format_with_code(price, market_code, decimals=2):
        """Format price with currency code"""
        code = CurrencyHelper.get_currency_code(market_code)
        
        if market_code == "JP":
            return f"{price:,.0f} {code}"
        
        return f"{price:,.{decimals}f} {code}"