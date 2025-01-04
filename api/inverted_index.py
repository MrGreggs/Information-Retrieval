import pandas as pd
import sys
import re
import json

def create_inverted_index(input_file):
    inverted_index = {}

    # Read the CSV file
    df = pd.read_csv(input_file)

    for idx, row in df.iterrows():
        # Process the speech column (tokenized into individual words)
        speech = str(row['speech']).lower()
        words = re.findall(r'\b\w+\b', speech)

        # Add words from the speech to the inverted index
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
        
        # Process the member_name column (as a single entity)
        member_name = str(row['member_name']).lower()
        if member_name not in inverted_index:
            inverted_index[member_name] = {
                'frequency': 0,
                'documents': []
            }
        inverted_index[member_name]['frequency'] += 1
        inverted_index[member_name]['documents'].append({
            'speech_id': idx,
            'count_in_speech': 1  # Always 1 since it's not tokenized
        })

        # Process the political_party column (as a single entity)
        political_party = str(row['political_party']).lower()
        if political_party not in inverted_index:
            inverted_index[political_party] = {
                'frequency': 0,
                'documents': []
            }
        inverted_index[political_party]['frequency'] += 1
        inverted_index[political_party]['documents'].append({
            'speech_id': idx,
            'count_in_speech': 1  # Always 1 since it's not tokenized
        })

    # Sort the inverted index alphabetically
    sorted_inverted_index = dict(sorted(inverted_index.items()))

    # Save the inverted index to a JSON file
    with open("inverted_index.json", "w", encoding="utf-8") as f:
        json.dump(sorted_inverted_index, f, ensure_ascii=False, indent=4)
    
    print("Inverted index created and saved to 'inverted_index.json'.")
    return sorted_inverted_index

def main():
    if len(sys.argv) != 2:
        print("Usage: python inverted_index.py <input_file.csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    create_inverted_index(input_file)

if __name__ == "__main__":
    main()
