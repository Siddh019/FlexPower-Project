# FlexPower-Project
* [Background](#Background)
* [Solution](#Solution)
  * [Task 1: Minimal Reporting Tool](#task-1-minimal-reporting-tool)
     * [Task 1.1: Total Buy/Sell Volume Calculation](#task-11-total-buy-sell-volume-calculation)
     * [Task 1.2: Strategy PnL Calculation](#task-12-strategy-pnl-calculation)
     * [Task 1.3: API for Strategy PnL](#task-13-api-for-strategy-pnl)
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
