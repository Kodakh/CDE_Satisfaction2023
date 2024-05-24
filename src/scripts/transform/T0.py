import os
import glob
import pandas as pd
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
from tqdm import tqdm
import csv
from datetime import datetime


base_path1 = '/data/ext'

def last_reviews():
    print("Chargement des reviews du jour...")
    csv_files = glob.glob(os.path.join(base_path1, 'reviews_*_raw.csv'))
    latest_csv_file = max(csv_files, key=os.path.getctime)
    df_last_reviews = pd.read_csv(latest_csv_file)
    print("Chargement OK.")
    return df_last_reviews

df = last_reviews()

# Changement type de donnees colonne 'review' 
df['review'] = df['review'].astype(str)

# Passage de 0 & 1 pour les réponses Cdiscount + type de données de la colonne 'response_yesno'
df['response_yesno'] = df['response_yesno'].fillna(0).astype(bool).astype(int)

# Suppression lignes NaN
df['review'].replace('nan', pd.NA, inplace=True)
df.dropna(subset=['review'], inplace=True)

# Suppression des doublons 
df.drop_duplicates(inplace=True)


print("Début de l'analyse de sentiment...")
SIA = SentimentIntensityAnalyzer()
tqdm.pandas()  
df['scores'] = df['review'].progress_apply(lambda x: SIA.polarity_scores(str(x)))

# Extraction des scores individuels
df['neg'] = df['scores'].apply(lambda x: x['neg'])
df['neu'] = df['scores'].apply(lambda x: x['neu'])
df['pos'] = df['scores'].apply(lambda x: x['pos'])
df['compound'] = df['scores'].apply(lambda x: x['compound'])

# Préparation export

print("Traitement des scores de sentiment...")
today = datetime.now().strftime('%Y-%m-%d')

basepath2 = '/data'
output_csv_path = os.path.join(basepath2, f'reviews_{today}_processed.csv')

with open(output_csv_path, 'w', newline='') as csv_file:
    fieldnames = ['author', 'review', 'review_date', 'note', 'response_yesno', 'response_date',
                  'response', 'neg', 'neu', 'pos', 'compound']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Export..."):
        row_dict = row.to_dict()
        row_dict.pop('scores', None)
        
        for key in row_dict:
            if pd.isna(row_dict[key]):
                row_dict[key] = ''
        
        writer.writerow(row_dict)

print("Transformation OK")