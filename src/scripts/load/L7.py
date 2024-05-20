import csv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from tqdm import tqdm

es = Elasticsearch(["http://elasticsearch:9200"])

### Intégration des données non relationnelles (commentaires)
index_name = 'reviews'

# Vérifier si l'index existe déjà et le supprimer s'il existe
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

# Création de l'index avec le mapping
es.indices.create(index=index_name, body=mapping)

csv_file_path = '/data/reviews_processed_7.csv'

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

# Obtenir le nombre total de lignes dans le fichier CSV
with open(csv_file_path, 'r', encoding='utf-8') as file:
    total_lines = sum(1 for _ in file) - 1  # Soustraire 1 pour exclure l'en-tête

# Initialiser la barre de progression
progress_bar = tqdm(total=total_lines, unit='lignes', desc='Ingestion des données')

# Wrapper pour mettre à jour la barre de progression
def progress_wrapper(actions):
    for action in actions:
        yield action
        progress_bar.update(1)

bulk(es, progress_wrapper(generate_actions()))

# Fermer la barre de progression
progress_bar.close()