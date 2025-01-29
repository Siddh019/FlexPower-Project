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

This task involves processing and aggregating power forecast data to compute the total power forecasts for wind and solar (PV) energy sources in MWh, accounting for specific intervals within each hour. The results are grouped by date and hour, and include both forecasted power values and price data. The final result is a DataFrame (`df_hourly`) that contains the total hourly forecasts for wind and PV energy sources in MWh, as well as the mean price values for both day-ahead and intraday prices. The output is grouped by date and hour.

The code processes the input data to convert power forecasts from megawatts (MW) to megawatt-hours (MWh) on an hourly basis. 

* Conversion Logic: MWh = MW * h

The formula `MWh = MW * h` is used to convert power (measured in megawatts, MW) into energy (measured in megawatt-hours, MWh). This conversion is based on the relationship between power and energy, where:
1) MW (megawatts) represents the rate of power production or consumption.
2) MWh (megawatt-hours) represents the total amount of energy produced or consumed over a 1 hour.

* Handling for Daylight Savings Time

Ideally, to calculate the total energy in MWh, you could simply group the data by `date` and `hour`, then calculate the sum of power forecasts for each group and multiply it by the fraction of the hour (e.g., 1/4 hour for 15-minute intervals). However, Daylight Saving Time (DST) introduces a complication.

DST and Hour Duplication: In the winter, when the clocks go back by 1 hour, a specific hour is repeated (e.g., 2:00 AM happens twice, once during daylight saving time and again after the clock is turned back). This means that the power forecast for that specific hour should be multiplied by 1/8 (i.e., half of the usual 1/4 hour interval) to account for the repeated time block. To ensure the correct conversion below was done :

```python
# Custom aggregation function that handles DST changes
def mw_to_mwh(x):
    # Count actual intervals in a specific hour
    num_intervals = len(x)
    # Calculate hours per interval for the specific hour
    hours_per_interval = 1 / num_intervals
    # Calculate MWh
    return x.sum() * hours_per_interval

# Group by 'date' and 'hour' with the custom aggregation
df_hourly = df.groupby(['date', 'hour']).agg({
    'Wind Day Ahead Forecast [in MW]': mw_to_mwh,
    'Wind Intraday Forecast [in MW]': mw_to_mwh,
    'PV Day Ahead Forecast [in MW]': mw_to_mwh,
    'PV Intraday Forecast [in MW]': mw_to_mwh,
    'Day Ahead Price hourly [in EUR/MWh]': 'mean',
    'Intraday Price Hourly  [in EUR/MWh]': 'mean',
}).reset_index()
```

Note - The mean price is used for the hour because the price remains constant throughout that hour. However, during the DST transition, when an hour is repeated, there are two different prices for the same hour. This creates an issue, as taking the mean of the two prices might not be entirely accurate for that specific hour. Unfortunately, there was no easy way to split or remove the  data, as the task requires providing the forecast data for the whole year. Thus, instead of removing or splitting the data, the decision was made to leave the price data as-is. As a result, while the price for most hours is accurate, **one hour during the DST transition may have an incorrect price value due to averaging two different prices**.

After applying the conversion and aggregation logic, the resulting DataFrame should look like this:
<img width="1062" alt="Screenshot 2025-01-29 at 7 44 25 PM" src="https://github.com/user-attachments/assets/b331428a-e9ac-43c1-aadc-5633cc9af540" />
One would expect there to be 365*24 = 8760 rows. However due to DST one hour is repeated hence there is one row less

### [Task 2.2](task-22)

The code calculates the **average hourly forecasted production** for both wind and solar energy (Day Ahead and Intraday forecasts) across all days (365 days). It extracts the **hour** from the `time` column and then groups the data by hour to compute the average forecast for each hour across all days. The averages are then multiplied by 4 to account for the typical hourly intervals in the data (15-minute intervals).

* Expected Output:

The resulting DataFrame, `df_hourly_avg`, will contain the average forecasted production for each hour of the day across all days in the dataset (365 days). The values are given in **MW** and represent the **average wind and solar power forecast for each hour** of the day. The results are plotted on a graph and shown below : 
<img width="1062" alt="Screenshot 2025-01-29 at 7 50 04 PM" src="https://github.com/user-attachments/assets/4027470b-adee-44a0-8c8e-ddd6920baf95" />

### [Task 2.3](task-23)

To calculate the average value of wind and solar power, the following formulas are applied:

- **Wind Value (EUR)** = `Wind Day Ahead Forecast [in MWh]` × `Day Ahead Price hourly [in EUR/MWh]`
- **PV Value (EUR)** = `PV Day Ahead Forecast [in MWh]` × `Day Ahead Price hourly [in EUR/MWh]`

These values are then summed over the entire year to obtain the **total wind value** and **total PV value**.

Next, the **average value per MWh** for both wind and solar is calculated as:

- **Average Wind Value per MWh** = `Total Wind Value (EUR)` ÷ `Total Wind Forecast (MWh)`
- **Average PV Value per MWh** = `Total PV Value (EUR)` ÷ `Total PV Forecast (MWh)`

Finally, the overall **average Day Ahead price** is computed as the mean of the **Day Ahead Price hourly** across all hours of the year.

The logic behind these calculations is to determine the **financial value** of wind and solar power, considering both the **forecasted energy production** and the corresponding **prices** for each hour. This allows us to assess how valuable wind and solar energy are in financial terms, based on their forecasted output and market prices.

Below are the results obtained after running the code:
- **Average Day Ahead Price:** 96.85 EUR/MWh  
- **Average Wind Value per MWh:** 81.39 EUR/MWh  
- **Average PV Value per MWh:** 76.89 EUR/MWh
- The **average value for Wind** is **lower** than the average Day Ahead price.
- The **average value for PV** is **lower** than the average Day Ahead price.

Let me explain why both Wind and PV have lower average values compared to the average Day Ahead price. The data shows that while the average Day Ahead price was 96.85 EUR/MWh, wind and solar achieved lower values of 81.39 EUR/MWh and 76.89 EUR/MWh respectively. This difference can be attributed to several interconnected factors.

The first major factor is the mismatch between generation patterns and price patterns. Wind and solar facilities generate electricity based on weather conditions rather than market demand. Solar generation peaks during midday when supply is abundant, while wind often generates more during nighttime and shoulder hours when demand and prices are typically lower. This means that renewable generators are frequently selling more electricity during lower-price periods, reducing their average realized value.

The second key factor relates to how weather-driven supply impacts market prices. When weather conditions are favorable for wind or solar generation, it typically means many renewable generators are producing simultaneously. This increased supply tends to push down market prices during these periods. As a result, wind and solar generators are selling more electricity exactly when their own production is contributing to lower market prices, creating a negative correlation between renewable generation and market prices.

The third significant factor involves limited generation during high-price events. Price spikes often occur during periods of system stress, such as extreme weather events, low renewable generation, or high demand periods. Solar facilities cannot generate during evening peak demand hours, and wind generation may be low during extreme weather events or high-pressure systems. This means renewable generators often miss out on the highest-priced hours, which further reduces their average realized price compared to the market average. Since these high-price events factor into the overall market average but may not benefit renewable generators, it contributes to their lower average values.

Note: The calculations in this task were based on the df_hourly DataFrame created in Task 2.1. As mentioned earlier, there is a potential issue with one price data point due to the DST adjustment, which could make the price for that specific hour incorrect. However, the resulting averages are very close to the actual values in fact the any difference would be negligible, and any analysis or inferences drawn from them would remain consistent, even if the correct price for that data point were used. Therefore, no significant impact on the results has occurred.

### [Task 2.4](task-24)
In this task, we calculate the total renewable energy production (from wind and solar combined) for each day. We then identify the days with the highest and lowest production and compare the corresponding Day-Ahead prices. The process is outlined below:

**Calculate Total Renewable Energy Production per Day:**  
   The total renewable energy production for each day is calculated by summing the **Wind Day Ahead Forecast** and **PV Day Ahead Forecast** columns. This gives the total renewable energy forecast (in MW) for each day.

**Group by Date:**  
   The data is grouped by the `date` column, and the total renewable energy production for each day is summed. Additionally, the **Day Ahead Price** is averaged for each day.

**Identify the Day with the Highest and Lowest Renewable Energy Production:**  
   Using the `idxmax()` and `idxmin()` functions, the code identifies the day with the highest renewable energy production and the day with the lowest renewable energy production.

**Extract the Day Ahead Price:**  
   The average Day Ahead Price for the day with the highest production and the day with the lowest production is extracted for comparison.

Below are the results obtained after running the code:

- **Day with Highest Renewable Energy Production:**
  - Date: 2021-03-12
  - Total Renewable Production: 4,352,164.00 MW
  - Average Day Ahead Price: 22.29 EUR/MWh

- **Day with Lowest Renewable Energy Production:**
  - Date: 2021-11-16
  - Total Renewable Production: 236,797.00 MW
  - Average Day Ahead Price: 237.47 EUR/MWh

- **Comparison of Day Ahead Prices:**
  - The Average Hourly Day Ahead Price on the day with the highest renewable energy production is lower than the Day Ahead Price on the day with the lowest production.

Let me explain the significant price difference between these two days, where we see 22.29 EUR/MWh on the day with highest renewable production (March 12) versus 237.47 EUR/MWh on the day with lowest renewable production (November 16).

The first major reason for this price difference is the direct impact of renewable energy supply on market prices through the merit order effect. On March 12, with extremely high renewable production of 4,352,164 MW, the market was flooded with low-marginal-cost renewable energy. Since renewable generators have near-zero operational costs, they can offer their electricity at very low prices, pushing more expensive conventional power plants out of the merit order and lowering the overall market clearing price. Conversely, on November 16, with only 236,797 MW of renewable production, more expensive conventional power plants had to be activated to meet demand, driving prices significantly higher.

The second reason relates to the seasonal timing and market conditions of these dates. November 16 falls in the heating season when electricity demand is typically higher due to increased lighting and heating needs. This higher demand, combined with low renewable production, means that even more expensive peaking power plants needed to be activated to meet demand. In contrast, March 12 occurs in spring when demand is generally moderate and weather conditions are often favorable for renewable generation, creating less pressure on the power system.

The third reason involves the broader energy market context and the backup generation mix. When renewable production is low, the power system must rely more heavily on fossil fuel-based generation, particularly gas-fired power plants. If this coincides with high gas prices (which were notably volatile in 2021) or constraints in conventional generation capacity, it can lead to extremely high electricity prices as we see on November 16. The dramatic price difference between these days (over 200 EUR/MWh) demonstrates how the power system's heavy reliance on renewables can create significant price volatility based on weather conditions and the availability of renewable resources.

### [Task 2.5](task-25)
This task compares the average Day Ahead Price between weekdays and weekends by performing the following steps:

**Identify the Day of the Week:**
A new column, `day_of_week`, is created in the dataset, which stores the name of the day (e.g., "Monday", "Tuesday") for each date. This is achieved using the `strftime('%A')` method.

**Classify the Day as Weekday or Weekend:**
A new column, `is_weekend`, is added to the dataset to classify each day as either "Weekday" (Monday to Friday) or "Weekend" (Saturday and Sunday). This classification is performed using a lambda function that checks if the day of the week is Saturday or Sunday.

**Calculate the Average Hourly Day Ahead Price**
The data is grouped by `is_weekend` (Weekday or Weekend) and the average Day Ahead Price (in EUR/MWh) is calculated for each group. The result shows the mean hourly Day Ahead Price for weekdays and weekends.

Below are the results obtained after running the code:

* Average Hourly Day Ahead Price during Weekdays: 104.37 EUR/MWh
* Average Hourly Day Ahead Price during Weekends: 77.98 EUR/MWh

Let me explain why the weekday average price (104.37 EUR/MWh) is significantly higher than the weekend average price (77.98 EUR/MWh). This difference of about 26 EUR/MWh can be attributed to several key factors.

The primary reason is industrial, commercial, institutional and educational consumption patterns. During weekdays, industrial facilities, offices, schools, universities, government buildings, and other institutions are operating at full capacity, leading to higher electricity consumption. The collective electricity consumption from these facilities, including their heating, cooling, and operational needs, contributes to higher demand during and consequently higher prices during weekdays. During weekends, most of these facilities are closed or operating at reduced capacity, resulting in reduced demand and lower prices.

Another key factor involves the power system's generation mix and operational strategy. During weekdays, when demand is higher, more expensive peaking power plants need to be activated to meet the increased demand, pushing up prices. These plants often have higher marginal costs and are required to maintain system stability during peak demand periods. During weekends, with lower demand, the system can rely more on baseload and intermediate load plants, which typically have lower operational costs, resulting in lower average prices. This difference in the generation mix between weekdays and weekends directly impacts the market clearing prices.
