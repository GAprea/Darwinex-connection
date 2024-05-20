# Darwinex MT5 Data Handler

## Overview
The Darwinex MT5 Data Handler is a Python module designed for fetching and analyzing historical forex and stock market data using the MetaTrader5 (MT5) platform. It allows users to retrieve historical price data and compute log returns for a specified timeframe and set of symbols.

## Features
- **Historical Data Retrieval**: Fetch historical data based on custom timeframes, from daily to minutes.
- **Customizable Lookback Periods**: Define the period over which historical data should be retrieved.
- **Exclusion of Specific Symbols**: Ability to exclude certain symbols from data retrieval.
- **Computation of Log Returns**: Automatically compute log returns for analysis.

## Installation

Before using the Darwinex MT5 Data Handler, ensure you have Python installed on your system. You also need to have MetaTrader5 installed and set up. You can install the required Python libraries using pip:

```bash
pip install pandas numpy matplotlib MetaTrader5 scipy
```

## Usage

### Initialization
Create an instance of the `Darwinex` class by specifying the start time, end time, timeframe, and any exclusions. This setup allows you to customize the parameters according to your data retrieval needs.

```python
from Darwinex import Darwinex
from datetime import datetime

# Initialize Darwinex with specific parameters
darwinex = Darwinex(start_time = datetime(2024, 1, 1),timeframe=mt5.TIMEFRAME_M5)  
excluded_symbols = darwinex.market_watch_exclusions("EURUSD", "GBPUSD", "EURGBP")
Fetch Data
Use the get_historical_data method to retrieve data for specific symbols. This method returns a dictionary where each key is a symbol and the value is a DataFrame containing the close prices and log returns.
# Fetch historical data for specified symbols
historical_data = darwinex.get_historical_data(excluded_symbols)
Data Analysis
Use the fetched data for further financial analysis, including computing log returns and visualizing data trends. Here's how you can compute log returns and plot closing prices:
import matplotlib.pyplot as plt

# Assuming data for 'AAPL' is available
aapl_data = historical_data.get('AAPL')
if aapl_data is not empty:
    # Plot closing prices
    aapl_data['close'].plot(title='AAPL Closing Prices')
    plt.show()

    # Display log returns
    print(aapl_data['log_returns'])
