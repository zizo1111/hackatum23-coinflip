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

# get classes
class_list = df['Class'].tolist()
# Define colors for each category
colors = {'ssh_cls': 'blue', 'error_cls': 'red', 'warning_cls':'orange'}

# Styling for the first graph
layout = go.Layout(
    title='Overview: Occurance analysis of messages',
    title_x=0.5,
    xaxis=dict(title='Category'),
    yaxis=dict(title='Count'),
    barmode='group',
    plot_bgcolor='rgba(0,0,0,0)'
)

# # Plotly chart for errors and ssh counts
# fig = go.Figure(data=[
#     go.Bar(name='Errors', x=['Errors'], y=[error_count], marker_color=colors['errors']),
#     go.Bar(name='SSH', x=['SSH'], y=[ssh_count], marker_color=colors['ssh'])
# ], layout=layout)

# Plotly chart for errors and ssh counts
data_list = [go.Bar(name=cls, x=[cls], y=[df[df['Class'] == cls]['Occurences'].values[0]], marker_color=colors[cls]) for cls in class_list]
fig = go.Figure(data=data_list, layout=layout)

st.plotly_chart(fig, use_container_width=True)
# # Capturing events from the Plotly chart 
# selected_points = plotly_events(fig, key="plot1")

# # Check if a bar was clicked and update the session state
# if selected_points:
#     point = selected_points[0]
#     category = point['x']
#     print(st.session_state.db_connector.get_resource_hist(category))
#     st.session_state.selected_category = category

# # Display the second graph based on the selection
# if 'selected_category' in st.session_state and st.session_state.selected_category:
#     category = st.session_state.selected_category
#     filtered_data = df[df[category] == True]
#     count_by_device = filtered_data['device_id'].value_counts().reset_index()
#     count_by_device.columns = ['device_id', 'count']

#     # Styling for the second graph
#     layout2 = go.Layout(
#         title=f'{category.capitalize()} Count by Device ID',
#         title_x=0.5,
#         xaxis=dict(title='Device ID'),
#         yaxis=dict(title='Count'),
#         plot_bgcolor='rgba(0,0,0,0)'
#     )

#     fig2 = go.Figure(data=[
#         go.Bar(x=count_by_device['device_id'], y=count_by_device['count'], 
#                marker_color=colors[category])
#     ], layout=layout2)

#     st.plotly_chart(fig2, use_container_width=True)
