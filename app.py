import streamlit as st
import pandas as pd
import os
import re

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Power Consumption Forecasting",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.title("⚡ Regional Power Consumption Forecasting")
st.markdown(
    "### AI-Based Power Forecasting and Natural Language Query System"
)

st.divider()

# ---------------------------------------------------------
# FILE PATHS
# ---------------------------------------------------------
DATA_FOLDER = "data"

processed_file = os.path.join(
    DATA_FOLDER, "processed_power_consumption.csv"
)

forecast_file = os.path.join(
    DATA_FOLDER, "next_24_hour_forecast.csv"
)

comparison_file = os.path.join(
    DATA_FOLDER, "model_comparison.csv"
)

# ---------------------------------------------------------
# CHECK FILES
# ---------------------------------------------------------
missing_files = []

for file in [processed_file, forecast_file, comparison_file]:
    if not os.path.exists(file):
        missing_files.append(file)

if missing_files:
    st.error("Some required data files are missing:")
    for file in missing_files:
        st.write(file)
    st.stop()

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    processed = pd.read_csv(processed_file)
    forecast = pd.read_csv(forecast_file)
    comparison = pd.read_csv(comparison_file)

    return processed, forecast, comparison


processed_df, forecast_df, comparison_df = load_data()

# ---------------------------------------------------------
# FIND NUMERIC POWER COLUMN
# ---------------------------------------------------------
def find_power_column(df):
    possible_names = [
        "power_consumption",
        "power",
        "consumption",
        "Global_active_power",
        "global_active_power",
        "load",
        "value"
    ]

    for name in possible_names:
        if name in df.columns:
            return name

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:
        return numeric_columns[-1]

    return None


power_column = find_power_column(processed_df)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
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
        st.warning("Could not automatically identify the power column.")
        st.write("Available columns:")
        st.write(processed_df.columns.tolist())
        st.stop()

    values = pd.to_numeric(
        processed_df[power_column],
        errors="coerce"
    ).dropna()

    if len(values) == 0:
        st.warning("No numeric power consumption data found.")
        st.stop()

    average_value = values.mean()
    maximum_value = values.max()
    minimum_value = values.min()
    total_records = len(values)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Average Consumption",
            f"{average_value:.2f}"
        )

    with col2:
        st.metric(
            "Peak Consumption",
            f"{maximum_value:.2f}"
        )

    with col3:
        st.metric(
            "Minimum Consumption",
            f"{minimum_value:.2f}"
        )

    with col4:
        st.metric(
            "Data Records",
            f"{total_records:,}"
        )

    st.divider()

    st.subheader("📈 Power Consumption Overview")

    chart_data = processed_df[[power_column]].copy()
    chart_data[power_column] = pd.to_numeric(
        chart_data[power_column],
        errors="coerce"
    )

    st.line_chart(chart_data)

    st.subheader("📋 Dataset Preview")

    st.dataframe(
        processed_df.head(20),
        use_container_width=True
    )


# =========================================================
# HISTORICAL ANALYSIS
# =========================================================
elif page == "Historical Analysis":

    st.header("📈 Historical Power Consumption")

    if power_column is None:
        st.error("Power consumption column could not be identified.")
        st.stop()

    chart_data = processed_df.copy()

    chart_data[power_column] = pd.to_numeric(
        chart_data[power_column],
        errors="coerce"
    )

    chart_data = chart_data.dropna(
        subset=[power_column]
    )

    st.write(
        f"Showing historical values from column: "
        f"**{power_column}**"
    )

    st.line_chart(
        chart_data[[power_column]]
    )

    st.subheader("Statistical Summary")

    st.dataframe(
        chart_data[power_column].describe(),
        use_container_width=True
    )


# =========================================================
# 24 HOUR FORECAST
# =========================================================
elif page == "24-Hour Forecast":

    st.header("🔮 Next 24-Hour Power Forecast")

    st.success(
        "The following values are generated by the forecasting "
        "models used in this project."
    )

    st.dataframe(
        forecast_df,
        use_container_width=True
    )

    # Find numeric forecast column
    numeric_columns = forecast_df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:

        forecast_column = numeric_columns[-1]

        st.subheader("📈 Forecast Visualization")

        chart_df = forecast_df[[forecast_column]].copy()

        st.line_chart(chart_df)

        forecast_values = pd.to_numeric(
            forecast_df[forecast_column],
            errors="coerce"
        ).dropna()

        if len(forecast_values) > 0:

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Forecast Average",
                    f"{forecast_values.mean():.2f}"
                )

            with col2:
                st.metric(
                    "Forecast Peak",
                    f"{forecast_values.max():.2f}"
                )

            with col3:
                st.metric(
                    "Forecast Minimum",
                    f"{forecast_values.min():.2f}"
                )

    else:
        st.warning(
            "No numeric forecast column was detected."
        )


# =========================================================
# MODEL COMPARISON
# =========================================================
elif page == "Model Comparison":

    st.header("🤖 Forecasting Model Comparison")

    st.write(
        "Comparison of the forecasting models used in the project."
    )

    st.dataframe(
        comparison_df,
        use_container_width=True
    )

    st.subheader("📊 Model Performance")

    numeric_columns = comparison_df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:

        selected_metric = st.selectbox(
            "Select a performance metric",
            numeric_columns
        )

        model_chart = comparison_df[
            [selected_metric]
        ].copy()

        st.bar_chart(model_chart)

    else:
        st.info(
            "No numeric performance metrics were detected."
        )


# =========================================================
# NATURAL LANGUAGE QUERY
# =========================================================
elif page == "Natural Language Query":

    st.header("💬 Natural Language Query")

    st.write(
        "Ask simple questions about the power consumption dataset."
    )

    question = st.text_input(
        "Enter your question",
        placeholder="Example: What is the average power consumption?"
    )

    if question:

        question_lower = question.lower()

        if power_column is None:
            st.error(
                "Power consumption column could not be identified."
            )
            st.stop()

        values = pd.to_numeric(
            processed_df[power_column],
            errors="coerce"
        ).dropna()

        # ---------------------------------------------
        # AVERAGE
        # ---------------------------------------------
        if (
            "average" in question_lower
            or "mean" in question_lower
        ):

            result = values.mean()

            st.success(
                f"Average power consumption is **{result:.2f}**."
            )

        # ---------------------------------------------
        # MAXIMUM / PEAK
        # ---------------------------------------------
        elif (
            "maximum" in question_lower
            or "max" in question_lower
            or "peak" in question_lower
            or "highest" in question_lower
        ):

            result = values.max()

            st.success(
                f"Peak power consumption is **{result:.2f}**."
            )

        # ---------------------------------------------
        # MINIMUM
        # ---------------------------------------------
        elif (
            "minimum" in question_lower
            or "min" in question_lower
            or "lowest" in question_lower
        ):

            result = values.min()

            st.success(
                f"Minimum power consumption is **{result:.2f}**."
            )

        # ---------------------------------------------
        # TOTAL
        # ---------------------------------------------
        elif "total" in question_lower:

            result = values.sum()

            st.success(
                f"Total recorded power consumption is **{result:.2f}**."
            )

        # ---------------------------------------------
        # NUMBER OF RECORDS
        # ---------------------------------------------
        elif (
            "how many" in question_lower
            or "records" in question_lower
            or "data points" in question_lower
        ):

            st.success(
                f"The dataset contains **{len(values):,}** "
                "valid power consumption records."
            )

        # ---------------------------------------------
        # FORECAST
        # ---------------------------------------------
        elif (
    "forecast" in question_lower
    or "future" in question_lower
    or "next 24" in question_lower
    or "predicted" in question_lower
):

    st.subheader("🔮 Forecast Results")

    # Find numeric forecast column
    numeric_columns = forecast_df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:

        forecast_column = numeric_columns[-1]

        forecast_values = pd.to_numeric(
            forecast_df[forecast_column],
            errors="coerce"
        ).dropna()

        if len(forecast_values) > 0:

            average_forecast = forecast_values.mean()
            peak_forecast = forecast_values.max()
            minimum_forecast = forecast_values.min()

            # Natural-language response
            st.success(
                f"The next 24-hour power consumption forecast has been generated. "
                f"The predicted average consumption is {average_forecast:.2f}, "
                f"with a peak of {peak_forecast:.2f} and a minimum of "
                f"{minimum_forecast:.2f}."
            )

            # Forecast summary
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Average Forecast",
                    f"{average_forecast:.2f}"
                )

            with col2:
                st.metric(
                    "Peak Forecast",
                    f"{peak_forecast:.2f}"
                )

            with col3:
                st.metric(
                    "Minimum Forecast",
                    f"{minimum_forecast:.2f}"
                )

            # Forecast graph
            st.subheader("📈 Forecast Trend")

            st.line_chart(
                forecast_df[[forecast_column]]
            )

            # Forecast table
            st.subheader("📋 Next 24-Hour Forecast")

            st.dataframe(
                forecast_df,
                use_container_width=True
            )

        else:
            st.warning(
                "No valid numeric forecast values were found."
            )

    else:
        st.warning(
            "No numeric forecast column was detected."
        )

        # ---------------------------------------------
        # MODEL
        # ---------------------------------------------
        elif (
            "model" in question_lower
            or "algorithm" in question_lower
            or "accuracy" in question_lower
        ):

            st.success(
                "The project compares multiple forecasting "
                "models. Open the **Model Comparison** section "
                "to view their performance."
            )

            st.dataframe(
                comparison_df,
                use_container_width=True
            )

        # ---------------------------------------------
        # UNKNOWN QUESTION
        # ---------------------------------------------
        else:

            st.info(
                "I can answer questions such as:\n\n"
                "• What is the average power consumption?\n"
                "• What is the peak consumption?\n"
                "• What is the minimum consumption?\n"
                "• What is the total consumption?\n"
                "• How many records are available?\n"
                "• Show the forecast\n"
                "• What models were used?"
            )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.divider()

st.caption(
    "⚡ Power Consumption Forecasting | "
    "AI & Machine Learning Project"
)
