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
    "επισης", "ενα", "ολοι", "οποιο", "οποια", "οποιους", "οποιες", "δια", "δυο", "ομως", "πρεπει", "μπορει", "αν", "προεδρε", "μα"
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
    
    # Remove diacritics, convert to lowercase, and tokenize
    text = remove_diacritics(text).lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation and special characters

    # Tokenize the text (split into words)
    words = text.split()

    # Convert verbs to first singular form (after tokenizing)
    words = [convert_to_first_singular(word) for word in words]

    # Remove stop words (after converting verbs)
    cleaned_words = [word for word in words if word not in STOP_WORDS]
    
    return ' '.join(cleaned_words)

if __name__ == "__main__":
    input_file = "medium.csv"
    
    df = pd.read_csv(input_file, encoding='utf-8')
    
    # Clean the 'speech' column and replace the original column with the cleaned content
    if 'speech' in df.columns:
        df['speech'] = df['speech'].apply(clean_text)

    # Save the cleaned data to a new CSV file
    output_file = "final.csv"
    df.to_csv(output_file, index=False)

    print(f"Cleaned data has been saved to {output_file}")

