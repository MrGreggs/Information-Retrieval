import pandas as pd
import unicodedata
import re

# list of common words that should be removed from the text during the preprocessing
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

def preprocess_data(file_path):
    """Load, clean, and preprocess the Greek dataset."""
    # load the CSV file
    df = pd.read_csv(file_path, encoding="utf-8")

    # parse dates to a standard format from DD/MM/YY to YY/MM/DD
    df["sitting_date"] = pd.to_datetime(df["sitting_date"], format="%d/%m/%Y", errors="coerce")

    # Normalize text fields
    text_columns = [
        "member_name",
        "parliamentary_period",
        "parliamentary_session",
        "parliamentary_sitting",
        "political_party",
        "government",
        "member_region",
        "roles",
        "speech"
    ]
    for col in text_columns:
        df[col] = df[col].apply(clean_text)

    return df

# Example usage
if __name__ == "__main__":
    # Replace with your actual file path
    input_file = "small.txt"
    processed_df = preprocess_data(input_file)
    print(processed_df.head())  # Display the first few rows of the cleaned dataset
    # Save the processed data
    processed_df.to_csv("clean.csv", index=False, encoding="utf-8")

