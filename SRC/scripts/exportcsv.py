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

# Categories, subcategories and number of subcateogies
        
    df_categories_sub_categories_number_sub_categories = pd.DataFrame(categories_sub_categories, columns=["cat","sous_cat", "number of sous_cat"])   


# Categories, resultats and links 


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
    
    return df_final.to_csv('new_file', index = False)