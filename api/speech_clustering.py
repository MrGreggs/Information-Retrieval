import json
import numpy as np
import pandas as pd
import sys
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# load TF-IDF JSON file
with open("tf_idf_speech.json", "r", encoding="utf-8") as f:
    tf_idf_data = json.load(f)

# determine maximum vector size dynamically
MAX_VECTOR_SIZE = max(len(words) for words in tf_idf_data.values())  

# create a feature matrix
speech_vectors = []
speech_ids = []

for speech_id, words in tf_idf_data.items():
    speech_ids.append(speech_id)
    
    # extract TF-IDF values
    tfidf_values = [entry[1] for entry in words]  

    # pad with zeros if necessary
    while len(tfidf_values) < MAX_VECTOR_SIZE:
        tfidf_values.append(0)

    speech_vectors.append(tfidf_values)

# convert to NumPy array
speech_vectors = np.array(speech_vectors, dtype=np.float32)  

# standardize features (helps clustering)
scaler = StandardScaler()
speech_vectors_scaled = scaler.fit_transform(speech_vectors)

# Apply K-Means Clustering
num_clusters = 8  # Adjust as needed
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
clusters = kmeans.fit_predict(speech_vectors_scaled)

# create a DataFrame mapping speeches to clusters
clustered_data = pd.DataFrame({"Speech_ID": speech_ids, "Cluster": clusters})

# group by cluster and save to CSV
grouped_clusters = clustered_data.groupby("Cluster")["Speech_ID"].apply(list).reset_index()
grouped_clusters.to_csv("clustered_speeches.csv", index=False)

# visualize with PCA (reduce to 2D)
pca = PCA(n_components=2)
speech_vectors_pca = pca.fit_transform(speech_vectors_scaled)

plt.scatter(speech_vectors_pca[:, 0], speech_vectors_pca[:, 1], c=clusters, cmap='viridis', alpha=0.7)
plt.title("Speech Clustering (PCA 2D)")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.colorbar(label="Cluster")
plt.show()
