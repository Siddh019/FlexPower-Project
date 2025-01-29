import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ## Task 2: Data analysis and building a trading strategy

raw_data = pd.read_excel('analysis_task_data.xlsx')
df = raw_data

num_rows = df.shape[0]
num_cols = df.shape[1]

print("Number of rows:", num_rows)
print("Number of columns:", num_cols)
print()  

# ### Task 2.1 - Total Power Forecast Calculator

# Convert the 'hour' column into a datetime format (if not already in datetime format)
df['time'] = pd.to_datetime(df['time'], format='%d/%m/%y %H:%M')

# Extract the 'hour' and 'date' from the 'time' column
df['date'] = df['time'].dt.date  # Extract just the date part (YYYY-MM-DD)
df['hour'] = df['time'].dt.hour  # Extract the hour part (0-23)

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

# Rename columns to reflect MWh units
new_columns = {
    'Wind Day Ahead Forecast [in MW]': 'Wind Day Ahead Forecast [in MWh]',
    'Wind Intraday Forecast [in MW]': 'Wind Intraday Forecast [in MWh]',
    'PV Day Ahead Forecast [in MW]': 'PV Day Ahead Forecast [in MWh]',
    'PV Intraday Forecast [in MW]': 'PV Intraday Forecast [in MWh]'
}
df_hourly = df_hourly.rename(columns=new_columns)

# Print the results
print("Task 2.1 - Total Power Forecast Calculator Results:")
print(df_hourly)
print()  

# ### Task 2.2 - Average Hourly Wind/Solar production

# Extract the hour from the 'date' column
df['hour'] = df['time'].dt.hour

# Calculate the average for each hour across all days (365 days)
df_hourly_avg = df.groupby('hour').agg({
    'Wind Day Ahead Forecast [in MW]': lambda x: x.mean() * 4,
    'Wind Intraday Forecast [in MW]': lambda x: x.mean() * 4,
    'PV Day Ahead Forecast [in MW]': lambda x: x.mean() * 4,
    'PV Intraday Forecast [in MW]': lambda x: x.mean() * 4,
}).reset_index()

# Print the results
print("Task 2.2 - Average Hourly Wind/Solar Production Results:")
print(df_hourly_avg)
print()  

# ### Task 2.3 - Average Value of Wind/Solar Power

# Calculate the value in EUR for Wind and PV
df_hourly['Wind Value (EUR)'] = df_hourly['Wind Day Ahead Forecast [in MWh]'] * df_hourly['Day Ahead Price hourly [in EUR/MWh]'] 
df_hourly['PV Value (EUR)'] = df_hourly['PV Day Ahead Forecast [in MWh]'] * df_hourly['Day Ahead Price hourly [in EUR/MWh]'] 

# Sum the total value (in EUR) for Wind and PV for the entire year
total_wind_value = df_hourly['Wind Value (EUR)'].sum()
total_pv_value = df_hourly['PV Value (EUR)'].sum()

# Sum the total forecasted power for Wind and PV for the entire year
total_wind_forecast = df_hourly['Wind Day Ahead Forecast [in MWh]'].sum()
total_pv_forecast = df_hourly['PV Day Ahead Forecast [in MWh]'].sum()

# Calculate the average value (in EUR/MWh) for Wind and PV
avg_wind_value_per_mwh = total_wind_value / total_wind_forecast
avg_pv_value_per_mwh = total_pv_value / total_pv_forecast

# Calculate the overall average Day Ahead price
avg_da_price = df_hourly['Day Ahead Price hourly [in EUR/MWh]'].mean()

# Print the results
print("Task 2.3 - Average Value of Wind/Solar Power Results:")
print(f"Average Day Ahead Price: {avg_da_price:.2f} EUR/MWh")
print(f"Average Wind Value per MWh: {avg_wind_value_per_mwh:.2f} EUR/MWh")
print(f"Average PV Value per MWh: {avg_pv_value_per_mwh:.2f} EUR/MWh")

# Comparing average Wind/PV value with the average DA price
if avg_wind_value_per_mwh > avg_da_price:
    print("The average value for Wind is higher than the average DA price.")
else:
    print("The average value for Wind is lower than the average DA price.")

if avg_pv_value_per_mwh > avg_da_price:
    print("The average value for PV is higher than the average DA price.")
else:
    print("The average value for PV is lower than the average DA price.")
    
print()  

# ### Task 2.4 - Day with Highest and Lowest Renewable Energy Production

# Calculate total renewable energy production for each day
df['Total Renewable Day Ahead Forecast (MW)'] = (df['Wind Day Ahead Forecast [in MW]'] + df['PV Day Ahead Forecast [in MW]'])

# Group by date and calculate the total renewable energy production for each day
df_daily = df.groupby('date').agg({
    'Total Renewable Day Ahead Forecast (MW)': 'sum',
    'Day Ahead Price hourly [in EUR/MWh]': 'mean'
}).reset_index()

# Find the day with the highest and lowest renewable energy production
max_renewable_day = df_daily.loc[df_daily['Total Renewable Day Ahead Forecast (MW)'].idxmax()]
min_renewable_day = df_daily.loc[df_daily['Total Renewable Day Ahead Forecast (MW)'].idxmin()]

# Extract the average Day Ahead Price for these days
max_renewable_day_price = max_renewable_day['Day Ahead Price hourly [in EUR/MWh]']
min_renewable_day_price = min_renewable_day['Day Ahead Price hourly [in EUR/MWh]']

# Print the results
print("Task 2.4 - Day with Highest and Lowest Renewable Energy Production Results:")
print(f"Day with Highest Renewable Energy Production: {max_renewable_day['date']}")
print(f"Total Renewable Production on this day: {max_renewable_day['Total Renewable Day Ahead Forecast (MW)']:.2f} MW")
print(f"Average Day Ahead Price on this day: {max_renewable_day_price:.2f} EUR/MWh\n")

print(f"Day with Lowest Renewable Energy Production: {min_renewable_day['date']}")
print(f"Total Renewable Production on this day: {min_renewable_day['Total Renewable Day Ahead Forecast (MW)']:.2f} MW")
print(f"Average Day Ahead Price on this day: {min_renewable_day_price:.2f} EUR/MWh\n")

if max_renewable_day_price > min_renewable_day_price:
    print("The Average Hourly DA price on the day with the highest renewable energy production is higher than the day with the lowest production.")
else:
    print("The Average Hourly DA price on the day with the highest renewable energy production is lower than the day with the lowest production.")

print()  

# ### Task 2.5 - Weekend vs Weekday Day Ahead Prices

# Identify the actual day on the date
df['day_of_week'] = df['date'].apply(lambda x: x.strftime('%A'))  # Get full day name

# Identify if it's a weekday (Mon-Fri) or weekend (Sat-Sun)
df['is_weekend'] = df['day_of_week'].apply(lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday')

# Calculate the average hourly Day Ahead Price for weekdays vs weekends
average_price_by_day_type = df.groupby('is_weekend')['Day Ahead Price hourly [in EUR/MWh]'].mean()

# Print the results
avg_weekday_price = average_price_by_day_type['Weekday']
avg_weekend_price = average_price_by_day_type['Weekend']
print("Task 2.5 - Weekend vs Weekday Day Ahead Prices Results:")
print(f"Average Hourly Day Ahead Price during Weekdays: {avg_weekday_price:.2f} EUR/MWh")
print(f"Average Hourly Day Ahead Price during Weekends: {avg_weekend_price:.2f} EUR/MWh")
print()

# ### Task 2.6 - Revenue from Battery Charging and Discharging (Maximizing Revenue)

# Initialize the daily_prices DataFrame with the 'date' column
daily_prices = pd.DataFrame({
    'date': df['date'].unique() 
})

# Initialize the columns in daily_prices
daily_prices['revenue'] = 0
daily_prices['max_price'] = 0
daily_prices['max_hour'] = 0
daily_prices['min_price'] = 0
daily_prices['min_hour'] = 0

# Iterate over each day to calculate the revenue-maximizing pair
for i, row in daily_prices.iterrows():
    date = row['date']
    
    # Filter data for the current date
    day_data = df_hourly[df_hourly['date'] == date]
    
    # Filter out any negative prices for max_price (as you cannot discharge at negative prices)
    day_data_positive_prices = day_data[day_data['Day Ahead Price hourly [in EUR/MWh]'] > 0]
    
    # If no positive prices are found for the day, skip the iteration
    if day_data_positive_prices.empty:
        continue
    
    # Find the top 12 maximum positive prices and their corresponding hours
    sorted_day_data = day_data_positive_prices.sort_values(by='Day Ahead Price hourly [in EUR/MWh]', ascending=False)
    
    # Limit to the top 12 prices, or fewer if there are not enough available hours
    top_12_prices = sorted_day_data.head(12)
    
    # Variables to store the best revenue pair for the day
    best_revenue = -float('inf')  # Start with a very low revenue
    best_max_price = None
    best_max_hour = None
    best_min_price = None
    best_min_hour = None
    
    # For each of the top 12 max prices, find the min price in the hours before the max hour
    for _, top_row in top_12_prices.iterrows():
        max_price = top_row['Day Ahead Price hourly [in EUR/MWh]']
        max_hour = top_row['hour']
        
        # Get the data for the hours before the max hour to calculate the min price
        previous_hours = day_data[day_data['hour'] < max_hour]
        
        # If there are valid previous hours, calculate the min price
        if not previous_hours.empty:
            # Do not filter out negative prices. Allow negative values to be considered.
            min_price = previous_hours['Day Ahead Price hourly [in EUR/MWh]'].min()
            
            # Find the hour corresponding to the minimum price
            min_hour = previous_hours[previous_hours['Day Ahead Price hourly [in EUR/MWh]'] == min_price]['hour'].values[0]
            
            # Calculate the revenue for this max-min pair
            revenue = max_price - min_price
            
            # If this revenue is the highest, update the best pair
            if revenue > best_revenue:
                best_revenue = revenue
                best_max_price = max_price
                best_max_hour = max_hour
                best_min_price = min_price
                best_min_hour = min_hour
    
    # Update the daily_prices DataFrame with the best pair for this day
    daily_prices.at[i, 'max_price'] = best_max_price
    daily_prices.at[i, 'max_hour'] = best_max_hour
    daily_prices.at[i, 'min_price'] = best_min_price
    daily_prices.at[i, 'min_hour'] = best_min_hour
    daily_prices.at[i, 'revenue'] = best_revenue

# Output the final DataFrame with only the required columns

# Set the new column names as per your requirement
output_columns = ['date', 'min_price', 'min_hour', 'max_price', 'max_hour', 'revenue']
daily_prices_output = daily_prices[output_columns]

# Rename the columns to the new names
daily_prices_output = daily_prices_output.rename(columns={
    'date': 'date',
    'max_price': 'sell price',
    'max_hour': 'discharge hour',
    'min_price': 'buy price',
    'min_hour': 'charge hour',
    'revenue': 'revenue'
})

# Print the output
print("Daily Prices with Revenue Maximizing Pairs:")
print(daily_prices_output)

# Optionally: Calculate the total revenue for the year
total_revenue = daily_prices_output['revenue'].sum()
print(f"\nTotal Revenue for the year (EUR): {total_revenue:.2f}")

# ### Task 2.2 - Graphing the Results

# Plot the results
plt.figure(figsize=(20, 6))

# Plot each line with a different color and label
plt.plot(df_hourly_avg['hour'], df_hourly_avg['Wind Day Ahead Forecast [in MW]'], label='Wind Day Ahead', color='blue')
plt.plot(df_hourly_avg['hour'], df_hourly_avg['Wind Intraday Forecast [in MW]'], label='Wind Intraday', color='green')
plt.plot(df_hourly_avg['hour'], df_hourly_avg['PV Day Ahead Forecast [in MW]'], label='PV Day Ahead', color='orange')
plt.plot(df_hourly_avg['hour'], df_hourly_avg['PV Intraday Forecast [in MW]'], label='PV Intraday', color='red')

# Add labels and title
plt.xlabel('Hour of the Day')
plt.ylabel('Average Forecasted Power (in MW)')
plt.title('Average Hourly Wind and Solar Production for 2021')

# Add a grid for better readability
plt.grid(True)

# Add a legend to the plot
plt.legend(title="Forecast Type")

# Show the plot
plt.show()
