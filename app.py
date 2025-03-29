import streamlit as st
from databases.mongo_connection import connect_mongodb
from queries.mongo_queries import (
    year_with_most_movies, movies_after_1999, avg_votes_2007, films_per_year, avg_runtime_by_decade, distinct_genres, highest_revenue_film,
    directors_with_more_than_5_films, top_genre_by_avg_revenue, top_3_rated_by_decade, high_score_high_revenue, longest_film_by_genre,
    correlation_runtime_revenue
)
from queries.neo4j_queries import (
    top_actor_by_films,
    actors_with_anne_hathaway,
    top_actor_by_revenue,
    avg_votes,
    top_genre,
    films_with_my_coworkers,
    top_director_by_distinct_actors,
    most_connected_film,
    top_5_actors_by_directors,
    recommend_by_genres,
    create_director_influence_relations,
    shortest_path_between_actors,
    detect_actor_communities
)
from utils.visualization import (
    plot_histogram_films_per_year, plot_avg_runtime_by_decade
)
from databases.neo4j_connection import connect_neo4j

st.set_page_config(page_title="Projet NoSQL", layout="wide")
st.title("📊 Projet NoSQL - MongoDB & Neo4j")

menu = st.sidebar.selectbox("📂 Choisir une base de données :", ["Accueil", "MongoDB", "Neo4j"])

if menu == "Accueil":
    st.subheader("Bienvenue 👋")
    st.markdown("- Explore MongoDB (documents)")
    st.markdown("- Explore Neo4j (graphes)")

elif menu == "MongoDB":
    st.header("📁 Requêtes MongoDB")
    try:
        collection = connect_mongodb()
        st.success("✅ Connexion MongoDB établie.")

        st.subheader("1️⃣ Année avec le plus grand nombre de films")
        result = year_with_most_movies(collection)
        if result:
            st.write(f"🎬 Année : **{result[0]['_id']}** avec **{result[0]['count']}** films")

        st.subheader("2️⃣ Nombre de films après 1999")
        count = movies_after_1999(collection)
        st.write(f"📈 Nombre de films : **{count}**")

        st.subheader("3️⃣ Moyenne des votes pour les films de 2007")
        avg_votes = avg_votes_2007(collection)
        st.write(f"⭐ Moyenne des votes : **{avg_votes:.2f}**" if avg_votes else "Pas de données")

        st.subheader("4️⃣ Histogramme du nombre de films par année")
        histogram_data = films_per_year(collection)
        fig1 = plot_histogram_films_per_year(histogram_data)
        st.pyplot(fig1)

        st.subheader("5️⃣ Genres disponibles")
        genres = distinct_genres(collection)
        st.write(genres)

        st.subheader("6️⃣ Film ayant généré le plus de revenus")
        top_film = highest_revenue_film(collection)
        if top_film:
            st.write(f"🎬 **{top_film['title']}** - 💵 {top_film['Revenue (Millions)']} millions")

        st.subheader("7️⃣ Réalisateurs avec plus de 5 films")
        directors = directors_with_more_than_5_films(collection)
        for d in directors:
            st.write(f"- 🎬 {d['_id']} ({d['count']} films)")

        st.subheader("8️⃣ Genre avec le revenu moyen le plus élevé")
        top_genres = top_genre_by_avg_revenue(collection)
        top = top_genres[0]
        st.write(f"🏆 Genre : **{top['genre']}** - Moyenne : **{top['avg']:.2f} M$**")
        st.bar_chart({g["genre"]: g["avg"] for g in top_genres[:10]})

        st.subheader("9️⃣ Top 3 films les mieux notés par décennie")
        top_per_decade = top_3_rated_by_decade(collection)
        for decade, films in top_per_decade.items():
            st.markdown(f"**🎞️ Décennie {decade}**")
            for film in films:
                st.write(f"- {film['title']} (Rating: {film['rating']})")

        st.subheader("🔟 Film le plus long par genre")
        longest_by_genre = longest_film_by_genre(collection)
        for genre, film in longest_by_genre.items():
            st.write(f"- **{genre}** : {film['title']} ({film['Runtime (Minutes)']} min)")

        st.subheader("1️⃣1️⃣ Films bien notés ET rentables")
        filtered = high_score_high_revenue(collection)
        for film in filtered:
            st.write(f"🎬 {film['title']} - 🎯 Metascore: {film['Metascore']} - 💰 {film['Revenue (Millions)']} M$")

        st.subheader("1️⃣2️⃣ Corrélation entre durée et revenu")
        corr = correlation_runtime_revenue(collection)
        if corr is not None:
            st.write(f"📊 Coefficient de corrélation : **{corr:.2f}**")
        else:
            st.warning("Pas assez de données pour calculer la corrélation.")

        st.subheader("1️⃣3️⃣ Évolution de la durée moyenne des films par décennie")
        avg_runtime_data = avg_runtime_by_decade(collection)
        fig2 = plot_avg_runtime_by_decade(avg_runtime_data)
        st.pyplot(fig2)
    except Exception as e:
        st.error(f"❌ Erreur de connexion à MongoDB : {e}")

elif menu == "Neo4j":
    st.header("🔗 Connexion à Neo4j")
    try:
        driver = connect_neo4j()
        with driver.session() as session:
            result = session.run("RETURN '✅ Connexion réussie à Neo4j !' AS msg")
            st.success(result.single()["msg"])

        st.subheader("🔍 14️⃣ Acteur ayant joué dans le plus de films")
        top_actor = top_actor_by_films(driver)
        if top_actor:
            st.write(f"🎭 **{top_actor['acteur']}** a joué dans **{top_actor['nb_films']}** films")

        st.subheader("🔍 15️⃣ Acteurs ayant joué avec Anne Hathaway")
        actors = actors_with_anne_hathaway(driver)
        st.write(actors)

        st.subheader("🔍 16️⃣ Acteur ayant généré le plus de revenus")
        top_revenue = top_actor_by_revenue(driver)
        if top_revenue:
            st.write(f"💰 **{top_revenue['acteur']}** avec **{top_revenue['total_revenue']:.2f} M$**")

        st.subheader("🔍 17️⃣ Moyenne des votes des films")
        avg = avg_votes(driver)
        st.write(f"⭐ Moyenne des votes : **{avg:.2f}**")

        st.subheader("🔍 18️⃣ Genre le plus représenté")
        genre = top_genre(driver)
        if genre:
            st.write(f"🎬 Genre : **{genre['genre']}** avec **{genre['nb_films']}** films")

        st.subheader("🔍 19️⃣ Films avec les acteurs qui ont joué avec toi")
        nom_utilisateur = st.text_input("Ton nom d'acteur enregistré dans la base :", value="Ton Nom")
        if nom_utilisateur:
            films = films_with_my_coworkers(driver, nom_utilisateur)
            st.write(films)

        st.subheader("🔍 20️⃣ Réalisateur ayant travaillé avec le plus d’acteurs différents")
        top_dir = top_director_by_distinct_actors(driver)
        if top_dir:
            st.write(f"🎬 **{top_dir['realisateur']}** avec **{top_dir['nb_acteurs']}** acteurs différents")

        st.subheader("🔍 21️⃣ Film le plus connecté")
        connected = most_connected_film(driver)
        if connected:
            st.write(
                f"🔗 **{connected['film']}** a des acteurs en commun avec **{connected['connexions']}** autres films")

        st.subheader("🔍 22️⃣ Acteurs ayant travaillé avec le plus de réalisateurs")
        top5 = top_5_actors_by_directors(driver)
        for record in top5:
            st.write(f"- 🎭 {record['acteur']} (avec {record['nb_realisateurs']} réalisateurs)")

        st.subheader("🔍 23️⃣ Recommandation de films à un acteur (par genre)")
        target_actor = st.text_input("Nom de l'acteur :", value="Tom Hanks")
        if target_actor:
            recos = recommend_by_genres(driver, target_actor)
            if recos:
                st.write("🎥 Suggestions :")
                for r in recos:
                    st.write(f"- {r}")
            else:
                st.warning("Aucune recommandation trouvée.")

        st.subheader("🔍 24️⃣ Créer les relations d'influence entre réalisateurs")
        if st.button("Créer les relations INFLUENCE_PAR"):
            create_director_influence_relations(driver)
            st.success("Relations d'influence créées ✅")

        st.subheader("🔍 25️⃣ Chemin le plus court entre deux acteurs")
        col1, col2 = st.columns(2)
        with col1:
            actor1 = st.text_input("Acteur 1", value="Tom Hanks")
        with col2:
            actor2 = st.text_input("Acteur 2", value="Scarlett Johansson")

        if actor1 and actor2:
            path = shortest_path_between_actors(driver, actor1, actor2)
            if path:
                st.success("✅ Chemin trouvé :")
                for step in path:
                    st.markdown(f"- {step}")
            else:
                st.warning("Aucun chemin trouvé entre ces deux acteurs.")

        st.subheader("🔍 26️⃣ Communautés d’acteurs (Louvain)")
        if st.button("Détecter les communautés (GDS)"):
            try:
                results = detect_actor_communities(driver)
                for r in results[:10]:  # affiche les 10 premiers
                    st.write(f"{r['acteur']} → Communauté {r['communityId']}")
            except Exception as e:
                st.error("⚠️ Neo4j Aura ne supporte peut-être pas GDS dans la version gratuite.")
    except Exception as e:
        st.error(f"❌ Erreur de connexion à Neo4j : {e}")