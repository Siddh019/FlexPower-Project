# FlexPower-Project
* [Background](#Background)
* [Solution](#Solution)
  * [Task 1: Minimal Reporting Tool](#task-1-minimal-reporting-tool)
     * [Task 1.1](#task-11)
     * [Task 1.2](#task-12)
     * [Task 1.3](#task-13)
  * [Task 2: Data Analysis and Building a Trading Strategy](#task-2-data-analysis-and-building-a-trading-strategy)
     * [Task 2.1: Wind/PV Power Forecast Analysis](#task-21-windpv-power-forecast-analysis)
     * [Task 2.2: Average Wind/Solar Production over 24 Hours](#task-22-average-windsolar-production-over-24-hours)
     * [Task 2.3: Average Value of Wind/Solar Power](#task-23-average-value-of-windsolar-power)
     * [Task 2.4: Days with Highest and Lowest Renewable Energy Production](#task-24-days-with-highest-and-lowest-renewable-energy-production)
     * [Task 2.5: Weekday vs Weekend Price Analysis](#task-25-weekday-vs-weekend-price-analysis)
     * [Task 2.6: Battery Revenue Calculation](#task-26-battery-revenue-calculation)
     * [Task 2.7: Trading Strategy Development](#task-27-trading-strategy-development)

## Background
This repo consists of solutions for the tasks in [**FlexPower QuantChallenge**](https://github.com/FlexPwr/QuantChallenge). Below are descriptions of each task. 
* Task 1
  * Task 1.1: Write functions that compute total buy volume and total sell volume.
  * Task 1.2: Write functions that compute the Profit and Loss for each strategy (PnL)
  * Task 1.3: Expose the function written in task 1.2 as an entrypoint of a web application

For this task, I used the following Python packages - pandas (for data manipulation and analysis), sqlite3 (for interacting with the SQLite database), and Flask (for creating the API). Hence, installing these packages is a necessary for running the code.

* Task 2
  * Task 2.1: Aggregate energy forecasts and prices by date and hour, converting MW values to MWh.
  * Task 2.2: Calculate the average hourly wind/solar production across all days
  * Task 2.3: Calculate the average value of wind/solar Power
  * Task 2.4: Find the day with the highest and the day with the lowest renewable energy production
  * Task 2.5: Calculate weekend vs weekday average prices
  * Task 2.6: Optimise the revenue from battery charging and discharging
  * Task 2.7: Create a trading strategy and display it's perfomance

For this task, I used the following Python packages - pandas (for data manipulation and analysis), numpy (for numerical operations), matplotlib (for visualizations), sklearn (for machine learning models and metrics), datetime (for working with date and time), and statsmodels (for statistical modeling). Hence, installing these packages is necessary for running the code.
 
## Solution
###  [Task 1: Minimal Reporting Tool](#task-1-minimal-reporting-tool)
[Task_1.py](Task_1.py)
### [Task 1.1](#task-11)
The `Volume_Calculator` class is designed to calculate the total buy and sell volumes from a given trade dataset. Below is an overview of its functionality and an example usage.

* Calculates Total Buy Volume
  
The `Buy_Volume` method filters the DataFrame for rows where the `'side'` column is `'buy'` and sums the `'quantity'` values to return the total buy volume.

* Calculates Total Sell Volume
  
The `Sell_Volume` method filters the DataFrame for rows where the `'side'` column is `'sell'` and sums the `'quantity'` values to return the total sell volume.

* Example Usage with Error Handling
  
The example usage demonstrates how to load trade data from an SQLite database, initialize the `Volume_Calculator` with the data, calculate total buy and sell volumes, and print the results. It also includes error handling to catch issues with database queries or calculations (e.g., missing columns or data-related errors).

```python
# Example Usage
if __name__ == "__main__":
    try:
        # Load the trades data from the SQLite database into a Pandas DataFrame
        # The SQLite query pulls data from the 'epex_12_20_12_13' table
        trades_df = pd.read_sql("SELECT * FROM epex_12_20_12_13", 
                                "sqlite:///trades.sqlite")  # SQLite database path

        # Initialize the Volume_Calculator with the loaded DataFrame
        total_volume = Volume_Calculator(trades_df)

        # Calculate total buy and sell volumes
        total_buy_volume = total_volume.Buy_Volume()
        total_sell_volume = total_volume.Sell_Volume()

        # Output the results for verification
        print(f"Total buy volume: {total_buy_volume}")
        print(f"Total sell volume: {total_sell_volume}")
    
    except Exception as e:
        print(f"Error: {e}")  # Error handling for database or calculation issues
```
### [Task 1.2](#task-12)

The `compute_pnl` function calculates the profit and loss (PnL) for a given trading strategy based on trade data. Below is an overview of its functionality and an example usage.

* Filters Trades by Strategy

The function filters the DataFrame to include only trades that belong to the specified `strategy_id`. This ensures that the PnL calculation is specific to a particular strategy.

* Calculates PnL for Each Trade

The function uses a vectorized approach to calculate PnL for each trade. For 'sell' orders, the PnL is positive (profit), and for 'buy' orders, the PnL is negative (loss), based on the quantity and price of each trade.

* Example Usage with Error Handling

The example usage demonstrates how to load trade data from an SQLite database, compute the PnL for different strategies, and print the results. The function also handles errors related to reading the database or calculations.

```python
# Example Usage
if __name__ == "__main__":
    try:
        # Load the trades data from the SQLite database into a Pandas DataFrame
        trades_df = pd.read_sql("SELECT * FROM epex_12_20_12_13",
                                "sqlite:///trades.sqlite")  # SQLite database path
        
        # Compute the PnL for different strategies
        strategy_id = 'strategy_1'
        pnl_value = compute_pnl(strategy_id, trades_df)
        print(f"The PnL of {strategy_id} is: {pnl_value}")

        strategy_id = 'strategy_2'
        pnl_value = compute_pnl(strategy_id, trades_df)
        print(f"The PnL of {strategy_id} is: {pnl_value}")
    
    except Exception as e:
        print(f"Error reading data from SQLite: {e}")
```
### [Task 1.3](#task-13)
[Task_1.3.py](Task_1.3.py)

This project exposes a the function defined in Task 1.2 API using Flask. The PnL is calculated based on trade data from a SQLite database and can be accessed via a simple API endpoint. The API response specification were provided in 

* Calculate PnL for a Specific Strategy

The API endpoint `/pnl/<strategy_id>` calculates and returns the PnL for a given trading strategy. It uses the `compute_pnl` function to calculate the PnL based on the trade data stored in an SQLite database.

* JSON Response with PnL Data

The API responds with a JSON object containing the strategy ID, the calculated PnL value, the currency unit (euro), and the timestamp of the PnL calculation in ISO 8601 format.

* Error Handling and Database Connectivity

The API includes error handling for both database-related issues (e.g., SQLite errors) and unexpected errors. If an error occurs, the API responds with an appropriate error message and status code.

* Example Usage


