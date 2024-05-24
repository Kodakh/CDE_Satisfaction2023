from bs4 import BeautifulSoup
import requests
import pandas as pd
import getpass
import time
import datetime
import os


# Fonction pour extraire les commentaires d'une page Trustpilot FR
def scrap_reviews(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    authors = []
    contents = []
    dates = []
    notes = []
    response_titles = []
    response_dates = []
    response_contents = []

    reviews = soup.find_all('div', class_='styles_reviewCardInner__EwDq2')

    for review in reviews:
        # Auteur client
        author = review.find('span', class_='typography_heading-xxs__QKBS8').text.strip()
        authors.append(author)

        # Contenu commentaire
        content_element = review.find('p', class_='typography_body-l__KUYFJ')
        content = content_element.text.strip() if content_element else None
        contents.append(content)

        # Date
        date = review.find('time')['datetime']
        formatted_date = pd.to_datetime(date).strftime('%d/%m/%Y')
        dates.append(formatted_date)

        # Note
        note_element = review.find('img', class_='icon_icon__ECGRl')
        if note_element and 'alt' in note_element.attrs:
            note = int(note_element['alt'].split()[1])
        else:
            note = int(review.find('div', {'data-service-review-rating': True})['data-service-review-rating'])
        notes.append(note)

        # Réponse de Cdiscount
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

    df = pd.DataFrame({
        'author': authors,
        'review': contents,
        'review_date': dates,
        'note': notes,
        'response_yesno': response_titles,
        'response_date': response_dates,
        'response': response_contents,
    })

    return df

# Paramètres de scraping
base_url = 'https://fr.trustpilot.com/review/www.cdiscount.com'

output_directory = '/data/ext'  

if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    print(f"Creation du repertoire: {output_directory}") 

num_pages = 5  # Nombre de pages à scraper
start_page = 1  # Page de départ

df_all_pages = pd.DataFrame()

for page_num in range(start_page, start_page + num_pages):
    page_url = f'{base_url}?page={page_num}'

    try:
        df_page = scrap_reviews(page_url)
        df_all_pages = pd.concat([df_all_pages, df_page], ignore_index=True)
        print(f"Scraping page {page_num} OK")
    except Exception as e:
        print(f"Error scraping page {page_num}: {e}")

today = datetime.datetime.now()
date_string = today.strftime("%Y-%m-%d")
csv_file_name = f'reviews_{date_string}_raw.csv'
csv_file_path = os.path.join(output_directory, csv_file_name)
df_all_pages.to_csv(csv_file_path, index=False)
print(f"Fichier CSV créé : {csv_file_path}")