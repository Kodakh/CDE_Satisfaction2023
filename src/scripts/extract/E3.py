from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import getpass
import time
import os
from tqdm import tqdm 

####################################################################################################
########################################### IMPORTANT ##############################################
####################################################################################################
#   Pas besoin d'utiliser un VPN tant que la quantité d'URLS de la catégorie ne dépasse pas 250    #
####################################################################################################

# Que fait le script ? extraction nombre avis + sous cats

def e3():
    noms_entreprises = []
    trust_scores = []
    nombres_d_avis = []
    noms_des_categories = []
    urls_entreprises = []
    data = pd.read_csv('CDE_Satisfaction2023/data/raw/sql/E2_raw.csv') 
    colonne_liens = data.iloc[:, 0]

    for url in tqdm(colonne_liens, desc="Traitement des URLs"):
        entreprise_details_page = requests.get(url)
        bs_entreprise_details_page= bs(entreprise_details_page.content, 'html.parser')
    
        entreprises_details_page = bs_entreprise_details_page.find_all('div', {'class' : 'paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_wrapper__2JOo2'})


# récupérer les noms des entreprises 

        for entreprise_detail_page in entreprises_details_page : 
            nom_entreprise = entreprise_detail_page.find('p', {'class' : 'typography_heading-xs__jSwUz typography_appearance-default__AAY17 styles_displayName__GOhL2'}).text
            noms_entreprises.append(nom_entreprise)

# récupérer le nombre d'avis par entreprise  : étant donné que pour certaines sociétés, il n'y a pas de trustscore, j'ai du faire plusieurs étapes pour éviter les erreurs

        for entreprise_detail_page in entreprises_details_page : 
            if entreprise_detail_page is not None :
                entreprise_trustScore_element = entreprise_detail_page.find('span', {'class' : 'typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_trustScore__8emxJ'})
                if entreprise_trustScore_element is not None :
                    entreprise_trustScore = entreprise_trustScore_element.text
                      
                    trust_scores.append(entreprise_trustScore.replace('TrustScore ', '').replace(',', '.'))
                else : 
                    trust_scores.append("N/A")
            else : 
                trust_scores.append("N/A")
     
#récupérer le nombre d'avis par entreprise  : étant donné que pour certaines sociétés, il n'y a pas d'avis client, j'ai du faire plusieurs étapes pour éviter les erreurs

        for entreprise_detail_page in entreprises_details_page : 
            if entreprise_detail_page is not None :
                nombre_d_avis_element = entreprise_detail_page.find('p', {'class' : 'typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_ratingText__yQ5S7'})
                if nombre_d_avis_element is not None :
                    nombre_d_avis = nombre_d_avis_element.text.replace ('\u202f', ' ') 
            
                    nombre_d_avis = nombre_d_avis.split("|")[1].strip().replace(' avis', '').replace(' ', '')  # voici le résultat sans cette ligne de code : 'TrustScore 5,0|14 169 avis',
                    nombres_d_avis.append(nombre_d_avis)
                else : 
                    nombres_d_avis.append("N/A")
            else : 
                nombres_d_avis.append("N/A")
                
  # récupérer les noms des catégories en bas qui apparaissent en bas de chaque entreprise : 

    

        for entreprise_detail_page in entreprises_details_page :  
            noms_des_categories_par_société = entreprise_detail_page.find('div', {'class' : 'styles_wrapper___E6__ styles_categoriesLabels__FiWQ4 styles_desktop__U5iWw'}).text.split('·')
            noms_des_categories.append(noms_des_categories_par_société)
        
        
        for entreprise_detail_page in entreprises_details_page :
            url_entreprise = entreprise_detail_page.find('a')
            urls_entreprise = 'https://fr.trustpilot.com' + url_entreprise.get('href')
            urls_entreprises.append(urls_entreprise)

# Création du dataframe noms_entreprises, trust_scores, nombres_d_avis et noms_des_categories + export csv

        df_entreprises_page = pd.DataFrame(list(zip(noms_entreprises,urls_entreprises, trust_scores, nombres_d_avis,noms_des_categories)), columns = ["nom de l'entreprise",'URL', 'Note', "Nombre d'avis", "nom_des_categories"])
        output_directory = 'CDE_Satisfaction2023/data/raw/sql'
        csv_file_path = os.path.join(output_directory, 'E3_raw.csv')
    return df_entreprises_page.to_csv(csv_file_path, index=False)

e3()