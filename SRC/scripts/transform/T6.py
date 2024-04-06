import pandas as pd
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
from tqdm import tqdm

SIA = SentimentIntensityAnalyzer()

print("Chargement du fichier CSV...")
df = pd.read_csv('data/processed/L5_processed.csv')
print("Fichier CSV chargé avec succès.")

# Initialize the 'scores' column with empty values
df['scores'] = ''

# Initialiser la barre de progression
progress_bar = tqdm(total=len(df), desc="Analyse de sentiment")

# Effectuer l'analyse de sentiment pour chaque ligne du DataFrame
for index, row in df.iterrows():
    df.at[index, 'scores'] = SIA.polarity_scores(row['review'])
    
    # Mettre à jour la barre de progression après chaque itération
    progress_bar.update(1)

# Fermer la barre de progression
progress_bar.close()

print("Analyse de sentiment terminée.")

print("Enregistrement du DataFrame dans un fichier CSV...")
df.to_csv('data/processed/L6_processed.csv', index=False)
print("Enregistrement terminé.")