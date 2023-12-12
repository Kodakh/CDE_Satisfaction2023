# import des fonctions + libraries
from bs4 import BeautifulSoup as bs
import requests 

# récupération des urls de toutes les pages de la catégorie choisie : 

url = "https://fr.trustpilot.com/categories/business_services"
urls = [url]  

while True : 
    bs_category = getdata(url)
    url = getnextpage (bs_category) 
    if not url :
        break
    urls.append(url) # J'ai mis les url dans une liste que j'ai appelée urls 

# Listes vides   

# Infos générales 
noms_entreprises = []
trust_scores = []
nombres_d_avis = []
noms_des_categories = []
urls_entreprises = []

# Pourcentages/ étoiles Trust/5
star_labels_entreprises = []
star_percentages_entreprises = []


# Boucle pour parcours des URL de la catégorie "Business Services"
for i in range(len(urls)):
        
    entreprise_details_page = requests.get(urls[i])
    bs_entreprise_details_page= bs(entreprise_details_page.content, 'html.parser')
    entreprises_details_page = bs_entreprise_details_page.find_all('div', {'class' : 'paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_wrapper__2JOo2'})



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


# Parcours des pages web

for url_entreprise in urls_entreprises : 
    page_entreprise = requests.get(url_entreprise)
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


# récupérer les noms des entreprises + traitement donnée

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