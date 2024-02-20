import pandas as pd
import requests
import time
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import os

### Ce script necessite l'utilisation d'un VPN >400 extractions

def e4():
    star_labels_entreprises = []
    star_percentages_entreprises = []
    data = pd.read_csv('CDE_Satisfaction2023/data/raw/E3_raw.csv')
    colonne_liens = data.iloc[:, 1]

    # Utilisation de tqdm pour la barre de progression
    for count, url in tqdm(enumerate(colonne_liens), total=len(colonne_liens)):
        page_entreprise = requests.get(url)
        bs_entreprise = bs(page_entreprise.content, 'html.parser')

        star_labels_entreprise = bs_entreprise.find_all('p', {'data-rating-label-typography': True})
        star_labels = [i.text.strip() for i in star_labels_entreprise]
        star_labels_entreprises.append(star_labels)

        star_percentages_entreprise = bs_entreprise.find_all('p', {'data-rating-distribution-row-percentage-typography': True})
        star_percentages = [i.text.strip().replace('\xa0', '') for i in star_percentages_entreprise]
        star_percentages_entreprises.append(star_percentages)

        # Pause après chaque 50 itérations
        if count % 50 == 0:
            time.sleep(10)

    # Enregistrement du dataframe en dehors de la boucle
    df_entreprise_page = pd.DataFrame(list(zip(colonne_liens, star_labels_entreprises, star_percentages_entreprises)), columns=["URL", "star labels", "star percentages"])
    output_directory = 'CDE_Satisfaction2023/data/raw'
    csv_file_path = os.path.join(output_directory, 'E4_raw.csv')
    df_entreprise_page.to_csv(csv_file_path, index=False)

# Appel de la fonction
e4()

