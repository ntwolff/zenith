import os
from neo4j import GraphDatabase
from shared.utilities import FuzzyMatching

# GRAPH DB INTERACTIONS

## ---------------
## Set-up
## ---------------

# driver = GraphDatabase.driver(
#     uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"), 
#     auth=(os.getenv("NEO4J_USER", "neo4j"), 
#           os.getenv("NEO4J_PASSWORD", "password")))

driver = GraphDatabase.driver(
    uri="bolt://localhost:7687", 
    auth=("neo4j", 
          "pinnacle"))

fuzzy = FuzzyMatching()

## ---------------
## Graph Operations
## ---------------

### Customer Graph CRUD

def create_customer_graph(tx, event):
    # Create nodes for potential fraud vectors
    tx.run("MERGE (a:Address {hash: $address_hash}) SET a += $address_props", 
           address_hash=fuzzy.hash_address(event.address), address_props=dict(event.address))
    tx.run("MERGE (d:Device {device_id: $device_id}) SET d += $device_props", 
           device_id=event.device.device_id, device_props=dict(event.device))
    tx.run("MERGE (i:IpAddress {ip: $ip})", ip=event.ip_address.ip)
    
    # Create nodes for hashed SSN, email, and stripped/standardized phone number
    tx.run("MERGE (s:SSN {hash: $ssn_hash})", ssn_hash=fuzzy.hash_ssn(event.ssn))
    tx.run("MERGE (e:Email {address: $email})", email=event.email)
    tx.run("MERGE (p:PhoneNumber {number: $phone_number})", phone_number=fuzzy.standardize_phone_number(event.phone_number))
    
    # Create customer node and link to fraud vector nodes
    tx.run("""
        MERGE (c:Customer {customer_id: $customer_id}) 
        SET c += $customer_props
        WITH c
        MATCH (a:Address {hash: $address_hash})
        MATCH (d:Device {device_id: $device_id})
        MATCH (i:IpAddress {ip: $ip})
        MATCH (s:SSN {hash: $ssn_hash})
        MATCH (e:Email {address: $email})
        MATCH (p:PhoneNumber {number: $phone_number})
        MERGE (c)-[:HAS_ADDRESS]->(a)
        MERGE (c)-[:USES_DEVICE]->(d)
        MERGE (c)-[:HAS_IP]->(i)
        MERGE (c)-[:HAS_SSN]->(s)
        MERGE (c)-[:HAS_EMAIL]->(e)
        MERGE (c)-[:HAS_PHONE_NUMBER]->(p)
    """, customer_id=event.customer_id, customer_props=dict(
        name=event.name,
        date_of_birth=event.date_of_birth,
        timestamp=event.timestamp
    ), address_hash=fuzzy.hash_address(event.address), device_id=event.device.device_id, ip=event.ip_address.ip,
    ssn_hash=fuzzy.hash_ssn(event.ssn), email=event.email, phone_number=fuzzy.standardize_phone_number(event.phone_number))


def get_customer_data(tx, customer_id):
    result = tx.run("""
        MATCH (c:Customer {customer_id: $customer_id})
        OPTIONAL MATCH (c)-[:HAS_ADDRESS]->(a:Address)
        OPTIONAL MATCH (c)-[:USES_DEVICE]->(d:Device)
        OPTIONAL MATCH (c)-[:HAS_IP]->(i:IpAddress)
        OPTIONAL MATCH (c)-[:HAS_SSN]->(s:SSN)
        OPTIONAL MATCH (c)-[:HAS_EMAIL]->(e:Email)
        OPTIONAL MATCH (c)-[:HAS_PHONE_NUMBER]->(p:PhoneNumber)
        RETURN c, a, d, i, s, e, p
    """, customer_id=customer_id)
    
    data = {}
    for record in result:
        data['customer'] = dict(record['c'])
        data['address'] = dict(record['a']) if record['a'] else None
        data['device'] = dict(record['d']) if record['d'] else None
        data['ip_address'] = record['i']['ip'] if record['i'] else None
        data['ssn'] = record['s']['hash'] if record['s'] else None
        data['email'] = record['e']['address'] if record['e'] else None
        data['phone_number'] = record['p']['number'] if record['p'] else None
    
    return data


## ---------------
## Graph Analytics
## ---------------

def detect_communities(tx):
    result = tx.run("""
        CALL gds.louvain.stream('customerGraph', {})
        YIELD nodeId, communityId
        RETURN gds.util.asNode(nodeId).customer_id AS customer_id, communityId
    """)
    communities = {}
    for record in result:
        communities[record['customer_id']] = record['communityId']
    return communities

def calculate_centrality(tx, customer_id):
    result = tx.run("""
        MATCH (c:Customer {customer_id: $customer_id})
        CALL gds.pageRank.stream('customerGraph', {maxIterations: 20})
        YIELD nodeId, score
        RETURN gds.util.asNode(nodeId).customer_id AS customer_id, score
        ORDER BY score DESC
        LIMIT 10
    """, customer_id=customer_id)
    centrality = []
    for record in result:
        centrality.append({"customer_id": record['customer_id'], "score": record['score']})
    return centrality