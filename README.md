# Zenith - Streaming Fraud Detection System

A proof-of-concept application that demonstrates real-time fraud detection using Kafka/Faust, Neo4j, and FastAPI.

## Features

- Process events in real-time
- Store and analyze data in a graph database (Neo4j)
- Expose API endpoints for handling events & analytics

## Installation

1. Clone the repository:
```sh
git clone https://github.com/ntwolff/zenith-fraud-detection.git
cd fraud-detection
```

2. Start the services using Docker Compose:
```sh
# docker-compose up --scale fake-data-producer=3
docker-compose up -d
```

To rebuild the Docker images:
```sh
docker-compose build
```

To see the Docker logs:
```sh
docker-compose logs -f
```

## Usage

- Send customer registration events to the Kafka topic `customer_registration`.
- Send login events to the Kafka topic `login`.
- Access the API endpoints (`http://localhost:8000/docs` locally):
- POST `/events/customer-event`: Handle a customer event (login, registration).
- POST `/fraud/shared-ip`: Find shared ip addresses from the graph in near real-time.
- POST `/fraud/risk-scores`: Graph pagerank algorithm
- Test via `pytest tests/`

## Next Steps

**More Fraud Signals**
- Enhance the CustomerEventGraphProcessor to derive more features from the event data, e.g.
    - Velocity: transaction amount over time, number of failed logins
    - Anomaly: deviation in amount, location, time from customer history
    - Linkage: to known fraudsters, previously flagged IPs/devices

- Add more Faust processors to detect additional fraud patterns, e.g.
    - Transaction laundering: many small transactions to avoid detection
    - Sleeper fraud: long time between account creation and first fraud
    - Mule account: money in and out immediately to other account

- Explore unsupervised ML (e.g. clustering, one-class SVM) to detect outliers

**Fraud Prevention & Workflows**
- Add ability to flag customers as high risk via the API and block in real-time
- Integrate downstream alerting/case management system for analysts to review
- Add API for analysts to give feedback on false positives/negatives to tune models

**Entity Resolution & Network**
- Enhance graph model and queries to link customers who share PII, e.g. Address, phone, email, SSN, IP, device
- Graph feature engineering: centrality, PageRank, community detection, motifs
- Create dashboard to visualize fraud networks in the graph

**Expanded Testing**
- Add integration tests with Kafka, Neo4j and the API running
- Chaos testing: simulate failures in Kafka, Neo4j, API
- Load testing: simulate high throughput of events, measure latency and resource usage
- Adversarial testing: simulate sophisticated fraud scenarios

**Deployment & Monitoring**
- Deploy to production environment (e.g. EKS), monitor performance and cost
- Set up CI/CD pipeline to automatically build, test and deploy new versions
- Define runbooks for common troubleshooting and maintenance tasks
- Monitor Kafka lag, Neo4j performance, API latency and error rates
- Set up alerts for anomalies and potential fraud

**Batch Processing**
- Set up batch pipeline (e.g. Spark) to process historical event data
- Reconcile stream and batch processing results
- Enhance feature engineering and model training with full historical data

**Model Evaluation & Tuning**
- Implement shadow mode to compare new models against production
- Define key metrics (e.g. precision, recall, F1, AUC) and monitor over time
- A/B test new models and fraud rules
- Set up regular retraining and evaluation cadence

**Regulation & Governance**
- Access control to the customer data, especially PII
- Data lineage to track data provenance and changes
- Audit logging of who accessed/changed what data when
- Data retention policy to comply with GDPR etc.
- Obtain legal/compliance review and sign off on models