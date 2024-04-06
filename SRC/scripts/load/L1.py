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