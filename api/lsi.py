import json
import numpy as np
from sklearn.decomposition import TruncatedSVD

with open('tf_idf_speech.json', 'r', encoding='utf-8') as f:
    tf_idf_speech = json.load(f)

# extract terms and documents
terms = set(term for doc_terms in tf_idf_speech.values() for term, score in doc_terms)
term_idx = {term: idx for idx, term in enumerate(terms)}

# create term-document matrix
num_terms = len(term_idx)
num_docs = len(tf_idf_speech)
term_doc_matrix = np.zeros((num_terms, num_docs))

for doc_id, terms_scores in tf_idf_speech.items():
    for term, score in terms_scores:
        term_id = term_idx[term]
        term_doc_matrix[term_id, int(doc_id)] = score

# apply SVD for LSI
num_topics = 100  # Define the number of topics
svd = TruncatedSVD(n_components=num_topics, n_iter=7, random_state=42)
lsa_matrix = svd.fit_transform(term_doc_matrix)

# extract top terms for each topic
top_terms_per_topic = {}
for topic_idx, terms in enumerate(svd.components_):
    top_terms = np.argsort(terms)[-10:]  # Get top 10 terms for each topic
    top_terms_per_topic[topic_idx] = [list(term_idx.keys())[idx] for idx in top_terms]

with open("lsi_topics.json", "w", encoding="utf-8") as f:
    json.dump(top_terms_per_topic, f, ensure_ascii=False, indent=4)

print("LSI topics and top terms saved to lsi_topics.json.")

