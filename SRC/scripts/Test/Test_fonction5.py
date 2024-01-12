from bs4 import BeautifulSoup
import requests
import pandas as pd
import getpass
import time

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
num_pages = 500




df_all_pages = pd.DataFrame()




# Loop starting from the specified page
start_page = 1

for page_num in range(start_page, num_pages + 1):
    page_url = f'{base_url}?page={page_num}'
    df_page = scrap_reviews(page_url)
    df_all_pages = pd.concat([df_all_pages, df_page], ignore_index=True)

    username = getpass.getuser()
    csv_file_path = fr'C:\Users\{username}\Desktop\ProjetDS\CDE_Satisfaction2023\data\raw\cdiscount_reviews_080124.csv'



    # Pause 
    if page_num % 3 == 0 or page_num == num_pages:
        if page_num < num_pages:
            print(f"Sleeping after scraping page {page_num}")
            time.sleep(5)  # Pause 
        else:
            print("Scraping complete.")



df_all_pages.to_csv(csv_file_path, index=False)