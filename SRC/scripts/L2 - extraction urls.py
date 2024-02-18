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