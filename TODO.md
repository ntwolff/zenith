# Zenith Next Steps

## Practical
-----------------------
- Refactor to "v2" model pattern (i.e. base model/record and factory).
- Integrate ip information api (ipinfo.io).
- Create mocks for other data services (Threatmetrix, Transunion, etc.). 
- Alerts and case management.
- Bulk data upload of events.
- Redesign API around investigations
- Investigate geospatial applications of the graph data.
- Graph data retention best practices investigation.
- Expand real-time signaling use cases.
- Kafka policies (e.g. PII obfuscation)

## Exploratory
-----------------------
- Key/value store database (e.g. RocksDB), vector database (e.g. Pinecone), document database (e.g. MongoDB).
- Synthetic data generation (e.g. Mostly.ai)
- Proving efficacy on out-of-the-box Kaggle dataset
- Neo4j alternatives (e.g. Memgraph (cypher), Aerospike (gremlin))
    - Aerospike clients: Paypal, ThreatMetrix
- XNetwork for graph algorithms
- Administrative user experience (ideally w/ embedded graph visualizations)
- Notebook environment (i.e. Jupyter Lab)
- ML model real-time inference - GraphDataScience library?  or other methodology?