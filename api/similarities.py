import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("final.csv")

# ensure 'speech' column contains only strings, replacing NaN with an empty string
df['speech'] = df['speech'].fillna('').astype(str)

# group speeches by party members
mp_speeches = df.groupby('member_name')['speech'].apply(lambda x: ' '.join(x)).reset_index()

# compute TF-IDF vectors 
vectorizer = TfidfVectorizer(max_features=5000)  # Adjust max_features if needed
tfidf_matrix = vectorizer.fit_transform(mp_speeches['speech'])

# create a dataframe for party member TF-IDF vectors
mp_tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), index=mp_speeches['member_name'])

# compute cosine pair similarities
similarity_matrix = cosine_similarity(tfidf_matrix)

# convert similarity matrix to a dataframe
similarity_df = pd.DataFrame(similarity_matrix, index=mp_speeches['member_name'], columns=mp_speeches['member_name'])

# extract top-k similar pairs
similarity_pairs = []

for i, mp1 in enumerate(mp_speeches['member_name']):
    for j, mp2 in enumerate(mp_speeches['member_name']):
        if i < j:  # avoid duplicate pairs
            similarity_pairs.append((mp1, mp2, similarity_matrix[i, j]))

similarity_pairs = sorted(similarity_pairs, key=lambda x: x[2], reverse=True)

k = 30
top_k_pairs = similarity_pairs[:k]

output_df = pd.DataFrame(top_k_pairs, columns=["MP1", "MP2", "Similarity"])
output_df.to_csv("top_k_similar_mps.csv", index=False)
print("Results saved to 'top_k_similar_mps.csv'")

