#!/usr/bin/env python3
"""
Export REAL cosine similarity scores for the demo.
This computes actual TF-IDF similarity between titles.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

print("Loading Netflix data...")
df = pd.read_csv('../netflix_clustered.csv')
print(f"Loaded {len(df)} titles")

# Use the processed_text column for TF-IDF if available
if 'processed_text' in df.columns:
    text_column = 'processed_text'
elif 'cleaned_text' in df.columns:
    text_column = 'cleaned_text'
elif 'combined_text' in df.columns:
    text_column = 'combined_text'
else:
    # Combine relevant text fields
    print("Creating combined text field...")
    df['combined_text'] = df['title'].fillna('') + ' ' + \
                          df['listed_in'].fillna('') + ' ' + \
                          df['description'].fillna('') + ' ' + \
                          df['cast'].fillna('') + ' ' + \
                          df['director'].fillna('')
    text_column = 'combined_text'

print(f"Using '{text_column}' for TF-IDF vectorization...")

# Fill NaN values
df[text_column] = df[text_column].fillna('')

# Create TF-IDF matrix
print("Creating TF-IDF matrix...")
tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
tfidf_matrix = tfidf.fit_transform(df[text_column])
print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")

# Compute similarity matrix (this can take time for large datasets)
print("Computing cosine similarity matrix...")
# For 7787 x 7787, we'll compute in batches to save memory
n = len(df)
batch_size = 500

# Create title to index mapping
title_to_idx = {row['title'].lower().strip(): idx for idx, row in df.iterrows()}

# Cluster names
cluster_names = {
    0: "Kids & Family",
    1: "Documentaries",
    2: "Stand-Up Comedy",
    3: "British & International Docuseries",
    4: "International Romantic Comedies",
    5: "Action & Adventure",
    6: "International Dramas",
    7: "Hollywood Dramas",
    8: "International Films",
    9: "Independent & Art Films",
    10: "Docuseries & Reality",
    11: "International TV Dramas",
    12: "Korean & Asian Romance",
    13: "Spanish Crime & Thriller"
}

# For each title, compute top 10 most similar titles
print("Computing top similar titles for each item...")
similarities = {}

for i in range(0, n, batch_size):
    end_idx = min(i + batch_size, n)
    batch_sim = cosine_similarity(tfidf_matrix[i:end_idx], tfidf_matrix)
    
    for j, global_idx in enumerate(range(i, end_idx)):
        row_sim = batch_sim[j]
        # Get top 15 most similar (excluding self)
        top_indices = np.argsort(row_sim)[::-1][1:16]  # Skip first (self)
        top_scores = row_sim[top_indices]
        
        title = df.iloc[global_idx]['title']
        similarities[title] = [
            {'idx': int(idx), 'score': float(score)} 
            for idx, score in zip(top_indices, top_scores)
        ]
    
    if (i + batch_size) % 1000 == 0 or end_idx == n:
        print(f"  Processed {end_idx}/{n} titles...")

# Prepare final export
print("Preparing JSON export...")
titles_data = []

for idx, row in df.iterrows():
    title = row['title']
    top_similar = similarities.get(title, [])[:10]  # Top 10
    
    # Get actual similar titles with scores
    similar_titles = []
    for sim in top_similar:
        sim_row = df.iloc[sim['idx']]
        similar_titles.append({
            'id': sim_row['show_id'],
            'title': sim_row['title'],
            'score': round(sim['score'] * 100, 1)  # Convert to percentage
        })
    
    title_entry = {
        'id': row['show_id'],
        'title': str(row['title']).strip(),
        'type': row['type'],
        'year': int(row['release_year']) if pd.notna(row['release_year']) else 0,
        'rating': str(row['rating']) if pd.notna(row['rating']) else 'NR',
        'duration': str(row['duration']) if pd.notna(row['duration']) else '',
        'genres': str(row['listed_in']).split(', ') if pd.notna(row['listed_in']) else [],
        'description': str(row['description'])[:200] if pd.notna(row['description']) else '',
        'cluster': int(row['kmeans_cluster']) if pd.notna(row['kmeans_cluster']) else 0,
        'country': str(row['country']).split(',')[0].strip() if pd.notna(row['country']) else '',
        'similar': similar_titles  # REAL similarity scores!
    }
    titles_data.append(title_entry)

# Create final output
output = {
    'totalTitles': len(titles_data),
    'clusterNames': cluster_names,
    'titles': titles_data
}

# Save to JSON
output_path = 'netflix_data.json'
print(f"Saving to {output_path}...")
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False)

file_size = os.path.getsize(output_path) / 1024 / 1024
print(f"✅ Exported {len(titles_data)} titles with REAL similarity scores!")
print(f"   File size: {file_size:.1f} MB")

# Show sample
sample_title = "Stranger Things"
sample_idx = title_to_idx.get(sample_title.lower())
if sample_idx is not None:
    print(f"\nSample - Similar to '{sample_title}':")
    for sim in titles_data[sample_idx]['similar'][:5]:
        print(f"  {sim['title']}: {sim['score']}%")
