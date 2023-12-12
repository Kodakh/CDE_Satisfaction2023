# C'est ici que nous allons regrouper l'ensemble des fonctions qui allons devoir utiliser pour la récolte, le traitement, et l'exportation des données

# Fonction qui permet de récupérer le content d'une page web à partir d'une URL 
def getdata(url):
    page_category = requests.get(url)
    bs_category = bs(page_category.content, 'html.parser')
    return bs_category


# Fonction qui permet de faire défiler les pages web du site "Trustpilot.fr" qui retourne l'URL de la page actuelle
def getnextpage (bs_category):
    page = bs_category.find('div', {'class' : 'styles_paginationWrapper__fukEb styles_pagination__USObu'})
    
    if not page.find('a', {'class' : 'link_internal__7XN06 link_disabled__mIxH1 button_button__T34Lr button_m__lq0nA button_appearance-outline__vYcdF button_squared__21GoE link_button___108l pagination-link_disabled__7qfis pagination-link_next__SDNU4 pagination-link_rel__VElFy'}):
        url = page.find('a', {'class' :'link_internal__7XN06 button_button__T34Lr button_m__lq0nA button_appearance-outline__vYcdF button_squared__21GoE link_button___108l pagination-link_next__SDNU4 pagination-link_rel__VElFy'})
        url = 'https://fr.trustpilot.com' + url.get('href')
        
        return url 


# Fonction qui permet le tri à l'aide d'une conversion format 
def tri_personnalisé(item):
    if item == 'N/A':
        return float('inf')  # Placer 'N/A' à la fin de la liste
    else:
        return -float(item)  # Convertir en float et inverser l'ordre