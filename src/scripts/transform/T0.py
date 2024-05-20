import os
import pandas as pd
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
from tqdm import tqdm
import csv
import json

# Chemin de base pour les données
base_path = '/data'

# Chargement et préparation du fichier CSV initial
print("Chargement du fichier CSV...")
df = pd.read_csv(os.path.join(base_path, 'reviewslast100.csv'))
print("Fichier CSV chargé avec succès.")

# Ensure all reviews are strings
df['review'] = df['review'].astype(str)
df['response_yesno'] = df['response_yesno'].fillna(0).map(lambda x: 1 if x else 0)

# Analyse de sentiment
print("Début de l'analyse de sentiment...")
SIA = SentimentIntensityAnalyzer()
df['scores'] = [SIA.polarity_scores(review) for review in tqdm(df['review'], desc="Analyse de sentiment")]


# Enregistrement des résultats intermédiaires
intermediate_csv_path = os.path.join(base_path, 'reviews_processed_6.csv')
df.to_csv(intermediate_csv_path, index=False)
print("Enregistrement intermédiaire terminé.")

# Traitement des scores de sentiment
print("Traitement des scores de sentiment...")
with open(intermediate_csv_path, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    data = list(reader)

output_csv_path = os.path.join(base_path, 'reviews_processed_7.csv')
with open(output_csv_path, 'w', newline='') as csv_file:
    fieldnames = ['author', 'review', 'review_date', 'note', 'response_yesno', 'response_date',
                  'response', 'neg', 'neu', 'pos', 'compound']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for row in tqdm(data, desc="Rajout des indices 'neg', 'neu', et 'pos'"):
        scores = json.loads(row['scores'].replace("'", "\""))
        row.update(scores)
        del row['scores']
        writer.writerow(row)

print("Traitement terminé. Le fichier final a été créé.")