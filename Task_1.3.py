from flask import Flask, jsonify
import pandas as pd
import sqlite3
from datetime import datetime
from Task_1 import compute_pnl  # Import the compute_pnl function from Task_1.py

app = Flask(__name__)

# Define API endpoint to calculate and return PnL for a specific strategy
@app.route('/pnl/<strategy_id>', methods=['GET'])
def get_pnl(strategy_id):
    """
    API endpoint to calculate Profit and Loss (PnL) for a given trading strategy.
    
    Args:
        strategy_id (str): Identifier of the trading strategy.

    Returns:
        JSON response containing:
            - strategy (str): The strategy ID.
            - value (float): Calculated PnL.
            - unit (str): Currency unit (euro).
            - capture_time (str): Timestamp of the PnL calculation in ISO 8601 format.
        If an error occurs, a JSON response with error details is returned.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('trades.sqlite')
        
        # Load trade data from the specified database table into a pandas DataFrame
        trades_df = pd.read_sql_query("SELECT * FROM epex_12_20_12_13", conn)

        # Calculate the PnL for the provided strategy using the imported compute_pnl function
        pnl_value = compute_pnl(strategy_id, trades_df)

        # Construct the response with calculated PnL and additional metadata
        response = {
            "strategy": strategy_id,  # The strategy ID for which PnL was calculated
            "value": pnl_value,       # The calculated PnL value
            "unit": "euro",           # The currency unit for PnL
            "capture_time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")  # Current UTC timestamp
        }

        return jsonify(response), 200  # Return the response with HTTP 200 OK status

    except sqlite3.Error as e:
        # Handle database-related errors
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

    finally:
        # Ensure the database connection is closed, even if an error occurs
        conn.close()

# Entry point to run the Flask application
if __name__ == "__main__":
    # Start the Flask app on all available network interfaces, port 5000, with debugging enabled
    app.run(host='0.0.0.0', port=5000, debug=True)
