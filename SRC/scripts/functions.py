# C'est ici que nous allons regrouper l'ensemble des fonctions qui allons devoir utiliser pour la récolte, le traitement, et l'exportation des données


import csv
import pandas as pd 
from bs4 import BeautifulSoup as bs
import requests 
import time

######################################################################
######################################################################
######################################################################

def resultats(url_categories):
    #url_categories = "https://fr.trustpilot.com/categories"
    page_categories = requests.get(url_categories)
    bs_categories = bs(page_categories.content, 'html.parser')
    bs_categories.prettify().splitlines()[0:30]
    categories_sub_categories = []
    categories = []
    links =[]
    results= []
    categories_html = bs_categories.find_all('div', class_="paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_card__slNee")

    for category_html in categories_html:
        category = category_html.find('h2', class_="typography_heading-xs__jSwUz typography_appearance-default__AAY17 styles_headingDisplayName__jetQq").text
        sous_cat_html = category_html.find_all('li', class_="styles_linkItem__KtBm6")
             
        sous_categories = []
    
        for i in range(len(sous_cat_html)):
        
            sous_cat = sous_cat_html[i].text
            sous_categories.append(sous_cat)
        number_sub_categories = len(sous_categories)
        categories_sub_categories.append((category,sous_categories, number_sub_categories) ) 

# Categories, subcategories & nbre de sous-cateogies
        
    df_categories_sub_categories_number_sub_categories = pd.DataFrame(categories_sub_categories, columns=["cat","sous_cat", "number of sous_cat"])   


# Categories, resultats & liens

    for category_html in categories_html:
        category = category_html.find('h2', class_="typography_heading-xs__jSwUz typography_appearance-default__AAY17 styles_headingDisplayName__jetQq").text
        categories.append(category)

    for link_html in categories_html:
        link = link_html.find('a')
        link = 'https://fr.trustpilot.com'+ link.get('href')
        links.append(link)

    for url in links:
        url_category = url
        page_category = requests.get(url_category)
        bs_category = bs(page_category.content, 'html.parser')
        results_cat = bs_category.find('p', class_="typography_body-m__xgxZ_ typography_appearance-default__AAY17").text.split(" ")[2].encode("ascii", "ignore").decode()
        results.append(results_cat)


    df_categories_resultats_links = pd.DataFrame(list(zip(categories, results, links)), columns = ['cat', 'Result', 'link'])

# Merge df_categories_sub_categories_number_sub_categories & df_categories_resultats_links

    df_links_resultats_cat_sub_cat_number_of_sub_cat = pd.merge(df_categories_resultats_links, df_categories_sub_categories_number_sub_categories, on = ['cat'], how = 'inner' )
    df_links_resultats_cat_sub_cat_number_of_sub_cat['Result']= df_links_resultats_cat_sub_cat_number_of_sub_cat['Result'].astype(float)
    df_final = df_links_resultats_cat_sub_cat_number_of_sub_cat.sort_values(by=['Result'], ascending=False)
    return df_final.to_csv('Nombre_entreprises_categorie_121223.csv', index = False)

######################################################################
######################################################################
######################################################################

def urls_categorie():

    url = "https://fr.trustpilot.com/categories/business_services"
    urls = [url]

    def getdata(url):
        page_category = requests.get(url)
        bs_category = bs(page_category.content, 'html.parser')
        return bs_category

    def getnextpage (bs_category):
        page = bs_category.find('div', {'class' : 'styles_paginationWrapper__fukEb styles_pagination__USObu'})
        if not page.find('a', {'class' : 'link_internal__7XN06 link_disabled__mIxH1 button_button__T34Lr button_m__lq0nA button_appearance-outline__vYcdF button_squared__21GoE link_button___108l pagination-link_disabled__7qfis pagination-link_next__SDNU4 pagination-link_rel__VElFy'}):
            url = page.find('a', {'class' :'link_internal__7XN06 button_button__T34Lr button_m__lq0nA button_appearance-outline__vYcdF button_squared__21GoE link_button___108l pagination-link_next__SDNU4 pagination-link_rel__VElFy'})
            url = 'https://fr.trustpilot.com' + url.get('href')
            return url 
    
    while True : 
        bs_category = getdata(url)
        url = getnextpage (bs_category) 
        if not url :
            break
        urls.append(url)
        df_urls_cat = pd.DataFrame(list(zip(urls)), columns = ['url'])

    return df_urls_cat.to_csv('urls_pages_categorie_121223.csv', index = False)


######################################################################
######################################################################
######################################################################


def details_entreprises():
    noms_entreprises = []
    trust_scores = []
    nombres_d_avis = []
    noms_des_categories = []
    urls_entreprises = []
    data = pd.read_csv('urls_pages_categorie_121223.csv') 
    colonne_liens = data.iloc[:, 0]
    for url in colonne_liens:
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

        df_entreprises_page = pd.DataFrame(list(zip(noms_entreprises,urls_entreprises, trust_scores, nombres_d_avis,noms_des_categories)), columns = ["nom de l'entreprise",'URL', 'Note', "Nombre d'avis", "nom des catérogies"])
    return df_entreprises_page.to_csv('details_entreprises_121223.csv', index = False)
    
######################################################################
######################################################################
######################################################################

# détails entreprise : 

def details_entreprise():
    star_labels_entreprises = []
    star_percentages_entreprises = []
    data = pd.read_csv('details_entreprises_121223.csv') 
    colonne_liens = data.iloc[:, 1]
    for count, url in enumerate(colonne_liens):
    
        page_entreprise = requests.get(url)
        bs_entreprise = bs(page_entreprise.content, 'html.parser')
    
    
        star_labels_entreprise = bs_entreprise.find_all('p', {'data-rating-label-typography': True})
    
        star_labels = []
        for i in star_labels_entreprise :
            labels = i.text.strip()
            star_labels.append(labels)
        star_labels_entreprises.append(star_labels)
    
    
        star_percentages_entreprise = bs_entreprise.find_all('p', {'data-rating-distribution-row-percentage-typography': True})
    
        star_percentages = []
        for i in star_percentages_entreprise : 
            percentages = i.text.strip().replace('\xa0', '')
            star_percentages.append(percentages)
        star_percentages_entreprises.append(star_percentages)
    
        df_entreprise_page = pd.DataFrame(list(zip(colonne_liens, star_labels_entreprises,star_percentages_entreprises )), columns = ["URL", "star labels", "star percentages"])
        df_entreprise_page.to_csv('details_entreprise_121223.csv', index = False)  
           
        if count % 50 == 0 : 
            time.sleep(10)

######################################################################
######################################################################
######################################################################
            
from bs4 import BeautifulSoup
import requests
import pandas as pd
import getpass

# Function to extract comments from a Trustpilot page
def scrap_reviews(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Listes
    authors = []
    contents = []
    dates = []
    notes = []
    response_titles = []
    response_dates = []
    response_contents = []

    # Debug
    print(f"Scrapping page: {url}")

    reviews = soup.find_all('div', class_='styles_reviewCardInner__EwDq2')

    for review in reviews:
        # Auteur client
        author = review.find('span', class_='typography_heading-xxs__QKBS8').text.strip()
        authors.append(author)

        # Contenu commentaire (avec NaN)
        content_element = review.find('p', class_='typography_body-l__KUYFJ')
        content = content_element.text.strip() if content_element else None
        contents.append(content)

        # Date
        date = review.find('time')['datetime']
        formatted_date = pd.to_datetime(date).strftime('%d/%m/%Y')
        dates.append(formatted_date)

        # Note (avec NaN)
        note_element = review.find('img', class_='icon_icon__ECGRl')
        if note_element and 'alt' in note_element.attrs:
            note = int(note_element['alt'].split()[1])
        else:
            note = int(review.find('div', {'data-service-review-rating': True})['data-service-review-rating'])

        notes.append(note)

        # Cdiscount
        response_tag = review.find('div', class_='styles_replyInfo__FYSje')
        if response_tag:
            response_title = response_tag.find('p', class_='styles_replyCompany__ro_yX')
            response_date = response_tag.find('time', class_='styles_replyDate__Iem0_')
            response_text = review.find('p', class_='styles_message__shHhX')

            title = response_title.text.strip() if response_title else None
            date = response_date.get('datetime') if response_date else None
            formatted_date_response = pd.to_datetime(date).strftime('%d/%m/%Y') if date else None

            text = response_text.attrs.get('content') if response_text else None
            if not text:
                text = response_text.text.strip() if response_text else None

            response_titles.append(title)
            response_dates.append(formatted_date_response)
            response_contents.append(text)
        else:
            response_titles.append(None)
            response_dates.append(None)
            response_contents.append(None)

    # df
    df = pd.DataFrame({
        'Author': authors,
        'Content': contents,
        'Date': dates,
        'Note': notes,
        'Réponse': response_titles,
        'Date Réponse': response_dates,
        'Contenu de la réponse': response_contents,
    })

    return df

##### Défilement page TEMPORAIRE !!!!!!!!!!!!!!!!! MODIFIER PAR SCRIPT MONTASSAR
base_url = 'https://fr.trustpilot.com/review/www.cdiscount.com'

# pages to scrape
num_pages = 5

# Sauvegarde local du CSV
username = getpass.getuser()
csv_file_path = fr'C:\Users\{username}\Desktop\ProjetDS\CDE_Satisfaction2023\data\raw\cdiscount_reviews.csv'


df_all_pages = pd.DataFrame()

# Loop 
for page_num in range(1, num_pages + 1):
    page_url = f'{base_url}?page={page_num}'
    df_page = scrap_reviews(page_url)
    df_all_pages = pd.concat([df_all_pages, df_page], ignore_index=True)

df_all_pages.to_csv(csv_file_path, index=False)


##############
df_all_pages.head()