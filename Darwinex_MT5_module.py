#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import MetaTrader5 as mt5
from scipy.stats import kendalltau
pd.options.display.float_format = '{:.4f}'.format
from datetime import datetime, timedelta

class Darwinex:
    """
    A class to interact with MetaTrader5 for fetching and analyzing forex or stock data.
    """
    def __init__(self, start_time = None, lookback_days = 250, timeframe = mt5.TIMEFRAME_D1, end_time = None):
        """
        Initializes the Darwinex object with specified parameters for data retrieval.
        
        Args:
            start_time (datetime, optional): The start time from which to fetch historical data.
            lookback_days (int, optional): The number of days to look back from the end time. Default is 250 days.
            timeframe (MT5 constant, optional): The timeframe for which to fetch the data. Default is mt5.TIMEFRAME_D1 (daily).
            end_time (datetime, optional): The end time until which to fetch data. Defaults to the current datetime if None.
            end_time = datetime(2023, 1, 1)  # Set an end time, e.g., January 1, 2023
        """
        if end_time is None:
            self.end_time = datetime.now()
        else:
            self.end_time = end_time
        
        if start_time is None:
            self.start_time = self.end_time - timedelta(days = lookback_days)
        else:
            self.start_time = start_time
        
        self.lookback_days = lookback_days
        self.timeframe = timeframe
        self.symbols = self.market_watch_exclusions()

    @staticmethod
    def market_watch_exclusions(*exclusions):
        """
        Generates a list of market symbols that are not in the exclusions list.
        
        Args:
            *exclusions (str): Symbols to exclude from the retrieval.
        
        Returns:
            list: List of non-excluded symbol objects.
        """
        exclusion_filter = "*,!" + ",!*".join(exclusions)
        symbols = mt5.symbols_get(group = exclusion_filter)
        return symbols
    
    
    def get_historical_data(self, symbols, period = False):
        """
        Retrieves historical data for the given symbols.
        
        Args:
            symbols (list): A list of symbol objects for which to fetch historical data.
        
        Returns:
            dict: A dictionary where keys are symbols and values are DataFrames containing 'close' prices and 'log_returns'.
        """
        symbol_names = [symbol.name for symbol in symbols] 
        historical_data = {}
        if period == True:
            for symbol in symbol_names:
                rates = mt5.copy_rates_range(symbol, self.timeframe, self.start_time, self.end_time)
                if rates is not None and len(rates) > 0:
                    df = pd.DataFrame(rates)
                    df['time'] = pd.to_datetime(df['time'], unit='s')
                    df.set_index('time', inplace=True)
                    df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
                    historical_data[symbol] = df[['close', 'log_returns']]
            return historical_data
        else:
            for symbol in symbol_names:
                rates = mt5.copy_rates_from(symbol, self.timeframe, self.start_time, 100000)
                if rates is not None and len(rates) > 0:
                    df = pd.DataFrame(rates)
                    df['time'] = pd.to_datetime(df['time'], unit='s')
                    df.set_index('time', inplace=True)
                    df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
                    historical_data[symbol] = df[['close', 'log_returns']]
            return historical_data
            
