# 🎮 Movie Analytics App – MongoDB & Neo4j with Streamlit

Une application de visualisation et d’analyse de données de films, basée sur MongoDB (orienté documents) et Neo4j (orienté graphes), avec une interface développée en Streamlit.

## 📦 Technologies utilisées

- Python 3.10+
- Streamlit
- MongoDB (MongoDB Atlas ou local)
- Neo4j (Neo4j Aura ou local)
- Matplotlib / Seaborn (visualisation)
- Neovis.js (visualisation de graphe - local)
- dotenv (gestion des variables d’environnement)

---

## ✨ Fonctionnalités

### 🟢 MongoDB
- Requêtes d’agrégation : années, votes, revenus, genres, etc.
- Visualisations : histogrammes, scatter plots, moyennes
- Corrélation entre durée et revenus

### 🔵 Neo4j
- Création automatique de nœuds et relations
- Requêtes Cypher avancées (recommandation, chemin, communautés)
- Visualisation du graphe (local)

---

## 🚀 Installation & Lancement

### 1. Cloner le dépôt

```bash
git clone https://github.com/sagnolkamdem/movie-analytics-app.git
cd movie-analytics-app
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer le fichier `.env`

Créer un fichier `.env` à la racine contenant :

```env
MONGO_URI=...
MONGO_DB=....
MONGO_COLLECTION=...

NEO4J_URI=...
NEO4J_USER=...
NEO4J_PASSWORD=...
```

> 🔐 Remplace les valeurs par tes vraies informations MongoDB et Neo4j.

### 5. Lancer l'application

```bash
streamlit run app.py
```

---

## 📁 Arborescence du projet

```
├── app.py                    # Application principale Streamlit
├── config/
│   └── config.py             # Chargement des variables d'environnement
├── database/
│   ├── mongo_connection.py
│   └── neo4j_connection.py
├── queries/
│   ├── mongo_queries.py
│   ├── mongo_to_neo4j.py
│   └── neo4j_queries.py
├── utils/
│   ├── export_report.py
│   └── visualizations.py
├── requirements.txt
└── .env
```

---

## ❓ Notes importantes

- Neo4j Aura **ne permet pas** la visualisation avec Neovis.js (préférer Neo4j Desktop en local pour cela).
- Pour utiliser Neovis.js, voir la fonction `show_neo4j_graph()` dans `utils/visualizations.py`.
- Le fichier `movies.json` doit être importé dans MongoDB au préalable.

---

## 🤝 Contribuer

1. Fork le projet
2. Crée une branche (`git checkout -b feature/ma-feature`)
3. Commit tes changements (`git commit -m 'Ajout de ma fonctionnalité'`)
4. Push (`git push origin feature/ma-feature`)
5. Ouvre une Pull Request

---

## 🧠 Auteurs

- Projet réalisé dans le cadre du cours **NoSQL** à l’**ESIEA**
- Développé avec ❤️ par :
  - Hind KHAYATI
  - Amira FATHALLA
  - Sagnol Boutal KAMDEM DJOKO

