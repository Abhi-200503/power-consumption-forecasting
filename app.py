import streamlit as st
import pandas as pd
import os
import re

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Power Forecast AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS - ATTRACTIVE UI
# =========================================================

st.markdown("""
<style>

    /* ================================
       MAIN APPLICATION BACKGROUND
       ================================ */

    .stApp {
        background: linear-gradient(
            135deg,
            #f8fbff 0%,
            #eef5ff 50%,
            #f7faff 100%
        );
    }

    /* ================================
       HEADER CARD
       ================================ */

    .header-card {
        padding: 35px 25px;
        border-radius: 22px;
        background: linear-gradient(
            135deg,
            #ffffff,
            #eaf3ff
        );
        border: 1px solid #d8e6f7;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        margin-bottom: 25px;
        text-align: center;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .main-subtitle {
        font-size: 18px;
        color: #5f6b7a;
        margin-top: 5px;
    }

    /* ================================
       FEATURE CARDS
       ================================ */

    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #e0e8f2;
        box-shadow: 0 5px 18px rgba(0, 0, 0, 0.06);
        min-height: 120px;
    }

    .feature-title {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .feature-text {
        color: #667085;
        font-size: 14px;
    }

    /* ================================
       METRIC CARDS
       ================================ */

    div[data-testid="metric-container"] {
        background: white;
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #e0e8f2;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.06);
    }

    /* ================================
       SIDEBAR
       ================================ */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #eef5ff 0%,
            #ffffff 100%
        );
        border-right: 1px solid #dce7f5;
    }

    /* ================================
       SIDEBAR TITLE
       ================================ */

    .sidebar-title {
        text-align: center;
        font-size: 23px;
        font-weight: 800;
        padding: 10px 0 15px 0;
    }

    .sidebar-description {
        text-align: center;
        font-size: 13px;
        color: #667085;
        margin-bottom: 20px;
    }

    /* ================================
       INPUT BOX
       ================================ */

    div[data-baseweb="input"] {
        border-radius: 12px;
    }

    /* ================================
       BUTTON
       ================================ */

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 20px;
    }

    /* ================================
       DATAFRAME
       ================================ */

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ================================
       ALERT BOXES
       ================================ */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* ================================
       HEADINGS
       ================================ */

    h1, h2, h3 {
        font-weight: 700;
    }

    /* ================================
       FOOTER
       ================================ */

    .footer {
        text-align: center;
        color: #718096;
        font-size: 14px;
        padding: 25px;
        margin-top: 20px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="header-card">

    <div class="main-title">
        ⚡ Power Consumption Forecasting
    </div>

    <div class="main-subtitle">
        AI-Based Power Forecasting & Natural Language Query System
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# FEATURE CARDS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("""
    <div class="feature-card">

        <div class="feature-title">
            📊 Historical Analysis
        </div>

        <div class="feature-text">
            Analyze historical power consumption,
            trends, statistics and peak readings.
        </div>

    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown("""
    <div class="feature-card">

        <div class="feature-title">
            🔮 24-Hour Forecast
        </div>

        <div class="feature-text">
            View predicted power consumption
            for the next 24 hours.
        </div>

    </div>
    """, unsafe_allow_html=True)


with col3:

    st.markdown("""
    <div class="feature-card">

        <div class="feature-title">
            💬 Natural Language
        </div>

        <div class="feature-text">
            Ask questions about consumption
            and forecasts using simple English.
        </div>

    </div>
    """, unsafe_allow_html=True)


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


# =========================================================
# CHECK REQUIRED FILES
# =========================================================

missing_files = [
    file
    for file in [
        processed_file,
        forecast_file,
        comparison_file
    ]
    if not os.path.exists(file)
]


if missing_files:

    st.error("❌ Required data files are missing.")

    st.write(
        "Please make sure these files are available:"
    )

    for file in missing_files:

        st.write(
            f"• {file}"
        )

    st.stop()


# =========================================================
# LOAD DATASETS
# =========================================================

processed_df = load_csv(
    processed_file
)

forecast_df = load_csv(
    forecast_file
)

comparison_df = load_csv(
    comparison_file
)


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

        "predicted_power",

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

        normalized_name = normalize_column(
            name
        )

        if normalized_name in normalized_columns:

            return normalized_columns[
                normalized_name
            ]

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

        normalized_name = normalize_column(
            name
        )

        if normalized_name in normalized_columns:

            return normalized_columns[
                normalized_name
            ]

    return None


# =========================================================
# DETECT COLUMNS
# =========================================================

power_column = find_power_column(
    processed_df
)

timestamp_column = find_timestamp_column(
    processed_df
)

forecast_power_column = find_power_column(
    forecast_df
)

forecast_timestamp_column = find_timestamp_column(
    forecast_df
)


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

    forecast_data[
        forecast_power_column
    ] = pd.to_numeric(
        forecast_data[
            forecast_power_column
        ],
        errors="coerce"
    )

    forecast_data = forecast_data.dropna(
        subset=[forecast_power_column]
    )


if forecast_timestamp_column is not None:

    forecast_data[
        forecast_timestamp_column
    ] = pd.to_datetime(
        forecast_data[
            forecast_timestamp_column
        ],
        errors="coerce"
    )

    forecast_data = forecast_data.dropna(
        subset=[forecast_timestamp_column]
    )


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-title">
        ⚡ Power Forecast AI
    </div>

    <div class="sidebar-description">
        Intelligent Power Consumption Analysis
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "📌 Select Module",
        [
            "Dashboard",
            "Historical Analysis",
            "24-Hour Forecast",
            "Model Comparison",
            "Natural Language Query"
        ]
    )

    st.divider()

    st.caption(
        "⚡ AI & Machine Learning Project"
    )


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.header(
        "📊 Power Consumption Dashboard"
    )

    st.write(
        "Overview of historical power consumption."
    )

    if power_column is None:

        st.error(
            "Power consumption column not found."
        )

        st.write(
            processed_df.columns.tolist()
        )

        st.stop()

    values = historical_df[
        power_column
    ]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📊 Average Consumption",
        f"{values.mean():.2f} MW"
    )

    col2.metric(
        "🔺 Peak Consumption",
        f"{values.max():.2f} MW"
    )

    col3.metric(
        "🔻 Minimum Consumption",
        f"{values.min():.2f} MW"
    )

    col4.metric(
        "📁 Total Records",
        f"{len(values):,}"
    )

    st.divider()

    st.subheader(
        "📈 Historical Consumption Trend"
    )

    if timestamp_column is not None:

        chart_df = historical_df.set_index(
            timestamp_column
        )[[power_column]]

        st.line_chart(
            chart_df
        )

    else:

        st.line_chart(
            historical_df[
                [power_column]
            ]
        )

    st.subheader(
        "📋 Dataset Preview"
    )

    st.dataframe(
        historical_df.head(20),
        use_container_width=True
    )


# =========================================================
# HISTORICAL ANALYSIS
# =========================================================

elif page == "Historical Analysis":

    st.header(
        "📈 Historical Power Consumption"
    )

    if power_column is None:

        st.error(
            "Power column not found."
        )

        st.stop()

    st.subheader(
        "📊 Statistical Summary"
    )

    st.dataframe(
        historical_df[
            power_column
        ].describe(),
        use_container_width=True
    )

    st.subheader(
        "📈 Historical Consumption Trend"
    )

    if timestamp_column is not None:

        chart_df = historical_df.set_index(
            timestamp_column
        )[[power_column]]

        st.line_chart(
            chart_df
        )

    else:

        st.line_chart(
            historical_df[
                [power_column]
            ]
        )

    st.subheader(
        "🔥 Top 10 Peak Consumption Records"
    )

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

    st.header(
        "🔮 Next 24-Hour Power Forecast"
    )

    st.write(
        "Predicted power consumption for the next 24 hours."
    )

    if forecast_power_column is None:

        st.error(
            "Forecast power column not found."
        )

        st.write(
            "Available forecast columns:"
        )

        st.write(
            forecast_df.columns.tolist()
        )

        st.stop()

    forecast_values = forecast_data[
        forecast_power_column
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "📊 Average Forecast",
        f"{forecast_values.mean():.2f} MW"
    )

    col2.metric(
        "🔺 Peak Forecast",
        f"{forecast_values.max():.2f} MW"
    )

    col3.metric(
        "🔻 Minimum Forecast",
        f"{forecast_values.min():.2f} MW"
    )

    st.divider()

    st.subheader(
        "📈 Forecast Trend"
    )

    if forecast_timestamp_column is not None:

        chart_df = forecast_data.set_index(
            forecast_timestamp_column
        )[[forecast_power_column]]

        st.line_chart(
            chart_df
        )

    else:

        st.line_chart(
            forecast_data[
                [forecast_power_column]
            ]
        )

    st.subheader(
        "📋 Forecast Readings"
    )

    st.dataframe(
        forecast_data,
        use_container_width=True
    )


# =========================================================
# MODEL COMPARISON
# =========================================================

elif page == "Model Comparison":

    st.header(
        "🤖 Forecasting Model Comparison"
    )

    st.write(
        "Compare the performance metrics of the forecasting models."
    )

    st.dataframe(
        comparison_df,
        use_container_width=True
    )

    numeric_columns = comparison_df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:

        selected_metric = st.selectbox(
            "📊 Select Performance Metric",
            numeric_columns
        )

        st.subheader(
            f"📈 {selected_metric} Comparison"
        )

        st.bar_chart(
            comparison_df.set_index(
                comparison_df.columns[0]
            )[[selected_metric]]
        )

    else:

        st.info(
            "No numeric model metrics found."
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
        "💡 Try: What is the predicted peak consumption?"
    )

    question = st.text_input(
        "Enter your question",
        placeholder=(
            "Example: What is the predicted peak consumption?"
        )
    )

    if question:

        q = question.lower().strip()

        # -------------------------------------------------
        # HISTORICAL VALUES
        # -------------------------------------------------

        if power_column is not None:

            values = historical_df[
                power_column
            ]

        else:

            values = None


        # =================================================
        # 1. TOP N PEAK READINGS
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

            if power_column is None:

                st.error(
                    "Historical power column not found."
                )

            else:

                n = int(
                    top_match.group(1)
                )

                n = max(
                    1,
                    min(
                        n,
                        len(historical_df)
                    )
                )

                top_records = historical_df.nlargest(
                    n,
                    power_column
                )

                st.subheader(
                    f"📊 Top {n} Peak Readings"
                )

                st.success(
                    f"Here are the top {n} "
                    "highest power consumption readings."
                )

                st.dataframe(
                    top_records,
                    use_container_width=True
                )

                st.metric(
                    "Highest Consumption",
                    f"{top_records[power_column].max():.2f} MW"
                )


        # =================================================
        # 2. FORECAST QUESTIONS
        # =================================================

        elif any(
            word in q
            for word in [
                "forecast",
                "predicted",
                "prediction",
                "future",
                "next 24",
                "next 24 hour",
                "next 24 hours",
                "tomorrow"
            ]
        ):

            if forecast_power_column is None:

                st.error(
                    "Forecast data is unavailable."
                )

                st.write(
                    "Available forecast columns:"
                )

                st.write(
                    forecast_df.columns.tolist()
                )

            else:

                fv = forecast_data[
                    forecast_power_column
                ]

                st.subheader(
                    "🔮 Forecast Results"
                )


                # -----------------------------------------
                # FORECAST PEAK
                # -----------------------------------------

                if any(
                    word in q
                    for word in [
                        "peak",
                        "maximum",
                        "max",
                        "highest"
                    ]
                ):

                    max_index = fv.idxmax()

                    max_value = fv.loc[
                        max_index
                    ]

                    st.success(
                        f"Predicted peak consumption "
                        f"is {max_value:.2f} MW."
                    )

                    st.metric(
                        "🔺 Predicted Peak",
                        f"{max_value:.2f} MW"
                    )

                    if forecast_timestamp_column is not None:

                        peak_time = forecast_data.loc[
                            max_index,
                            forecast_timestamp_column
                        ]

                        st.info(
                            f"⏰ Expected peak time: "
                            f"{peak_time}"
                        )


                # -----------------------------------------
                # FORECAST MINIMUM
                # -----------------------------------------

                elif any(
                    word in q
                    for word in [
                        "minimum",
                        "lowest",
                        "smallest",
                        "min"
                    ]
                ):

                    min_index = fv.idxmin()

                    min_value = fv.loc[
                        min_index
                    ]

                    st.success(
                        f"Predicted minimum consumption "
                        f"is {min_value:.2f} MW."
                    )

                    st.metric(
                        "🔻 Predicted Minimum",
                        f"{min_value:.2f} MW"
                    )

                    if forecast_timestamp_column is not None:

                        min_time = forecast_data.loc[
                            min_index,
                            forecast_timestamp_column
                        ]

                        st.info(
                            f"⏰ Expected minimum time: "
                            f"{min_time}"
                        )


                # -----------------------------------------
                # FORECAST AVERAGE
                # -----------------------------------------

                elif any(
                    word in q
                    for word in [
                        "average",
                        "mean",
                        "avg"
                    ]
                ):

                    avg_value = fv.mean()

                    st.success(
                        f"Predicted average consumption "
                        f"is {avg_value:.2f} MW."
                    )

                    st.metric(
                        "📊 Predicted Average",
                        f"{avg_value:.2f} MW"
                    )


                # -----------------------------------------
                # COMPLETE FORECAST
                # -----------------------------------------

                else:

                    st.success(
                        f"The next 24-hour forecast "
                        f"contains {len(fv)} predicted readings."
                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Average Forecast",
                        f"{fv.mean():.2f} MW"
                    )

                    col2.metric(
                        "Peak Forecast",
                        f"{fv.max():.2f} MW"
                    )

                    col3.metric(
                        "Minimum Forecast",
                        f"{fv.min():.2f} MW"
                    )


                # -----------------------------------------
                # FORECAST TABLE
                # -----------------------------------------

                st.subheader(
                    "📋 Forecast Readings"
                )

                st.dataframe(
                    forecast_data,
                    use_container_width=True
                )


                # -----------------------------------------
                # FORECAST CHART
                # -----------------------------------------

                st.subheader(
                    "📈 Forecast Trend"
                )

                if forecast_timestamp_column is not None:

                    chart_df = forecast_data.set_index(
                        forecast_timestamp_column
                    )[[forecast_power_column]]

                    st.line_chart(
                        chart_df
                    )

                else:

                    st.line_chart(
                        forecast_data[
                            [forecast_power_column]
                        ]
                    )


        # =================================================
        # 3. LAST N READINGS
        # =================================================

        elif (
            "last" in q
            or "recent" in q
            or "latest" in q
        ) and any(
            word in q
            for word in [
                "reading",
                "record",
                "data",
                "consumption"
            ]
        ):

            if power_column is None:

                st.error(
                    "Historical power column not found."
                )

            else:

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
                        len(historical_df)
                    )
                )

                last_records = historical_df.tail(n)

                st.success(
                    f"Showing the last {n} readings."
                )

                st.dataframe(
                    last_records,
                    use_container_width=True
                )


        # =================================================
        # 4. AVERAGE AT SPECIFIC HOUR
        # =================================================

        elif (
            ("average" in q or "mean" in q)
            and re.search(
                r"\b(at|during)\b",
                q
            )
            and timestamp_column is not None
        ):

            hour_match = re.search(
                r"\b(at|during)\s+"
                r"(\d{1,2})"
                r"(?::\d{2})?\s*"
                r"(am|pm)?\b",
                q
            )

            if hour_match:

                hour = int(
                    hour_match.group(2)
                )

                period = hour_match.group(3)

                if period == "pm" and hour < 12:

                    hour += 12

                elif period == "am" and hour == 12:

                    hour = 0

                if 0 <= hour <= 23:

                    matching_values = historical_df[
                        historical_df[
                            timestamp_column
                        ].dt.hour == hour
                    ][power_column]

                    if len(matching_values) > 0:

                        result = matching_values.mean()

                        st.success(
                            f"Average power consumption "
                            f"at {hour:02d}:00 is "
                            f"{result:.2f} MW."
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
                        "Please enter a valid hour "
                        "between 0 and 23."
                    )

            else:

                st.info(
                    "Try: What is the average "
                    "consumption at 5 PM?"
                )


        # =================================================
        # 5. MODEL COMPARISON
        # =================================================

        elif any(
            word in q
            for word in [
                "model",
                "algorithm",
                "mae",
                "rmse",
                "mape",
                "accuracy",
                "performance",
                "compare"
            ]
        ):

            st.subheader(
                "🤖 Model Performance"
            )

            st.dataframe(
                comparison_df,
                use_container_width=True
            )


        # =================================================
        # 6. TOTAL CONSUMPTION
        # =================================================

        elif "total" in q:

            if power_column is not None:

                st.success(
                    f"Total recorded consumption "
                    f"is {values.sum():.2f} MW."
                )

            else:

                st.error(
                    "Historical power column not found."
                )


        # =================================================
        # 7. AVERAGE
        # =================================================

        elif (
            "average" in q
            or "mean" in q
        ):

            if power_column is not None:

                st.success(
                    f"Average power consumption "
                    f"is {values.mean():.2f} MW."
                )

            else:

                st.error(
                    "Historical power column not found."
                )


        # =================================================
        # 8. MINIMUM
        # =================================================

        elif any(
            word in q
            for word in [
                "minimum",
                "lowest",
                "smallest"
            ]
        ):

            if power_column is not None:

                min_index = historical_df[
                    power_column
                ].idxmin()

                st.success(
                    f"Minimum power consumption "
                    f"is {values.min():.2f} MW."
                )

                st.dataframe(
                    historical_df.loc[
                        [min_index]
                    ],
                    use_container_width=True
                )

            else:

                st.error(
                    "Historical power column not found."
                )


        # =================================================
        # 9. MAXIMUM / PEAK
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

            if power_column is not None:

                max_index = historical_df[
                    power_column
                ].idxmax()

                st.success(
                    f"Peak power consumption "
                    f"is {values.max():.2f} MW."
                )

                st.dataframe(
                    historical_df.loc[
                        [max_index]
                    ],
                    use_container_width=True
                )

            else:

                st.error(
                    "Historical power column not found."
                )


        # =================================================
        # 10. NUMBER OF RECORDS
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
                f"{len(historical_df):,} "
                "valid power consumption records."
            )


        # =================================================
        # 11. UNKNOWN QUESTION
        # =================================================

        else:

            st.warning(
                "I could not identify that question."
            )

            st.markdown("""
            ### 💡 Try these questions

            **Historical Data**

            1. What is the average power consumption?
            2. What was the peak power consumption?
            3. What was the minimum power consumption?
            4. What is the average consumption at 5 PM?
            5. Show the last 10 readings.
            6. Show the top 10 peak readings.

            **Forecast Data**

            7. Show the next 24-hour forecast.
            8. What is the predicted average consumption?
            9. What is the predicted peak consumption?
            10. What is the predicted minimum consumption?

            **Model Performance**

            11. Compare the forecasting models.

            **Dataset**

            12. How many records are available?
            13. What is the total consumption?
            """)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown("""
<div class="footer">

    ⚡ <b>Power Consumption Forecasting</b>
    &nbsp; | &nbsp;
    AI & Machine Learning Project
    &nbsp; | &nbsp;
    Natural Language Forecast Assistant

</div>
""", unsafe_allow_html=True)
