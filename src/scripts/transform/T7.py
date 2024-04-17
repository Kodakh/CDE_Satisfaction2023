import csv
import json
from tqdm import tqdm

# Nom du fichier CSV source
fichier_source = 'data/processed/L6_processed.csv'

# Nom du fichier CSV de destination
fichier_destination = 'data/processed/L7_processed.csv'

# Lire le fichier CSV source
with open(fichier_source, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    data = list(reader)

# Ouvrir le fichier CSV de destination en mode écriture
with open(fichier_destination, 'w', newline='') as csv_file:
    fieldnames = ['author', 'review', 'date_review', 'note', 'cdiscount_response', 'cdiscount_response_date',
                  'cdiscount_response_content', 'neg', 'neu', 'pos', 'compound']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Parcourir les lignes du CSV source avec tqdm
    for row in tqdm(data, desc="Rajout des indices 'neg', 'neu' et 'pos'"):
        scores = json.loads(row['scores'].replace("'", "\""))
        row.update(scores)
        del row['scores']
        writer.writerow(row)

print("Traitement terminé. Le fichier destination a été créé.")