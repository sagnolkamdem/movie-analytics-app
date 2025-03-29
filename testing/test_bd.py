from databases.mongo_connection import connect_mongodb
from databases.neo4j_connection import connect_neo4j

# MongoDB Test
collection = connect_mongodb()
print("Nombre de documents dans MongoDB:", collection.count_documents({}))

# Neo4j Test
# driver = connect_neo4j()
# with driver.session() as session:
#     result = session.run("RETURN 'Connexion réussie à Neo4j' AS message")
#     print(result.single()["message"])
