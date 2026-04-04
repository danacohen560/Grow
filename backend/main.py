import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_difficulty_score(title):
    t = str(title).lower()
    if any(word in t for word in ['beginner', 'intro', 'foundation', '101', 'start']):
        return {"label": "Beginner", "score": 1}
    if any(word in t for word in ['advanced', 'expert', 'professional', 'master', 'deep']):
        return {"label": "Advanced", "score": 3}
    return {"label": "Intermediate", "score": 2}

df = pd.read_csv('unified_courses.csv')
if 'instructor' in df.columns:
    df['instructor'] = df['instructor'].str.replace(r"[\[\]']", "", regex=True).fillna('Expert Instructors')

df['difficulty_info'] = df['title'].apply(get_difficulty_score)
df['difficulty_label'] = df['difficulty_info'].apply(lambda x: x['label'])
df['difficulty_score'] = df['difficulty_info'].apply(lambda x: x['score'])

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['search_corpus'].fillna(''))

@app.get("/stats")
def get_stats():
    category_counts = df['category'].value_counts().head(5).to_dict()
    platform_counts = df['platform'].value_counts().to_dict()
    return {
        "total_courses": len(df),
        "category_data": [{"name": k, "value": v} for k, v in category_counts.items()],
        "platform_data": [{"name": k, "value": v} for k, v in platform_counts.items()]
    }

@app.get("/recommend")
def get_recommendations(skills: str):
    try:
        if not skills:
            return {"recommendations": []}

        user_vector = vectorizer.transform([skills.lower()])
        scores = cosine_similarity(user_vector, tfidf_matrix)[0]
        

        temp_df = df.copy()
        temp_df['score'] = scores

        relevant = temp_df[temp_df['score'] > 0.01].sort_values(by='score', ascending=False)
        
        if relevant.empty:
            return {"recommendations": []}

        final_roadmap = []
        seen_titles = set()

        for level in [1, 2, 3]:
            level_subset = relevant[relevant['difficulty_score'] == level].head(3)
            for _, row in level_subset.iterrows():
                short_title = str(row['title'])[:20]
                if short_title not in seen_titles:
                    final_roadmap.append({
                        "title": row['title'],
                        "platform": row['platform'],
                        "category": row['category'],
                        "instructor": row['instructor'],
                        "score": float(row['score']),
                        "difficulty": row['difficulty_label'],
                        "difficulty_score": int(row['difficulty_score']),
                        "url": row['url']
                    })
                    seen_titles.add(short_title)
        
        final_roadmap.sort(key=lambda x: x['difficulty_score'])
        
        return {"recommendations": final_roadmap[:8]} # מחזירים עד 8 קורסים סך הכל
        
    except Exception as e:
        print(f"CRASH ERROR: {e}") 
        return {"error": str(e)}

@app.get("/")
def home():
    return {"status": "EduSync Backend is Online"}