from bs4 import BeautifulSoup
import requests

url = "https://fr.trustpilot.com/review/www.cdiscount.com"  # l'URL de l'entreprise dont il faut scrap les avis
response = requests.get(url)

# Entrée RAW (variable "html" =>> .text)
html = response.text
soup = BeautifulSoup(html, 'html.parser')



# Traitement données (variables "total_reviews", "star_labels", "star_ratings", "total_reviews", "star_labels", "star_percentages")
total_reviews = soup.find('p', {'data-reviews-count-typography': True}).text
star_labels = soup.find_all('p', {'data-rating-label-typography': True})
star_ratings = soup.find_all('div', {'data-star-rating': True})
total_reviews = soup.find('p', {'data-reviews-count-typography': True}).text
star_labels = soup.find_all('p', {'data-rating-label-typography': True})
star_percentages = soup.find_all('p', {'data-rating-distribution-row-percentage-typography': True})

star_reviews = {}


for i in range(len(star_labels)):
    star_name = star_labels[i].text.strip()
    star_percentage = star_percentages[i].text.strip()
    star_reviews[star_name] = star_percentage

print("Nombre d'avis total :", total_reviews)
for star_name, star_percentage in star_reviews.items():
    print(f"Nombre d'avis {star_name} :", star_percentage)

url = "https://fr.trustpilot.com/review/www.cdiscount.com"  # l'URL de l'entreprise dont il faut scrap les avis
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')
total_reviews = soup.find('p', {'data-reviews-count-typography': True}).text

star_labels = soup.find_all('p', {'data-rating-label-typography': True})
star_ratings = soup.find_all('div', {'data-star-rating': True})

total_reviews = soup.find('p', {'data-reviews-count-typography': True}).text


star_labels = soup.find_all('p', {'data-rating-label-typography': True})
star_percentages = soup.find_all('p', {'data-rating-distribution-row-percentage-typography': True})

star_reviews = {}


for i in range(len(star_labels)):
    star_name = star_labels[i].text.strip()
    star_percentage = star_percentages[i].text.strip()
    star_reviews[star_name] = star_percentage

print("Nombre d'avis total :", total_reviews)
for star_name, star_percentage in star_reviews.items():
    print(f"Nombre d'avis {star_name} :", star_percentage)