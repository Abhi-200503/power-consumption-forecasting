
# ⚡ Regional Power Consumption Forecasting and Natural Language Query Interface

## Project Overview

This project forecasts hourly regional power consumption using time-series analysis and machine-learning models. It also provides an interactive Streamlit dashboard with a natural-language query interface for analyzing historical power consumption, generating forecasts, and comparing model performance.

The application helps users understand electricity demand patterns, identify peak and minimum consumption, and explore future power consumption trends.

## Objectives

- Forecast hourly regional electricity demand.
- Analyze historical power consumption patterns.
- Identify peak and minimum electricity demand.
- Compare forecasting models using evaluation metrics.
- Generate 24-hour power consumption forecasts.
- Provide a natural-language query interface for exploring power telemetry data.
- Visualize historical trends and forecasting results through an interactive dashboard.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Statsmodels
- Streamlit
- Machine Learning
- Time-Series Analysis
- GitHub

## Dataset

The project initially uses a synthetic hourly regional power-consumption dataset containing 8,760 observations representing one year of hourly measurements.

### Dataset Attributes

| Column | Description |
|---|---|
| timestamp | Date and time of power consumption measurement |
| power_consumption_mw | Electricity consumption in megawatts |

The dataset is used for preprocessing, exploratory data analysis, feature engineering, model training, and forecasting.

## Forecasting Features

The forecasting models use the following features:

- Hour
- Day of week
- Month
- Weekend indicator
- Previous-hour consumption
- Previous-day consumption
- Previous-week consumption
- 24-hour rolling average
- 168-hour rolling average

These features help capture daily, weekly, and seasonal electricity demand patterns.

## Machine Learning Models

### 1. Random Forest Regressor

A Random Forest regression model is used to predict hourly power consumption based on engineered time-series features.

### 2. AutoReg Model

An autoregressive time-series model is used as a second forecasting approach to capture dependencies between historical power consumption observations.

## Model Evaluation Metrics

The forecasting models are evaluated using the following metrics:

- **MAE (Mean Absolute Error):** Measures the average absolute difference between actual and predicted consumption.
- **RMSE (Root Mean Squared Error):** Measures prediction error while giving greater weight to larger errors.
- **MAPE (Mean Absolute Percentage Error):** Measures prediction error as a percentage of actual consumption.

The evaluation results are used to compare forecasting model performance.

## Application Features

### 1. Dashboard
- Overview of power consumption data.
- Key consumption statistics.
- Interactive visualizations.

### 2. Historical Analysis
- Historical power consumption trends.
- Consumption pattern analysis.
- Peak and minimum demand identification.

### 3. 24-Hour Forecast
- Generate the next 24 hours of predicted power consumption.
- Display average, peak, and minimum forecast values.
- Visualize forecast trends.

### 4. Model Comparison
- Compare Random Forest and AutoReg forecasting models.
- Display model evaluation metrics.
- Analyze forecasting performance.

### 5. Natural Language Query Interface

The application allows users to ask questions about power consumption data using natural language.

Example queries:

- What is the average power consumption?
- What was the peak power consumption?
- What was the minimum power consumption?
- What is the average consumption at 5 PM?
- Show me the last readings.
- Show the top 10 peak readings.

## Project Workflow

```text
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
 Random Forest        AutoReg
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
    Interactive Streamlit Dashboard
                |
                v
 Natural Language Query Interface
```

## Project Structure

```text
power-consumption-forecasting/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── processed_power_consumption.csv
│   ├── next_24_hour_forecast.csv
│   └── model_comparison.csv
│
└── Power-Consumption-Forecasting/
    └── Original project dataset
```

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/Abhi-200503/power-consumption-forecasting.git
```

### Step 2: Navigate to the Project Directory

```bash
cd power-consumption-forecasting
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Streamlit Application

```bash
streamlit run app.py
```

### Step 5: Open the Application

After running the command, Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open this URL in your browser to access the Power Consumption Forecasting Dashboard.

## Future Improvements

- Replace synthetic data with real electricity grid telemetry.
- Integrate weather information for improved forecasting.
- Include renewable energy generation data.
- Implement real-time telemetry ingestion.
- Explore advanced forecasting models such as XGBoost, LSTM, and Transformers.
- Connect the natural-language query system to a SQL database.
- Deploy the application using Streamlit Community Cloud.

## Author

**Abhi-200503**
## Grid Telemetry Documentation and Metadata

- [Grid Telemetry Documentation](docs/grid_telemetry_documentation.md)
- [Grid Telemetry Metadata](metadata/grid_telemetry_metadata.json)

The documentation describes the dataset, forecasting models, evaluation metrics,
application features, and example queries. The metadata provides structured
information to support document organization and retrieval.
GitHub Repository:  
https://github.com/Abhi-200503/power-consumption-forecasting

---

⚡ **Regional Power Consumption Forecasting | Machine Learning | Streamlit Dashboard**
