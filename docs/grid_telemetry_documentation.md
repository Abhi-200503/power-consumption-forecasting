
# Grid Telemetry Documentation

## 1. Project Information

Project Name: Regional Power Consumption Forecasting

Domain: Smart Grid and Energy Analytics

Purpose: Analyze historical electricity consumption and forecast future power demand using machine learning and time-series models.

Application: Streamlit Dashboard with Natural Language Query Interface.

## 2. Dataset Description

The project uses a synthetic hourly regional power consumption dataset containing 8,760 observations representing one year of measurements.

### Dataset Fields

| Field | Description | Unit |
|---|---|---|
| timestamp | Date and time of observation | DateTime |
| power_consumption_mw | Recorded electricity consumption | MW |

Sampling Frequency: Hourly

Dataset Type: Synthetic

## 3. Data Processing

The dataset is processed using Python and Pandas.

Processing includes:
- Loading telemetry CSV files.
- Converting power consumption values to numeric format.
- Processing timestamps.
- Handling invalid numeric values.
- Preparing data for analysis and forecasting.

## 4. Forecasting Features

The forecasting system uses:

1. Hour
2. Day of week
3. Month
4. Weekend indicator
5. Previous-hour consumption
6. Previous-day consumption
7. Previous-week consumption
8. 24-hour rolling average
9. 168-hour rolling average

## 5. Forecasting Models

### Random Forest Regression

Used for predicting hourly electricity demand using historical and temporal features.

### AutoReg

An autoregressive time-series model used to predict future power consumption based on historical observations.

## 6. Evaluation Metrics

- MAE: Mean Absolute Error
- RMSE: Root Mean Squared Error
- MAPE: Mean Absolute Percentage Error

## 7. Application Features

### Dashboard
Displays average, peak, minimum, and total record statistics.

### Historical Analysis
Displays historical power consumption trends and statistical summaries.

### 24-Hour Forecast
Displays predicted power consumption, forecast statistics, charts, and tables.

### Model Comparison
Displays model evaluation results.

### Natural Language Query
Allows users to retrieve information using ordinary English questions.

## 8. Example Retrieval Queries

- What is the average power consumption?
- What was the peak consumption?
- What is the minimum consumption?
- What is the average consumption at 5 PM?
- Show the last 10 readings.
- Show the top 10 peak readings.
- What is the predicted average consumption?
- Which forecasting models are used?

## 9. Data Files

| File | Description |
|---|---|
| data/processed_power_consumption.csv | Historical consumption data |
| data/next_24_hour_forecast.csv | Forecast output |
| data/model_comparison.csv | Model evaluation results |

## 10. Limitations

- Initial dataset is synthetic.
- Forecasts are based on stored project data.
- Real-time grid telemetry integration is not currently documented.
- Weather and renewable energy inputs are future improvements.

## 11. Future Enhancements

- Real-time grid telemetry ingestion.
- Weather data integration.
- Renewable energy generation data.
- SQL database integration.
- Retrieval-Augmented Generation (RAG).
- Advanced forecasting models.
