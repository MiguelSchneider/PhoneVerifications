# Phone Verifications Dashboard

This project is a Streamlit-based dashboard for analyzing phone verification data from a CSV file. It provides interactive filters, data visualizations, and insights into verification statuses over time.

## Features

- **File Upload**: Upload a CSV file containing phone verification data.
- **Filters**:
  - Date range filter to narrow down data by creation date.
  - Status filter to view "Approved" and/or "Expired" verifications.
- **Data Table**: Displays a pivot table of verifications per country and date.
- **Visualization**: A bar chart showing daily counts of "Approved" vs "Expired" verifications.

## Requirements

- Python 3.7 or higher
- Required Python libraries:
  - `streamlit`
  - `pandas`
  - `matplotlib`

## How to Run

1. Install the required dependencies:
   ```bash
   pip install streamlit pandas matplotlib
