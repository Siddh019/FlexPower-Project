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
This repo consists of solutions for the tasks in [**FlexPower QuantChallenge**](https://github.com/FlexPwr/QuantChallenge). Below are simple descriptions of each task. 
* Task 1: Write two functions for compute buy and sell total volume each.
* Task 2: Write a function computing Profit and Loss for each strategy (PnL)
* Task 3: Expose the function written in task 2 as an entrypoint of a web application

Here, I mostly used Python packages [sqlite3](https://docs.python.org/3/library/sqlite3.html) (task 1 & 2), [flask_restx](https://flask-restx.readthedocs.io/en/latest/) (task 3). Therefore, installing these packages is a prerequisite. 

## Solution
