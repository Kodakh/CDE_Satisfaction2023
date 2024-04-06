import csv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from tqdm import tqdm

es = Elasticsearch(
    ['http://localhost:9200'],
    http_auth=('elastic', '4862')
)

### Intégration des données non relationnelles (commentaires)
index_name = 'test_norelationnel'

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
            "cdiscount_response": {
                "type": "long"
            },
            "cdiscount_response_content": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "cdiscount_response_date": {
                "type": "date",
                "format": "dd/MM/yyyy"
            },
            "compound": {
                "type": "float"
            },
            "date_review": {
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

csv_file_path = 'data/processed/L7_processed.csv'

def generate_actions():
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            note = int(row['note'])

            entry = {
                'author': row['author'],
                'review': row['review'],
                'date_review': row['date_review'],
                'note': note,
                'cdiscount_response': int(row['cdiscount_response']) if row['cdiscount_response'] else None,
                'cdiscount_response_date': row['cdiscount_response_date'] if row['cdiscount_response_date'] else None,
                'cdiscount_response_content': row['cdiscount_response_content'] if row['cdiscount_response_content'] else None,
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