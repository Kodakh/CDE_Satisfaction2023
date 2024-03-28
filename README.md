# CDE_Satisfaction2023
Projet Satisfaction Client - CDE 2023

Il s'agit du repository GitHub concernant le projet "Satisfaction Client" proposé par DataScientest de la promotion Data Engineer de Juillet 2023

Chef de projet : Sebastien SIME - DataScientest

Membre : Joris BENOIT

I. Clonage et installation des packages externes 

1. git clone https://github.com/Kodakh/CDE_Satisfaction2023
2. pip install -r requirements.txt





II. Architecture du projet 
```bash
├── data
│   ├── processed
│   │   ├── L4_processed.csv
│   │   ├── L5_processed.csv
│   │   ├── L6_processed.csv
│   │   └── L7_processed.csv
│   └── raw
│       ├── nosql
│       │   ├── cdiscount_reviews_000-200.csv
│       │   ├── cdiscount_reviews_1000-1200.csv
│       │   ├── cdiscount_reviews_1200-1400.csv
│       │   ├── cdiscount_reviews_1400-1600.csv
│       │   ├── cdiscount_reviews_1600-1800.csv
│       │   ├── cdiscount_reviews_1800-2000.csv
│       │   ├── cdiscount_reviews_2000-2200.csv
│       │   ├── cdiscount_reviews_200-400.csv
│       │   ├── cdiscount_reviews_2200-2400.csv
│       │   ├── cdiscount_reviews_2400-2600.csv
│       │   ├── cdiscount_reviews_2600-2800.csv
│       │   ├── cdiscount_reviews_2800-3000.csv
│       │   ├── cdiscount_reviews_3000-3200.csv
│       │   ├── cdiscount_reviews_3200-3400.csv
│       │   ├── cdiscount_reviews_3400-3600.csv
│       │   ├── cdiscount_reviews_3600-3800.csv
│       │   ├── cdiscount_reviews_3800-4000.csv
│       │   ├── cdiscount_reviews_4000-4200.csv
│       │   ├── cdiscount_reviews_400-600.csv
│       │   ├── cdiscount_reviews_4200-4400.csv
│       │   ├── cdiscount_reviews_4400-4600.csv
│       │   ├── cdiscount_reviews_4600-4800.csv
│       │   ├── cdiscount_reviews_4800-5000.csv
│       │   ├── cdiscount_reviews_5000-5200.csv
│       │   ├── cdiscount_reviews_5200-5400.csv
│       │   ├── cdiscount_reviews_5400-5600.csv
│       │   ├── cdiscount_reviews_5600-5800.csv
│       │   ├── cdiscount_reviews_5800-6000.csv
│       │   ├── cdiscount_reviews_6000-6200.csv
│       │   ├── cdiscount_reviews_600-800.csv
│       │   ├── cdiscount_reviews_6200-6400.csv
│       │   ├── cdiscount_reviews_800-1000.csv
│       │   └── cdiscount_reviews_last.csv
│       └── sql
│           ├── details_entreprise_191223.csv
│           ├── E1_raw.csv
│           ├── E2_raw.csv
│           ├── E3_raw.csv
│           └── E4_raw.csv
├── notebook
│   └── connector_KIBANA_ES.ipynb
├── README.md
├── Report
│   └── Rendu Rapport Etape 1 - SC DIACOH - BELKHIR - BENOIT.rtf
├── requirements.txt
└── SRC
    ├── doc
    │   └── crontab
    └── scripts
        ├── extract
        │   ├── E1.py
        │   ├── E2.py
        │   ├── E3.py
        │   ├── E4.py
        │   ├── E5.py
        │   └── __init__.py
        ├── load
        │   └── L7.py
        ├── main.py
        └── transform
            ├── __init__.py
            ├── T1.py
            ├── T2.py
            ├── T5.py
            ├── T6.py
            └── T7.py

13 directories, 61 files

```
