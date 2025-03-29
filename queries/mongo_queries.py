from pymongo.collection import Collection
from bson.son import SON

# 1. Année avec le plus grand nombre de films
def year_with_most_movies(collection: Collection):
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1)])},
        {"$limit": 1}
    ]
    return list(collection.aggregate(pipeline))

# 2. Nombre de films après 1999
def movies_after_1999(collection: Collection):
    return collection.count_documents({"year": {"$gt": 1999}})

# 3. Moyenne des votes pour les films sortis en 2007
def avg_votes_2007(collection: Collection):
    pipeline = [
        {"$match": {"year": 2007}},
        {"$group": {"_id": None, "averageVotes": {"$avg": "$Votes"}}}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0]["averageVotes"] if result else None

# 4. Histogramme : Nombre de films par année
def films_per_year(collection: Collection):
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    return list(collection.aggregate(pipeline))

# 5. Genres de films disponibles
def distinct_genres(collection: Collection):
    genres = collection.distinct("genre")
    flat_genres = set()
    for g in genres:
        if g:
            flat_genres.update([x.strip() for x in g.split(",")])
    return sorted(flat_genres)

# 6. Film ayant généré le plus de revenu
def highest_revenue_film(collection: Collection):
    return collection.find_one(
        {"Revenue (Millions)": {"$exists": True}},
        sort=[("Revenue (Millions)", -1)]
    )

# 7. Réalisateurs ayant fait plus de 5 films
def directors_with_more_than_5_films(collection: Collection):
    pipeline = [
        {"$group": {"_id": "$Director", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 5}}},
        {"$sort": {"count": -1}}
    ]
    return list(collection.aggregate(pipeline))

# 8. Genre rapportant en moyenne le plus de revenus
def top_genre_by_avg_revenue(collection: Collection):
    pipeline = [
        {"$project": {"genre": 1, "Revenue (Millions)": 1}},
        {"$match": {"Revenue (Millions)": {"$exists": True}}}
    ]

    docs = list(collection.aggregate(pipeline))
    genre_stats = {}

    for doc in docs:
        genre_field = doc.get("genre")
        revenue_raw = doc.get("Revenue (Millions)")

        try:
            revenue = float(revenue_raw)
        except (ValueError, TypeError):
            continue  # skip malformed revenue

        if genre_field:
            for g in genre_field.split(","):
                g = g.strip()
                if g not in genre_stats:
                    genre_stats[g] = []
                genre_stats[g].append(revenue)

    # 🧽 nettoyage ultime avant calcul
    avg_by_genre = []
    for genre, revenues in genre_stats.items():
        cleaned_revenues = []
        for r in revenues:
            try:
                cleaned_revenues.append(float(r))
            except (ValueError, TypeError):
                continue
        if cleaned_revenues:
            avg = sum(cleaned_revenues) / len(cleaned_revenues)
            avg_by_genre.append({"genre": genre, "avg": avg})

    return sorted(avg_by_genre, key=lambda x: x["avg"], reverse=True)

# 9. Top 3 films les mieux notés par décennie
def top_3_rated_by_decade(collection: Collection):
    pipeline = [
        {"$match": {"year": {"$exists": True}, "rating": {"$exists": True}}},
        {"$project": {
            "title": 1,
            "rating": 1,
            "year": 1,
            "decade": {"$multiply": [{"$floor": {"$divide": ["$year", 10]}}, 10]}
        }},
        {"$sort": {"decade": 1, "rating": -1}},
    ]
    results = list(collection.aggregate(pipeline))
    from collections import defaultdict
    top_by_decade = defaultdict(list)
    for film in results:
        decade = film["decade"]
        if len(top_by_decade[decade]) < 3:
            top_by_decade[decade].append(film)
    return dict(top_by_decade)

# 10. Film le plus long par genre
def longest_film_by_genre(collection: Collection):
    docs = collection.find({"Runtime (Minutes)": {"$exists": True}})
    genre_max = {}
    for doc in docs:
        if "genre" in doc and "Runtime (Minutes)" in doc:
            for g in doc["genre"].split(","):
                g = g.strip()
                current = genre_max.get(g)
                if not current or doc["Runtime (Minutes)"] > current["Runtime (Minutes)"]:
                    genre_max[g] = doc
    return genre_max

# 11. Vue MongoDB : films notés > 80 et revenus > 50 millions
def high_score_high_revenue(collection: Collection):
    pipeline = [
        {"$match": {
            "Metascore": {"$gt": 80},
            "Revenue (Millions)": {"$gt": 50}
        }},
        {"$project": {"title": 1, "Metascore": 1, "Revenue (Millions)": 1}}
    ]
    return list(collection.aggregate(pipeline))

# 12. Corrélation entre runtime et revenu
def correlation_runtime_revenue(collection: Collection):
    docs = collection.find({
        "Runtime (Minutes)": {"$exists": True},
        "Revenue (Millions)": {"$exists": True}
    }, {"Runtime (Minutes)": 1, "Revenue (Millions)": 1})

    runtimes = []
    revenues = []

    for d in docs:
        try:
            runtime = float(d["Runtime (Minutes)"])
            revenue = float(d["Revenue (Millions)"])
            runtimes.append(runtime)
            revenues.append(revenue)
        except (ValueError, TypeError):
            continue  # Ignore les valeurs invalides

    if len(runtimes) > 1:
        import numpy as np
        correlation = np.corrcoef(runtimes, revenues)[0][1]
        return correlation
    return None

# 13. Évolution de la durée moyenne des films par décennie
def avg_runtime_by_decade(collection: Collection):
    pipeline = [
        {"$project": {
            "decade": {"$multiply": [{"$floor": {"$divide": ["$year", 10]}}, 10]},
            "Runtime (Minutes)": 1
        }},
        {"$group": {
            "_id": "$decade",
            "avg_runtime": {"$avg": "$Runtime (Minutes)"}
        }},
        {"$sort": {"_id": 1}}
    ]
    return list(collection.aggregate(pipeline))