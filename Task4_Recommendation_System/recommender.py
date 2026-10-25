import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
 
# ----------------------------------------------------------------------
# 1. Sample data (small built-in dataset so the project runs anywhere)
# ----------------------------------------------------------------------
MOVIES = pd.DataFrame(
    [
        ("The Matrix", "Action Sci-Fi", "A hacker discovers reality is a simulation and joins a rebellion against machines."),
        ("Inception", "Action Sci-Fi Thriller", "A thief enters dreams to steal secrets and plant an idea in a target's mind."),
        ("Interstellar", "Sci-Fi Drama", "Astronauts travel through a wormhole to find a new home for humanity."),
        ("The Dark Knight", "Action Crime Drama", "Batman faces the Joker, a criminal mastermind who spreads chaos in Gotham."),
        ("Avengers: Endgame", "Action Sci-Fi Adventure", "Superheroes unite to undo a villain's destruction of half the universe."),
        ("Iron Man", "Action Sci-Fi", "A billionaire engineer builds a powered suit of armor to fight evil."),
        ("Titanic", "Romance Drama", "A young couple from different classes fall in love aboard a doomed ship."),
        ("The Notebook", "Romance Drama", "A couple's enduring love story told across decades."),
        ("La La Land", "Romance Musical Drama", "A jazz pianist and an actress chase their dreams and love in Los Angeles."),
        ("The Godfather", "Crime Drama", "The aging head of a crime family passes control to his reluctant son."),
        ("Pulp Fiction", "Crime Thriller", "Intertwined stories of hitmen, a boxer and a gangster's wife in Los Angeles."),
        ("Goodfellas", "Crime Drama", "The rise and fall of a mobster and his associates in the mafia."),
        ("Toy Story", "Animation Comedy Family", "Toys come to life when humans are not around and go on adventures."),
        ("Finding Nemo", "Animation Adventure Family", "A clownfish crosses the ocean to rescue his lost son."),
        ("The Lion King", "Animation Drama Family", "A young lion prince flees his kingdom and returns to take his place."),
        ("Shrek", "Animation Comedy Fantasy", "A grumpy ogre rescues a princess with the help of a talking donkey."),
        ("The Hangover", "Comedy", "Friends wake up after a bachelor party in Las Vegas with no memory of the night."),
        ("Superbad", "Comedy", "Two teenage friends try to enjoy one last wild night before graduating."),
        ("Get Out", "Horror Thriller", "A young man uncovers disturbing secrets while visiting his girlfriend's family."),
        ("A Quiet Place", "Horror Sci-Fi Thriller", "A family must live in silence to hide from deadly creatures that hunt by sound."),
        ("The Conjuring", "Horror Thriller", "Paranormal investigators help a family terrorized by a dark presence."),
        ("Harry Potter", "Fantasy Adventure Family", "A young orphan discovers he is a wizard and attends a school of magic."),
        ("The Lord of the Rings", "Fantasy Adventure", "A hobbit sets out to destroy a powerful ring and defeat a dark lord."),
        ("Jurassic Park", "Sci-Fi Adventure Thriller", "Scientists and visitors fight to survive on an island of cloned dinosaurs."),
        ("Forrest Gump", "Drama Romance", "A kind man with a low IQ unwittingly witnesses and influences decades of history."),
    ],
    columns=["title", "genres", "description"],
)
 
# Ratings given by sample users (1-5). NaN = not watched yet.
RATINGS = pd.DataFrame(
    {
        "Aman": {"The Matrix": 5, "Inception": 5, "Interstellar": 4, "The Dark Knight": 5, "Iron Man": 4,
                 "Avengers: Endgame": 5, "Titanic": 2, "Toy Story": 3, "The Notebook": 1, "Jurassic Park": 4},
        "Priya": {"Titanic": 5, "The Notebook": 5, "La La Land": 4, "Forrest Gump": 5, "The Lion King": 4,
                  "The Matrix": 2, "Toy Story": 4, "Finding Nemo": 4, "Get Out": 1, "The Hangover": 3},
        "Rahul": {"The Godfather": 5, "Pulp Fiction": 5, "Goodfellas": 4, "The Dark Knight": 5, "Inception": 4,
                  "The Notebook": 1, "Forrest Gump": 4, "The Matrix": 4, "Superbad": 2, "Iron Man": 3},
        "Sneha": {"Toy Story": 5, "Finding Nemo": 5, "Shrek": 4, "The Lion King": 5, "Harry Potter": 4,
                  "Get Out": 1, "The Notebook": 3, "La La Land": 4, "The Hangover": 2, "Titanic": 3},
        "Karan": {"Get Out": 5, "A Quiet Place": 5, "The Conjuring": 4, "Jurassic Park": 4, "Inception": 3,
                  "Toy Story": 2, "Pulp Fiction": 4, "The Hangover": 4, "Superbad": 4, "The Matrix": 4},
        "Neha": {"Harry Potter": 5, "The Lord of the Rings": 5, "Shrek": 4, "Finding Nemo": 4, "Interstellar": 4,
                 "The Conjuring": 1, "The Lion King": 4, "Toy Story": 4, "Inception": 3, "Jurassic Park": 3},
        "Vikram": {"Avengers: Endgame": 5, "Iron Man": 5, "The Matrix": 4, "Jurassic Park": 5, "Interstellar": 4,
                   "La La Land": 2, "Inception": 5, "The Dark Knight": 4, "A Quiet Place": 4, "The Lord of the Rings": 4},
    }
).T  # rows = users, columns = movies
 
 
# ----------------------------------------------------------------------
# 2. Content-Based Filtering
# ----------------------------------------------------------------------
class ContentBasedRecommender:
    def __init__(self, movies: pd.DataFrame):
        self.movies = movies.reset_index(drop=True)
        # Repeat genres so they carry more weight than the description words.
        text = (self.movies["genres"] + " ") * 3 + self.movies["description"]
        tfidf = TfidfVectorizer(stop_words="english")
        matrix = tfidf.fit_transform(text)
        self.similarity = cosine_similarity(matrix)
        self.index = pd.Series(self.movies.index, index=self.movies["title"].str.lower())
 
    def find_title(self, query: str):
        """Case-insensitive title lookup (exact first, then partial match)."""
        q = query.strip().lower()
        if q in self.index:
            return self.movies.loc[self.index[q], "title"]
        matches = [t for t in self.movies["title"] if q and q in t.lower()]
        return matches[0] if matches else None
 
    def recommend(self, title: str, n: int = 5) -> pd.DataFrame:
        idx = self.index[title.lower()]
        scores = list(enumerate(self.similarity[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        scores = [s for s in scores if s[0] != idx][:n]
        result = self.movies.iloc[[i for i, _ in scores]][["title", "genres"]].copy()
        result["similarity"] = [round(s, 2) for _, s in scores]
        return result.reset_index(drop=True)
 
 
# ----------------------------------------------------------------------
# 3. Collaborative Filtering (user-based)
# ----------------------------------------------------------------------
class CollaborativeRecommender:
    def __init__(self, ratings: pd.DataFrame, damping: float = 0.5):
        self.ratings = ratings
        self.damping = damping
        # Compare users by their rating vectors (unrated movies count as 0).
        sim = cosine_similarity(ratings.fillna(0))
        self.user_sim = pd.DataFrame(sim, index=ratings.index, columns=ratings.index)
 
    def recommend(self, user: str, n: int = 5) -> pd.DataFrame:
        """Predict ratings for unwatched movies using similar users' ratings."""
        sims = self.user_sim[user].drop(user)
        unseen = self.ratings.columns[self.ratings.loc[user].isna()]
        predictions = {}
        for movie in unseen:
            rated = self.ratings.loc[sims.index, movie].dropna()
            if rated.empty:
                continue
            weights = sims[rated.index]
            # Weighted average of similar users' ratings. The damping term
            # lowers scores that rest on only one or two weakly similar users.
            predictions[movie] = float(
                np.dot(weights, rated) / (weights.sum() + self.damping)
            )
 
        result = pd.DataFrame(
            sorted(predictions.items(), key=lambda x: x[1], reverse=True)[:n],
            columns=["title", "score"],
        )
        result["score"] = result["score"].round(2)
        return result
 
 
# ----------------------------------------------------------------------
# 4. Simple command-line menu
# ----------------------------------------------------------------------
def show(df: pd.DataFrame):
    print()
    print(df.to_string(index=False))
    print()
 
 
def main():
    content_rec = ContentBasedRecommender(MOVIES)
    collab_rec = CollaborativeRecommender(RATINGS)
 
    print("=" * 52)
    print("  Movie Recommendation System (CodSoft Task 4)")
    print("=" * 52)
 
    while True:
        print("1. Movies similar to a movie you like (content-based)")
        print("2. Recommendations for a user (collaborative)")
        print("3. List all movies")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()
 
        if choice == "1":
            query = input("Enter a movie you like: ")
            title = content_rec.find_title(query)
            if title is None:
                print("Movie not found. Choose option 3 to see the list.\n")
                continue
            print(f"\nBecause you liked '{title}', you might enjoy:")
            show(content_rec.recommend(title))
 
        elif choice == "2":
            print("Users:", ", ".join(RATINGS.index))
            name = input("Enter a user name: ").strip().title()
            if name not in RATINGS.index:
                print("User not found.\n")
                continue
            watched = RATINGS.loc[name].dropna()
            print(f"\n{name} has rated: " + ", ".join(f"{m} ({int(r)})" for m, r in watched.items()))
            print(f"\nRecommended for {name}:")
            show(collab_rec.recommend(name))
 
        elif choice == "3":
            show(MOVIES[["title", "genres"]])
 
        elif choice == "4":
            print("Thanks for using the recommender. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4.\n")
 
 
if __name__ == "__main__":
    main()
 
