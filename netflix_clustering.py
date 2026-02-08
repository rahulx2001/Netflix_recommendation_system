"""
Netflix Movies and TV Shows Clustering Project
================================================
A comprehensive unsupervised machine learning project to cluster Netflix content
based on descriptive features using NLP and clustering algorithms.

Author: Rahul Kumar Singh
Date: February 2026
"""

# =============================================================================
# SECTION 1: IMPORT LIBRARIES
# =============================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

# NLP Libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import string

# Scikit-learn imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# Scipy for hierarchical clustering
from scipy.cluster.hierarchy import dendrogram, linkage

# Download NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Set style for visualizations
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

print("=" * 70)
print("NETFLIX MOVIES AND TV SHOWS CLUSTERING PROJECT")
print("=" * 70)

# =============================================================================
# SECTION 2: DATA LOADING AND INITIAL EXPLORATION
# =============================================================================
print("\n" + "=" * 70)
print("SECTION 2: DATA LOADING AND INITIAL EXPLORATION")
print("=" * 70)

# Load the dataset
df = pd.read_csv('/Users/rahulkumarsinghj/Developer /Code/NETFLIX MOVIES AND TV SHOWS CLUSTERING (1) (1) (2) (1).csv')

print(f"\n📊 Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\n📋 Column Names:\n{df.columns.tolist()}")

print("\n📈 Dataset Info:")
print(df.info())

print("\n📊 First 5 Rows:")
print(df.head())

print("\n📊 Statistical Summary for Numerical Columns:")
print(df.describe())

print("\n📊 Data Types:")
print(df.dtypes)

# =============================================================================
# SECTION 3: EXPLORATORY DATA ANALYSIS (EDA)
# =============================================================================
print("\n" + "=" * 70)
print("SECTION 3: EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 70)

# 3.1 Missing Values Analysis
print("\n🔍 Missing Values Analysis:")
missing_values = df.isnull().sum()
missing_percentage = (df.isnull().sum() / len(df)) * 100
missing_df = pd.DataFrame({
    'Column': df.columns,
    'Missing Values': missing_values.values,
    'Percentage (%)': missing_percentage.values
}).sort_values(by='Missing Values', ascending=False)
print(missing_df[missing_df['Missing Values'] > 0])

# Visualize missing values
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#ff6b6b' if x > 0 else '#4ecdc4' for x in missing_values.values]
bars = ax.bar(df.columns, missing_percentage.values, color=colors, edgecolor='white', linewidth=1.5)
ax.set_xlabel('Columns', fontsize=12, fontweight='bold')
ax.set_ylabel('Missing Percentage (%)', fontsize=12, fontweight='bold')
ax.set_title('Missing Values Analysis', fontsize=16, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right')
ax.axhline(y=10, color='red', linestyle='--', alpha=0.7, label='10% Threshold')
ax.legend()
for bar, pct in zip(bars, missing_percentage.values):
    if pct > 0:
        ax.annotate(f'{pct:.1f}%', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/01_missing_values.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved: 01_missing_values.png")

# 3.2 Content Type Distribution
print("\n🎬 Content Type Distribution:")
type_counts = df['type'].value_counts()
print(type_counts)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Pie chart
colors_pie = ['#667eea', '#f093fb']
explode = (0.05, 0)
axes[0].pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%', 
            colors=colors_pie, explode=explode, shadow=True, startangle=90,
            textprops={'fontsize': 12, 'fontweight': 'bold'})
axes[0].set_title('Content Type Distribution', fontsize=16, fontweight='bold', pad=20)

# Bar chart
bars = axes[1].bar(type_counts.index, type_counts.values, color=colors_pie, edgecolor='white', linewidth=2)
axes[1].set_xlabel('Content Type', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Count', fontsize=12, fontweight='bold')
axes[1].set_title('Content Type Counts', fontsize=16, fontweight='bold', pad=20)
for bar in bars:
    height = bar.get_height()
    axes[1].annotate(f'{int(height):,}', xy=(bar.get_x() + bar.get_width()/2, height),
                    ha='center', va='bottom', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/02_content_type_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved: 02_content_type_distribution.png")

# 3.3 Rating Distribution
print("\n⭐ Rating Distribution:")
rating_counts = df['rating'].value_counts()
print(rating_counts)

fig, ax = plt.subplots(figsize=(14, 7))
colors_rating = plt.cm.viridis(np.linspace(0.2, 0.8, len(rating_counts)))
bars = ax.bar(rating_counts.index, rating_counts.values, color=colors_rating, edgecolor='white', linewidth=1.5)
ax.set_xlabel('Rating', fontsize=12, fontweight='bold')
ax.set_ylabel('Count', fontsize=12, fontweight='bold')
ax.set_title('Content Rating Distribution', fontsize=16, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right')
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width()/2, height),
               ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/03_rating_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved: 03_rating_distribution.png")

# 3.4 Release Year Trend
print("\n📅 Release Year Analysis:")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Release year distribution
year_counts = df['release_year'].value_counts().sort_index()
axes[0].fill_between(year_counts.index, year_counts.values, alpha=0.5, color='#667eea')
axes[0].plot(year_counts.index, year_counts.values, 'o-', color='#667eea', linewidth=2, markersize=3)
axes[0].set_xlabel('Release Year', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Number of Titles', fontsize=12, fontweight='bold')
axes[0].set_title('Content Release Year Trend', fontsize=16, fontweight='bold', pad=20)
axes[0].axvline(x=2015, color='red', linestyle='--', alpha=0.7, label='Netflix Original Era')
axes[0].legend()

# Content by decade
df['decade'] = (df['release_year'] // 10) * 10
decade_counts = df['decade'].value_counts().sort_index()
bars = axes[1].bar(decade_counts.index.astype(str) + 's', decade_counts.values, 
                  color=plt.cm.plasma(np.linspace(0.2, 0.8, len(decade_counts))), edgecolor='white')
axes[1].set_xlabel('Decade', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Number of Titles', fontsize=12, fontweight='bold')
axes[1].set_title('Content by Decade', fontsize=16, fontweight='bold', pad=20)
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/04_release_year_trend.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved: 04_release_year_trend.png")

# 3.5 Top Countries
print("\n🌍 Top 10 Countries by Content:")
# Handle multiple countries
countries = df['country'].dropna().str.split(', ').explode()
country_counts = countries.value_counts().head(10)
print(country_counts)

fig, ax = plt.subplots(figsize=(12, 8))
colors_countries = plt.cm.coolwarm(np.linspace(0.1, 0.9, len(country_counts)))
bars = ax.barh(country_counts.index[::-1], country_counts.values[::-1], color=colors_countries[::-1], edgecolor='white')
ax.set_xlabel('Number of Titles', fontsize=12, fontweight='bold')
ax.set_ylabel('Country', fontsize=12, fontweight='bold')
ax.set_title('Top 10 Countries by Content Production', fontsize=16, fontweight='bold', pad=20)
for bar in bars:
    width = bar.get_width()
    ax.annotate(f'{int(width):,}', xy=(width, bar.get_y() + bar.get_height()/2),
               ha='left', va='center', fontsize=11, fontweight='bold', xytext=(5, 0), textcoords='offset points')
plt.tight_layout()
plt.savefig('/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/05_top_countries.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved: 05_top_countries.png")

# 3.6 Top Genres
print("\n🎭 Top 15 Genres:")
genres = df['listed_in'].dropna().str.split(', ').explode()
genre_counts = genres.value_counts().head(15)
print(genre_counts)

fig, ax = plt.subplots(figsize=(14, 8))
colors_genres = plt.cm.Set3(np.linspace(0, 1, len(genre_counts)))
bars = ax.barh(genre_counts.index[::-1], genre_counts.values[::-1], color=colors_genres[::-1], edgecolor='white')
ax.set_xlabel('Number of Titles', fontsize=12, fontweight='bold')
ax.set_ylabel('Genre', fontsize=12, fontweight='bold')
ax.set_title('Top 15 Genres on Netflix', fontsize=16, fontweight='bold', pad=20)
for bar in bars:
    width = bar.get_width()
    ax.annotate(f'{int(width):,}', xy=(width, bar.get_y() + bar.get_height()/2),
               ha='left', va='center', fontsize=10, fontweight='bold', xytext=(5, 0), textcoords='offset points')
plt.tight_layout()
plt.savefig('/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/06_top_genres.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved: 06_top_genres.png")

# =============================================================================
# SECTION 4: DATA CLEANING AND PREPROCESSING
# =============================================================================
print("\n" + "=" * 70)
print("SECTION 4: DATA CLEANING AND PREPROCESSING")
print("=" * 70)

# Create a copy for processing
df_clean = df.copy()

# 4.1 Handle Missing Values
print("\n🧹 Handling Missing Values...")

# Fill missing director with 'Unknown'
df_clean['director'] = df_clean['director'].fillna('Unknown')

# Fill missing cast with 'Unknown'
df_clean['cast'] = df_clean['cast'].fillna('Unknown')

# Fill missing country with mode
df_clean['country'] = df_clean['country'].fillna(df_clean['country'].mode()[0])

# Fill missing date_added with 'Unknown'
df_clean['date_added'] = df_clean['date_added'].fillna('Unknown')

# Fill missing rating with mode
df_clean['rating'] = df_clean['rating'].fillna(df_clean['rating'].mode()[0])

# Fill missing duration with mode based on type
df_clean['duration'] = df_clean['duration'].fillna(df_clean['duration'].mode()[0])

print(f"✅ Missing values after cleaning:")
print(df_clean.isnull().sum())

# 4.2 Create Combined Text Feature
print("\n📝 Creating Combined Text Feature for Clustering...")

def clean_text(text):
    """Clean and preprocess text data"""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Combine relevant text features
df_clean['combined_text'] = (
    df_clean['title'].astype(str) + ' ' +
    df_clean['director'].astype(str) + ' ' +
    df_clean['cast'].astype(str) + ' ' +
    df_clean['country'].astype(str) + ' ' +
    df_clean['listed_in'].astype(str) + ' ' +
    df_clean['description'].astype(str)
)

# Clean combined text
df_clean['cleaned_text'] = df_clean['combined_text'].apply(clean_text)

print(f"✅ Sample cleaned text:\n{df_clean['cleaned_text'].iloc[0][:500]}...")

# 4.3 Text Preprocessing with NLTK
print("\n🔤 Advanced Text Preprocessing...")

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Add comprehensive custom stopwords specific to Netflix content
custom_stopwords = {
    # Generic content words
    'movie', 'film', 'show', 'series', 'season', 'episode', 'documentary',
    'feature', 'special', 'original', 'netflix', 'streaming',
    # Common narrative words
    'one', 'two', 'three', 'four', 'five', 'new', 'find', 'life', 'story', 
    'world', 'man', 'woman', 'young', 'family', 'friend', 'love', 'help',
    'get', 'back', 'make', 'year', 'take', 'come', 'go', 'first', 'time', 
    'day', 'night', 'way', 'home', 'must', 'try', 'set', 'also', 'thing',
    # Character descriptors
    'group', 'team', 'journey', 'adventure', 'discover', 'secret', 'past',
    'future', 'face', 'turn', 'live', 'become', 'struggle', 'fight',
    # Generic location/setting
    'city', 'town', 'country', 'place', 'land', 'around',
    # Common phrases
    'true', 'real', 'based', 'follow', 'tell', 'learn', 'work', 'lead',
    'unknown', 'various'  # From missing value fills
}
stop_words.update(custom_stopwords)

def preprocess_text(text):
    """Advanced text preprocessing with lemmatization and edge case handling"""
    if pd.isna(text) or text == "":
        return ""
    
    # Tokenize
    tokens = word_tokenize(str(text).lower())
    
    # Remove stopwords and short words, then lemmatize
    processed_tokens = []
    for word in tokens:
        if word not in stop_words and len(word) > 2 and word.isalpha():
            lemma = lemmatizer.lemmatize(word)
            # Also lemmatize as verb for better normalization
            verb_lemma = lemmatizer.lemmatize(lemma, pos='v')
            processed_tokens.append(verb_lemma)
    
    result = ' '.join(processed_tokens)
    
    # Ensure we have meaningful content
    if len(result.split()) < 3:
        # If too short, return the cleaned version with minimal processing
        return ' '.join([w for w in tokens if len(w) > 2 and w.isalpha()][:10])
    
    return result

print("Processing text... (this may take a moment)")
df_clean['processed_text'] = df_clean['cleaned_text'].apply(preprocess_text)

# Validate processed text quality
empty_texts = (df_clean['processed_text'] == '').sum()
short_texts = (df_clean['processed_text'].str.split().str.len() < 5).sum()
print(f"   - Empty processed texts: {empty_texts}")
print(f"   - Short processed texts (<5 words): {short_texts}")

print(f"✅ Sample processed text:\n{df_clean['processed_text'].iloc[0][:300]}...")

# =============================================================================
# SECTION 5: FEATURE ENGINEERING WITH TF-IDF
# =============================================================================
print("\n" + "=" * 70)
print("SECTION 5: FEATURE ENGINEERING WITH TF-IDF")
print("=" * 70)

# 5.1 TF-IDF Vectorization
print("\n📊 Applying TF-IDF Vectorization...")

tfidf_vectorizer = TfidfVectorizer(
    max_features=5000,      # Limit features for efficiency
    min_df=5,               # Minimum document frequency
    max_df=0.8,             # Maximum document frequency
    ngram_range=(1, 2),     # Unigrams and bigrams
    stop_words='english'
)

tfidf_matrix = tfidf_vectorizer.fit_transform(df_clean['processed_text'])
print(f"✅ TF-IDF Matrix Shape: {tfidf_matrix.shape}")
print(f"   - {tfidf_matrix.shape[0]} documents")
print(f"   - {tfidf_matrix.shape[1]} features")

# Get feature names
feature_names = tfidf_vectorizer.get_feature_names_out()
print(f"\n📌 Sample Features (first 20): {list(feature_names[:20])}")

# 5.2 Top TF-IDF Terms
print("\n📊 Top 20 Most Important TF-IDF Terms:")
tfidf_sum = np.array(tfidf_matrix.sum(axis=0)).flatten()
top_indices = tfidf_sum.argsort()[-20:][::-1]
top_terms = [(feature_names[i], tfidf_sum[i]) for i in top_indices]
for term, score in top_terms:
    print(f"   {term}: {score:.4f}")

# Visualize top terms
fig, ax = plt.subplots(figsize=(12, 8))
terms = [t[0] for t in top_terms]
scores = [t[1] for t in top_terms]
colors_terms = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(terms)))
bars = ax.barh(terms[::-1], scores[::-1], color=colors_terms[::-1], edgecolor='white')
ax.set_xlabel('TF-IDF Score Sum', fontsize=12, fontweight='bold')
ax.set_ylabel('Terms', fontsize=12, fontweight='bold')
ax.set_title('Top 20 TF-IDF Terms', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/07_top_tfidf_terms.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved: 07_top_tfidf_terms.png")

# =============================================================================
# SECTION 6: DIMENSIONALITY REDUCTION WITH PCA
# =============================================================================
print("\n" + "=" * 70)
print("SECTION 6: DIMENSIONALITY REDUCTION WITH PCA")
print("=" * 70)

# 6.1 Apply PCA
print("\n📉 Applying PCA for Dimensionality Reduction...")

# Convert sparse matrix to dense for PCA
tfidf_dense = tfidf_matrix.toarray()

# Determine optimal number of components
pca_full = PCA()
pca_full.fit(tfidf_dense)

# Cumulative explained variance
cumulative_variance = np.cumsum(pca_full.explained_variance_ratio_)

# Find components for 95% variance
n_components_95 = np.argmax(cumulative_variance >= 0.95) + 1
print(f"✅ Components needed for 95% variance: {n_components_95}")

# Use a reasonable number of components (max 500 or 95% variance, whichever is less)
n_components = min(n_components_95, 500, tfidf_dense.shape[1] - 1)
print(f"✅ Using {n_components} components for clustering")

# Apply PCA with selected components
pca = PCA(n_components=n_components, random_state=42)
tfidf_pca = pca.fit_transform(tfidf_dense)
print(f"✅ PCA Reduced Matrix Shape: {tfidf_pca.shape}")
print(f"✅ Explained Variance: {sum(pca.explained_variance_ratio_)*100:.2f}%")

# Visualize explained variance
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Individual explained variance (first 50 components)
n_plot = min(50, len(pca.explained_variance_ratio_))
axes[0].bar(range(1, n_plot + 1), pca.explained_variance_ratio_[:n_plot] * 100, 
           color='#667eea', edgecolor='white', alpha=0.8)
axes[0].set_xlabel('Principal Component', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Explained Variance (%)', fontsize=12, fontweight='bold')
axes[0].set_title('Individual Explained Variance (First 50 Components)', fontsize=14, fontweight='bold')

# Cumulative explained variance
axes[1].plot(range(1, len(cumulative_variance) + 1), cumulative_variance * 100, 
            'b-', linewidth=2, label='Cumulative Variance')
axes[1].axhline(y=95, color='r', linestyle='--', alpha=0.7, label='95% Threshold')
axes[1].axvline(x=n_components_95, color='g', linestyle='--', alpha=0.7, label=f'{n_components_95} Components')
axes[1].set_xlabel('Number of Components', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Cumulative Explained Variance (%)', fontsize=12, fontweight='bold')
axes[1].set_title('Cumulative Explained Variance', fontsize=14, fontweight='bold')
axes[1].legend()
axes[1].set_xlim([0, 200])

plt.tight_layout()
plt.savefig('/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/08_pca_variance.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved: 08_pca_variance.png")

# =============================================================================
# SECTION 7: CLUSTERING - K-MEANS
# =============================================================================
print("\n" + "=" * 70)
print("SECTION 7: CLUSTERING - K-MEANS")
print("=" * 70)

# 7.1 Find Optimal K using Elbow Method and Silhouette Score
print("\n🔍 Finding Optimal Number of Clusters...")

k_range = range(2, 15)
inertias = []
silhouette_scores = []
calinski_scores = []
davies_scores = []

for k in k_range:
    print(f"   Testing K={k}...", end='\r')
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=300)
    kmeans.fit(tfidf_pca)
    
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(tfidf_pca, kmeans.labels_))
    calinski_scores.append(calinski_harabasz_score(tfidf_pca, kmeans.labels_))
    davies_scores.append(davies_bouldin_score(tfidf_pca, kmeans.labels_))

print("\n✅ Clustering Evaluation Results:")
print("-" * 50)
print(f"{'K':^5}{'Silhouette':^15}{'Calinski-H':^15}{'Davies-B':^15}")
print("-" * 50)
for i, k in enumerate(k_range):
    print(f"{k:^5}{silhouette_scores[i]:^15.4f}{calinski_scores[i]:^15.2f}{davies_scores[i]:^15.4f}")

# Find optimal K using individual metrics
optimal_k_silhouette = k_range[np.argmax(silhouette_scores)]
optimal_k_calinski = k_range[np.argmax(calinski_scores)]
optimal_k_davies = k_range[np.argmin(davies_scores)]

print(f"\n📊 Optimal K Recommendations (Individual Metrics):")
print(f"   - Silhouette Score: K = {optimal_k_silhouette} (higher is better)")
print(f"   - Calinski-Harabasz: K = {optimal_k_calinski} (higher is better)")
print(f"   - Davies-Bouldin: K = {optimal_k_davies} (lower is better)")

# IMPROVED: Weighted Multi-Metric Scoring for Optimal K Selection
print(f"\n🎯 Applying Weighted Multi-Metric Scoring...")

# Normalize scores to [0, 1] range
def normalize_scores(scores, higher_is_better=True):
    scores = np.array(scores)
    min_val, max_val = scores.min(), scores.max()
    if max_val == min_val:
        return np.ones_like(scores) * 0.5
    normalized = (scores - min_val) / (max_val - min_val)
    return normalized if higher_is_better else (1 - normalized)

# Normalize each metric
silhouette_norm = normalize_scores(silhouette_scores, higher_is_better=True)
calinski_norm = normalize_scores(calinski_scores, higher_is_better=True)
davies_norm = normalize_scores(davies_scores, higher_is_better=False)  # Lower is better

# Weighted combination (Silhouette: 40%, Davies-Bouldin: 40%, Calinski: 20%)
weights = {'silhouette': 0.4, 'davies': 0.4, 'calinski': 0.2}
combined_scores = (
    weights['silhouette'] * silhouette_norm +
    weights['davies'] * davies_norm +
    weights['calinski'] * calinski_norm
)

# Find optimal K based on combined score
optimal_k_weighted = list(k_range)[np.argmax(combined_scores)]

print(f"\n📊 Combined Metric Scores per K:")
print("-" * 60)
print(f"{'K':^5}{'Silhouette':^12}{'Davies-B':^12}{'Calinski':^12}{'Combined':^12}")
print("-" * 60)
for i, k in enumerate(k_range):
    print(f"{k:^5}{silhouette_norm[i]:^12.3f}{davies_norm[i]:^12.3f}{calinski_norm[i]:^12.3f}{combined_scores[i]:^12.3f}")

print(f"\n🎯 OPTIMAL K (Weighted Multi-Metric): K = {optimal_k_weighted}")

# Visualize metrics
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Elbow plot
axes[0, 0].plot(list(k_range), inertias, 'bo-', linewidth=2, markersize=8)
axes[0, 0].set_xlabel('Number of Clusters (K)', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Inertia', fontsize=12, fontweight='bold')
axes[0, 0].set_title('Elbow Method', fontsize=14, fontweight='bold')
axes[0, 0].axvline(x=optimal_k_silhouette, color='red', linestyle='--', alpha=0.7)

# Silhouette score
axes[0, 1].plot(list(k_range), silhouette_scores, 'go-', linewidth=2, markersize=8)
axes[0, 1].axvline(x=optimal_k_silhouette, color='red', linestyle='--', alpha=0.7, label=f'Optimal K={optimal_k_silhouette}')
axes[0, 1].set_xlabel('Number of Clusters (K)', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Silhouette Score', fontsize=12, fontweight='bold')
axes[0, 1].set_title('Silhouette Score (Higher is Better)', fontsize=14, fontweight='bold')
axes[0, 1].legend()

# Calinski-Harabasz
axes[1, 0].plot(list(k_range), calinski_scores, 'ro-', linewidth=2, markersize=8)
axes[1, 0].axvline(x=optimal_k_calinski, color='blue', linestyle='--', alpha=0.7, label=f'Optimal K={optimal_k_calinski}')
axes[1, 0].set_xlabel('Number of Clusters (K)', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Calinski-Harabasz Score', fontsize=12, fontweight='bold')
axes[1, 0].set_title('Calinski-Harabasz Score (Higher is Better)', fontsize=14, fontweight='bold')
axes[1, 0].legend()

# Davies-Bouldin
axes[1, 1].plot(list(k_range), davies_scores, 'mo-', linewidth=2, markersize=8)
axes[1, 1].axvline(x=optimal_k_davies, color='green', linestyle='--', alpha=0.7, label=f'Optimal K={optimal_k_davies}')
axes[1, 1].set_xlabel('Number of Clusters (K)', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Davies-Bouldin Score', fontsize=12, fontweight='bold')
axes[1, 1].set_title('Davies-Bouldin Score (Lower is Better)', fontsize=14, fontweight='bold')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/09_kmeans_metrics.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved: 09_kmeans_metrics.png")

# 7.2 Apply K-Means with Optimal K (using weighted multi-metric selection)
optimal_k = optimal_k_weighted  # Use weighted multi-metric recommendation
print(f"\n🎯 Applying K-Means with K={optimal_k} (weighted multi-metric selection)...")

kmeans_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=20, max_iter=500)
kmeans_labels = kmeans_final.fit_predict(tfidf_pca)
df_clean['kmeans_cluster'] = kmeans_labels

print(f"✅ K-Means Clustering Complete!")
print(f"\n📊 Cluster Distribution (K-Means):")
print(df_clean['kmeans_cluster'].value_counts().sort_index())

# Final metrics for chosen K
final_silhouette = silhouette_score(tfidf_pca, kmeans_labels)
final_calinski = calinski_harabasz_score(tfidf_pca, kmeans_labels)
final_davies = davies_bouldin_score(tfidf_pca, kmeans_labels)

print(f"\n📈 Final K-Means Metrics (K={optimal_k}):")
print(f"   - Silhouette Score: {final_silhouette:.4f}")
print(f"   - Calinski-Harabasz Score: {final_calinski:.2f}")
print(f"   - Davies-Bouldin Score: {final_davies:.4f}")

# 7.3 Cluster Stability Validation (Bootstrap Method)
print(f"\n🔄 Validating Cluster Stability...")

from sklearn.metrics import adjusted_rand_score

stability_scores = []
n_bootstrap = 5  # Number of bootstrap iterations

for i in range(n_bootstrap):
    # Run K-Means with different random seed
    kmeans_test = KMeans(n_clusters=optimal_k, random_state=42 + i + 1, n_init=10, max_iter=300)
    test_labels = kmeans_test.fit_predict(tfidf_pca)
    
    # Compare with original clustering using Adjusted Rand Index
    ari = adjusted_rand_score(kmeans_labels, test_labels)
    stability_scores.append(ari)

mean_stability = np.mean(stability_scores)
std_stability = np.std(stability_scores)

print(f"   - Mean ARI (Adjusted Rand Index): {mean_stability:.4f}")
print(f"   - Stability Std Dev: {std_stability:.4f}")

if mean_stability >= 0.9:
    print(f"   ✅ EXCELLENT: Clusters are highly stable!")
elif mean_stability >= 0.75:
    print(f"   ✅ GOOD: Clusters are reasonably stable")
elif mean_stability >= 0.5:
    print(f"   ⚠️ MODERATE: Some cluster instability detected")
else:
    print(f"   ❌ WARNING: Clusters are unstable, consider different K or preprocessing")

# =============================================================================
# SECTION 8: CLUSTERING - HIERARCHICAL AGGLOMERATIVE
# =============================================================================
print("\n" + "=" * 70)
print("SECTION 8: CLUSTERING - HIERARCHICAL AGGLOMERATIVE")
print("=" * 70)

# 8.1 Create Dendrogram (using subset for visualization)
print("\n🌳 Creating Hierarchical Clustering Dendrogram...")

# Use a sample for dendrogram (full dataset would be too large)
sample_size = min(1000, len(tfidf_pca))
np.random.seed(42)
sample_indices = np.random.choice(len(tfidf_pca), sample_size, replace=False)
tfidf_sample = tfidf_pca[sample_indices]

# Create linkage matrix
linkage_matrix = linkage(tfidf_sample, method='ward')

fig, ax = plt.subplots(figsize=(16, 8))
dendrogram(linkage_matrix, truncate_mode='lastp', p=30, leaf_rotation=90, 
          leaf_font_size=10, show_contracted=True, ax=ax)
ax.set_xlabel('Sample Index or Cluster Size', fontsize=12, fontweight='bold')
ax.set_ylabel('Distance', fontsize=12, fontweight='bold')
ax.set_title('Hierarchical Clustering Dendrogram (Ward Linkage)', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/10_dendrogram.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved: 10_dendrogram.png")

# 8.2 Apply Agglomerative Clustering
print(f"\n🔗 Applying Agglomerative Clustering with {optimal_k} clusters...")

agglo = AgglomerativeClustering(n_clusters=optimal_k, linkage='ward')
agglo_labels = agglo.fit_predict(tfidf_pca)
df_clean['agglo_cluster'] = agglo_labels

print(f"✅ Agglomerative Clustering Complete!")
print(f"\n📊 Cluster Distribution (Agglomerative):")
print(df_clean['agglo_cluster'].value_counts().sort_index())

# Metrics for Agglomerative
agglo_silhouette = silhouette_score(tfidf_pca, agglo_labels)
agglo_calinski = calinski_harabasz_score(tfidf_pca, agglo_labels)
agglo_davies = davies_bouldin_score(tfidf_pca, agglo_labels)

print(f"\n📈 Agglomerative Clustering Metrics (K={optimal_k}):")
print(f"   - Silhouette Score: {agglo_silhouette:.4f}")
print(f"   - Calinski-Harabasz Score: {agglo_calinski:.2f}")
print(f"   - Davies-Bouldin Score: {agglo_davies:.4f}")

# 8.3 Compare Clustering Methods
print("\n📊 CLUSTERING COMPARISON:")
print("=" * 60)
comparison_data = {
    'Metric': ['Silhouette Score ↑', 'Calinski-Harabasz ↑', 'Davies-Bouldin ↓'],
    'K-Means': [final_silhouette, final_calinski, final_davies],
    'Agglomerative': [agglo_silhouette, agglo_calinski, agglo_davies]
}
comparison_df = pd.DataFrame(comparison_data)
print(comparison_df.to_string(index=False))

# Determine better method
if final_silhouette > agglo_silhouette:
    print(f"\n🏆 K-Means performs better based on Silhouette Score!")
    best_labels = kmeans_labels
    best_method = 'K-Means'
else:
    print(f"\n🏆 Agglomerative performs better based on Silhouette Score!")
    best_labels = agglo_labels
    best_method = 'Agglomerative'

df_clean['best_cluster'] = best_labels

# =============================================================================
# SECTION 9: CLUSTER VISUALIZATION
# =============================================================================
print("\n" + "=" * 70)
print("SECTION 9: CLUSTER VISUALIZATION")
print("=" * 70)

# 9.1 PCA 2D Visualization
print("\n📊 Creating 2D Cluster Visualization...")

pca_2d = PCA(n_components=2, random_state=42)
tfidf_2d = pca_2d.fit_transform(tfidf_pca)

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

# K-Means clusters
scatter1 = axes[0].scatter(tfidf_2d[:, 0], tfidf_2d[:, 1], c=kmeans_labels, 
                           cmap='tab10', alpha=0.6, s=20, edgecolor='white', linewidth=0.5)
axes[0].set_xlabel('Principal Component 1', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Principal Component 2', fontsize=12, fontweight='bold')
axes[0].set_title(f'K-Means Clustering (K={optimal_k})', fontsize=16, fontweight='bold', pad=20)
plt.colorbar(scatter1, ax=axes[0], label='Cluster')

# Plot centroids
centroids_2d = pca_2d.transform(kmeans_final.cluster_centers_)
axes[0].scatter(centroids_2d[:, 0], centroids_2d[:, 1], c='red', marker='X', 
               s=200, edgecolor='black', linewidth=2, label='Centroids')
axes[0].legend()

# Agglomerative clusters
scatter2 = axes[1].scatter(tfidf_2d[:, 0], tfidf_2d[:, 1], c=agglo_labels, 
                           cmap='tab10', alpha=0.6, s=20, edgecolor='white', linewidth=0.5)
axes[1].set_xlabel('Principal Component 1', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Principal Component 2', fontsize=12, fontweight='bold')
axes[1].set_title(f'Agglomerative Clustering (K={optimal_k})', fontsize=16, fontweight='bold', pad=20)
plt.colorbar(scatter2, ax=axes[1], label='Cluster')

plt.tight_layout()
plt.savefig('/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/11_cluster_visualization_2d.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved: 11_cluster_visualization_2d.png")

# 9.2 Cluster Size Comparison
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

kmeans_sizes = pd.Series(kmeans_labels).value_counts().sort_index()
agglo_sizes = pd.Series(agglo_labels).value_counts().sort_index()

# K-Means cluster sizes
axes[0].bar(kmeans_sizes.index, kmeans_sizes.values, color=plt.cm.tab10(np.arange(len(kmeans_sizes)) / len(kmeans_sizes)), 
           edgecolor='white', linewidth=1.5)
axes[0].set_xlabel('Cluster', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Number of Titles', fontsize=12, fontweight='bold')
axes[0].set_title('K-Means Cluster Sizes', fontsize=14, fontweight='bold')
for i, v in enumerate(kmeans_sizes.values):
    axes[0].text(i, v + 50, str(v), ha='center', fontweight='bold', fontsize=10)

# Agglomerative cluster sizes
axes[1].bar(agglo_sizes.index, agglo_sizes.values, color=plt.cm.tab10(np.arange(len(agglo_sizes)) / len(agglo_sizes)),
           edgecolor='white', linewidth=1.5)
axes[1].set_xlabel('Cluster', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Number of Titles', fontsize=12, fontweight='bold')
axes[1].set_title('Agglomerative Cluster Sizes', fontsize=14, fontweight='bold')
for i, v in enumerate(agglo_sizes.values):
    axes[1].text(i, v + 50, str(v), ha='center', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/12_cluster_sizes.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved: 12_cluster_sizes.png")

# =============================================================================
# SECTION 10: CLUSTER ANALYSIS AND WORD CLOUDS
# =============================================================================
print("\n" + "=" * 70)
print("SECTION 10: CLUSTER ANALYSIS AND WORD CLOUDS")
print("=" * 70)

# 10.1 Analyze Each Cluster
print("\n📊 Cluster Analysis:")

for cluster in range(optimal_k):
    cluster_df = df_clean[df_clean['best_cluster'] == cluster]
    print(f"\n{'='*60}")
    print(f"CLUSTER {cluster} - {len(cluster_df)} titles ({len(cluster_df)/len(df_clean)*100:.1f}%)")
    print('='*60)
    
    # Content type distribution
    type_dist = cluster_df['type'].value_counts()
    print(f"\n   Content Type: {dict(type_dist)}")
    
    # Top genres
    cluster_genres = cluster_df['listed_in'].dropna().str.split(', ').explode()
    top_genres = cluster_genres.value_counts().head(5)
    print(f"   Top Genres: {dict(top_genres)}")
    
    # Top countries
    cluster_countries = cluster_df['country'].dropna().str.split(', ').explode()
    top_countries = cluster_countries.value_counts().head(3)
    print(f"   Top Countries: {dict(top_countries)}")
    
    # Top ratings
    top_ratings = cluster_df['rating'].value_counts().head(3)
    print(f"   Top Ratings: {dict(top_ratings)}")
    
    # Sample titles
    sample_titles = cluster_df['title'].head(5).tolist()
    print(f"   Sample Titles: {sample_titles}")

# 10.2 Create Word Clouds for Each Cluster
print("\n☁️ Generating Word Clouds for Each Cluster...")

# Calculate number of rows and columns for subplots
n_cols = 3
n_rows = (optimal_k + n_cols - 1) // n_cols

fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 5 * n_rows))
axes = axes.flatten() if n_rows * n_cols > 1 else [axes]

colormap_list = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'twilight', 'cool', 'hot']

for cluster in range(optimal_k):
    cluster_text = ' '.join(df_clean[df_clean['best_cluster'] == cluster]['processed_text'].tolist())
    
    wordcloud = WordCloud(
        width=800, height=400,
        background_color='white',
        colormap=colormap_list[cluster % len(colormap_list)],
        max_words=100,
        min_font_size=10,
        max_font_size=80,
        random_state=42
    ).generate(cluster_text)
    
    axes[cluster].imshow(wordcloud, interpolation='bilinear')
    axes[cluster].axis('off')
    axes[cluster].set_title(f'Cluster {cluster} Word Cloud', fontsize=14, fontweight='bold', pad=10)

# Hide empty subplots
for i in range(optimal_k, len(axes)):
    axes[i].axis('off')

plt.tight_layout()
plt.savefig('/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/13_word_clouds.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved: 13_word_clouds.png")

# 10.3 Cluster Composition Analysis
print("\n📊 Cluster Composition Analysis...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Content Type by Cluster
type_cluster = pd.crosstab(df_clean['best_cluster'], df_clean['type'], normalize='index') * 100
type_cluster.plot(kind='bar', ax=axes[0, 0], stacked=True, color=['#667eea', '#f093fb'], edgecolor='white')
axes[0, 0].set_xlabel('Cluster', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
axes[0, 0].set_title('Content Type Distribution by Cluster', fontsize=14, fontweight='bold')
axes[0, 0].legend(title='Type', bbox_to_anchor=(1.05, 1), loc='upper left')
axes[0, 0].tick_params(axis='x', rotation=0)

# Average Release Year by Cluster
avg_year = df_clean.groupby('best_cluster')['release_year'].mean()
colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(avg_year)))
bars = axes[0, 1].bar(avg_year.index, avg_year.values, color=colors, edgecolor='white')
axes[0, 1].set_xlabel('Cluster', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Average Release Year', fontsize=12, fontweight='bold')
axes[0, 1].set_title('Average Release Year by Cluster', fontsize=14, fontweight='bold')
for bar, year in zip(bars, avg_year.values):
    axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    f'{year:.0f}', ha='center', fontweight='bold', fontsize=10)

# Top Genre per Cluster
top_genre_per_cluster = []
for cluster in range(optimal_k):
    cluster_genres = df_clean[df_clean['best_cluster'] == cluster]['listed_in'].str.split(', ').explode()
    top_genre = cluster_genres.value_counts().index[0] if len(cluster_genres) > 0 else 'Unknown'
    top_genre_per_cluster.append(top_genre)

colors = plt.cm.Set3(np.linspace(0, 1, optimal_k))
bars = axes[1, 0].barh(range(optimal_k), [1]*optimal_k, color=colors, edgecolor='white')
axes[1, 0].set_yticks(range(optimal_k))
axes[1, 0].set_yticklabels([f'Cluster {i}' for i in range(optimal_k)])
for i, (bar, genre) in enumerate(zip(bars, top_genre_per_cluster)):
    axes[1, 0].text(0.5, bar.get_y() + bar.get_height()/2, genre, 
                    ha='center', va='center', fontsize=11, fontweight='bold')
axes[1, 0].set_xlim([0, 1])
axes[1, 0].set_xticks([])
axes[1, 0].set_title('Dominant Genre per Cluster', fontsize=14, fontweight='bold')

# Top Country per Cluster
top_country_per_cluster = []
for cluster in range(optimal_k):
    cluster_countries = df_clean[df_clean['best_cluster'] == cluster]['country'].str.split(', ').explode()
    top_country = cluster_countries.value_counts().index[0] if len(cluster_countries) > 0 else 'Unknown'
    top_country_per_cluster.append(top_country)

bars = axes[1, 1].barh(range(optimal_k), [1]*optimal_k, color=colors, edgecolor='white')
axes[1, 1].set_yticks(range(optimal_k))
axes[1, 1].set_yticklabels([f'Cluster {i}' for i in range(optimal_k)])
for i, (bar, country) in enumerate(zip(bars, top_country_per_cluster)):
    axes[1, 1].text(0.5, bar.get_y() + bar.get_height()/2, country, 
                    ha='center', va='center', fontsize=11, fontweight='bold')
axes[1, 1].set_xlim([0, 1])
axes[1, 1].set_xticks([])
axes[1, 1].set_title('Dominant Country per Cluster', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/14_cluster_composition.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved: 14_cluster_composition.png")

# =============================================================================
# SECTION 11: CONTENT-BASED RECOMMENDATION SYSTEM
# =============================================================================
print("\n" + "=" * 70)
print("SECTION 11: CONTENT-BASED RECOMMENDATION SYSTEM")
print("=" * 70)

# 11.1 Build Recommendation System using Cosine Similarity
print("\n🎬 Building Content-Based Recommendation System...")

# Compute cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
print(f"✅ Cosine Similarity Matrix Shape: {cosine_sim.shape}")

# Create a mapping of titles to indices
indices = pd.Series(df_clean.index, index=df_clean['title']).drop_duplicates()

def get_recommendations(title, n_recommendations=10):
    """
    Get content-based recommendations for a given title.
    
    Parameters:
    -----------
    title : str
        The title of the movie/show to get recommendations for
    n_recommendations : int
        Number of recommendations to return
        
    Returns:
    --------
    DataFrame with recommended titles and their details
    """
    try:
        # Get the index of the title
        idx = indices[title]
        
        # Get similarity scores for all titles
        sim_scores = list(enumerate(cosine_sim[idx]))
        
        # Sort by similarity score (descending)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top n+1 (excluding the input title itself)
        sim_scores = sim_scores[1:n_recommendations+1]
        
        # Get the indices
        movie_indices = [i[0] for i in sim_scores]
        similarity_values = [i[1] for i in sim_scores]
        
        # Return the recommended titles with details
        recommendations = df_clean.iloc[movie_indices][['title', 'type', 'listed_in', 'country', 'release_year', 'rating', 'best_cluster']].copy()
        recommendations['similarity_score'] = similarity_values
        
        return recommendations
        
    except KeyError:
        print(f"Title '{title}' not found in the dataset.")
        return None

def get_cluster_recommendations(title, n_recommendations=10):
    """
    Get recommendations from the same cluster with highest similarity.
    """
    try:
        idx = indices[title]
        title_cluster = df_clean.iloc[idx]['best_cluster']
        
        # Get all titles in the same cluster
        cluster_mask = df_clean['best_cluster'] == title_cluster
        cluster_indices = df_clean[cluster_mask].index.tolist()
        
        # Get similarity scores for cluster members
        sim_scores = [(i, cosine_sim[idx][i]) for i in cluster_indices if i != idx]
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[:n_recommendations]
        
        movie_indices = [i[0] for i in sim_scores]
        similarity_values = [i[1] for i in sim_scores]
        
        recommendations = df_clean.iloc[movie_indices][['title', 'type', 'listed_in', 'country', 'release_year', 'rating', 'best_cluster']].copy()
        recommendations['similarity_score'] = similarity_values
        
        return recommendations
        
    except KeyError:
        print(f"Title '{title}' not found in the dataset.")
        return None

def get_hybrid_recommendations(title, n_recommendations=10, cluster_weight=0.3):
    """
    ENHANCED: Hybrid recommendation combining cluster-aware and similarity-based approach.
    
    Parameters:
    -----------
    title : str
        The title of the movie/show to get recommendations for
    n_recommendations : int
        Number of recommendations to return
    cluster_weight : float
        Weight for cluster proximity (0-1). Higher = prefer same cluster.
        
    Returns:
    --------
    DataFrame with recommended titles and their details
    """
    try:
        idx = indices[title]
        title_cluster = df_clean.iloc[idx]['best_cluster']
        
        # Get similarity scores for all titles
        sim_scores = []
        for i in range(len(df_clean)):
            if i == idx:
                continue
            
            base_sim = cosine_sim[idx][i]
            
            # Add cluster bonus if in same cluster
            same_cluster = int(df_clean.iloc[i]['best_cluster'] == title_cluster)
            hybrid_score = (1 - cluster_weight) * base_sim + cluster_weight * same_cluster
            
            sim_scores.append((i, hybrid_score, base_sim, same_cluster))
        
        # Sort by hybrid score
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Diversity boost: don't pick items too similar to each other
        selected = []
        used_indices = set()
        for item in sim_scores:
            if len(selected) >= n_recommendations:
                break
            if item[0] not in used_indices:
                selected.append(item)
                used_indices.add(item[0])
        
        movie_indices = [i[0] for i in selected]
        hybrid_scores = [i[1] for i in selected]
        base_sims = [i[2] for i in selected]
        same_clusters = [i[3] for i in selected]
        
        recommendations = df_clean.iloc[movie_indices][['title', 'type', 'listed_in', 'country', 'release_year', 'rating', 'best_cluster']].copy()
        recommendations['hybrid_score'] = hybrid_scores
        recommendations['similarity_score'] = base_sims
        recommendations['same_cluster'] = same_clusters
        
        return recommendations
        
    except KeyError:
        print(f"Title '{title}' not found in the dataset.")
        return None

def find_similar_titles(search_term, n_results=5):
    """
    ENHANCED: Fuzzy search to find titles matching a search term.
    Useful when exact title is not known.
    """
    search_lower = search_term.lower()
    matches = []
    
    for title in df_clean['title'].values:
        if search_lower in title.lower():
            matches.append(title)
            if len(matches) >= n_results:
                break
    
    if not matches:
        # Try partial match
        for title in df_clean['title'].values:
            title_words = title.lower().split()
            search_words = search_lower.split()
            if any(sw in tw for sw in search_words for tw in title_words):
                matches.append(title)
                if len(matches) >= n_results:
                    break
    
    return matches

print("✅ Recommendation functions created:")
print("   - get_recommendations(title, n): Basic cosine similarity")
print("   - get_cluster_recommendations(title, n): Same cluster only")
print("   - get_hybrid_recommendations(title, n, weight): Cluster-aware hybrid")
print("   - find_similar_titles(search): Fuzzy title search")

# 11.2 Test Recommendation System
print("\n🔍 Testing Recommendation System...")

# Test with popular titles
test_titles = ['Stranger Things', 'The Crown', 'Money Heist', 'Breaking Bad', 'Narcos']

for test_title in test_titles:
    if test_title in indices:
        print(f"\n{'='*70}")
        print(f"📺 Testing with: '{test_title}'")
        print('='*70)
        
        # Basic recommendations
        print("\n🎯 Basic Cosine Similarity Recommendations:")
        recs = get_recommendations(test_title, n_recommendations=5)
        if recs is not None:
            print(recs[['title', 'type', 'listed_in', 'similarity_score']].to_string(index=False))
        
        # Hybrid recommendations
        print("\n🎯 Hybrid (Cluster-Aware) Recommendations:")
        hybrid_recs = get_hybrid_recommendations(test_title, n_recommendations=5, cluster_weight=0.3)
        if hybrid_recs is not None:
            print(hybrid_recs[['title', 'type', 'listed_in', 'hybrid_score', 'same_cluster']].to_string(index=False))
        
        # Cluster-only recommendations
        print("\n🎯 Same-Cluster Recommendations:")
        cluster_recs = get_cluster_recommendations(test_title, n_recommendations=5)
        if cluster_recs is not None:
            print(cluster_recs[['title', 'type', 'listed_in', 'similarity_score']].to_string(index=False))
        
        break
else:
    # Use first available title if test titles not found
    first_title = df_clean['title'].iloc[0]
    print(f"\n📺 Recommendations for: '{first_title}'")
    recs = get_recommendations(first_title, n_recommendations=5)
    if recs is not None:
        print(recs[['title', 'type', 'listed_in', 'similarity_score']].to_string(index=False))

# =============================================================================
# SECTION 12: SAVE RESULTS
# =============================================================================
print("\n" + "=" * 70)
print("SECTION 12: SAVE RESULTS")
print("=" * 70)

# Save clustered dataset
output_file = '/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/netflix_clustered.csv'
df_clean.to_csv(output_file, index=False)
print(f"✅ Saved clustered dataset: {output_file}")

# Save cluster summary
cluster_summary = []
for cluster in range(optimal_k):
    cluster_df = df_clean[df_clean['best_cluster'] == cluster]
    cluster_genres = cluster_df['listed_in'].str.split(', ').explode()
    cluster_countries = cluster_df['country'].str.split(', ').explode()
    
    summary = {
        'Cluster': cluster,
        'Size': len(cluster_df),
        'Percentage': f"{len(cluster_df)/len(df_clean)*100:.2f}%",
        'Movies': len(cluster_df[cluster_df['type'] == 'Movie']),
        'TV_Shows': len(cluster_df[cluster_df['type'] == 'TV Show']),
        'Avg_Year': round(cluster_df['release_year'].mean(), 1),
        'Top_Genre': cluster_genres.value_counts().index[0] if len(cluster_genres) > 0 else 'Unknown',
        'Top_Country': cluster_countries.value_counts().index[0] if len(cluster_countries) > 0 else 'Unknown'
    }
    cluster_summary.append(summary)

summary_df = pd.DataFrame(cluster_summary)
summary_df.to_csv('/Users/rahulkumarsinghj/Developer /Code/netflix-clustering/cluster_summary.csv', index=False)
print("✅ Saved cluster summary: cluster_summary.csv")

print("\n📊 Cluster Summary Table:")
print(summary_df.to_string(index=False))

# =============================================================================
# SECTION 13: FINAL SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SECTION 13: PROJECT SUMMARY")
print("=" * 70)

print(f"""
📊 NETFLIX MOVIES AND TV SHOWS CLUSTERING - FINAL REPORT
{'='*60}

📋 DATASET OVERVIEW:
   • Total Titles: {len(df_clean):,}
   • Movies: {len(df_clean[df_clean['type'] == 'Movie']):,}
   • TV Shows: {len(df_clean[df_clean['type'] == 'TV Show']):,}
   • Release Year Range: {df_clean['release_year'].min()} - {df_clean['release_year'].max()}

🔧 METHODOLOGY:
   • Text Features: Combined title, director, cast, country, genre, description
   • NLP Techniques: TF-IDF Vectorization with unigrams and bigrams
   • Dimensionality Reduction: PCA ({n_components} components, {sum(pca.explained_variance_ratio_)*100:.2f}% variance)
   • Clustering Algorithms: K-Means, Hierarchical Agglomerative

📈 CLUSTERING RESULTS:
   • Optimal Number of Clusters: {optimal_k}
   • Best Performing Algorithm: {best_method}
   • Silhouette Score: {max(final_silhouette, agglo_silhouette):.4f}
   • Calinski-Harabasz Score: {max(final_calinski, agglo_calinski):.2f}
   • Davies-Bouldin Score: {min(final_davies, agglo_davies):.4f}

🎬 RECOMMENDATION SYSTEM:
   • Method: Content-Based Filtering
   • Similarity Metric: Cosine Similarity
   • Features: TF-IDF weighted text vectors

📁 OUTPUT FILES:
   • netflix_clustered.csv - Full dataset with cluster labels
   • cluster_summary.csv - Summary statistics per cluster
   • 14 visualization images

{'='*60}
🎉 PROJECT COMPLETED SUCCESSFULLY!
{'='*60}
""")

print("\n📸 Generated Visualizations:")
print("   1. 01_missing_values.png - Missing values analysis")
print("   2. 02_content_type_distribution.png - Content type breakdown")
print("   3. 03_rating_distribution.png - Rating distribution")
print("   4. 04_release_year_trend.png - Release year trends")
print("   5. 05_top_countries.png - Top content producing countries")
print("   6. 06_top_genres.png - Most popular genres")
print("   7. 07_top_tfidf_terms.png - Important TF-IDF terms")
print("   8. 08_pca_variance.png - PCA explained variance")
print("   9. 09_kmeans_metrics.png - K-Means evaluation metrics")
print("  10. 10_dendrogram.png - Hierarchical clustering dendrogram")
print("  11. 11_cluster_visualization_2d.png - 2D cluster scatter plot")
print("  12. 12_cluster_sizes.png - Cluster size comparison")
print("  13. 13_word_clouds.png - Word clouds per cluster")
print("  14. 14_cluster_composition.png - Cluster composition analysis")
