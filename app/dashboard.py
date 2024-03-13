import streamlit as st
from streamlit_cytoscapejs import st_cytoscapejs
import pandas as pd
import requests

st.set_page_config(page_title='Fraud Detection Dashboard', layout='wide')

# Graph Visualization
st.header('Fraud Network Visualization')

# Fetch graph data from the FastAPI backend
graph_data = requests.get('http://localhost:8000/api/events/graph').json()

print(graph_data)

# Create Cytoscape.js graph
cytoscape_graph = st_cytoscapejs(
    elements=graph_data['elements'],
    stylesheet=[
        {'selector': 'node', 'style': {'label': 'data(id)'}},
        {'selector': 'edge', 'style': {'label': 'data(type)'}}
    ]
)

# Fetch data from the FastAPI backend
centrality_scores = requests.get('http://localhost:8000/api/fraud/centrality').json()['centrality_scores']

communities = requests.get('http://localhost:8000/api/fraud/communities').json()['communities']

# Create a DataFrame for centrality scores
centrality_df = pd.DataFrame(centrality_scores)

# Create a DataFrame for communities
communities_df = pd.DataFrame(communities)

# Display centrality scores
st.header('Centrality Scores')
st.dataframe(centrality_df)

# Display communities
st.header('Fraud Communities')
st.dataframe(communities_df)