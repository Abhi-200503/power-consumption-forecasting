
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

    col4.metric(
        "Total Records",
        f"{len(values):,}"
    )

    st.subheader(
        "📈 Historical Consumption Trend"
    )

    chart_df = df.set_index(
        "timestamp"
    )[[target]]

    st.line_chart(
        chart_df
    )

    st.subheader(
        "📋 Dataset Preview"
    )

    st.dataframe(
        df.head(20),
        use_container_width=True
    )


# =========================================================
# HISTORICAL ANALYSIS
# =========================================================

elif page == "Historical Analysis":

    st.header(
        "📈 Historical Power Consumption"
    )

    st.subheader(
        "📊 Statistical Summary"
    )

    st.dataframe(
        df[target].describe(),
        use_container_width=True
    )

    st.subheader(
        "📈 Historical Consumption Trend"
    )

    chart_df = df.set_index(
        "timestamp"
    )[[target]]

    st.line_chart(
        chart_df
    )

    st.subheader(
        "🔥 Top 10 Peak Consumption Records"
    )

    top_records = df.nlargest(
        10,
        target
    )

    st.dataframe(
        top_records,
        use_container_width=True
    )


# =========================================================
# 24-HOUR FORECAST
# =========================================================

elif page == "24-Hour Forecast":

    st.header(
        "🔮 Next 24-Hour Power Forecast"
    )

    st.write(
        "Forecast generated using the trained "
        "Random Forest model."
    )

    # -----------------------------------------------------
    # Check sufficient historical data
    # -----------------------------------------------------

    if len(df) < 168:

        st.error(
            "At least 168 historical records are required "
            "to generate the forecast."
        )

        st.stop()


    # -----------------------------------------------------
    # Generate future predictions
    # -----------------------------------------------------

    history = df[
        [
            "timestamp",
            "power_consumption_mw"
        ]
    ].copy()

    predictions = []

    last_timestamp = history[
        "timestamp"
    ].iloc[-1]


    for i in range(1, 25):

        future_timestamp = (
            last_timestamp
            + pd.Timedelta(hours=i)
        )

        values = history[
            "power_consumption_mw"
        ].tolist()

        # Need previous 1 hour
        lag_1 = values[-1]

        # Need value 24 hours ago
        lag_24 = values[-24]

        # Need value 168 hours ago
        lag_168 = values[-168]

        # Rolling 24-hour average
        rolling_24 = np.mean(
            values[-24:]
        )

        # Rolling 168-hour average
        rolling_168 = np.mean(
            values[-168:]
        )


        # Calendar features

        hour = future_timestamp.hour

        day = future_timestamp.day

        day_of_week = (
            future_timestamp.dayofweek
        )

        month = future_timestamp.month

        day_of_year = (
            future_timestamp.dayofyear
        )

        is_weekend = int(
            day_of_week >= 5
        )


        # Create model input

        input_data = pd.DataFrame(
            [[
                hour,
                day,
                day_of_week,
                month,
                day_of_year,
                is_weekend,
                lag_1,
                lag_24,
                lag_168,
                rolling_24,
                rolling_168
            ]],
            columns=features
        )


        # Prediction

        prediction = model.predict(
            input_data
        )[0]

        predictions.append(
            prediction
        )


        # Add predicted value to history
        # so the next hour can use it.

        history = pd.concat(
            [
                history,
                pd.DataFrame(
                    {
                        "timestamp": [
                            future_timestamp
                        ],
                        "power_consumption_mw": [
                            prediction
                        ]
                    }
                )
            ],
            ignore_index=True
        )


    # -----------------------------------------------------
    # Create forecast dataframe
    # -----------------------------------------------------

    forecast_data = pd.DataFrame(
        {
            "timestamp": [
                last_timestamp
                + pd.Timedelta(hours=i)
                for i in range(1, 25)
            ],
            "predicted_power_mw": predictions
        }
    )


    # -----------------------------------------------------
    # Forecast metrics
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Forecast",
        f"{forecast_data['predicted_power_mw'].mean():.2f} MW"
    )

    col2.metric(
        "Peak Forecast",
        f"{forecast_data['predicted_power_mw'].max():.2f} MW"
    )

    col3.metric(
        "Minimum Forecast",
        f"{forecast_data['predicted_power_mw'].min():.2f} MW"
    )


    # -----------------------------------------------------
    # Peak information
    # -----------------------------------------------------

    peak_index = forecast_data[
        "predicted_power_mw"
    ].idxmax()

    peak_value = forecast_data.loc[
        peak_index,
        "predicted_power_mw"
    ]

    peak_time = forecast_data.loc[
        peak_index,
        "timestamp"
    ]

    st.success(
        f"⚡ Predicted peak consumption: "
        f"{peak_value:.2f} MW"
    )

    st.info(
        f"Expected peak time: {peak_time}"
    )


    # -----------------------------------------------------
    # Forecast chart
    # -----------------------------------------------------

    st.subheader(
        "📈 Next 24-Hour Forecast Trend"
    )

    chart_df = forecast_data.set_index(
        "timestamp"
    )[[
        "predicted_power_mw"
    ]]

    st.line_chart(
        chart_df
    )


    # -----------------------------------------------------
    # Forecast table
    # -----------------------------------------------------

    st.subheader(
        "📋 Forecast Readings"
    )

    st.dataframe(
        forecast_data,
        use_container_width=True
    )


# =========================================================
# MODEL PERFORMANCE
# =========================================================

elif page == "Model Performance":

    st.header(
        "🤖 Random Forest Model Performance"
    )

    st.write(
        "Performance of the trained Random Forest "
        "power consumption forecasting model."
    )


    # -----------------------------------------------------
    # Remove rows with missing lag/rolling features
    # -----------------------------------------------------

    evaluation_df = df.dropna(
        subset=features
    ).copy()


    if len(evaluation_df) == 0:

        st.error(
            "Not enough data available for model evaluation."
        )

        st.stop()


    X = evaluation_df[features]

    y = evaluation_df[target]


    # -----------------------------------------------------
    # Time-series 80/20 split
    # -----------------------------------------------------

    split = int(
        len(evaluation_df) * 0.8
    )

    X_test = X.iloc[split:]

    y_test = y.iloc[split:]


    # -----------------------------------------------------
    # Predictions
    # -----------------------------------------------------

    y_pred = model.predict(
        X_test
    )


    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    mae = mean_absolute_error(
        y_test,
        y_pred
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            y_pred
        )
    )

    r2 = r2_score(
        y_test,
        y_pred
    )


    # -----------------------------------------------------
    # Display metrics
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "MAE",
        f"{mae:.2f} MW"
    )

    col2.metric(
        "RMSE",
        f"{rmse:.2f} MW"
    )

    col3.metric(
        "R² Score",
        f"{r2:.4f}"
    )


    st.subheader(
        "📊 Actual vs Predicted"
    )


    comparison = pd.DataFrame(
        {
            "Actual": y_test.values,
            "Predicted": y_pred
        }
    )


    st.line_chart(
        comparison.head(200)
    )


    st.subheader(
        "📋 Prediction Comparison"
    )

    st.dataframe(
        comparison.head(50),
        use_container_width=True
    )


    st.info(
        "The model was trained using an 80% historical "
        "training split and evaluated on the later 20% "
        "test period."
    )


# =========================================================
# NATURAL LANGUAGE QUERY
# =========================================================

elif page == "Natural Language Query":

    st.header(
        "💬 Natural Language Query"
    )

    st.write(
        "Ask questions about historical power consumption, "
        "24-hour forecasts, and model performance."
    )

    st.info(
        "💡 Example: What is the predicted peak consumption?"
    )


    question = st.text_input(
        "Enter your question",
        placeholder=(
            "Example: What is the predicted peak consumption?"
        )
    )


    if question:

        q = question.lower().strip()


        # =================================================
        # BASIC HISTORICAL VALUES
        # =================================================

        values = df[target]


        # =================================================
        # TOP N
        # =================================================

        top_match = re.search(
            r"(?:top|highest|largest)\s*(\d+)",
            q
        )


        if (
            top_match
            and any(
                word in q
                for word in [
                    "peak",
                    "reading",
                    "consumption",
                    "value",
                    "power"
                ]
            )
        ):

            n = int(
                top_match.group(1)
            )

            n = max(
                1,
                min(
                    n,
                    len(df)
                )
            )

            top_records = df.nlargest(
                n,
                target
            )

            st.subheader(
                f"📊 Top {n} Peak Readings"
            )

            st.dataframe(
                top_records,
                use_container_width=True
            )

            st.metric(
                "Highest Consumption",
                f"{top_records[target].max():.2f} MW"
            )


        # =================================================
        # FORECAST QUESTIONS
        # =================================================

        elif any(
            word in q
            for word in [
                "forecast",
                "predicted",
                "prediction",
                "future",
                "next 24",
                "tomorrow"
            ]
        ):

            # Generate forecast using same logic

            history = df[
                [
                    "timestamp",
                    "power_consumption_mw"
                ]
            ].copy()

            predictions = []

            last_timestamp = history[
                "timestamp"
            ].iloc[-1]


            for i in range(1, 25):

                future_timestamp = (
                    last_timestamp
                    + pd.Timedelta(hours=i)
                )

                values_list = history[
                    "power_consumption_mw"
                ].tolist()

                input_data = pd.DataFrame(
                    [[
                        future_timestamp.hour,
                        future_timestamp.day,
                        future_timestamp.dayofweek,
                        future_timestamp.month,
                        future_timestamp.dayofyear,
                        int(
                            future_timestamp.dayofweek >= 5
                        ),
                        values_list[-1],
                        values_list[-24],
                        values_list[-168],
                        np.mean(
                            values_list[-24:]
                        ),
                        np.mean(
                            values_list[-168:]
                        )
                    ]],
                    columns=features
                )

                prediction = model.predict(
                    input_data
                )[0]

                predictions.append(
                    prediction
                )

                history = pd.concat(
                    [
                        history,
                        pd.DataFrame(
                            {
                                "timestamp": [
                                    future_timestamp
                                ],
                                "power_consumption_mw": [
                                    prediction
                                ]
                            }
                        )
                    ],
                    ignore_index=True
                )


            forecast_data = pd.DataFrame(
                {
                    "timestamp": [
                        last_timestamp
                        + pd.Timedelta(hours=i)
                        for i in range(1, 25)
                    ],
                    "predicted_power_mw": predictions
                }
            )


            # Peak

            if any(
                word in q
                for word in [
                    "peak",
                    "maximum",
                    "max",
                    "highest"
                ]
            ):

                index = forecast_data[
                    "predicted_power_mw"
                ].idxmax()

                value = forecast_data.loc[
                    index,
                    "predicted_power_mw"
                ]

                time = forecast_data.loc[
                    index,
                    "timestamp"
                ]

                st.success(
                    f"Predicted peak consumption "
                    f"is {value:.2f} MW."
                )

                st.metric(
                    "Predicted Peak",
                    f"{value:.2f} MW"
                )

                st.info(
                    f"Expected peak time: {time}"
                )


            # Minimum

            elif any(
                word in q
                for word in [
                    "minimum",
                    "lowest",
                    "smallest",
                    "min"
                ]
            ):

                index = forecast_data[
                    "predicted_power_mw"
                ].idxmin()

                value = forecast_data.loc[
                    index,
                    "predicted_power_mw"
                ]

                st.success(
                    f"Predicted minimum consumption "
                    f"is {value:.2f} MW."
                )

                st.metric(
                    "Predicted Minimum",
                    f"{value:.2f} MW"
                )


            # Average

            elif any(
                word in q
                for word in [
                    "average",
                    "mean",
                    "avg"
                ]
            ):

                value = forecast_data[
                    "predicted_power_mw"
                ].mean()

                st.success(
                    f"Predicted average consumption "
                    f"is {value:.2f} MW."
                )

                st.metric(
                    "Predicted Average",
                    f"{value:.2f} MW"
                )


            # Complete forecast

            else:

                st.success(
                    "The next 24-hour forecast "
                    "has been generated successfully."
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Average",
                    f"{forecast_data['predicted_power_mw'].mean():.2f} MW"
                )

                col2.metric(
                    "Peak",
                    f"{forecast_data['predicted_power_mw'].max():.2f} MW"
                )

                col3.metric(
                    "Minimum",
                    f"{forecast_data['predicted_power_mw'].min():.2f} MW"
                )


            st.subheader(
                "📋 Forecast"
            )

            st.dataframe(
                forecast_data,
                use_container_width=True
            )


        # =================================================
        # LAST / RECENT READINGS
        # =================================================

        elif (
            "last" in q
            or "recent" in q
            or "latest" in q
        ):

            number_match = re.search(
                r"(?:last|recent|latest)\s*(\d+)",
                q
            )

            n = (
                int(number_match.group(1))
                if number_match
                else 10
            )

            n = max(
                1,
                min(
                    n,
                    len(df)
                )
            )

            st.dataframe(
                df.tail(n),
                use_container_width=True
            )


        # =================================================
        # AVERAGE
        # =================================================

        elif (
            "average" in q
            or "mean" in q
        ):

            st.success(
                f"Average power consumption "
                f"is {values.mean():.2f} MW."
            )

            st.metric(
                "Average Consumption",
                f"{values.mean():.2f} MW"
            )


        # =================================================
        # MINIMUM
        # =================================================

        elif any(
            word in q
            for word in [
                "minimum",
                "lowest",
                "smallest"
            ]
        ):

            index = values.idxmin()

            st.success(
                f"Minimum power consumption "
                f"is {values.min():.2f} MW."
            )

            st.dataframe(
                df.loc[[index]],
                use_container_width=True
            )


        # =================================================
        # MAXIMUM / PEAK
        # =================================================

        elif any(
            word in q
            for word in [
                "maximum",
                "max",
                "peak",
                "highest"
            ]
        ):

            index = values.idxmax()

            st.success(
                f"Peak power consumption "
                f"is {values.max():.2f} MW."
            )

            st.dataframe(
                df.loc[[index]],
                use_container_width=True
            )


        # =================================================
        # TOTAL
        # =================================================

        elif "total" in q:

            st.success(
                f"Total recorded consumption "
                f"is {values.sum():.2f} MW."
            )


        # =================================================
        # NUMBER OF RECORDS
        # =================================================

        elif any(
            word in q
            for word in [
                "how many",
                "number of records",
                "data points",
                "record count"
            ]
        ):

            st.success(
                f"The dataset contains "
                f"{len(df):,} valid power "
                "consumption records."
            )


        # =================================================
        # MODEL PERFORMANCE
        # =================================================

        elif any(
            word in q
            for word in [
                "model",
                "algorithm",
                "mae",
                "rmse",
                "r2",
                "accuracy",
                "performance",
                "compare"
            ]
        ):

            st.info(
                "The trained Random Forest model "
                "is used for power consumption forecasting."
            )

            st.write(
                "Use the **Model Performance** page "
                "to view MAE, RMSE and R²."
            )


        # =================================================
        # UNKNOWN QUESTION
        # =================================================

        else:

            st.warning(
                "I could not identify that question."
            )

            st.markdown(
                """
                ### 💡 Try these questions

                **Historical Data**

                • What is the average power consumption?

                • What was the peak power consumption?

                • What was the minimum power consumption?

                • Show the last 10 readings.

                • Show the top 10 peak readings.

                **Forecast**

                • Show the next 24-hour forecast.

                • What is the predicted average consumption?

                • What is the predicted peak consumption?

                • What is the predicted minimum consumption?

                **Model**

                • What is the model performance?

                • Show the RMSE.

                **Dataset**

                • How many records are available?

                • What is the total consumption?
                """
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "⚡ Power Consumption Forecasting | "
    "AI & Machine Learning Project | "
    "Random Forest | "
    "Natural Language Forecast Assistant"
)

