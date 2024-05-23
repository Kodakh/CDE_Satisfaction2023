import os
import pandas as pd
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
from tqdm import tqdm
import csv

# Chemin de base pour les données
base_path = '/arch'

def load_archive_raw():
    print("Chargement du fichier archive_raw.csv...")
    df_archive = pd.read_csv(os.path.join(base_path, 'archive_raw.csv'))
    print("Archive_raw.csv chargé avec succès.")
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


import csv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, BulkIndexError
from elasticsearch.helpers import bulk
from tqdm import tqdm

es = Elasticsearch(["http://elasticsearch:9200"])
index_name = 'reviews_archive'

if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# Définition du mapping
mapping = {
    "mappings": {
        "properties": {
            "author": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "response_yesno": {
                "type": "long"
            },
            "response": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "response_date": {
                "type": "date",
                "format": "dd/MM/yyyy"
            },
            "compound": {
                "type": "float"
            },
            "review_date": {
                "type": "date",
                "format": "dd/MM/yyyy"
            },
            "neg": {
                "type": "float"
            },
            "neu": {
                "type": "float"
            },
            "note": {
                "type": "integer"
            },
            "pos": {
                "type": "float"
            },
            "review": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            }
        }
    }
}

es.indices.create(index=index_name, body=mapping)
csv_file_path = '/arch/archive_processed.csv'

def generate_actions():
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            note = int(row['note'])
            
            entry = {
                'author': row['author'],
                'review': row['review'],
                'review_date': row['review_date'],
                'note': note,
                'response_yesno': int(row['response_yesno']) if row['response_yesno'] else None,
                'response_date': row['response_date'] if row['response_date'] else None,
                'response': row['response'] if row['response'] else None,
                'neg': float(row['neg']) if row['neg'] else None,
                'neu': float(row['neu']) if row['neu'] else None,
                'pos': float(row['pos']) if row['pos'] else None,
                'compound': float(row['compound']) if row['compound'] else None

            }

            yield {
                "_index": index_name,
                "_source": entry
            }


with open(csv_file_path, 'r', encoding='utf-8') as file:
    total_lines = sum(1 for _ in file) - 1

progress_bar = tqdm(total=total_lines, unit='rows', desc='Loading archive data...')

def progress_wrapper(actions):
    for action in actions:
        yield action
        progress_bar.update(1)

try:
    bulk(es, progress_wrapper(generate_actions()))
except BulkIndexError as e:
    print("Errors occurred:", e.errors)

progress_bar.close()