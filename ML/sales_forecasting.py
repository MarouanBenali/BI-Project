"""
SALES FORECASTING USING TIME SERIES ANALYSIS
AdventureWorks Data Warehouse
"""
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sqlalchemy import create_engine, text

# Add ETL_Project to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "ETL_Project"))
from config import DATABASE_URI


def load_sales_time_series():
    """Load monthly sales time series from data warehouse"""
    print("[1] Loading monthly sales data...")
    engine = create_engine(DATABASE_URI)
    with engine.connect() as conn:
        df = pd.read_sql(text("""
            SELECT 
                YEAR(OrderDate) AS Year,
                MONTH(OrderDate) AS Month,
                COUNT(*) AS TotalSales
            FROM aw_sales
            GROUP BY YEAR(OrderDate), MONTH(OrderDate)
            ORDER BY Year, Month
        """), conn)
    
    # Create date column
    df['Date'] = pd.to_datetime(df.assign(Day=1)[['Year', 'Month', 'Day']])
    df = df.sort_values('Date')
    return df


def prepare_features(df):
    """Prepare time series features for forecasting"""
    print("\n[2] Preparing features for forecasting...")
    df = df.copy()
    
    # Create time index (months since start)
    df['TimeIndex'] = np.arange(len(df))
    
    # Create lag features
    df['Lag1'] = df['TotalSales'].shift(1)
    df = df.dropna()
    
    return df


def split_train_test(df, test_size=0.2):
    """Split data into training and testing sets"""
    print("\n[3] Splitting data into train/test sets...")
    split_idx = int(len(df) * (1 - test_size))
    train = df.iloc[:split_idx]
    test = df.iloc[split_idx:]
    return train, test


def train_forecast_model(train):
    """Train a simple linear regression model for forecasting"""
    print("\n[4] Training forecasting model...")
    X_train = train[['TimeIndex', 'Lag1']]
    y_train = train['TotalSales']
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, test):
    """Evaluate forecasting model"""
    print("\n[5] Evaluating model performance...")
    X_test = test[['TimeIndex', 'Lag1']]
    y_test = test['TotalSales']
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    
    return y_pred


def visualize_forecast(df, train, test, y_pred, save_dir='ML/results'):
    """Visualize sales and forecast"""
    print("\n[6] Visualizing forecast...")
    os.makedirs(save_dir, exist_ok=True)
    
    plt.figure(figsize=(16, 8))
    plt.plot(train['Date'], train['TotalSales'], label='Training Data', color='blue')
    plt.plot(test['Date'], test['TotalSales'], label='Actual Test Data', color='green')
    plt.plot(test['Date'], y_pred, label='Forecast', color='red', linestyle='--')
    
    plt.title('Sales Forecasting - AdventureWorks', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Number of Sales', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'sales_forecast.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Visualization saved to {save_dir}")


def main():
    print("=" * 80)
    print("SALES FORECASTING - TIME SERIES ANALYSIS")
    print("=" * 80)
    
    # Step 1: Load data
    df = load_sales_time_series()
    
    # Step 2: Prepare features
    df_features = prepare_features(df)
    
    # Step 3: Split data
    train, test = split_train_test(df_features)
    
    # Step 4: Train model
    model = train_forecast_model(train)
    
    # Step 5: Evaluate
    y_pred = evaluate_model(model, test)
    
    # Step 6: Visualize
    visualize_forecast(df_features, train, test, y_pred)
    
    print("\n" + "=" * 80)
    print("SALES FORECASTING COMPLETED!")
    print("=" * 80)


if __name__ == "__main__":
    main()
