import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Phone Verifications Dashboard", layout="wide")

st.title("📱 Phone Verifications Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your verification CSV file", type=["csv"])

if uploaded_file:
    # Load CSV
    df = pd.read_csv(uploaded_file)

    # Clean and parse date_created
    df['date_created'] = pd.to_datetime(df['date_created'].str.replace(' UTC', ''), errors='coerce').dt.date

    # Clean status column
    df['status'] = df['status'].str.strip().str.lower()

    # -----------------------------
    # 🧰 FILTERS
    # -----------------------------
    st.sidebar.header("Filters")

    # 📅 Date range filter
    st.sidebar.subheader("📅 Date Range")
    min_date = df['date_created'].min()
    max_date = df['date_created'].max()

    date_range = st.sidebar.date_input(
        "Select range:",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        st.error("❌ Please select a valid date range (start and end).")
        st.stop()

    # Filter DataFrame by date
    filtered_df = df[(df['date_created'] >= start_date) & (df['date_created'] <= end_date)]

    # 🎯 Status filter
    st.sidebar.subheader("🎯 Verification Status")
    show_approved = st.sidebar.checkbox("Approved", value=True)
    show_expired = st.sidebar.checkbox("Expired", value=True)

    # -----------------------------
    # 📊 Country-by-Date Table with Status Filters
    # -----------------------------
    st.subheader("📊 Data Table: Verifications per Country and Date")
    st.write("This table shows the total number of verifications by country for the selected date range and status filters.")

    if show_approved and show_expired:
        st.info("✅🕓 Showing all statuses: approved and expired verifications.")
    elif show_approved:
        st.success("✅ Showing only approved verifications.")
    elif show_expired:
        st.warning("🕓 Showing only expired verifications.")
    else:
        st.error("🚫 No statuses selected. Please select at least one status to view the data.")
        st.stop()

    # Build status filter list
    selected_statuses = []
    if show_approved:
        selected_statuses.append("approved")
    if show_expired:
        selected_statuses.append("expired")

    # Filter by selected statuses
    status_filtered_df = filtered_df[filtered_df['status'].isin(selected_statuses)]

    # Pivot table like the first image
    pivot_table = pd.pivot_table(
        status_filtered_df,
        index='date_created',
        columns='country',
        values='sid',
        aggfunc='count',
        fill_value=0
    )

    # Add totals
    pivot_table['Total'] = pivot_table.sum(axis=1)
    pivot_table.loc['Total'] = pivot_table.sum()

    # Styled table
    st.dataframe(pivot_table.style.format(na_rep='-'), use_container_width=True)

    # -----------------------------
    # 📈 Approved vs Expired Chart
    # -----------------------------
    st.subheader("📈 Phone Verifications Over Time")

    summary = filtered_df[filtered_df['status'].isin(['approved', 'expired'])] \
        .groupby(['date_created', 'status']) \
        .size() \
        .unstack(fill_value=0)

    for col in ['approved', 'expired']:
        if col not in summary.columns:
            summary[col] = 0

    fig, ax = plt.subplots(figsize=(12, 6))

    approved_bars = ax.bar(summary.index, summary['approved'], label='Approved', color='skyblue')
    expired_bars = ax.bar(summary.index, summary['expired'], bottom=summary['approved'], label='Expired', color='sandybrown')

    # Add data labels in the middle of each segment
    for i, date in enumerate(summary.index):
        approved = summary.loc[date, 'approved']
        expired = summary.loc[date, 'expired']
        bar = approved_bars[i]
        x = bar.get_x() + bar.get_width() / 2

        if approved > 0:
            ax.text(x, approved / 2, str(approved), ha='center', va='center', fontsize=9, color='black')

        if expired > 0:
            ax.text(x, approved + expired / 2, str(expired), ha='center', va='center', fontsize=9, color='black')

    # Format chart
    ax.set_ylabel("Number of Verifications")
    ax.set_title("Daily Approved vs Expired Verifications")
    ax.legend()

    # 🗓 Format x-axis dates like '25-Mar'
    ax.set_xticks(summary.index)
    ax.set_xticklabels([d.strftime('%d-%b') for d in summary.index], rotation=45)

    st.pyplot(fig)