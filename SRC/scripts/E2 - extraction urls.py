import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import os
from tqdm import tqdm  # pour la barre de progression

def urls_categorie():
    url = "https://fr.trustpilot.com/categories/business_services"
    urls = [url]

    def getdata(url):
        page_category = requests.get(url)
        bs_category = bs(page_category.content, 'html.parser')
        return bs_category

    def getnextpage(bs_category):
        page = bs_category.find('div', {'class': 'styles_paginationWrapper__fukEb styles_pagination__USObu'})
        next_page = page.find('a', {'class': 'link_internal__7XN06 button_button__T34Lr button_m__lq0nA button_appearance-outline__vYcdF button_squared__21GoE link_button___108l pagination-link_next__SDNU4 pagination-link_rel__VElFy'})
        if next_page and 'href' in next_page.attrs:
            return 'https://fr.trustpilot.com' + next_page.get('href')
        else:
            return None

    while True:
        bs_category = getdata(url)
        url = getnextpage(bs_category)
        if not url or url in urls:
            break
        urls.append(url)

    df_urls_cat = pd.DataFrame(list(zip(urls)), columns=['url'])
    return df_urls_cat

# Exécution de la fonction
df_urls_cat = urls_categorie()

# Export du fichier CSV
output_directory = r'CDE_Satisfaction2023/data/raw'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
csv_file_path = os.path.join(output_directory, 'E2_raw.csv')
df_urls_cat.to_csv(csv_file_path, index=False)
