
import streamlit as st
import pandas as pd
import os
import re

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Power Consumption Forecasting",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Regional Power Consumption Forecasting")

st.markdown(
    "### AI-Based Power Forecasting and Natural Language Query System"
)

st.divider()


# =========================================================
# FILE PATHS
# =========================================================

DATA_FOLDER = "data"

processed_file = os.path.join(
    DATA_FOLDER,
    "processed_power_consumption.csv"
)

forecast_file = os.path.join(
    DATA_FOLDER,
    "next_24_hour_forecast.csv"
)

comparison_file = os.path.join(
    DATA_FOLDER,
    "model_comparison.csv"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_csv(file_path):
    return pd.read_csv(file_path)


missing_files = [
    file for file in [
        processed_file,
        forecast_file,
        comparison_file
    ]
    if not os.path.exists(file)
]

if missing_files:
    st.error("Required data files are missing.")

    for file in missing_files:
        st.write(file)

    st.stop()


processed_df = load_csv(processed_file)
forecast_df = load_csv(forecast_file)
comparison_df = load_csv(comparison_file)


# =========================================================
# COLUMN DETECTION
# =========================================================

def normalize_column(column):
    return re.sub(
        r"[^a-z0-9]",
        "",
        str(column).lower()
    )


def find_power_column(df):

    preferred_names = [
        "power_consumption_mw",
        "predicted_power_mw",
        "power_consumption",
        "global_active_power",
        "power",
        "consumption",
        "load",
        "value"
    ]

    normalized_columns = {
        normalize_column(col): col
        for col in df.columns
    }

    for name in preferred_names:

        normalized_name = normalize_column(name)

        if normalized_name in normalized_columns:
            return normalized_columns[normalized_name]

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:
        return numeric_columns[-1]

    return None


def find_timestamp_column(df):

    preferred_names = [
        "timestamp",
        "datetime",
        "date_time",
        "date",
        "time"
    ]

    normalized_columns = {
        normalize_column(col): col
        for col in df.columns
    }

    for name in preferred_names:

        normalized_name = normalize_column(name)

        if normalized_name in normalized_columns:
            return normalized_columns[normalized_name]

    return None


power_column = find_power_column(processed_df)

timestamp_column = find_timestamp_column(processed_df)

forecast_power_column = find_power_column(forecast_df)

forecast_timestamp_column = find_timestamp_column(forecast_df)


# =========================================================
# PREPARE HISTORICAL DATA
# =========================================================

historical_df = processed_df.copy()

if power_column is not None:

    historical_df[power_column] = pd.to_numeric(
        historical_df[power_column],
        errors="coerce"
    )

    historical_df = historical_df.dropna(
        subset=[power_column]
    )

if timestamp_column is not None:

    historical_df[timestamp_column] = pd.to_datetime(
        historical_df[timestamp_column],
        errors="coerce"
    )

    historical_df = historical_df.dropna(
        subset=[timestamp_column]
    )

    historical_df = historical_df.sort_values(
        timestamp_column
    )


# =========================================================
# PREPARE FORECAST DATA
# =========================================================

forecast_data = forecast_df.copy()

if forecast_power_column is not None:

    forecast_data[forecast_power_column] = pd.to_numeric(
        forecast_data[forecast_power_column],
        errors="coerce"
    )

    forecast_data = forecast_data.dropna(
        subset=[forecast_power_column]
    )

if forecast_timestamp_column is not None:

    forecast_data[forecast_timestamp_column] = pd.to_datetime(
        forecast_data[forecast_timestamp_column],
        errors="coerce"
    )


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Historical Analysis",
        "24-Hour Forecast",
        "Model Comparison",
        "Natural Language Query"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.header("📊 Power Consumption Dashboard")

    if power_column is None:
        st.error("Power consumption column not found.")
        st.write(processed_df.columns.tolist())
        st.stop()

    values = historical_df[power_column]

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

    st.divider()

    st.subheader("📈 Historical Consumption Trend")

    if timestamp_column is not None:

        chart_df = historical_df.set_index(
            timestamp_column
        )[[power_column]]

        st.line_chart(chart_df)

    else:
        st.line_chart(
            historical_df[[power_column]]
        )

    st.subheader("📋 Dataset Preview")

    st.dataframe(
        historical_df.head(20),
        use_container_width=True
    )


# =========================================================
# HISTORICAL ANALYSIS
# =========================================================

elif page == "Historical Analysis":

    st.header("📈 Historical Power Consumption")

    if power_column is None:
        st.error("Power column not found.")
        st.stop()

    st.subheader("Statistical Summary")

    st.dataframe(
        historical_df[power_column].describe(),
        use_container_width=True
    )

    st.subheader("Historical Consumption Trend")

    if timestamp_column is not None:

        chart_df = historical_df.set_index(
            timestamp_column
        )[[power_column]]

        st.line_chart(chart_df)

    else:
        st.line_chart(
            historical_df[[power_column]]
        )

    st.subheader("Peak Consumption Records")

    top_records = historical_df.nlargest(
        10,
        power_column
    )

    st.dataframe(
        top_records,
        use_container_width=True
    )


# =========================================================
# 24-HOUR FORECAST
# =========================================================

elif page == "24-Hour Forecast":

    st.header("🔮 Next 24-Hour Power Forecast")

    if forecast_power_column is None:
        st.error("Forecast power column not found.")
        st.stop()

    forecast_values = forecast_data[
        forecast_power_column
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Forecast",
        f"{forecast_values.mean():.2f} MW"
    )

    col2.metric(
        "Peak Forecast",
        f"{forecast_values.max():.2f} MW"
    )

    col3.metric(
        "Minimum Forecast",
        f"{forecast_values.min():.2f} MW"
    )

    st.subheader("Forecast Trend")

    if forecast_timestamp_column is not None:

        chart_df = forecast_data.set_index(
            forecast_timestamp_column
        )[[forecast_power_column]]

        st.line_chart(chart_df)

    else:
        st.line_chart(
            forecast_data[[forecast_power_column]]
        )

    st.subheader("Forecast Readings")

    st.dataframe(
        forecast_data,
        use_container_width=True
    )


# =========================================================
# MODEL COMPARISON
# =========================================================

elif page == "Model Comparison":

    st.header("🤖 Forecasting Model Comparison")

    st.dataframe(
        comparison_df,
        use_container_width=True
    )

    numeric_columns = comparison_df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:

        selected_metric = st.selectbox(
            "Select Performance Metric",
            numeric_columns
        )

        st.bar_chart(
            comparison_df.set_index(
                comparison_df.columns[0]
            )[[selected_metric]]
        )

    else:
        st.info("No numeric model metrics found.")


# =========================================================
# NATURAL LANGUAGE QUERY
# =========================================================

elif page == "Natural Language Query":

    st.header("💬 Natural Language Query")

    st.write(
        "Ask questions about historical power consumption, "
        "24-hour forecasts, and model performance."
    )

    question = st.text_input(
        "Enter your question",
        placeholder="Example: Show the top 10 peak readings"
    )

    if question:

        q = question.lower().strip()

        if power_column is None:

            st.error("Historical power column not found.")
            st.stop()

        values = historical_df[power_column]

        # -------------------------------------------------
        # 1. TOP N PEAK READINGS
        # IMPORTANT: Check this BEFORE generic peak queries.
        # -------------------------------------------------

        top_match = re.search(
            r"(?:top|highest|largest)\s*(\d+)",
            q
        )

        if (
            top_match
            and any(word in q for word in [
                "peak",
                "reading",
                "consumption",
                "value",
                "power"
            ])
        ):

            n = int(top_match.group(1))

            n = max(1, min(n, len(historical_df)))

            top_records = historical_df.nlargest(
                n,
                power_column
            )

            st.success(
                f"Here are the top {n} power consumption readings."
            )

            st.dataframe(
                top_records,
                use_container_width=True
            )

            st.metric(
                "Highest Consumption",
                f"{top_records[power_column].max():.2f} MW"
            )

        # -------------------------------------------------
        # 2. LAST N READINGS
        # -------------------------------------------------

        elif (
            "last" in q
            or "recent" in q
            or "latest" in q
        ) and any(word in q for word in [
            "reading",
            "record",
            "data",
            "consumption"
        ]):

            number_match = re.search(
                r"(?:last|recent|latest)\s*(\d+)",
                q
            )

            n = int(number_match.group(1)) if number_match else 10

            n = max(1, min(n, len(historical_df)))

            last_records = historical_df.tail(n)

            st.success(
                f"Showing the last {n} readings."
            )

            st.dataframe(
                last_records,
                use_container_width=True
            )

        # -------------------------------------------------
        # 3. AVERAGE CONSUMPTION AT SPECIFIC HOUR
        # -------------------------------------------------

        elif (
            ("average" in q or "mean" in q)
            and re.search(r"\b(at|during)\b", q)
            and timestamp_column is not None
        ):

            hour_match = re.search(
                r"\b(at|during)\s+(\d{1,2})(?::\d{2})?\s*(am|pm)?\b",
                q
            )

            if hour_match:

                hour = int(hour_match.group(2))
                period = hour_match.group(3)

                if period == "pm" and hour < 12:
                    hour += 12

                elif period == "am" and hour == 12:
                    hour = 0

                if 0 <= hour <= 23:

                    matching_values = historical_df[
                        historical_df[timestamp_column].dt.hour == hour
                    ][power_column]

                    if len(matching_values) > 0:

                        result = matching_values.mean()

                        st.success(
                            f"Average power consumption at "
                            f"{hour:02d}:00 is {result:.2f} MW."
                        )

                        st.metric(
                            "Average Consumption",
                            f"{result:.2f} MW"
                        )

                        st.write(
                            f"Number of matching readings: "
                            f"{len(matching_values)}"
                        )

                    else:
                        st.warning(
                            "No readings found for that hour."
                        )

                else:
                    st.warning(
                        "Please enter a valid hour between 0 and 23."
                    )

            else:
                st.info(
                    "Try asking: What is the average consumption at 5 PM?"
                )

        # -------------------------------------------------
        # 4. FORECAST QUESTIONS
        # -------------------------------------------------

        elif any(word in q for word in [
            "forecast",
            "predicted",
            "future",
            "next 24",
            "tomorrow"
        ]):

            if forecast_power_column is None:

                st.error("Forecast data is unavailable.")

            else:

                fv = forecast_data[forecast_power_column]

                st.subheader("🔮 Forecast Results")

                if "peak" in q or "maximum" in q:

                    st.success(
                        f"Predicted peak consumption is "
                        f"{fv.max():.2f} MW."
                    )

                elif "minimum" in q or "lowest" in q:

                    st.success(
                        f"Predicted minimum consumption is "
                        f"{fv.min():.2f} MW."
                    )

                elif "average" in q or "mean" in q:

                    st.success(
                        f"Predicted average consumption is "
                        f"{fv.mean():.2f} MW."
                    )

                else:

                    st.success(
                        f"The forecast contains {len(fv)} readings. "
                        f"Average: {fv.mean():.2f} MW, "
                        f"peak: {fv.max():.2f} MW, "
                        f"minimum: {fv.min():.2f} MW."
                    )

                st.dataframe(
                    forecast_data,
                    use_container_width=True
                )

                st.line_chart(
                    forecast_data.set_index(
                        forecast_timestamp_column
                    )[[forecast_power_column]]
                    if forecast_timestamp_column is not None
                    else forecast_data[[forecast_power_column]]
                )

        # -------------------------------------------------
        # 5. MODEL COMPARISON
        # -------------------------------------------------

        elif any(word in q for word in [
            "model",
            "algorithm",
            "mae",
            "rmse",
            "mape",
            "accuracy",
            "performance"
        ]):

            st.subheader("🤖 Model Performance")

            st.dataframe(
                comparison_df,
                use_container_width=True
            )

        # -------------------------------------------------
        # 6. TOTAL CONSUMPTION
        # -------------------------------------------------

        elif "total" in q:

            st.success(
                f"Total recorded consumption is "
                f"{values.sum():.2f} MW."
            )

        # -------------------------------------------------
        # 7. AVERAGE
        # -------------------------------------------------

        elif "average" in q or "mean" in q:

            st.success(
                f"Average power consumption is "
                f"{values.mean():.2f} MW."
            )

        # -------------------------------------------------
        # 8. MINIMUM
        # -------------------------------------------------

        elif any(word in q for word in [
            "minimum",
            "lowest",
            "smallest"
        ]):

            min_index = historical_df[power_column].idxmin()

            st.success(
                f"Minimum power consumption is "
                f"{values.min():.2f} MW."
            )

            st.dataframe(
                historical_df.loc[[min_index]],
                use_container_width=True
            )

        # -------------------------------------------------
        # 9. MAXIMUM / PEAK
        # -------------------------------------------------

        elif any(word in q for word in [
            "maximum",
            "max",
            "peak",
            "highest"
        ]):

            max_index = historical_df[power_column].idxmax()

            st.success(
                f"Peak power consumption is "
                f"{values.max():.2f} MW."
            )

            st.dataframe(
                historical_df.loc[[max_index]],
                use_container_width=True
            )

        # -------------------------------------------------
        # 10. NUMBER OF RECORDS
        # -------------------------------------------------

        elif any(word in q for word in [
            "how many",
            "number of records",
            "data points",
            "record count"
        ]):

            st.success(
                f"The dataset contains {len(values):,} "
                f"valid power consumption records."
            )

        # -------------------------------------------------
        # 11. UNKNOWN QUESTION
        # -------------------------------------------------

        else:

            st.warning(
                "I could not identify that question. "
                "Please try one of the supported questions below."
            )

            st.markdown("""
            **Try these questions:**

            1. What is the average power consumption?
            2. What was the peak power consumption?
            3. What was the minimum power consumption?
            4. What is the average consumption at 5 PM?
            5. Show the last 10 readings.
            6. Show the top 10 peak readings.
            7. Show the next 24-hour forecast.
            8. What is the predicted average consumption?
            9. What is the predicted peak consumption?
            10. Compare the forecasting models.
            11. How many records are available?
            12. What is the total consumption?
            """)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "⚡ Power Consumption Forecasting | "
    "AI & Machine Learning Project"
)
