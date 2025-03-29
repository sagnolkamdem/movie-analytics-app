from dotenv import load_dotenv
import os

load_dotenv()  # charge les variables depuis .env

MONGODB_URI = os.getenv("MONGODB_URI")

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")