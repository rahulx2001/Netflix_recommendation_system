#!/usr/bin/env python3
"""
Export Netflix clustered data to JSON for the demo website.
This creates a file that the browser can load for real recommendations.
"""

import pandas as pd
import json
import os

# Load the clustered data
data_path = '../netflix_clustered.csv'
df = pd.read_csv(data_path)

print(f"Loaded {len(df)} titles")

# Define cluster names based on genre analysis (14 clusters)
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

# Prepare the data for JSON export
titles_data = []

for _, row in df.iterrows():
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
        'country': str(row['country']).split(',')[0].strip() if pd.notna(row['country']) else ''
    }
    titles_data.append(title_entry)

# Create the final JSON structure
output = {
    'totalTitles': len(titles_data),
    'clusterNames': cluster_names,
    'titles': titles_data
}

# Save to JSON
output_path = 'netflix_data.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False)

print(f"Exported {len(titles_data)} titles to {output_path}")
print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")

# Print cluster distribution
print("\nCluster distribution:")
for cluster, name in cluster_names.items():
    count = len([t for t in titles_data if t['cluster'] == cluster])
    print(f"  Cluster {cluster} ({name}): {count} titles")
