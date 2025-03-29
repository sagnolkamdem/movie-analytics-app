import matplotlib.pyplot as plt
import seaborn as sns

def plot_histogram_films_per_year(data):
    years = [d['_id'] for d in data]
    counts = [d['count'] for d in data]

    fig, ax = plt.subplots()
    sns.barplot(x=years, y=counts, ax=ax)
    ax.set_title("Nombre de films par année")
    ax.set_xlabel("Année")
    ax.set_ylabel("Nombre de films")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_avg_runtime_by_decade(data):
    decades = [d['_id'] for d in data]
    avg_runtimes = [d['avg_runtime'] for d in data]

    fig, ax = plt.subplots()
    sns.lineplot(x=decades, y=avg_runtimes, marker='o', ax=ax)
    ax.set_title("Durée moyenne des films par décennie")
    ax.set_xlabel("Décennie")
    ax.set_ylabel("Durée moyenne (minutes)")
    plt.tight_layout()
    return fig