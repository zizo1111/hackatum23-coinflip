import streamlit as st

st.set_page_config(page_title="Plotly", page_icon="👋", layout='wide')

st.header('Integration with plotly')

desc = """
Streamlit intgrates with plotly mostly seamlessly.

With plotly (and plotly.express) you can create interactiv and responsive plots easily.

"""

st.write(desc)

with st.echo():
    import plotly.express as px

    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

    st.plotly_chart(fig)

    fig = px.scatter_matrix(df, dimensions=["sepal_width", "sepal_length", "petal_width", "petal_length"], color="species")
    st.plotly_chart(fig)
