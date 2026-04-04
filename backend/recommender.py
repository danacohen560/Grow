import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_recommendations_tfidf(user_input, df_path='courses_en.csv', top_n=5):
    df = pd.read_csv(df_path)


    df['skills'] = df['skills'].fillna('')

    # Define TF - IDF model
    # ngram_range(1,2) => model will refer to single words as well as to duo's
    # stop_words => Filters out unrelated words
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))

    # train & turn the skills column to a matrix
    tfidf_matrix = vectorizer.fit_transform(df['skills'])

    # turn user request to a vector in the same format
    user_vector = vectorizer.transform([user_input])

    # Calculate cosine resemblance
    cosine_sim = cosine_similarity(user_vector, tfidf_matrix)[0]

    # add grades to table and sort
    df['score'] = cosine_sim
    results = df[df['score'] > 0].sort_values(by='score', ascending=False).head(top_n)

    return results[['name', 'category', 'skills', 'score', 'url']]


if __name__ == "__main__":
    my_skills = "Python, Data Analysis, SQL, Machine Learning"
    print(f"--- Searching recommendations (TF-IDF) for: {my_skills} ---\n")

    recommendations = get_recommendations_tfidf(my_skills)
    print(recommendations.to_string())