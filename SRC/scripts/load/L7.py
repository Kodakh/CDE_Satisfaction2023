import csv
from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['http://localhost:9200'],
    http_auth=('elastic', '4862')
)


### Intégration des données non relationnelles (commentaires)
index_name = 'test_norelationnel'

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

with open('../data/processed/L7_processed.csv', 'r', encoding='utf-8') as file:
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

        es.index(index=index_name, body=entry)


### Intégration des données  relationnelles (mapping site trustpilot)
        
from elasticsearch import Elasticsearch
import csv

index_name = "test_relationnel"

mapping = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "URL": {"type": "keyword"},
            "note": {"type": "float"},
            "avis": {"type": "integer"},
            "sous-cat": {"type": "text"}
        }
    }
}

# Supprimer l'index existant
es.indices.delete(index=index_name, ignore=[400, 404])

# Créer l'index avec le nouveau mapping
es.indices.create(index=index_name, body=mapping)

# Réindexer les données à partir du fichier CSV
with open('/home/jben/Documents/CDE_Satisfaction2023/data/processed/L4_processed.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    next(csv_reader)  # Skip the header row
    
    for row in csv_reader:
        entry = {
            'name': row['﻿name'],
            'URL': row['URL'],
            'note': float(row['note']),
            'avis': int(row['avis']),
            'sous-cat': row['sous-cat']
        }
        
        es.index(index=index_name, body=entry)