"""
Script to update the Netflix Clustering Analysis notebook with all improvements
"""
import json

notebook_path = '/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/Netflix_Clustering_Analysis.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Improved K-selection with weighted scoring
improved_k_selection = '''# Finding optimal K using MULTIPLE metrics combined
# Instead of just one, we use weighted scoring for better results

k_range = range(2, 15)
metrics = {'inertia': [], 'silhouette': [], 'calinski': [], 'davies': []}

print("Testing K values...")
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=300)
    km.fit(tfidf_pca)
    
    metrics['inertia'].append(km.inertia_)
    metrics['silhouette'].append(silhouette_score(tfidf_pca, km.labels_))
    metrics['calinski'].append(calinski_harabasz_score(tfidf_pca, km.labels_))
    metrics['davies'].append(davies_bouldin_score(tfidf_pca, km.labels_))

# Individual metric recommendations
print("\\n📊 Individual Metrics suggest:")
print(f"  Silhouette: K = {list(k_range)[np.argmax(metrics['silhouette'])]}")
print(f"  Calinski-Harabasz: K = {list(k_range)[np.argmax(metrics['calinski'])]}")
print(f"  Davies-Bouldin: K = {list(k_range)[np.argmin(metrics['davies'])]}")

# Weighted multi-metric approach
def normalize(scores, higher_is_better=True):
    scores = np.array(scores)
    min_v, max_v = scores.min(), scores.max()
    if max_v == min_v:
        return np.ones_like(scores) * 0.5
    norm = (scores - min_v) / (max_v - min_v)
    return norm if higher_is_better else (1 - norm)

# Normalize and combine: 40% Silhouette + 40% Davies + 20% Calinski
sil_n = normalize(metrics['silhouette'], True)
dav_n = normalize(metrics['davies'], False)  # lower is better
cal_n = normalize(metrics['calinski'], True)

combined = 0.4 * sil_n + 0.4 * dav_n + 0.2 * cal_n
optimal_k = list(k_range)[np.argmax(combined)]

print(f"\\n🎯 Weighted Multi-Metric Optimal K = {optimal_k}")

# Visualize
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

axes[0,0].plot(k_range, metrics['inertia'], 'bo-')
axes[0,0].axvline(x=optimal_k, color='r', linestyle='--', label=f'K={optimal_k}')
axes[0,0].set_title('Elbow Method (Inertia ↓)')
axes[0,0].legend()

axes[0,1].plot(k_range, metrics['silhouette'], 'go-')
axes[0,1].axvline(x=optimal_k, color='r', linestyle='--', label=f'K={optimal_k}')
axes[0,1].set_title('Silhouette Score ↑')
axes[0,1].legend()

axes[1,0].plot(k_range, metrics['calinski'], 'ro-')
axes[1,0].axvline(x=optimal_k, color='gray', linestyle='--', label=f'K={optimal_k}')
axes[1,0].set_title('Calinski-Harabasz ↑')
axes[1,0].legend()

axes[1,1].plot(k_range, metrics['davies'], 'mo-')
axes[1,1].axvline(x=optimal_k, color='gray', linestyle='--', label=f'K={optimal_k}')
axes[1,1].set_title('Davies-Bouldin ↓')
axes[1,1].legend()

for ax in axes.flat:
    ax.set_xlabel('K')

plt.suptitle('K-Means Metrics Comparison', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()'''

# Final K-Means with stability check
improved_kmeans_final = '''# Apply final K-Means with our optimal K
print(f"Applying K-Means with K = {optimal_k}")

kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=20, max_iter=500)
kmeans_labels = kmeans.fit_predict(tfidf_pca)
df_clean['kmeans_cluster'] = kmeans_labels

# Calculate metrics
km_sil = silhouette_score(tfidf_pca, kmeans_labels)
km_cal = calinski_harabasz_score(tfidf_pca, kmeans_labels)
km_dav = davies_bouldin_score(tfidf_pca, kmeans_labels)

print(f"\\n📈 K-Means Results (K={optimal_k}):")
print(f"  Silhouette: {km_sil:.4f}")
print(f"  Calinski-Harabasz: {km_cal:.2f}")
print(f"  Davies-Bouldin: {km_dav:.4f}")

# Cluster stability validation
from sklearn.metrics import adjusted_rand_score

print("\\n🔄 Checking cluster stability...")
stability_scores = []
for i in range(5):
    test_km = KMeans(n_clusters=optimal_k, random_state=i+100, n_init=10)
    test_labels = test_km.fit_predict(tfidf_pca)
    ari = adjusted_rand_score(kmeans_labels, test_labels)
    stability_scores.append(ari)

mean_ari = np.mean(stability_scores)
print(f"  Mean ARI: {mean_ari:.4f}")
if mean_ari >= 0.9:
    print("  ✅ Clusters are highly stable!")
elif mean_ari >= 0.7:
    print("  ✅ Clusters are reasonably stable")
else:
    print("  ⚠️ Some cluster instability detected")

print(f"\\n📊 Cluster Distribution:")
print(df_clean['kmeans_cluster'].value_counts().sort_index())'''

# Find and update cells
updated_count = 0
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        
        # Update K selection cell (the first one with metric calculations)
        if 'k_range = range(2, 15)' in source and "metrics = {'inertia'" in source and 'weighted' not in source.lower():
            # Only update if it's not already updated
            if 'Weighted Multi-Metric' not in source:
                cell['source'] = [improved_k_selection]
                cell['outputs'] = []
                print(f"Updated cell {i}: K selection with weighted scoring")
                updated_count += 1
        
        # Update final K-Means cell
        elif 'kmeans = KMeans(n_clusters=optimal_k' in source and 'stability' not in source.lower():
            cell['source'] = [improved_kmeans_final]
            cell['outputs'] = []
            print(f"Updated cell {i}: K-Means with stability check")
            updated_count += 1

# Save
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print(f"\n✅ Updated {updated_count} cells in the notebook!")
print(f"File saved: {notebook_path}")
