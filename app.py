```python
import streamlit as st
import pandas as pd
import numpy as np
import os
import re
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Power Consumption Forecasting",
    page_icon="⚡",
    layout="wide"
)


# =========================================================
# FILE PATHS
# =========================================================

MODEL_FILE = "power_consumption_model_small.pkl"

# The application supports the CSV either in the root folder
# or inside the data folder.

CSV_OPTIONS = [
    "power_consumption.csv",
    "processed_power_consumption.csv",
    os.path.join("data", "power_consumption.csv"),
    os.path.join("data", "processed_power_consumption.csv")
]


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():
    return joblib.load(MODEL_FILE)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)


# =========================================================
# FIND AVAILABLE CSV
# =========================================================

data_file = None

for file_path in CSV_OPTIONS:
    if os.path.exists(file_path):
        data_file = file_path
        break


# =========================================================
# CHECK REQUIRED FILES
# =========================================================

if not os.path.exists(MODEL_FILE):

    st.error(
        "❌ Trained model file not found: "
        f"{MODEL_FILE}"
    )

    st.info(
        "Make sure power_consumption_model_small.pkl "
        "is uploaded to the same GitHub repository as app.py."
    )

    st.stop()


if data_file is None:

    st.error("❌ Power consumption CSV file was not found.")

    st.info(
        "Upload your power consumption CSV to the repository."
    )

    st.stop()


# =========================================================
# LOAD MODEL AND DATA
# =========================================================

try:

    model = load_model()
    df = load_data(data_file)

except Exception as e:

    st.error("❌ Error loading model or dataset.")
    st.write(e)
    st.stop()


# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [
    "timestamp",
    "power_consumption_mw"
]

missing_columns = [
    col
    for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        "❌ Required columns are missing from the dataset:"
    )

    st.write(missing_columns)

    st.info(
        "The CSV must contain timestamp and "
        "power_consumption_mw columns."
    )

    st.stop()


# =========================================================
# PREPARE DATA
# =========================================================

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)

df["power_consumption_mw"] = pd.to_numeric(
    df["power_consumption_mw"],
    errors="coerce"
)

df = df.dropna(
    subset=[
        "timestamp",
        "power_consumption_mw"
    ]
)

df = df.sort_values(
    "timestamp"
).reset_index(drop=True)


# =========================================================
# CREATE / RECREATE FEATURES
# =========================================================

df["hour"] = df["timestamp"].dt.hour

df["day"] = df["timestamp"].dt.day

df["day_of_week"] = df["timestamp"].dt.dayofweek

df["month"] = df["timestamp"].dt.month

df["day_of_year"] = df["timestamp"].dt.dayofyear

df["is_weekend"] = (
    df["day_of_week"] >= 5
).astype(int)


# Lag features

df["lag_1"] = df["power_consumption_mw"].shift(1)

df["lag_24"] = df["power_consumption_mw"].shift(24)

df["lag_168"] = df["power_consumption_mw"].shift(168)


# Rolling features

df["rolling_24"] = (
    df["power_consumption_mw"]
    .rolling(24)
    .mean()
)

df["rolling_168"] = (
    df["power_consumption_mw"]
    .rolling(168)
    .mean()
)


# =========================================================
# MODEL FEATURES
# =========================================================

features = [
    "hour",
    "day",
    "day_of_week",
    "month",
    "day_of_year",
    "is_weekend",
    "lag_1",
    "lag_24",
    "lag_168",
    "rolling_24",
    "rolling_168"
]

target = "power_consumption_mw"


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚡ Power Forecasting")

st.sidebar.write(
    "Select an option:"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Historical Analysis",
        "24-Hour Forecast",
        "Model Performance",
        "Natural Language Query"
    ]
)


# =========================================================
# HEADER
# =========================================================

st.title(
    "⚡ Regional Power Consumption Forecasting"
)

st.markdown(
    "### AI-Based Power Forecasting and Natural Language Query System"
)

st.caption(
    f"Dataset: {data_file} | "
    f"Records: {len(df):,}"
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.header(
        "📊 Power Consumption Dashboard"
    )

    st.write(
        "Overview of historical regional power consumption."
    )

    values = df[target]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Average Consumption",
        f"{values.mean():.2f} MW"
    )

    col2.metric(
        "Peak Consumption",
        f"{values.max():.2f} MW"
    )

    col3.metric(
        "Minimum Consumption",
        f"{values.min():.2f} MW"
    )

    co
```
