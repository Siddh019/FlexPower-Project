# FlexPower-Project
* [Background](#Background)
* [Solution](#Solution)
  * [Task 1: Minimal Reporting Tool](#task-1-minimal-reporting-tool)
     * [Task 1.1](#task-11)
     * [Task 1.2](#task-12)
     * [Task 1.3](#task-13)
  * [Task 2: Data Analysis and Building a Trading Strategy](#task-2-data-analysis-and-building-a-trading-strategy)
     * [Task 2.1](#task-21)
     * [Task 2.2](#task-22)
     * [Task 2.3](#task-23)
     * [Task 2.4](#task-24)
     * [Task 2.5](#task-25)
     * [Task 2.6](#task-26)
     * [Task 2.7](#task-27)

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

This project exposes a the function defined in Task 1.2 API using Flask. The PnL is calculated based on trade data from a SQLite database and can be accessed via a simple API endpoint. 

* Calculate PnL for a Specific Strategy

The API endpoint `/pnl/<strategy_id>` calculates and returns the PnL for a given trading strategy. It uses the `compute_pnl` function to calculate the PnL based on the trade data stored in an SQLite database.

* JSON Response with PnL Data

The API responds with a JSON object containing the strategy ID, the calculated PnL value, the currency unit (euro), and the timestamp of the PnL calculation in ISO 8601 format. 

* Response Data Specification

We define the specification of the response data using a fuction, which specifies the structure and type of the response fields. The specification is used to define the expected response from the API. 

* Example Usage

Open your terminal and run the file [Task_1.3.py](Task_1.3.py). You should get an expected output as below: 

<img width="603" alt="Screenshot 2025-01-29 at 7 06 33 PM" src="https://github.com/user-attachments/assets/a8cfda40-e59e-4239-a74e-ce146c159a77" />


Copy, Paste the website on your browser and you should hopefully get the desired result. 

Note: Due to some technical difficulties (i.e., a bug), I am currently unable to run the Flask app on my laptop. The output shown in the picture was generated on a friend's laptop. However, he didn't copy and paste the link into his browser, so I’m unable to confirm the exact output. Nevertheless, I am confident that the code produces the expected result, despite not being able to verify it directly due to these unfortunate circumstances.

### [Task 2: Data Analysis and Building a Trading Strategy](#task-2-data-analysis-and-building-a-trading-strategy)
[Task_2.py](Task_2.py)
### [Task 2.1](task-21)
# Task 2.1 - Total Power Forecast Calculator

This task involves processing and aggregating power forecast data to compute the total power forecasts for wind and solar (PV) energy sources in MWh, accounting for specific intervals within each hour. The results are grouped by date and hour, and include both forecasted power values and price data. The final result is a DataFrame (`df_hourly`) that contains the total hourly forecasts for wind and PV energy sources in MWh, as well as the mean price values for both day-ahead and intraday prices. The output is grouped by date and hour.

The code processes the input data to convert power forecasts from megawatts (MW) to megawatt-hours (MWh) on an hourly basis. 

* Conversion Logic: MWh = MW * h

The formula `MWh = MW * h` is used to convert power (measured in megawatts, MW) into energy (measured in megawatt-hours, MWh). This conversion is based on the relationship between power and energy, where:

 1) MW (megawatts) represents the rate of power production or consumption.
 2) MWh (megawatt-hours) represents the total amount of energy produced or consumed over a 1 hour.


## 2. **Convert Time Column into Date and Hour**

The first step involves converting the 'time' column into a `datetime` format, then extracting the `date` and `hour` components.

```python
# Convert the 'hour' column into a datetime format (if not already in datetime format)
df['time'] = pd.to_datetime(df['time'], format='%d/%m/%y %H:%M')

# Extract the 'hour' and 'date' from the 'time' column
df['date'] = df['time'].dt.date  # Extract just the date part (YYYY-MM-DD)
df['hour'] = df['time'].dt.hour  # Extract the hour part (0-23)


