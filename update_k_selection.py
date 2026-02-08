import json

notebook_path = '/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/Netflix_Clustering_Analysis.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        new_source = []
        for line in source:
            if 'optimal_k = list(k_range)[np.argmax(metrics[\'silhouette\'])]' in line:
                new_source.append(line.replace('silhouette', 'davies').replace('argmax', 'argmin'))
            elif "print(f'✅ Optimal K (Silhouette): {optimal_k}')" in line:
                new_source.append(line.replace('Silhouette', 'Davies-Bouldin'))
            else:
                new_source.append(line)
        cell['source'] = new_source

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print("Updated optimal_k selection in", notebook_path)
