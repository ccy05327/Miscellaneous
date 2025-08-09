import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import calendar
import os
from datetime import datetime
import numpy as np

# --- Configuration & Setup ---
DATA_FILE = 'step_count_20250809.csv'
st.set_page_config(layout="wide", page_title="Samsung Health Dashboard")

# --- Helper Functions ---


def create_dummy_data_if_not_exists():
    """
    If the CSV file doesn't exist, create a dummy one with realistic data
    matching the user's specified format.
    """
    if not os.path.exists(DATA_FILE):
        print("Creating dummy data file...")
        dates = pd.to_datetime(pd.date_range(
            start='2020-01-01', end=datetime.today(), freq='D'))

        df = pd.DataFrame({'date': dates})

        step_counts = np.random.randint(500, 15000, size=len(df))
        high_step_indices = np.random.choice(
            df.index, size=int(len(df) * 0.05), replace=False)
        low_step_indices = np.random.choice(
            df.index, size=int(len(df) * 0.15), replace=False)
        step_counts[high_step_indices] = np.random.randint(
            20000, 40000, size=len(high_step_indices))
        step_counts[low_step_indices] = np.random.randint(
            0, 1000, size=len(low_step_indices))

        missing_days_indices = np.random.choice(
            df.index, size=int(len(df) * 0.1), replace=False)
        df = df.drop(missing_days_indices)

        df['step_count'] = step_counts[df.index]
        df['active_time'] = np.random.randint(1000000, 8000000, size=len(df))
        df['distance'] = df['step_count'] * 0.000762
        df['calorie'] = df['step_count'] * 0.04

        df = df[['date', 'step_count', 'active_time', 'distance', 'calorie']]

        df.to_csv(DATA_FILE, index=False)
        print(f"'{DATA_FILE}' created successfully.")


@st.cache_data
def load_data(filepath):
    """
    Loads step data from the specified CSV file.
    Converts 'date' column to datetime objects and sets it as the index.
    """
    try:
        df = pd.read_csv(filepath)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df.dropna(subset=['date'], inplace=True)
        df.set_index('date', inplace=True)
        return df
    except FileNotFoundError:
        st.error(
            f"Error: The data file '{filepath}' was not found. Please make sure it's in the same directory as the script.")
        return pd.DataFrame()

# --- Main Application ---


create_dummy_data_if_not_exists()
data = load_data(DATA_FILE)

if not data.empty:
    st.title("🏃‍♂️ Samsung Health Step Analysis")
    st.markdown("An overview of your daily step data.")

    available_years = sorted(data.index.year.unique(), reverse=True)
    all_possible_years = sorted(
        list(set(available_years + [y for y in range(2020, 2026)])), reverse=True)

    # --- Year selection moved from sidebar to main page ---
    st.header("Filters")
    selected_year = st.selectbox(
        "Select a Year for 'At a Glance' Stats:",
        options=all_possible_years
    )

    # --- Section 1: Year at a Glance ---
    st.header(f"📅 Year at a Glance: {selected_year}")

    df_year = data[data.index.year == selected_year]

    if df_year.empty:
        st.warning(f"No data found for the year {selected_year}.")
    else:
        total_steps = int(df_year['step_count'].sum())
        days_in_year = 366 if calendar.isleap(selected_year) else 365
        total_days_with_data = len(df_year)
        max_steps_row = df_year.loc[df_year['step_count'].idxmax()]
        max_steps_val = int(max_steps_row['step_count'])
        max_steps_date = max_steps_row.name.strftime('%B %d, %Y')
        min_df = df_year[df_year['step_count'] > 0]
        if not min_df.empty:
            min_steps_row = min_df.loc[min_df['step_count'].idxmin()]
            min_steps_val = int(min_steps_row['step_count'])
            min_steps_date = min_steps_row.name.strftime('%B %d, %Y')
        else:
            min_steps_val = 0
            min_steps_date = "N/A"

        # Milestone calculations for specific ranges
        days_10k_to_20k = len(
            df_year[(df_year['step_count'] >= 10000) & (df_year['step_count'] < 20000)])
        days_20k_to_30k = len(
            df_year[(df_year['step_count'] >= 20000) & (df_year['step_count'] < 30000)])
        days_over_30k = len(df_year[df_year['step_count'] >= 30000])
        days_under_1k = len(df_year[df_year['step_count'] < 1000])

        # --- NEW: Longest under 1k streak calculation ---
        is_under_1k = df_year['step_count'] < 1000
        streaks = is_under_1k.ne(is_under_1k.shift()).cumsum()
        streak_lengths = streaks[is_under_1k].value_counts()
        longest_under_1k_streak = streak_lengths.max() if not streak_lengths.empty else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Steps", value=f"{total_steps:,}")
        with col2:
            st.metric(label="Active Days",
                      value=f"{total_days_with_data} / {days_in_year}")
        with col3:
            st.metric(label="Average Daily Steps",
                      value=f"{int(df_year['step_count'].mean()):,}")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            # --- UPDATED: Title changed from "Bests" ---
            st.subheader("🏆 Records & Streaks")
            st.info(
                f"**Max Steps:** {max_steps_val:,} steps on {max_steps_date}")
            st.warning(
                f"**Min Steps:** {min_steps_val:,} steps on {min_steps_date}")
            # --- NEW: Displaying the streak stat ---
            st.error(
                f"**Longest Under 1k Streak:** {longest_under_1k_streak} days")
        with col2:
            st.subheader("🎯 Milestones")
            # --- UPDATED: Labels corrected to show ranges ---
            st.error(f"**Under 1k steps:** {days_under_1k} days")
            st.success(f"**10k+ steps:** {days_10k_to_20k} days")
            st.success(f"**20k+ steps:** {days_20k_to_30k} days")
            st.success(f"**30k+ steps:** {days_over_30k} days")

    # --- Section 2: Your Custom Plotly Graph (Now Dynamic) ---
    st.markdown("---")
    st.header("📊 Monthly Step Comparison by Year")

    # Let user select which years to show on the graph
    years_to_compare = st.multiselect(
        "Select years to compare on the graph:",
        options=available_years,
        # Default to last 3 years
        default=available_years[-3:] if len(
            available_years) >= 3 else available_years
    )

    if not years_to_compare:
        st.warning("Please select at least one year to display the graph.")
    else:
        fig = go.Figure()
        annotations_text = []
        months_of_year = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                          'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        for year in sorted(years_to_compare):
            # Filter data for the current year in the loop
            df_loop_year = data[data.index.year == year]

            # Group by month and sum the steps, then reindex to ensure all 12 months are present
            monthly_totals = df_loop_year.groupby(df_loop_year.index.month)[
                'step_count'].sum()
            monthly_totals = monthly_totals.reindex(
                range(1, 13), fill_value=None)  # Use None for missing months

            # Add a line for the year's data
            fig.add_trace(go.Scatter(
                x=months_of_year,
                y=monthly_totals,
                mode='lines+markers',
                name=str(year),
                # This will draw lines across months with no data (None)
                connectgaps=True
            ))

            # Prepare annotation text
            total_steps_year = int(monthly_totals.sum())
            days_in_year = 366 if calendar.isleap(year) else 365
            avg_day = round(total_steps_year / days_in_year,
                            1) if days_in_year > 0 else 0

            annotations_text.append(
                f"**{year}** Total: `{total_steps_year:,}` steps  &nbsp;·&nbsp;  Avg Daily: `{avg_day:,}` steps"
            )

        # --- FIX: Calculate dynamic y position for the annotation ---
        num_years = len(years_to_compare)
        # Start at a base y position and push it down for each line of text
        y_position = -0.1 - (num_years * 0.03)

        # Display annotations using st.markdown for better theme integration
        st.markdown("#### Yearly Summary")
        for line in annotations_text:
            st.markdown(f"{line}")

        fig.update_layout(
            title='Total Monthly Steps by Year',
            yaxis_title='Total Steps per Month',
            template='plotly_white',  # Using a lighter theme for better readability
            # Increased bottom margin for annotations
            margin=dict(t=50, b=200),
            legend_title_text='Year'
        )

        # Use st.plotly_chart to embed the figure in the Streamlit app
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Awaiting data file...")
