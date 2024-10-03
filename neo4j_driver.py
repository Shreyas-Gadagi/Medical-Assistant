from langchain.graphs import Neo4jGraph
import streamlit as st

host = st.secrets["NEO4J_URI"]
user = st.secrets["NEO4J_USER"]
password = st.secrets["NEO4J_PASSWORD"]
db = st.secrets["NEO4J_DB"]

neo4j_graph = Neo4jGraph(url=host, username=user, password=password)

# gds.set_database("neo4j")

def run_query(query, params=None):
    return neo4j_graph.query(query, params=params)
