import os
import pandas as pd
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
from tqdm import tqdm
import csv

# Chemin de base pour les données
base_path = 'data/'

def load_archive_raw():
    print("Chargement du fichier archive_raw.csv...")
    df_archive = pd.read_csv(os.path.join(base_path, 'archive_raw.csv'))
    print("Fichier archive_raw.csv chargé avec succès.")
    return df_archive

# Chargement des données
df = load_archive_raw()

# Changement type de données colonne 'review' 
df['review'] = df['review'].astype(str)

# Passage de 0 & 1 pour les réponses Cdiscount + type de données de la colonne 'response_yesno'
df['response_yesno'] = df['response_yesno'].fillna(0).astype(bool).astype(int)

# Suppression lignes NaN pour la colonne 'review'
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

# Préparation de l'écriture CSV
print("Traitement des scores de sentiment...")
output_csv_path = os.path.join(base_path, 'archive_processed.csv')
with open(output_csv_path, 'w', newline='') as csv_file:
    fieldnames = ['author', 'review', 'review_date', 'note', 'response_yesno', 'response_date',
                  'response', 'neg', 'neu', 'pos', 'compound']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Export..."):
        row_dict = row.to_dict()
        # Suppression du dictionnaire 'scores' pour éviter les erreurs
        row_dict.pop('scores', None)
        
        # Remplacement des valeurs NaN par une chaîne vide
        for key in row_dict:
            if pd.isna(row_dict[key]):
                row_dict[key] = ''
        
        writer.writerow(row_dict)

print("Transformation OK")