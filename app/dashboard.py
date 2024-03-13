import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import pandas as pd
import requests

# DASHBOARD
# streamlit run app/dashboard.py

#@TODO Expand dashboard, investigate graphistry / iframe approach (https://github.com/graphistry/graph-app-kit)

# Set page configuration
st.set_page_config(page_title='Fraud Detection Dashboard', layout='wide')

# Graph Visualization
st.header('Fraud Network Visualization')

# Configure the Agraph visualization
config = Config(
    node={'labelProperty': 'label', 'renderLabel': True, 'size': 25},
    link={'labelProperty': 'label', 'renderLabel': True},
    width=1500,
    height=1000,
    directed=True,
    collapsible=True,
    nodeHighlightBehavior=True,
    highlightColor='#F7A7A6',
)

graph_expander = st.expander(label='Graph visualization', expanded=True)
with graph_expander:
    with st.spinner('Loading graph data...'):
        graph_data = requests.get('http://localhost:8000/api/events/graph').json()

        # Create nodes and edges for the Agraph visualization
        nodes = []
        edges = []

        for node in graph_data['elements']['nodes']:
            nodes.append(Node(id=node['data']['id'], label=node['data']['label'], properties=node['data']['properties']))

        for edge in graph_data['elements']['edges']:
            edges.append(Edge(source=edge['data']['source'], target=edge['data']['target'], label=edge['data']['type'], **edge['data']['properties']))

        # Render the Agraph visualization
        agraph(nodes=nodes, edges=edges, config=config)

tables_expander = st.expander(label='Data Tables', expanded=True)
with tables_expander:
    with st.spinner('Loading table data...'):
        centrality_scores = requests.get('http://localhost:8000/api/fraud/centrality').json()['centrality_scores']
        communities = requests.get('http://localhost:8000/api/fraud/communities').json()['communities']

        # Create a DataFrame for centrality scores
        centrality_df = pd.DataFrame(centrality_scores)

        # Create a DataFrame for communities
        communities_df = pd.DataFrame(communities)

        col1, col2 = st.columns(2)

        with col1:
            st.header('Centrality Scores')
            st.dataframe(centrality_df, width=600)

        with col2:
            st.header('Fraud Communities')
            st.dataframe(communities_df, width=600)