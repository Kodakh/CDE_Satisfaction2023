import os
import pandas as pd
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
from tqdm import tqdm
import csv

# Chemin de base pour les données
base_path1 = '/data/ext'
base_path2 = '/data'

global df_merged
df_merged = None

def load_archive_reviews():
    print("Chargement du fichier archive_reviews.csv...")
    df_archive_reviews = pd.read_csv(os.path.join(base_path1, 'archive_reviews.csv'))
    print("Fichier archive_reviews.csv chargé avec succès.")
    return df_archive_reviews

def load_other_file():
    print("Chargement de l'autre fichier...")
    df_last_reviews = pd.read_csv(os.path.join(base_path1, 'last_reviews.csv'))
    print("Autre fichier chargé avec succès.")
    return df_last_reviews

def load_merged_data():
    global df_merged
    df_archive_reviews = load_archive_reviews()
    df_last_reviews = load_other_file()
    print("Fusion des fichiers...")
    df_merged = pd.concat([df_archive_reviews, df_last_reviews], ignore_index=True)
    print("Fichiers fusionnés avec succès.")
    return df_merged

# Utilisation de la fonction pour charger et fusionner les données
df_merged = load_merged_data()

df = df_merged

# Changement type de donnees colonne 'review' 
df['review'] = df['review'].astype(str)

# Passage de 0 & 1 pour les reponses Cdiscount + type de donnees de la colonne 'response_yesno'
df['response_yesno'] = df['response_yesno'].fillna(0).map(lambda x: 1 if x else 0)

# Suppression lignes NaN
df['review'].replace('nan', pd.NA, inplace=True)
df.dropna(subset=['review'], inplace=True)

# Suppression des doublons 
df.drop_duplicates(inplace=True)


print("Début de l'analyse de sentiment...")
SIA = SentimentIntensityAnalyzer()
df['scores'] = df['review'].apply(lambda x: SIA.polarity_scores(str(x)))

# Extracting individual scores
df['neg'] = df['scores'].apply(lambda x: x['neg'])
df['neu'] = df['scores'].apply(lambda x: x['neu'])
df['pos'] = df['scores'].apply(lambda x: x['pos'])
df['compound'] = df['scores'].apply(lambda x: x['compound'])

# Prepare CSV writing
print("Traitement des scores de sentiment...")
output_csv_path = os.path.join('/data', 'reviews_processed.csv')
with open(output_csv_path, 'w', newline='') as csv_file:
    fieldnames = ['author', 'review', 'review_date', 'note', 'response_yesno', 'response_date',
                  'response', 'neg', 'neu', 'pos', 'compound']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Writing to CSV"):
        row_dict = row.to_dict()
        # Remove the 'scores' dictionary to avoid errors
        row_dict.pop('scores', None)
        writer.writerow(row_dict)

print("Transformation OK")