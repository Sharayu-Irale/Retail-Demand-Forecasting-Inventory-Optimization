from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "retail_store_inventory.csv"

# Global objects (kept in memory)
pipeline_model = None
processed_data = None

NUM_FEATURES = [
    'lag_1', 'lag_7', 'lag_14',
    'rolling_7_mean', 'rolling_14_mean',
    'Day', 'Week', 'Month', 'DayOfWeek',
    'Price', 'Discount', 'is_promo'
]

CAT_FEATURES = [
    'Store ID', 'Product ID', 'Category',
    'Region', 'Seasonality', 'Weather Condition'
]


def prepare_data():
    global processed_data

    data = pd.read_csv(DATA_PATH)
    data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)
    data = data.drop(columns=['Demand Forecast'], errors='ignore')

    data = data.sort_values(['Store ID', 'Product ID', 'Date'])

    # Time features
    data['Day'] = data['Date'].dt.day
    data['Week'] = data['Date'].dt.isocalendar().week.astype(int)
    data['Month'] = data['Date'].dt.month
    data['DayOfWeek'] = data['Date'].dt.dayofweek

    # Lag features
    for lag in [1, 7, 14]:
        data[f'lag_{lag}'] = (
            data.groupby(['Store ID', 'Product ID'])['Units Sold'].shift(lag)
        )

    # Rolling features
    data['rolling_7_mean'] = (
        data.groupby(['Store ID', 'Product ID'])['Units Sold']
        .shift(1).rolling(7).mean()
    )

    data['rolling_14_mean'] = (
        data.groupby(['Store ID', 'Product ID'])['Units Sold']
        .shift(1).rolling(14).mean()
    )

    data['is_promo'] = (data['Discount'] > 0).astype(int)

    processed_data = data.dropna().reset_index(drop=True)
    return processed_data


def train_model():
    global pipeline_model, processed_data

    if processed_data is None:
        prepare_data()

    # Use a sample of data for faster & stable training on Render
    processed_data_sample = processed_data.sample(
        n=min(20000, len(processed_data)),
        random_state=42
    )

    X = processed_data[NUM_FEATURES + CAT_FEATURES]
    y = processed_data['Units Sold']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', NUM_FEATURES),
            ('cat', OneHotEncoder(handle_unknown='ignore'), CAT_FEATURES)
        ]
    )

    model = RandomForestRegressor(
    n_estimators=30,
    max_depth=10,
    random_state=42,
    n_jobs=1
    )

    pipeline_model = Pipeline(steps=[
        ('preprocessing', preprocessor),
        ('model', model)
    ])

    pipeline_model.fit(X, y)

    return {
        "message": "Model trained successfully",
        "records_used": len(processed_data)
    }


def predict_inventory(store_id: str, product_id: str):
    if pipeline_model is None:
        raise ValueError("Model not trained. Call /train first.")

    subset = processed_data[
        (processed_data['Store ID'] == store_id) &
        (processed_data['Product ID'] == product_id)
    ]

    if subset.empty:
        raise ValueError("Invalid Store ID or Product ID")

    X = subset[NUM_FEATURES + CAT_FEATURES]
    forecast = pipeline_model.predict(X)

    subset = subset.copy()
    subset['Forecast'] = forecast

    stats = (
        subset
        .groupby(['Store ID', 'Product ID'])['Forecast']
        .agg(['mean', 'std'])
        .reset_index()
    )

    lead_time = 7
    service_level = 1.65

    safety_stock = service_level * stats['std'].iloc[0] * np.sqrt(lead_time)
    reorder_point = stats['mean'].iloc[0] * lead_time + safety_stock

    current_inventory = (
        subset.sort_values('Date')
        .iloc[-1]['Inventory Level']
    )

    order_qty = max(reorder_point - current_inventory, 0)

    return {
        "store_id": store_id,
        "product_id": product_id,
        "forecasted_daily_demand": round(stats['mean'].iloc[0], 2),
        "safety_stock": round(safety_stock, 2),
        "reorder_point": round(reorder_point, 2),
        "current_inventory": int(current_inventory),
        "order_quantity": round(order_qty, 2)
    }
