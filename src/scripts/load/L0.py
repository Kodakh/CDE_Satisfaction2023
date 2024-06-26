import csv
import glob
import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, BulkIndexError
from elasticsearch.helpers import bulk
from tqdm import tqdm
from datetime import datetime

es = Elasticsearch(["http://elasticsearch:9200"])


print("Traitement des scores de sentiment...")
today = datetime.now().strftime('%Y-%m-%d')

index_name = f'reviews_{today}'

if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

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

basepath2 = '/data'
csv_file_path0 = glob.glob(os.path.join(basepath2, 'reviews_*_processed.csv'))
csv_file_path = max(csv_file_path0, key=os.path.getctime)


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

progress_bar = tqdm(total=total_lines, unit='rows', desc='Loading data')

def progress_wrapper(actions):
    for action in actions:
        yield action
        progress_bar.update(1)

try:
    bulk(es, progress_wrapper(generate_actions()))
except BulkIndexError as e:
    print("Errors occurred:", e.errors)

progress_bar.close()