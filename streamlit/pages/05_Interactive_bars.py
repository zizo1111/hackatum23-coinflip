import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from streamlit_plotly_events import plotly_events

# Setting the page layout to wide mode for better visual appeal
st.set_page_config(layout="wide")

query = None
if 'user_query' in st.session_state:
    query = st.session_state.user_query
df = st.session_state.db_connector.get_data_frame(query)

# Streamlit app layout
st.title("Device Analysis Dashboard")

# Customizing the sidebar
with st.sidebar:
    st.markdown("## Controls")
    st.markdown("Use the interactive charts to explore device data.")

# Count occurrences of errors and ssh
error_count = df['errors'].sum()
ssh_count = df['ssh'].sum()

# Define colors for each category
colors = {'errors': 'blue', 'ssh': 'red'}

# Styling for the first graph
layout = go.Layout(
    title='Overview: Counts of Errors and SSH',
    title_x=0.5,
    xaxis=dict(title='Category'),
    yaxis=dict(title='Count'),
    barmode='group',
    plot_bgcolor='rgba(0,0,0,0)'
)

# Plotly chart for errors and ssh counts
fig = go.Figure(data=[
    go.Bar(name='Errors', x=['Errors'], y=[error_count], marker_color=colors['errors']),
    go.Bar(name='SSH', x=['SSH'], y=[ssh_count], marker_color=colors['ssh'])
], layout=layout)

# Capturing events from the Plotly chart
selected_points = plotly_events(fig, key="plot1")

# Check if a bar was clicked and update the session state
if selected_points:
    point = selected_points[0]
    category = 'errors' if point['x'] == 'Errors' else 'ssh'
    st.session_state.selected_category = category

# Display the second graph based on the selection
if 'selected_category' in st.session_state and st.session_state.selected_category:
    category = st.session_state.selected_category
    filtered_data = df[df[category] == True]
    count_by_device = filtered_data['device_id'].value_counts().reset_index()
    count_by_device.columns = ['device_id', 'count']

    # Styling for the second graph
    layout2 = go.Layout(
        title=f'{category.capitalize()} Count by Device ID',
        title_x=0.5,
        xaxis=dict(title='Device ID'),
        yaxis=dict(title='Count'),
        plot_bgcolor='rgba(0,0,0,0)'
    )

    fig2 = go.Figure(data=[
        go.Bar(x=count_by_device['device_id'], y=count_by_device['count'], 
               marker_color=colors[category])
    ], layout=layout2)

    st.plotly_chart(fig2, use_container_width=True)
