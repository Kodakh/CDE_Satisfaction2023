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

with open('CDE_Satisfaction2023/data/processed/L7_processed.csv', 'r', encoding='utf-8') as file:
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