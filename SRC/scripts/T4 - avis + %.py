import pandas as pd
import os
import re

csv_file_path = '/home/jben/Desktop/ProjetDS/CDE_Satisfaction2023/data/raw/details_entreprise_191223.csv'
df = pd.read_csv(csv_file_path)

# Nettoyer le nom de l'entreprise
df['entreprise'] = df['URL'].apply(lambda x: re.sub(r'www\.|\.com|\.fr|https://fr\.trustpilot\.com/review/', '', x))

# Fonction pour nettoyer et transformer les pourcentages des étoiles
def clean_and_split_percentages(s):
    # Enlever les symboles "%" et "<" et remplacer "<1" par "1"
    percentages = re.sub(r'[<%]', '', s)
    # Convertir la chaîne de caractères en liste
    percentages = eval(percentages)
    return percentages

# Appliquer la fonction de nettoyage et de séparation
df['star percentages'] = df['star percentages'].apply(clean_and_split_percentages)

# Créer des colonnes individuelles pour chaque note d'étoile
df[['%5 étoiles', '%4 étoiles', '%3 étoiles', '%2 étoiles', '%1 étoile']] = pd.DataFrame(df['star percentages'].tolist(), index=df.index)

# Supprimer les colonnes originales non nécessaires
df.drop(columns=['URL', 'star labels', 'star percentages'], inplace=True)


output_dir = 'CDE_Satisfaction2023/data/processed' 
if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)  # Crée le répertoire s'il n'existe pas

# Chemin du fichier de sortie
output_file_path = os.path.join(output_dir, 'L3_processed.csv')

# Sauvegarder le DataFrame dans le fichier CSV
df.to_csv(output_file_path, index=False)

print(f'Fichier sauvegardé avec succès à {output_file_path}')