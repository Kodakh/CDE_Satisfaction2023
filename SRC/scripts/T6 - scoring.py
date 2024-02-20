import pandas as pd
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
from tqdm import tqdm, tqdm_pandas

# Read the CSV file
df = pd.read_csv('CDE_Satisfaction2023/data/processed/L5_processed.csv')

# Define the sentiment analysis function
def analyse_sentiment(texte):
    try:
        blob = TextBlob(texte, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        return blob.sentiment[0], blob.sentiment[1]  #  polarity & subjectivity
    except Exception as e:
        print(f"Error processing text: {texte}, Error: {e}")
        return None, None

tqdm_pandas(tqdm())

# Apply the sentiment analysis
df['polarite'], df['subjectivite'] = zip(*df['review'].progress_apply(analyse_sentiment))

# Ensure that 'note' is a numerical column (if it's not already)
df['note'] = pd.to_numeric(df['note'], errors='coerce')

# Save the DataFrame to a new CSV file
df.to_csv("CDE_Satisfaction2023/data/processed/L6_processed.csv", index=False)
