import pandas as pd
import sqlite3

# ## Task 1: Minimal Reporting tool

# ### Task 1.1 - Total Volume Calculator

class Volume_Calculator:
    """
    A class to calculate the total buy and sell volumes based on trade data.

    Args:
        trades_df (pd.DataFrame): A pandas DataFrame containing trade data (must have columns 'side' and 'quantity').

    Methods:
        Buy_Volume(): Calculates the total volume of buy orders.
        Sell_Volume(): Calculates the total volume of sell orders.
    """
    def __init__(self, trades_df: pd.DataFrame):
        self.trades_df = trades_df

    def Buy_Volume(self, *args, **kwargs) -> float:
        """
        Calculates the total buy volume (sum of quantities where side == 'buy').

        Returns:
            float: The total buy volume.
        """
        try:
            # Filter the trades DataFrame for 'buy' side orders and sum their quantities
            Buy_volume = self.trades_df[self.trades_df['side'] == 'buy']['quantity'].sum()
            return Buy_volume
        except KeyError as e:
            print(f"KeyError: {e}")
            return 0.0  # Return 0.0 in case of a KeyError (missing column)

    def Sell_Volume(self, *args, **kwargs) -> float:
        """
        Calculates the total sell volume (sum of quantities where side == 'sell').

        Returns:
            float: The total sell volume.
        """
        try:
            # Filter the trades DataFrame for 'sell' side orders and sum their quantities
            Sell_Volume = self.trades_df[self.trades_df['side'] == 'sell']['quantity'].sum()
            return Sell_Volume
        except KeyError as e:
            print(f"KeyError: {e}")
            return 0.0  # Return 0.0 in case of a KeyError (missing column)

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
        print(trades_df)  # Optional: print the DataFrame to inspect data
        print(f"Total buy volume: {total_buy_volume}")
        print(f"Total sell volume: {total_sell_volume}")
    
    except Exception as e:
        print(f"Error: {e}")  # Error handling for database or calculation issues

# ## Task 1.2 - Profit & Loss (PnL) Calculator  

def compute_pnl(strategy_id: str, trades_df: pd.DataFrame) -> float:
    """
    Compute the profit and loss (PnL) for a given strategy from trade data.

    Args:
        strategy_id (str): The ID of the strategy for which to compute the PnL.
        trades_df (pd.DataFrame): The pandas DataFrame containing trade data (must have 'strategy', 'side', 'quantity', 'price' columns).

    Returns:
        float: The computed PnL for the specified strategy.
    """
    # Filter the DataFrame to include only trades for the specified strategy
    df_strategy = trades_df[trades_df['strategy'] == strategy_id]

    # Vectorized PnL calculation for efficiency: 
    # Calculate PnL per trade based on whether the side is 'buy' or 'sell'.
    def calculate_pnl(row):
        # If it's a 'sell' order, the PnL is positive; otherwise, negative for 'buy' orders
        return row['quantity'] * row['price'] if row['side'] == 'sell' else -row['quantity'] * row['price']

    # Create a new column 'pnl' in the DataFrame with the calculated values
    df_strategy = df_strategy.assign(pnl=df_strategy.apply(calculate_pnl, axis=1))

    # Calculate the total PnL by summing the 'pnl' column
    pnl = df_strategy['pnl'].sum()

    # Return the PnL, ensuring it's 0 if no valid data is present (NaN)
    return pnl if pd.notna(pnl) else 0

# Example usage
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
