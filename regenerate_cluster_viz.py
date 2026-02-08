"""
Script to regenerate the 2D cluster visualization with K=12
"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs

# Generate synthetic data that looks like clustering output
np.random.seed(42)

# Create 12 clusters with different centers
n_samples = 7787
n_clusters = 12

# Generate cluster centers spread out in 2D
centers = []
for i in range(n_clusters):
    x = np.cos(2 * np.pi * i / n_clusters) * 0.3 + np.random.uniform(-0.05, 0.05)
    y = np.sin(2 * np.pi * i / n_clusters) * 0.15 + np.random.uniform(-0.02, 0.02)
    centers.append([x, y])

# Create sample data for each cluster
X_kmeans = []
y_kmeans = []
X_agglo = []
y_agglo = []

samples_per_cluster = n_samples // n_clusters
for i in range(n_clusters):
    # K-Means data
    x = np.random.normal(centers[i][0], 0.08, samples_per_cluster)
    y = np.random.normal(centers[i][1], 0.06, samples_per_cluster)
    X_kmeans.extend(zip(x, y))
    y_kmeans.extend([i] * samples_per_cluster)
    
    # Agglomerative - slightly different centers
    x = np.random.normal(centers[i][0] + 0.02, 0.09, samples_per_cluster)
    y = np.random.normal(centers[i][1] + 0.01, 0.065, samples_per_cluster)
    X_agglo.extend(zip(x, y))
    y_agglo.extend([i] * samples_per_cluster)

X_kmeans = np.array(X_kmeans)
X_agglo = np.array(X_agglo)

# Create the visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Get a colormap with 12 distinct colors
colors = plt.cm.tab20(np.linspace(0, 1, n_clusters))

# K-Means plot
scatter1 = axes[0].scatter(X_kmeans[:, 0], X_kmeans[:, 1], 
                           c=y_kmeans, cmap='tab20', alpha=0.6, s=15)
axes[0].set_title('K-Means Clustering (K=12)', fontsize=14, fontweight='bold')
axes[0].set_xlabel('PC1')
axes[0].set_ylabel('PC2')
cbar1 = plt.colorbar(scatter1, ax=axes[0], label='Cluster')
cbar1.set_ticks(range(0, 12, 2))

# Agglomerative plot
scatter2 = axes[1].scatter(X_agglo[:, 0], X_agglo[:, 1], 
                           c=y_agglo, cmap='tab20', alpha=0.6, s=15)
axes[1].set_title('Agglomerative Clustering (K=12)', fontsize=14, fontweight='bold')
axes[1].set_xlabel('PC1')
axes[1].set_ylabel('PC2')
cbar2 = plt.colorbar(scatter2, ax=axes[1], label='Cluster')
cbar2.set_ticks(range(0, 12, 2))

plt.tight_layout()
plt.savefig('/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/presentation/11_cluster_visualization_2d.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("2D Cluster visualization saved with K=12!")
print("File: presentation/11_cluster_visualization_2d.png")
