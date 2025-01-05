import pandas as pd
import sys
import re
import json

def is_greek_word(word):
    # regular expression for a Greek word (includes accented characters)
    return bool(re.match(r'^[\u0370-\u03FF\u1F00-\u1FFF]+$', word))

def create_inverted_index(input_file):
    inverted_index = {}

    df = pd.read_csv(input_file)

    for idx, row in df.iterrows():
        speech = str(row['speech']).lower()
        words = re.findall(r'\b\w+\b', speech)

        for word in words:
            if is_greek_word(word):
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
        
        # process the member_name column (as a single entity) and not tokenize it to multiple words
        member_name = str(row['member_name']).lower()
        if is_greek_word(member_name):
            if member_name not in inverted_index:
                inverted_index[member_name] = {
                    'frequency': 0,
                    'documents': []
                }
            inverted_index[member_name]['frequency'] += 1
            inverted_index[member_name]['documents'].append({
                'speech_id': idx,
                'count_in_speech': 1  
            })

        # process the political_party column (as a single entity), same as member_name
        political_party = str(row['political_party']).lower()
        if is_greek_word(political_party):
            if political_party not in inverted_index:
                inverted_index[political_party] = {
                    'frequency': 0,
                    'documents': []
                }
            inverted_index[political_party]['frequency'] += 1
            inverted_index[political_party]['documents'].append({
                'speech_id': idx,
                'count_in_speech': 1  
            })

    sorted_inverted_index = dict(sorted(inverted_index.items()))

    with open("inverted_index.json", "w", encoding="utf-8") as f:
        json.dump(sorted_inverted_index, f, ensure_ascii=False, indent=4)
    
    print("Inverted index created and saved to 'inverted_index.json'.")
    return sorted_inverted_index

def main():
    input_file = "final.csv"
    create_inverted_index(input_file)

if __name__ == "__main__":
    main()

