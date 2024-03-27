import pandas as pd
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
from tqdm import tqdm, tqdm_pandas


# Que fait le script ? - scoring


df = pd.read_csv('/home/jben/Documents/CDE_Satisfaction2023/data/processed/L5_processed.csv')

# sentiment analysis function
def analyse_sentiment(texte):
    try:
        blob = TextBlob(texte, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        return blob.sentiment[0], blob.sentiment[1]  #  polarity & subjectivity
    except Exception as e:
        print(f"Error processing text: {texte}, Error: {e}")
        return None, None

tqdm_pandas(tqdm())

# Apply
df['polarite'], df['subjectivite'] = zip(*df['review'].progress_apply(analyse_sentiment))

# type note
df['note'] = pd.to_numeric(df['note'], errors='coerce')

df.to_csv("/home/jben/Documents/CDE_Satisfaction2023/data/processed/L6_processed.csv", index=False)
