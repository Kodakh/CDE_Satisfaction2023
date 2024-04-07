# CDE_Satisfaction2023
Projet Satisfaction Client - CDE 2023

Il s'agit du repository GitHub concernant le projet "Satisfaction Client" proposé par DataScientest de la promotion Data Engineer de Juillet 2023

Chef de projet : Sebastien SIME - DataScientest

Membre : Joris BENOIT

I. Clonage et installation des packages externes 

1. git clone https://github.com/Kodakh/CDE_Satisfaction2023
2. sudo apt install python3-pip
3. cd CDE_Satisfaction2023
4. pip install -r requirements.txt
5. python3 SRC/main.py





II. Architecture du projet "CDE_Satisfaction2023"
```bash
.
├── README.md
├── Report
│   └── Rendu Rapport Etape 1 - SC DIACOH - BELKHIR - BENOIT.rtf
├── SRC
│   ├── containers
│   │   └── docker-compose.yml
│   ├── doc
│   │   └── crontab
│   ├── main.py
│   └── scripts
│       ├── extract
│       │   ├── E1.py
│       │   ├── E2.py
│       │   ├── E3.py
│       │   ├── E4.py
│       │   ├── E5.py
│       │   └── __init__.py
│       │
│       ├── load
│       │   ├── L1.py
│       │   ├── L7.py
│       │   └── __init__.py   
│       │
│       └── transform
│           ├── T1.py
│           ├── T2.py
│           ├── T5.py
│           ├── T6.py
│           ├── T7.py
│           └── __init__.py
│ 
├── data
│   ├── processed
│   │   ├── L5_processed.csv
│   │   ├── L6_processed.csv
│   │   └── L7_processed.csv
│   └── raw
│       └── nosql
│           ├── cdiscount_reviews_1_X.csv
│           └── cdiscount_reviews_last.csv
├── logs
│   └── cron.log
├── notebook
└── requirements.txt


```
