# Telemetry Query and Forecast Explanation Prompts

## 1. Purpose

This document contains example prompts for asking questions about regional
power consumption and understanding forecasting results.

The prompts are designed around the project's hourly power consumption
dataset and forecasting application.

## 2. Telemetry Query Prompts

### General Consumption
- What is the average power consumption?
- What is the minimum and maximum power consumption?
- Show the power consumption trend over time.
- What was the power consumption during a specific date and time?

### Peak Demand
- When did peak power consumption occur?
- Show the top 10 peak power consumption readings.
- Which hours recorded the highest demand?
- Compare peak demand across different days.

### Time-Based Analysis
- What is the average power consumption by hour?
- Compare weekday and weekend power consumption.
- How does power consumption vary throughout the day?
- Compare power consumption between two selected dates.

## 3. Forecast Explanation Prompts

### Forecast Overview
- Explain the next 24-hour power consumption forecast.
- What is the predicted power consumption for the next hour?
- Which hour has the highest predicted demand?
- Which hour has the lowest predicted demand?

### Forecast Interpretation
- Describe the overall trend in the 24-hour forecast.
- Explain whether predicted demand increases or decreases.
- Identify the hours when demand is expected to be high.
- Summarize the forecast in simple language.

### Model Comparison
- Compare the Random Forest and AutoReg forecasting models.
- Explain the MAE, RMSE, and MAPE metrics.
- What do the model evaluation results indicate?
- Explain the difference between actual and predicted consumption.

## 4. Prompt Template for Telemetry Questions

Use this template when creating a telemetry query:

"You are a power consumption data assistant.
Answer the user's question using only the available dataset.
Include relevant values, units, and time periods.
If the required information is unavailable, state that clearly.
Do not invent measurements.

User question: [Insert telemetry question]"

## 5. Prompt Template for Forecast Explanations

"You are a power forecasting assistant.
Explain the available 24-hour power consumption forecast in simple language.
Identify important trends, high-demand periods, and relevant predicted values.
Use only the available forecast data.
Do not present predictions as actual measurements.
If a value is unavailable, state that clearly.

Forecast data: [Insert forecast data]
User question: [Insert forecast question]"

## 6. Important Notes

- Power consumption is measured in megawatts (MW).
- The project dataset is synthetic hourly data.
- Forecast values are predictions, not actual measurements.
- Explanations should be based on available data and model results.
- These prompts are documentation examples and do not by themselves
  implement an AI assistant or connect an LLM to the application.
