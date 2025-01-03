import pandas as pd
import sys
import re
import json

def create_inverted_index(input_file):
    inverted_index = {}

    df = pd.read_csv(input_file)

    for idx, row in df.iterrows():
        speech = str(row['speech']).lower()  
        words = re.findall(r'\b\w+\b', speech)  

        for word in words:
            if word not in inverted_index:
                inverted_index[word] = {
                    'frequency': 0,
                    'documents': []
                }
            inverted_index[word]['frequency'] += 1
            inverted_index[word]['documents'].append({
                'speech_id': idx,
                'count_in_speech': words.count(word)
            })
    
    sorted_inverted_index = dict(sorted(inverted_index.items()))

    with open("inverted_index.json", "w", encoding="utf-8") as f:
        json.dump(sorted_inverted_index, f, ensure_ascii=False, indent=4)
    
    print("Inverted index created and saved to 'inverted_index.json'.")
    return sorted_inverted_index

def main():
    if len(sys.argv) != 2:
        print("Usage: python inverted_index.py <input_file.csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    inverted_index = create_inverted_index(input_file)

if __name__ == "__main__":
    main()

