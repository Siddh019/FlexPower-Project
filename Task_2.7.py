import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from datetime import datetime
import statsmodels.api as sm

# Load raw data from the Excel file and inspect its structure
raw_data = pd.read_excel('analysis_task_data.xlsx')
df = raw_data

# Display the number of rows and columns in the dataset
num_rows = df.shape[0]
num_cols = df.shape[1]
print("Number of rows:", num_rows)
print("Number of columns:", num_cols)

# ## Task 2.7: Building a trading strategy

# ### Task 2.7.1: Data Handling & Cleaning

# Convert the 'time' column to datetime format
df['time'] = pd.to_datetime(df['time'], format='%d/%m/%y %H:%M')

# Select the relevant columns for analysis
selected_columns = [
    'time',
    'Intraday Price Hourly  [in EUR/MWh]',
    'Day Ahead Price hourly [in EUR/MWh]',
    'Wind Day Ahead Forecast [in MW]',
    'PV Day Ahead Forecast [in MW]',
]

# Create a new DataFrame with the selected columns
d1 = df[selected_columns]

# Rename columns for better readability
new_column_names = {
    'time': 'Day T',
    'Wind Day Ahead Forecast [in MW]': 'Wind DA Forecast (MW)',
    'PV Day Ahead Forecast [in MW]': 'PV DA Forecast (MW)',
    'Day Ahead Price hourly [in EUR/MWh]': 'DA Price (EUR/MWh)',
    'Intraday Price Hourly  [in EUR/MWh]': 'Intra Price (EUR/MWh)',
}

# Apply new column names to the DataFrame
d1 = d1.rename(columns=new_column_names)

# Shift the 'Day T' and 'Intra Price' columns for prediction
d1['Day T+1'] = d1['Day T'].shift(-96)  # Shift by 96 rows for hourly prediction
d1['Intra T+1 Price (EUR/MWh)'] = d1['Intra Price (EUR/MWh)'].shift(-96)

# Reorder columns for better clarity
new_order = ['Day T+1', 'Intra T+1 Price (EUR/MWh)'] + [col for col in d1.columns if col not in ['Day T+1', 'Intra T+1 Price (EUR/MWh)']]
d1 = d1[new_order]
d1.head(100)

# ### Task 2.7.2: Prediction using OLS Method

# Remove rows with missing 'Intra T+1 Price' data
d1_cleaned = d1.dropna(subset=['Intra T+1 Price (EUR/MWh)'])

# Define independent variables (features) and dependent variable (target)
X = d1_cleaned[['Intra Price (EUR/MWh)', 'DA Price (EUR/MWh)', 'Wind DA Forecast (MW)', 'PV DA Forecast (MW)']]
y = d1_cleaned['Intra T+1 Price (EUR/MWh)']

# Add a constant term to the features (for intercept in regression model)
X = sm.add_constant(X)

# Fit an Ordinary Least Squares (OLS) regression model
model = sm.OLS(y, X).fit()

# Output the regression results for analysis
print(model.summary())

# Extract the fitted values and residuals from the OLS model
fitted_values = model.fittedvalues
residuals = model.resid
print(fitted_values)

# ### Task 2.7.3: P/l using OLS Method Fitted Values

# Initialize 'buy', 'sell', and 'P/L' columns in the cleaned DataFrame
d1_cleaned.loc[:, 'buy'] = pd.NA
d1_cleaned.loc[:, 'sell'] = pd.NA
d1_cleaned.loc[:, 'P/L'] = pd.NA

# Define conditions for buying and selling based on fitted values and DA price
condition_buy_at_da = fitted_values > d1_cleaned['DA Price (EUR/MWh)']
condition_buy_at_intra = fitted_values < d1_cleaned['DA Price (EUR/MWh)']

# If fitted value > DA Price, buy at DA Price and sell at Intra Price
d1_cleaned.loc[condition_buy_at_da, 'buy'] = d1_cleaned.loc[condition_buy_at_da, 'DA Price (EUR/MWh)']
d1_cleaned.loc[condition_buy_at_da, 'sell'] = d1_cleaned.loc[condition_buy_at_da, 'Intra T+1 Price (EUR/MWh)']

# If fitted value < DA Price, buy at Intra Price and sell at DA Price
d1_cleaned.loc[condition_buy_at_intra, 'buy'] = d1_cleaned.loc[condition_buy_at_intra, 'Intra T+1 Price (EUR/MWh)']
d1_cleaned.loc[condition_buy_at_intra, 'sell'] = d1_cleaned.loc[condition_buy_at_intra, 'DA Price (EUR/MWh)']

# Calculate profit/loss (P/L) as the difference between 'sell' and 'buy' prices
d1_cleaned['P/L'] = (d1_cleaned['sell'] - d1_cleaned['buy']) / 4 # Divide by 4 since the DA and Intra Price is constant accross the hour

# Replace NaN values in 'P/L' with 0 where no trade occurred
d1_cleaned['P/L'] = d1_cleaned['P/L'].fillna(0)

# Sum the numerical columns to get overall performance metrics
pd.set_option('display.float_format', '{:.2f}'.format)
numeric_columns = d1_cleaned.select_dtypes(include=[np.number]).columns
sum_result = d1_cleaned[numeric_columns].sum()
print(sum_result)

# ### Task 2.7.4: Prediction using Random Forest Regression Method

# Import the neceassy libraries
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Re-clean the data and define features and target variable
d1_cleaned = d1.dropna(subset=['Intra T+1 Price (EUR/MWh)'])
X = d1_cleaned[['Intra Price (EUR/MWh)', 'DA Price (EUR/MWh)', 'Wind DA Forecast (MW)', 'PV DA Forecast (MW)']]
y = d1_cleaned['Intra T+1 Price (EUR/MWh)']

# Split the data into training and test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and fit the Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred_rf = rf_model.predict(X_test)

# Output Random Forest model evaluation metrics
print(f"Random Forest Regression Model Summary")
print("="*40)
print(f"Number of Trees (n_estimators): {rf_model.n_estimators}")
print(f"Max Depth of Trees (max_depth): {rf_model.max_depth}")
print(f"Min Samples Split (min_samples_split): {rf_model.min_samples_split}")
print(f"Min Samples Leaf (min_samples_leaf): {rf_model.min_samples_leaf}")
print(f"Max Features (max_features): {rf_model.max_features}")
print("="*40)
print(f"Model Evaluation Metrics:")
mse_rf = mean_squared_error(y_test, y_pred_rf)
print(f"Random Forest Model MSE: {mse_rf}")
r2 = r2_score(y_test, y_pred_rf)
print(f"  - R²: {r2}")

# Output the feature importances from the Random Forest model
for feature, importance in zip(X.columns, rf_model.feature_importances_):
    print(f"  - {feature}: {importance:.4f}")

# Get predictions (fitted values) for the entire dataset using the Random Forest model
fitted_values_rf = rf_model.predict(X)
print("Fitted values (Random Forest):")
print(fitted_values_rf)

# ### Task 2.7.5: P/l using Random Forest Regression Fitted Values

# Implement the buy/sell decision logic based on Random Forest predictions
d1_cleaned.loc[:, 'buy'] = pd.NA
d1_cleaned.loc[:, 'sell'] = pd.NA
d1_cleaned.loc[:, 'P/L'] = pd.NA

# Buy at DA Price if RF prediction > DA Price, else sell at Intra Price
condition_buy_at_da_rf = fitted_values_rf > d1_cleaned['DA Price (EUR/MWh)']
condition_buy_at_intra_rf = fitted_values_rf < d1_cleaned['DA Price (EUR/MWh)']

# Apply the buy/sell logic for trades based on the RF model predictions
d1_cleaned.loc[condition_buy_at_da_rf, 'buy'] = d1_cleaned.loc[condition_buy_at_da_rf, 'DA Price (EUR/MWh)']
d1_cleaned.loc[condition_buy_at_da_rf, 'sell'] = d1_cleaned.loc[condition_buy_at_da_rf, 'Intra T+1 Price (EUR/MWh)']

# Reverse the logic for the opposite scenario
d1_cleaned.loc[condition_buy_at_intra_rf, 'buy'] = d1_cleaned.loc[condition_buy_at_intra_rf, 'Intra T+1 Price (EUR/MWh)']
d1_cleaned.loc[condition_buy_at_intra_rf, 'sell'] = d1_cleaned.loc[condition_buy_at_intra_rf, 'DA Price (EUR/MWh)']

# Calculate profit/loss (P/L) for trades based on Random Forest predictions
d1_cleaned['P/L'] = (d1_cleaned['sell'] - d1_cleaned['buy']) / 4  # Divide by 4 since the DA and Intra Price is constant accross the hour
d1_cleaned['P/L'] = d1_cleaned['P/L'].fillna(0)

# Calculate and print overall strategy performance
pd.set_option('display.float_format', '{:.2f}'.format)
numeric_columns = d1_cleaned.select_dtypes(include=[np.number]).columns
sum_result = d1_cleaned[numeric_columns].sum()
print(sum_result)

# ### Task 2.7.6: Comparing OLS vs RF for out-of-sample-data

# Predicting the Intraday Price Hourly (in EUR/MWh) for 01-01-2022
# Extract the independent variables for out-of-sample data (rows 34944 to 35039)
out_of_sample_data = d1.loc[34944:35039, [
    'Intra Price (EUR/MWh)', 
    'DA Price (EUR/MWh)', 
    'Wind DA Forecast (MW)', 
    'PV DA Forecast (MW)'
]]

# Use the trained Random Forest model to make predictions on the out-of-sample data
rf_predictions = rf_model.predict(out_of_sample_data)

# Compute the fitted values from the OLS model for the same out-of-sample data
# Add a constant for the intercept term (same as during training)
X_out_of_sample = sm.add_constant(out_of_sample_data)

# Get the fitted values for the OLS model
ols_fitted_values = model.predict(X_out_of_sample)

# Create a DataFrame to compare the Random Forest and OLS model predictions
comparison_df = pd.DataFrame({
    'RF Prediction (Intra T+1 Price)': rf_predictions,
    'OLS Fitted Value (Intra T+1 Price)': ols_fitted_values
})

# Set the 'Day T' column as the index for easy comparison
comparison_df['Day T'] = d1.loc[34944:35039, 'Day T']
comparison_df.set_index('Day T', inplace=True)

# Display the comparison DataFrame
print(comparison_df)

# ### Task 2.7.7: Visualising the P/L over time (RF data only)

# Calculate cumulative P/L in EUR 
d1_cleaned = d1_cleaned.copy()
d1_cleaned['Cumulative_PL'] = d1_cleaned['P/L'].cumsum()

# Visualize the cumulative profit/loss over time
def format_yaxis(value, tick_pos):
    return f'{int(value):,}'

plt.figure(figsize=(12, 6))
plt.plot(d1_cleaned['Day T'], d1_cleaned['Cumulative_PL'], color='blue')
plt.title('Cumulative P/L Over Time')
plt.xlabel('Date')
plt.ylabel('Cumulative P/L (EUR)')
plt.gca().yaxis.set_major_formatter(FuncFormatter(format_yaxis))
plt.grid(True)
plt.show()

# Output key performance metrics for the strategy
total_pl = d1_cleaned['Cumulative_PL'].iloc[-1]
max_drawdown = (d1_cleaned['Cumulative_PL'] - d1_cleaned['Cumulative_PL'].cummax()).min()
profitable_trades = (d1_cleaned['P/L'] > 0).sum()
total_trades = len(d1_cleaned[d1_cleaned['P/L'] != 0])
win_rate = profitable_trades / total_trades * 100 if total_trades > 0 else 0

print(f"\nStrategy Performance Metrics")
print(f"Total P/L: €{total_pl:,.2f}")
print(f"Maximum Drawdown: €{max_drawdown:,.2f}")
print(f"Number of Trades: {total_trades}")
print(f"Win Rate: {win_rate:.2f}%")
