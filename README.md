# 1. Présentation du projet  

# Satisfaction Client - Marketplace/Trustpilot

Repository GitHub concernant le projet "Satisfaction Client" pour la promotion DS Paris Data Engineer de Juillet 2023 (Continue).

#### *Chef de projet : Sebastien SIME*
#### *Membre : Joris BENOIT*



## Comment pourrait-on évaluer la qualité du service client d'une Marketplace à travers le site Trustpilot ?
#### Objectif : S'assurer à l'aide de différentes métrics (taux de réponse, satisfaction client, keywords..) de la qualité du service client de Cdiscount et de la conformité des avis laissés.

#### *Méthodologie*

Ce projet développe et met en œuvre un pipeline ETL simple pour extraire, transformer et charger des données issues du site 'Trustpilot'. 
Après le traitement des données, celles-ci sont indexées dans ElasticSearch puis exposées via Kibana, un outil de visualisation open source permettant une analyse et une visualisation intéractives.

Le projet s'éxecute de facon quotidienne et automatisée.
Des logs sont disponibles pour s'assurer que les services fonctionnent correctement :

![Logs du container 'Extraction'](src/doc/logs_extraction.png)
![Logs du container 'Transformation'](src/doc/logs_transformation.png)


# 2. **Installation** 
#### *Projet Testé et Installé dans une machine virtuelle hebergée sur un serveur FreeboxDelta utilisant la distribution Ubuntu Jammy 22.04.4 LTS*
```bash

# Clonage du repository 
git clone https://github.com/Kodakh/CDE_Satisfaction2023/tree/release


# Lancement du script bash pour l'installation des dépendances + création des images 
cd CDE_Satisfaction2023
./run.sh
cd src
cd containers
docker-compose up -d

```


# 3. **Architecture**

Le projet s'articule autour de 7 micro-services construits via des images Dockerfiles spécifiques pour chaque étape du pipeline ETL, conditionnés avec des wrappers & healthchecks, ainsi qu'un fichier docker-compose.yml pour orchestrer le déploiement de ces services :
1. *Archive* => Charge en memoire l'historique des reviews pre-2024 (+ de 120 000 avis)
2. *Extraction* => Scraping des reviews
3. *Tranformation* => Cleaning & valorisation des données extraites
4. *Loading* => Chargement et indexation des données transformées dans le SGBD
5. *ElasticSearch* => Moteur de recherche pour les données 
6. *Kibana* => Visualisation et interprétation a l'aide d'un Dashboard
7. *Network* => réseau partagé par l'ensemble des containers pour faire passerelle entre chaque service

![Containers Dockers](src/doc/Docker.png)


```bash
.
├── README.md
├── Report
│   └── Rendu Rapport Etape 1 - SC DIACOH - BELKHIR - BENOIT.rtf
├── requirements.txt
├── run.sh
└── src
    ├── containers
    │   ├── Dockerfile.archive
    │   ├── Dockerfile.extraction
    │   ├── Dockerfile.loading
    │   ├── Dockerfile.transformation
    │   └── docker-compose.yml
    ├── doc
    └── scripts
        ├── archive
        │   ├── A0.py
        │   └── data
        │       └── archive_raw.csv
        ├── extract
        │   ├── E0.py
        │   ├── healthcheck_extract.py
        │   └── wrapper_extraction.py
        ├── load
        │   ├── L0.py
        │   └── wrapper_loading.py
        └── transform
            ├── T0.py
            ├── healthcheck_transform.py
            └── wrapper_transformation.py

10 directories, 19 files


```


# 4. **Dashboard Final**

![Dashboard Kibana](src/doc/dashboardv2.png)




# 5. **Conclusion**
#### Ce projet a été une expérience d'apprentissage inestimable qui a nécessité de faire face à des challenges techniques importants (architecture en microservices, networking) mais qui m'ont aussi permis le développement de compétences sur des technologies essentielles utilisées par le Data Engineer.
#### J'ai ainsi pu approfondir ma maîtrise sur les bibliotheques Python (Pandas, BS4,vaderSentiment,TQDM...), sur Docker qui m'a permis de rendre mon application plus portable et facile à déployer, FastAPI pour la création d'endpoints clés.
#### Mais au-delà des compétences techniques, ce projet m'a aussi enseigné des leçons précieuses sur la persévérance, l'autonomie et la planification. Je suis impatient de mettre en pratique tout ce que j'ai appris dans de futurs projets, et de continuer à monter en compétence !
