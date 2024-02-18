def l3():
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