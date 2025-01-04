import pandas as pd
import math
import json
from collections import defaultdict

def calculate_tf_idf(input_file, inverted_index_file):
    # Load the CSV file and inverted index
    df = pd.read_csv(input_file)
    with open(inverted_index_file, "r", encoding="utf-8") as f:
        inverted_index = json.load(f)

    # Total number of documents (speeches)
    total_documents = len(df)

    # Pre-compute IDF for all terms
    idf = {}
    for term, data in inverted_index.items():
        doc_count = len(data["documents"])
        idf[term] = math.log((total_documents / (1 + doc_count)), 10)  # Add 1 to avoid division by zero

    # Calculate TF-IDF for each speech
    tf_idf = defaultdict(lambda: defaultdict(float))
    for idx, row in df.iterrows():
        speech = str(row['speech']).lower()
        words = speech.split()
        total_terms = len(words)

        # Calculate TF for each term in the speech
        term_frequencies = defaultdict(int)
        for word in words:
            if not word.isnumeric():  # Skip purely numerical strings
                term_frequencies[word] += 1

        # Compute TF-IDF for each term in the speech
        for term, count in term_frequencies.items():
            tf = count / total_terms
            tf_idf[idx][term] = tf * idf.get(term, 0)  # Use IDF if the term exists

    # Aggregate TF-IDF by member and party
    member_keywords = defaultdict(lambda: defaultdict(float))
    party_keywords = defaultdict(lambda: defaultdict(float))
    for idx, row in df.iterrows():
        member = str(row['member_name']).lower()
        party = str(row['political_party']).lower()

        for term, score in tf_idf[idx].items():
            member_keywords[member][term] += score
            party_keywords[party][term] += score

    # Get top keywords for each speech, member, and party
    top_speech_keywords = {idx: sorted(terms.items(), key=lambda x: x[1], reverse=True)[:10] for idx, terms in tf_idf.items()}
    top_member_keywords = {member: sorted(terms.items(), key=lambda x: x[1], reverse=True)[:10] for member, terms in member_keywords.items()}
    top_party_keywords = {party: sorted(terms.items(), key=lambda x: x[1], reverse=True)[:10] for party, terms in party_keywords.items()}

    # Save results
    with open("tf_idf_speech.json", "w", encoding="utf-8") as f:
        json.dump(top_speech_keywords, f, ensure_ascii=False, indent=4)
    with open("tf_idf_member.json", "w", encoding="utf-8") as f:
        json.dump(top_member_keywords, f, ensure_ascii=False, indent=4)
    with open("tf_idf_party.json", "w", encoding="utf-8") as f:
        json.dump(top_party_keywords, f, ensure_ascii=False, indent=4)

    print("TF-IDF calculation completed and saved.")
    return top_speech_keywords, top_member_keywords, top_party_keywords

def main():
    input_file = "final.csv"  
    inverted_index_file = "inverted_index.json"
    calculate_tf_idf(input_file, inverted_index_file)

if __name__ == "__main__":
    main()

