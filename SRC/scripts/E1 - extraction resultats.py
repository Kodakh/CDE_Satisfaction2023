import csv
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from tqdm import tqdm # Ajout J 
import os # Ajout J 

def resultats(url_categories):
    page_categories = requests.get(url_categories)
    if page_categories.status_code != 200: # Ajout J
        print(f"Échec de la requête HTTP. Code de statut: {page_categories.status_code}")
        return
    
    bs_categories = bs(page_categories.content, 'html.parser')
    categories_sub_categories = []
    categories = []
    links = []
    results = []
    categories_html = bs_categories.find_all('div', class_="paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_card__slNee")

    if not categories_html: # Ajout J
        print("Aucune catégorie trouvée.")
        return

    for category_html in tqdm(categories_html, desc="Traitement des catégories"): # Modif J
        category = category_html.find('h2', class_="typography_heading-xs__jSwUz typography_appearance-default__AAY17 styles_headingDisplayName__jetQq").text
        sous_cat_html = category_html.find_all('li', class_="styles_linkItem__KtBm6")

        sous_categories = [sous_cat.text for sous_cat in sous_cat_html]
        number_sub_categories = len(sous_categories)
        categories_sub_categories.append((category, sous_categories, number_sub_categories))

    df_categories_sub_categories_number_sub_categories = pd.DataFrame(categories_sub_categories, columns=["cat", "sous_cat", "number of sous_cat"])

    for category_html in tqdm(categories_html, desc="Traitement des catégories pour liens"): # Modif J
        category = category_html.find('h2', class_="typography_heading-xs__jSwUz typography_appearance-default__AAY17 styles_headingDisplayName__jetQq").text
        categories.append(category)
        link = category_html.find('a').get('href', '')
        links.append('https://fr.trustpilot.com' + link)

    for url in tqdm(links, desc="Traitement des liens"): # Modif J
        page_category = requests.get(url)
        if page_category.status_code != 200:
            print(f"Échec de la requête HTTP pour {url}. Code de statut: {page_category.status_code}") # Ajout J
            results.append('Erreur')
            continue

        bs_category = bs(page_category.content, 'html.parser')
        result_text = bs_category.find('p', class_="typography_body-m__xgxZ_ typography_appearance-default__AAY17").text
        result_number = result_text.split(" ")[2].encode("ascii", "ignore").decode()
        results.append(result_number)

    df_categories_resultats_links = pd.DataFrame(list(zip(categories, results, links)), columns=['cat', 'Result', 'link'])

    df_links_resultats_cat_sub_cat_number_of_sub_cat = pd.merge(df_categories_resultats_links, df_categories_sub_categories_number_sub_categories, on=['cat'], how='inner')
    df_links_resultats_cat_sub_cat_number_of_sub_cat['Result'] = pd.to_numeric(df_links_resultats_cat_sub_cat_number_of_sub_cat['Result'], errors='coerce')
    df_final = df_links_resultats_cat_sub_cat_number_of_sub_cat.sort_values(by=['Result'], ascending=False)

    # Export
    output_directory = r'CDE_Satisfaction2023/data/raw'
    csv_file_path = os.path.join(output_directory, 'E1_raw.csv')
    df_final.to_csv(csv_file_path, index=False)
    return df_final

# Lancement script
resultats("https://fr.trustpilot.com/categories")
