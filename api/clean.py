import pandas as pd
import re
import unicodedata

# List of common stop words
STOP_WORDS = {
    "ο", "η", "το", "οι", "τα", "του", "τον", "των", "τους", "τη", "την", "της", "αν", "ν", "κ", "τις", "και", "σε", "με", 
    "για", "να", "στο", "στον", "στου", "στη", "στην", "στης", "στα", "στων", "στις", "στες", "κ.", "κα", "που", 
    "τι", "πως", "κι", "μου", "μας", "σου", "σας", "του", "της", "εγω", "εσυ", "αυτος", "αυτη", "αυτο", "αυτον", "αυτου", "μονου",
    "εμεις", "εσεις", "αυτοι", "αυτες", "αυτα", "δικος", "δικη", "δικο", "δικοι", "δικες", "δικα", "απο", "κατα", "μεσω", 
    "μεταξυ", "προς", "διχως", "χωρις", "παρα", "αλλα", "ειτε", "ουτε", "ενω", "αν", "και", "μολις", "επειδη", 
    "διοτι", "κυριος", "κυρια", "κυριε", "κυριοι", "κυριες", "παρακαλω", "εξοχοτατε", "ειναι", "ηταν", "ειμαι", 
    "εισαι", "ειμαστε", "ειστε", "εχει", "ειχαν", "εχω", "εχουμε", "εχουν", "λοιπον", "ακριβως", "βασικα", 
    "εννοειται", "οπως", "δηλαδη", "επι", "ναι", "οχι", "δεν", "δε", "μην", "μη", "οταν", "οπως", "οτι", "κατ", "καν", "εκ",
    "κανεις", "καμια", "κανεναν", "κανενα", "κανενος", "μετα", "τωρα", "θα", "ξανα", "παρ", "α", "ε", "ω", "ολους", "γιατι",
    "επισης", "ενα", "ολοι", "οποιο", "οποια", "οποιους", "οποιες", "δια", "δυο", "ομως", "πρεπει", "μπορει", "αν"
}

def convert_to_first_singular(verb):
    endings_to_replace = ["εις", "ει", "ουμε", "ετε", "ειτε", "ειστε", "ουντε", "ουν", "αμε", "ατε", "αν", "ισε", "εται", 
                          "ουνται", "ειται"]
    first_singular_form = "ω"
    
    for ending in endings_to_replace:
        if verb.endswith(ending):
            return verb[:-len(ending)] + first_singular_form
    return verb

def remove_diacritics(text):
    """Remove Greek diacritics from text."""
    normalized = unicodedata.normalize("NFD", text)
    cleaned = ''.join([char for char in normalized if not unicodedata.combining(char)])
    return cleaned 

def clean_text(text):
    """Clean and normalize Greek text."""
    if pd.isna(text):  # handle NaN values
        return ""
    # remove diacritics, convert to lowercase, and tokenize
    text = remove_diacritics(text).lower()
    # remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)
    # remove stop words
    words = text.split()
    cleaned_words = [convert_to_first_singular(word) for word in words if word not in STOP_WORDS]
    return ' '.join(cleaned_words)

def create_inverted_index(input_file):
    """Create the inverted index and save it to a file."""
    df = pd.read_csv(input_file, encoding="utf-8")
    inverted_index = {}
    
    for index, row in df.iterrows():
        speech = row['speech']
        cleaned_speech = clean_text(speech)
        words = cleaned_speech.split()
        for word in words:
            if word in inverted_index:
                inverted_index[word].append(index)
            else:
                inverted_index[word] = [index]
    
    # Save the inverted index to a file
    with open("inverted_index.txt", "w", encoding="utf-8") as f:
        for word, doc_ids in inverted_index.items():
            f.write(f"{word}:{','.join(map(str, doc_ids))}\n")
    
    print("Inverted index created and saved to 'inverted_index.txt'.")
    return inverted_index

if __name__ == "__main__":
    input_file = "medium.csv"
    inverted_index = create_inverted_index(input_file)

