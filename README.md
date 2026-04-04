# Grow | AI-Powered Course Recommender 🎓

Grow is a full-stack platform designed to bridge the gap between fragmented online learning resources. By unifying datasets from multiple platforms (Coursera & Udemy), the system provides personalized, career-oriented course recommendations based on technical skill matching and NLP-driven similarity scoring.

---

## Key Features

* **Career-Path Matching:** Users can select a target job role (e.g., Data Engineer, Cybersecurity Analyst), and the system automatically generates a tailored curriculum of relevant courses.
* **Skill-Based Search:** Real-time search engine that maps user-inputted skills to course content using advanced text vectorization.
* **Unified Multi-Source Data:** A custom ETL pipeline that merges disparate schemas from Coursera and Udemy into a single, searchable data warehouse.
* **Smart Filtering:** Dynamic UI filters allowing users to toggle between learning platforms.
* **Persistent Favorites:** A localized bookmarking system that allows users to save courses for future reference using Browser LocalStorage.

---

## Tech Stack

### Backend (Data & API)
* **Python / FastAPI:** High-performance asynchronous API framework.
* **Pandas:** Data manipulation and analysis.
* **Scikit-Learn:** Implementation of the TF-IDF vectorizer and Cosine Similarity calculations.

### Frontend (User Interface)
* **React (Vite):** Modern, fast frontend development environment.
* **CSS3:** Custom responsive design with a "High-Tech" aesthetic (Glassmorphism, gradients, and fluid layouts).

---

##  Engineering & Logic

### 1. Data Engineering (ETL Pipeline)
The project handles raw data from multiple sources with inconsistent structures. The `etl_pipeline.py` script performs:
* **Extraction:** Ingesting raw CSV datasets.
* **Transformation:** Mapping platform-specific columns (e.g., Coursera's `skills` vs. Udemy's `course_description`) into a unified **Search Corpus**.
* **Normalization:** Cleaning text, handling null values, and ensuring schema consistency across 10,000+ records.

### 2. Recommendation Engine (NLP)
Instead of basic keyword matching, EduSync utilizes **TF-IDF (Term Frequency-Inverse Document Frequency)**:
* **Vectorization:** Converting the text corpus into numerical vectors, emphasizing unique technical terms while de-emphasizing common words.
* **Cosine Similarity:** Measuring the mathematical distance between the user's input vector and the course vectors to determine the highest relevance scores.



---

## Installation & Setup

### Prerequisites
* Python 3.8+
* Node.js (npm)

### Backend Setup
1. Navigate to the root directory.
2. Install dependencies: `pip install fastapi uvicorn pandas scikit-learn`
3. Run the ETL pipeline: `python etl_pipeline.py`
4. Start the server: `uvicorn main:app --reload`

### Frontend Setup
1. Navigate to the `/frontend` directory.
2. Install dependencies: `npm install`
3. Start the dev server: `npm run dev`

---

### Contact
**Dana Cohen** - Data Engineering Student @ Ben Gurion University  

