from neo4j import GraphDatabase
from config.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

# Connexion à la BD Neo4j
def connect_neo4j():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    return driver