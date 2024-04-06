import os
import pandas as pd
import re
from tqdm import tqdm

folder_path = 'data/raw/nosql'
all_files = os.listdir(folder_path)

# Filter out non-CSV files
csv_files = [f for f in all_files if f.endswith('.csv')]
df_list = []

for csv in tqdm(csv_files, desc="Reading CSV files"):
    file_path = os.path.join(folder_path, csv)
    try:
        # Try reading the file using default UTF-8 encoding
        df = pd.read_csv(file_path)
        df_list.append(df)
    except UnicodeDecodeError:
        try:
            # If UTF-8 fails, try reading the file using UTF-16 encoding with tab separator
            df = pd.read_csv(file_path, sep='\t', encoding='utf-16')
            df_list.append(df)
        except Exception as e:
            print(f"Could not read file {csv} because of error: {e}")
    except Exception as e:
        print(f"Could not read file {csv} because of error: {e}")

# Concatenate
big_df = pd.concat(df_list, ignore_index=True)

#############################
######## FIN COMPIL #########
#############################

# Drop duplicates
big_df = big_df.drop_duplicates()

# col "Réponse" 0/1
big_df['Réponse'] = big_df['Réponse'].fillna(0).map(lambda x: 1 if x else 0)
big_df = big_df.rename(columns={'Réponse': 'Response'})

# lowercase
big_df = big_df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)

# columns to lowercase
big_df.columns = map(str.lower, big_df.columns)

# Renames columns
big_df = big_df.rename(columns={'response': 'cdiscount_response'})
big_df = big_df.rename(columns={'date réponse': 'cdiscount_response_date'})
big_df = big_df.rename(columns={'contenu de la réponse': 'cdiscount_response_content'})
big_df = big_df.rename(columns={'content': 'review'})
big_df = big_df.rename(columns={'date': 'date_review'})

# Drop NA "reviews"
big_df = big_df.dropna(subset=['review'])

def clean_text(text):
    # Remplace "é", "è", "ê" par "e"
    text = re.sub(r"[éèê]", "e", text)
    # Remplace "ç" par "c"
    text = re.sub(r"ç", "c", text)
    return text
    # Ensuite, supprime tous les caractères non-ASCII
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    return text

big_df['review'] = big_df['review'].apply(clean_text)

def separate_punctuation(text):
    # Utilise une expression régulière pour insérer des espaces avant et après les caractères de ponctuation
    return re.sub(r"(\w)([.,;!?])", r"\1 \2 ", text)

tqdm.pandas(desc="Separating punctuation")
big_df['review'] = big_df['review'].progress_apply(separate_punctuation)


# Définir le répertoire de sortie
output_directory = 'data/processed'


# Vérifier si le répertoire de destination existe, sinon le créer
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Définir le chemin complet du fichier CSV de sortie
output_csv_path = os.path.join(output_directory, 'L5_processed.csv')

# Enregistrer le fichier CSV
big_df.to_csv(output_csv_path, index=False)

# Afficher un message indiquant que les données ont été sauvegardées
print(f"Data has been saved to {output_csv_path}")