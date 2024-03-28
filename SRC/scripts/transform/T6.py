import pandas as pd
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
from tqdm import tqdm
from multiprocessing import Pool
import numpy as np

SIA = SentimentIntensityAnalyzer()

# Charger le fichier CSV
df = pd.read_csv('data/processed/L5_processed.csv')

# Diviser les données en chunks pour le traitement parallèle
num_chunks = 8  # Nombre de chunks (peut être ajusté selon le nombre de cœurs de processeur)
chunks = np.array_split(df, num_chunks)

# Fonction pour l'analyse de sentiment sur un chunk de données
def process_chunk(chunk):
    chunk['scores'] = chunk['review'].apply(lambda x: SIA.polarity_scores(x))
    return chunk

# Effectuer l'analyse de sentiment en parallèle
with Pool(num_chunks) as pool:
    chunks = list(tqdm(pool.imap(process_chunk, chunks), total=num_chunks))

# Concaténer les résultats des chunks en un seul DataFrame
df = pd.concat(chunks)

# Enregistrer le DataFrame modifié dans un nouveau fichier CSV
df.to_csv('data/processed/L6_processed.csv', index=False)