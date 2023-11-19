import streamlit as st
from datetime import datetime

# Streamlit page configuration
st.set_page_config(page_title="Time Range Data Viewer", layout="wide")

# Database path
DB_PATH = "/home/hackathon26/omar/hackatum23-coinflip/src/logs_test_log1.out.db"
db_connector = DBConnector(DB_PATH)
db_connector.connect()

# Streamlit app layout
st.title("Database Viewer")

# Styling
st.markdown("""
    <style>
    .big-font {
        font-size:16px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Date and time range selection
with st.form(key='date_time_form'):
    # Assuming you are using st.columns, make sure they are wide enough.
    col1, col2 = st.columns([1, 1])  # Adjust the ratio if necessary.

    with col1:
        start_date = st.date_input("Start Date", datetime.now())
        # Use a shorter label and a placeholder for the full format.
        start_time = st.text_input("Start Time", "00:00:00", placeholder="HH:MM:SS")

    with col2:
        end_date = st.date_input("End Date", datetime.now())
        end_time = st.text_input("End Time", "23:59:59", placeholder="HH:MM:SS")

    submit_button = st.form_submit_button(label='Load Data')

# Function to combine date and time input into a datetime string
def combine_datetime(date, time_str):
    try:
        return datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M:%S")
    except ValueError:
        st.error("Invalid time format. Please use HH:MM:SS.")
        return None

# Combining date and time inputs
if submit_button:
    start_datetime = combine_datetime(start_date, start_time)
    end_datetime = combine_datetime(end_date, end_time)

    # Loading data and error handling
    if start_datetime and end_datetime:
        if start_datetime >= end_datetime:
            st.error("End datetime must be after start datetime.")
        else:
            try:
                data = db_connector.get_data_in_time_range(start_datetime, end_datetime)
                if data:
                    st.markdown('## Query Results')
                    for row in data:
                        st.text(', '.join(str(v) for v in row))  # Display each row
                else:
                    st.info("No data found for the selected time range.")
            except ValueError as e:
                st.error(str(e))
