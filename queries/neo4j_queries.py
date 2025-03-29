def top_actor_by_films(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Actor)-[:A_JOUE]->(f:films)
            RETURN a.name AS acteur, COUNT(f) AS nb_films
            ORDER BY nb_films DESC
            LIMIT 1
        """)
        return result.single()

def actors_with_anne_hathaway(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Actor)-[:A_JOUE]->(f:films)<-[:A_JOUE]-(anne:Actor {name: "Anne Hathaway"})
            WHERE a.name <> "Anne Hathaway"
            RETURN DISTINCT a.name AS acteur
        """)
        return [record["acteur"] for record in result]

def top_actor_by_revenue(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Actor)-[:A_JOUE]->(f:films)
            WHERE f.`Revenue (Millions)` IS NOT NULL
            WITH a.name AS acteur, SUM(toFloat(f.`Revenue (Millions)`)) AS total_revenue
            RETURN acteur, total_revenue
            ORDER BY total_revenue DESC
            LIMIT 1
        """)
        return result.single()

def avg_votes(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (f:films)
            WHERE f.Votes IS NOT NULL
            RETURN avg(toFloat(f.Votes)) AS moyenne_votes
        """)
        return result.single()["moyenne_votes"]

def top_genre(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (f:films)-[:A_GENRE]->(g:Genre)
            RETURN g.name AS genre, COUNT(f) AS nb_films
            ORDER BY nb_films DESC
            LIMIT 1
        """)
        return result.single()

def films_with_my_coworkers(driver, my_name="Ton Nom"):
    with driver.session() as session:
        result = session.run("""
            MATCH (me:Actor {name: $my_name})-[:A_JOUE]->(:films)<-[:A_JOUE]-(a:Actor)
            MATCH (a)-[:A_JOUE]->(f:films)
            RETURN DISTINCT f.title AS film
        """, my_name=my_name)
        return [record["film"] for record in result]

def top_director_by_distinct_actors(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (r:Realisateur)-[:A_REALISE]->(f:films)<-[:A_JOUE]-(a:Actor)
            RETURN r.name AS realisateur, COUNT(DISTINCT a) AS nb_acteurs
            ORDER BY nb_acteurs DESC
            LIMIT 1
        """)
        return result.single()

def most_connected_film(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (f1:films)<-[:A_JOUE]-(a:Actor)-[:A_JOUE]->(f2:films)
            WHERE f1 <> f2
            WITH f1, COUNT(DISTINCT f2) AS connexions
            RETURN f1.title AS film, connexions
            ORDER BY connexions DESC
            LIMIT 1
        """)
        return result.single()

def top_5_actors_by_directors(driver):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Actor)-[:A_JOUE]->(f:films)<-[:A_REALISE]-(r:Realisateur)
            RETURN a.name AS acteur, COUNT(DISTINCT r) AS nb_realisateurs
            ORDER BY nb_realisateurs DESC
            LIMIT 5
        """)
        return result.data()

def recommend_by_genres(driver, actor_name):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Actor {name: $actor_name})-[:A_JOUE]->(:films)-[:A_GENRE]->(g:Genre)
            WITH a, COLLECT(DISTINCT g.name) AS genres
            MATCH (f:films)-[:A_GENRE]->(g2:Genre)
            WHERE g2.name IN genres
            AND NOT (a)-[:A_JOUE]->(f)
            RETURN DISTINCT f.title AS titre
            LIMIT 5
        """, actor_name=actor_name)
        return [record["titre"] for record in result]

def create_director_influence_relations(driver):
    with driver.session() as session:
        session.run("""
            MATCH (r1:Realisateur)-[:A_REALISE]->(:films)-[:A_GENRE]->(g:Genre),
                  (r2:Realisateur)-[:A_REALISE]->(:films)-[:A_GENRE]->(g)
            WHERE r1 <> r2
            MERGE (r1)-[:INFLUENCE_PAR]->(r2)
        """)


def shortest_path_between_actors(driver, actor1, actor2):
    with driver.session() as session:
        result = session.run("""
            MATCH (a1:Actor {name: $a1}), (a2:Actor {name: $a2}),
            p = shortestPath((a1)-[:A_JOUE*]-(a2))
            RETURN nodes(p) AS nodes, relationships(p) AS rels
        """, a1=actor1, a2=actor2)

        if not result.peek():
            return None

        record = result.single()
        nodes = record["nodes"]
        rels = record["rels"]
        path_list = []

        for i in range(len(rels)):
            n1 = nodes[i]
            n2 = nodes[i + 1]
            r = rels[i]
            path_list.append(f"{n1['name'] if 'name' in n1 else n1.get('title')} "
                             f"--[{r.type}]--> "
                             f"{n2['name'] if 'name' in n2 else n2.get('title')}")
        return path_list

def detect_actor_communities(driver):
    with driver.session() as session:
        session.run("CALL gds.graph.project('actorGraph', 'Actor', 'A_JOUE')")
        result = session.run("""
            CALL gds.louvain.stream('actorGraph')
            YIELD nodeId, communityId
            RETURN gds.util.asNode(nodeId).name AS acteur, communityId
            ORDER BY communityId
        """)
        return result.data()