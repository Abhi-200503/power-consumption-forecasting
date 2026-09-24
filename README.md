
# Regional Power Consumption Forecasting and Natural Language Query Interface

## Project Overview

This project forecasts hourly regional power consumption using time-series and machine-learning models and provides a natural-language interface for querying power telemetry data.

## Objectives

- Forecast hourly regional electricity demand
- Analyze historical power consumption
- Detect peak and minimum demand
- Compare forecasting models
- Provide a natural-language query interface for grid operators

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Statsmodels
- Gradio
- Google Colab
- GitHub

## Dataset

The initial project uses a synthetic hourly regional power-consumption dataset containing 8760 observations representing one year of hourly measurements.

The dataset contains:

- timestamp
- power_consumption_mw

## Forecasting Features

The forecasting model uses:

- Hour
- Day of week
- Month
- Weekend indicator
- Previous-hour consumption
- Previous-day consumption
- Previous-week consumption
- 24-hour rolling average
- 168-hour rolling average

## Models

### Random Forest

A Random Forest regression model is used for hourly demand prediction.

### AutoReg

An autoregressive time-series model is used as a second forecasting approach.

## Evaluation Metrics

The models are evaluated using:

- MAE
- RMSE
- MAPE

## Natural Language Interface

The system allows grid operators to ask questions such as:

- What is the average power consumption?
- What was the peak power consumption?
- What was the minimum power consumption?
- What is the average consumption at 5 PM?
- Show me the last readings.
- Show the top 10 peak readings.

## Project Workflow

Raw Telemetry Data
        |
        v
Data Preprocessing
        |
        v
Feature Engineering
        |
        v
Exploratory Data Analysis
        |
        v
Time-Series Forecasting
        |
        +----------------+
        |                |
        v                v
Random Forest         AutoReg
        |                |
        +-------+--------+
                |
                v
        Model Evaluation
                |
                v
       24-Hour Forecast
                |
                v
Natural Language Query Interface

## Future Improvements

- Replace synthetic data with real grid telemetry
- Add weather data
- Add renewable-energy generation data
- Add real-time telemetry ingestion
- Use advanced models such as XGBoost, LSTM or Transformer models
- Connect the query system to a SQL database
- Deploy the application using Streamlit
