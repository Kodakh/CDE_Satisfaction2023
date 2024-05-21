# CDE_Satisfaction2023
Projet Satisfaction Client - CDE 2023

Repository GitHub concernant le projet "Satisfaction Client" proposé par DataScientest pour la promotion Data Engineer de Juillet 2023 Continue

Chef de projet : Sebastien SIME - DataScientest
Membre : Joris BENOIT

I. Installation du projet - Testé sur Ubuntu Jammy 22.04.4 LTS

sudo apt update
sudo apt install python3-pip
git clone https://github.com/Kodakh/CDE_Satisfaction2023
pip install -r requirements.txt
sudo groupadd docker
sudo usermod -aG docker $USER
nano ~/.bashrc
export PATH="/home/freebox/.local/bin:$PATH"
source ~/.bashrc

cd CDE_Satisfaction2023
run.sh





II. Architecture du projet "CDE_Satisfaction2023"
```bash
.
├── README.md
├── Report
│   └── Rendu Rapport Etape 1.rtf
├── requirements.txt
├── run.sh
└── src
    ├── containers
    │   ├── Dockerfile.extraction
    │   ├── Dockerfile.loading
    │   ├── Dockerfile.transformation
    │   ├── app
    │   │   └── data
    │   │       └── ext
    │   │           └── raw_reviews.csv
    │   ├── docker-compose.yml
    │   └── setup.sh
    ├── doc
    │   └── crontab
    └── scripts
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

11 directories, 19 files


```
