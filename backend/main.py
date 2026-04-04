from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
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

# Load data and train model
print("Loading data...")
df = pd.read_csv('unified_courses.csv')

# Handle brackets in instructor names & Null values
if 'instructor' in df.columns:
    df['instructor'] = df['instructor'].str.replace(r"[\[\]']", "", regex=True)
    # If the instructor is empty or null, set a default value
    df['instructor'] = df['instructor'].fillna('Expert Instructors')


df['search_corpus'] = df['search_corpus'].fillna('')

vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
tfidf_matrix = vectorizer.fit_transform(df['search_corpus'])
print("Backend Ready!")

def get_difficulty_level(title):
    """Categorizes course difficulty based on keywords in the title"""
    title = title.lower()
    if any(word in title for word in ['intro', 'beginner', 'foundation', 'basic', 'starting', '101']):
        return {"label": "Beginner", "score": 1}
    if any(word in title for word in ['advanced', 'expert', 'professional', 'masterclass', 'complex']):
        return {"label": "Advanced", "score": 3}
    return {"label": "Intermediate", "score": 2}


@app.get("/")
def read_root():
    return {"status": "online"}


@app.get("/stats")
def get_stats():
    """Generates statistics for the dashboard safely"""
    try:
        platform_counts = df['platform'].value_counts().to_dict()
        top_categories = df['category'].value_counts().head(5).to_dict()

        return {
            "total_courses": len(df),
            "platform_data": [{"name": k, "value": int(v)} for k, v in platform_counts.items()],
            "category_data": [{"name": k, "value": int(v)} for k, v in top_categories.items()]
        }
    except Exception as e:
        print(f"Stats Error: {e}")
        return {"error": "Could not load stats"}

@app.get("/recommend")
def get_recommendations(skills: str):
    try:
        if not skills:
            return {"recommendations": []}

        user_vector = vectorizer.transform([skills.lower()])
        cosine_sim = cosine_similarity(user_vector, tfidf_matrix)[0]
        
        temp_df = df.copy()
        temp_df['score'] = cosine_sim
        temp_df['difficulty_label'] = temp_df['title'].apply(lambda x: get_difficulty_level(x)['label'])
        temp_df['difficulty_score'] = temp_df['title'].apply(lambda x: get_difficulty_level(x)['score'])
        
        # Filter relevant courses
        relevant_courses = temp_df[temp_df['score'] > 0.05].sort_values(by='score', ascending=False)
        
        final_roadmap = []
        # Logic: Pick top 2 for each level to create a progressive path
        for level in [1, 2, 3]:  # 1=Beginner, 2=Intermediate, 3=Advanced
            level_courses = relevant_courses[relevant_courses['difficulty_score'] == level].head(2)
            
            for _, row in level_courses.iterrows():
                # Avoid duplicate titles (simple check)
                if not any(row['title'][:15] in r['title'] for r in final_roadmap):
                    final_roadmap.append({
                        'title': row['title'],
                        'category': row['category'],
                        'instructor': row['instructor'],
                        'platform': row['platform'],
                        'score': row['score'],
                        'url': row['url'],
                        'difficulty': row['difficulty_label'],
                        'difficulty_score': int(row['difficulty_score'])
                    })
        
        # Sort the final list by difficulty so it's always a path
        final_roadmap.sort(key=lambda x: x['difficulty_score'])
            
        return {"recommendations": final_roadmap}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}