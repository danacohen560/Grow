import pandas as pd
df = pd.read_csv('courses_en.csv')

python_courses = df[df['skills'].str.contains('python', case=False, na=False)]

# הדפסת 3 התוצאות הראשונות כדי שנראה את הפורמט האמיתי
print(f"Found {len(python_courses)} courses mentioning Python.")
print("\n--- Here is how the skills actually look: ---")
for skills_string in python_courses['skills'].head(3):
    print(skills_string)