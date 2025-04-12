# AI generated and maintained by Claude 3.7 Sonnet
# This file provides currency formatting utilities
# License: MIT

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def format_currency(amount: float, currency: str, config: Dict[str, Any]) -> str:
    """Format a currency amount according to the configuration.
    
    Args:
        amount: The amount to format
        currency: The currency code (e.g., 'CAD', 'USD')
        config: The currency formatting configuration from config.yml
        
    Returns:
        Formatted currency string
    """
    try:
        # Get currency formatting settings
        formatting = config.get('currency_formatting', {}).get(currency, {})
        symbol = formatting.get('symbol', '$')
        position = formatting.get('position', 'before')
        decimal_places = formatting.get('decimal_places', 2)
        
        # Format the number
        formatted_amount = f"{abs(amount):.{decimal_places}f}"
        
        # Add the symbol
        if position == 'before':
            formatted = f"{symbol}{formatted_amount}"
        else:
            formatted = f"{formatted_amount}{symbol}"
            
        # Add sign if needed
        if amount < 0:
            formatted = f"-{formatted}"
            
        return formatted
    except Exception as e:
        logger.error(f"Error formatting currency {amount} {currency}: {e}", exc_info=True)
        # Fallback to simple formatting
        return f"{currency} {amount:.2f}"

def get_currency_columns(config: Dict[str, Any]) -> Dict[str, str]:
    """Get the currency column mapping from the configuration.
    
    Args:
        config: The configuration dictionary
        
    Returns:
        Dictionary mapping currency codes to column names
    """
    return config.get('currency_columns', {'CAD': 'CAD$'})

def get_currency_priority(config: Dict[str, Any]) -> List[str]:
    """Get the currency priority list from the configuration.
    
    Args:
        config: The configuration dictionary
        
    Returns:
        List of currency codes in priority order
    """
    return config.get('currency_priority', ['CAD'])

def get_default_currency(config: Dict[str, Any]) -> str:
    """Get the default currency from the configuration.
    
    Args:
        config: The configuration dictionary
        
    Returns:
        Default currency code
    """
    return config.get('default_currency', 'CAD') 