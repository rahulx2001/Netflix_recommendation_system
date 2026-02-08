# 🎬 Netflix Movies and TV Shows Clustering

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Machine%20Learning-Unsupervised-green.svg" alt="ML">
  <img src="https://img.shields.io/badge/NLP-TF--IDF-orange.svg" alt="NLP">
  <img src="https://img.shields.io/badge/Status-Complete-brightgreen.svg" alt="Status">
</p>

## 📋 Project Overview

This project applies **unsupervised machine learning techniques** to cluster Netflix's catalog of movies and TV shows into meaningful groups based on their descriptive features—without relying on user interaction data.

### 🎯 Objectives

- **Enhance content discoverability** through structural segmentation
- **Enable genre-level exploration** beyond traditional classification
- **Support personalized recommendations** by suggesting content from similar clusters

## 🛠️ Methodology

### Data Pipeline

```
Raw Data → Cleaning → Text Preprocessing → TF-IDF Vectorization → PCA → Clustering → Recommendations
```

### Techniques Used

| Stage | Technique |
|-------|-----------|
| **Data Cleaning** | Missing value imputation, text normalization |
| **NLP** | Tokenization, lemmatization, stopword removal |
| **Feature Engineering** | TF-IDF with unigrams & bigrams (5000 features) |
| **Dimensionality Reduction** | PCA (95% variance retention) |
| **Clustering** | K-Means, Hierarchical Agglomerative |
| **Evaluation** | Silhouette Score, Calinski-Harabasz, Davies-Bouldin |
| **Recommendation** | Cosine Similarity based content filtering |

## 📊 Dataset

- **Source**: Netflix Titles Dataset
- **Size**: ~7,800 titles
- **Features**: 12 columns including title, director, cast, country, genre, description

## 🔍 Key Findings

### Cluster Characteristics

The clustering reveals distinct content groupings based on:
- **Genre patterns** (International content, Drama, Comedy, etc.)
- **Geographic origin** (US productions, Indian content, Korean shows)
- **Content type** (Movies vs. TV Shows)
- **Target audience** (Rating-based segmentation)

## 📈 Evaluation Metrics

| Metric | K-Means | Agglomerative |
|--------|---------|---------------|
| Silhouette Score | Higher is better | Comparable |
| Calinski-Harabasz | Measures cluster separation | Robust |
| Davies-Bouldin | Lower is better | Efficient |

## 🎬 Recommendation System

The content-based recommendation system uses:
- **Cosine similarity** on TF-IDF vectors
- **Cluster-aware recommendations** for better grouping
- Returns similar titles with similarity scores

### Example Usage

```python
# Get recommendations for a title
recommendations = get_recommendations("Stranger Things", n_recommendations=10)
print(recommendations)
```

## 📁 Project Structure

```
netflix-clustering/
├── netflix_clustering.py      # Main analysis script
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── netflix_clustered.csv      # Output: Clustered dataset
├── cluster_summary.csv        # Output: Cluster statistics
└── *.png                      # Output: Visualization images
```

## 🚀 Getting Started

### Prerequisites

```bash
pip install -r requirements.txt
```

### Run the Analysis

```bash
python netflix_clustering.py
```

## 📸 Visualizations

The project generates 14 comprehensive visualizations:

1. **Missing Values Analysis** - Data quality assessment
2. **Content Type Distribution** - Movies vs TV Shows breakdown
3. **Rating Distribution** - Content rating analysis
4. **Release Year Trends** - Temporal patterns
5. **Top Countries** - Geographic content distribution
6. **Top Genres** - Popular genre categories
7. **TF-IDF Terms** - Important text features
8. **PCA Variance** - Dimensionality reduction analysis
9. **K-Means Metrics** - Cluster evaluation (Elbow, Silhouette)
10. **Dendrogram** - Hierarchical clustering visualization
11. **2D Cluster Plot** - PCA-reduced cluster visualization
12. **Cluster Sizes** - Cluster distribution comparison
13. **Word Clouds** - Key terms per cluster
14. **Cluster Composition** - Demographic breakdown

## 💡 Business Impact

This clustering approach enables Netflix (or similar platforms) to:

- ✅ **Recommend newly added content** by cluster similarity
- ✅ **Identify viewing trends** for targeted content acquisition
- ✅ **Improve exploratory browsing** experience
- ✅ **Handle cold-start problem** for new content
- ✅ **Support international content discovery**

## 🔧 Technologies

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-154F5B?style=flat&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat&logoColor=white)

## 📝 Author

**Rahul Kumar Singh**

---

<p align="center">
  Made with ❤️ for Data Science
</p>
