import json

notebook_path = '/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/Netflix_Clustering_Analysis.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        new_source = []
        for line in source:
            if 'feature_names = tfidf_matrix.get_feature_names_out()' in line:
                new_source.append(line.replace('tfidf_matrix.get_feature_names_out()', 'tfidf.get_feature_names_out()'))
            else:
                new_source.append(line)
        cell['source'] = new_source

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print("Fixed AttributeError in", notebook_path)
