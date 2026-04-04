import pandas as pd
import numpy as np


def run_etl():
    """
        Executes the ETL process to unify
        Coursera and Udemy datasets into a single searchable format.
        """
    print("Starting ETL Process")

    print("Extracting data from files...")
    try:
        df_coursera = pd.read_csv('courses_en.csv')
        df_udemy = pd.read_csv('udemy_courses.csv')
    except FileNotFoundError as e:
        print(f"Error: Could not find file. {e}")
        return

    print("Transforming data")
    df_coursera['skills'] = df_coursera['skills'].fillna('')
    df_coursera['category'] = df_coursera['category'].fillna('')

    coursera_clean = pd.DataFrame({
        'title': df_coursera['name'],
        'url': df_coursera['url'],
        'category': df_coursera['category'],
        'instructor': df_coursera['instructors'],
        'platform': 'Coursera',
        # Combine key features for the recommendation engine
        'search_corpus': df_coursera['name'] + ' ' + df_coursera['category'] + ' ' + df_coursera['skills']
    })

    # Map Udemy columns to the same unified schema
    print("Transforming Udemy data")
    df_udemy['course_description'] = df_udemy['course_description'].fillna('')
    df_udemy['category'] = df_udemy['category'].fillna('')

    udemy_clean = pd.DataFrame({
        'title': df_udemy['course_title'],
        'url': df_udemy['course_link'],
        'category': df_udemy['category'],
        'instructor': df_udemy['instructor'],
        'platform': 'Udemy',
        'search_corpus': df_udemy['course_title'] + ' ' + df_udemy['category'] + ' ' + df_udemy['course_description']
    })

    # Merge datasets anf normalize text data
    unified_df = pd.concat([coursera_clean, udemy_clean], ignore_index=True)

    unified_df = unified_df.dropna(subset=['title', 'url', 'search_corpus'])

    unified_df['search_corpus'] = unified_df['search_corpus'].str.lower()

    # save to a single csv
    output_filename = 'unified_courses.csv'
    unified_df.to_csv(output_filename, index=False)

    print(f"Total courses ready for recommendation: {len(unified_df)}")
    print(f"Saved to: {output_filename}")

if __name__ == "__main__":
    run_etl()