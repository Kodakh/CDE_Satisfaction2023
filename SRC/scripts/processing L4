import pandas as pd
import ast

# Fonction pour nettoyer et convertir les chaînes de catégories en listes
def clean_and_convert_categories(category_str):
    try:
        # Normaliser les guillemets pour créer une chaîne valide pour ast.literal_eval
        cleaned_str = category_str.replace('\'', '"').replace('["', "['").replace('"]', "']").replace('", "', "', '").replace('", "', "', '")
        # Convertir la chaîne nettoyée en liste
        return ast.literal_eval(cleaned_str)
    except Exception as e:
        print(f"Error converting category string: {category_str} | Exception: {e}")
        return []

# Exemple d'utilisation avec un DataFrame
chemin_fichier_csv = '/home/jben/Desktop/ProjetDS/CDE_Satisfaction2023/data/raw/details_entreprises_191223.csv'
df = pd.read_csv(chemin_fichier_csv)

# Post processing colonnes
df['nom_des_categories'] = df['nom_des_categories'].apply(clean_and_convert_categories)
df = df.dropna(subset=["Nombre d'avis"])
df["Nombre d'avis"] = df["Nombre d'avis"].astype(int)

# Afficher les résultats
print(df.head())

# Chemin du fichier de sortie
output_file_path = "/home/jben/Desktop/ProjetDS/CDE_Satisfaction2023/data/processed/L4_processed.csv"

# Exporter le DataFrame vers un fichier CSV
df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

# Chemin du fichier CSV à charger
fichier_csv_path = "/home/jben/Desktop/ProjetDS/CDE_Satisfaction2023/data/processed/L4_processed.csv"

# Chargement des données CSV depuis le fichier
df = pd.read_csv(fichier_csv_path, delimiter=',', quotechar='"')

# Utilisation de ast.literal_eval pour convertir les chaînes de la colonne 'nom_des_categories' en listes Python
df['nom_des_categories'] = df['nom_des_categories'].apply(lambda x: ast.literal_eval(x))

# Définition des règles pour assigner les sous-catégories
def assign_subcategory(categories):
    mapping = {
        "Magasin d'articles promotionnels": 'Ventes & marketing',
        "Boutique de cadeaux": 'Commerce de gros',
        "Service de stockage et de disques durs": 'Informatique & communication',
        "Papeterie": 'Locaux & fournitures de bureau',
        "Magasin de fête": 'Commerce de gros',
        "Fabricant d'articles de papeterie": 'Impression & design graphique',
        "Graphiste": 'Impression & design graphique',
        "Magasin d'impressions et de signalisation": 'Impression & design graphique',
        "Services de déménagement et de stockage": 'Transport & logistique',
        "Société de transport international de marchandises": 'Transport & logistique',
        "Service de transport": 'Transport & logistique',
        "Déménageur": 'Transport & logistique',
        "Entreprise de livraison": 'Transport & logistique',
        "Magasin de vitamines et compléments alimentaires": 'Commerce de gros',
        "Magasin d'alimentation bio": 'Commerce de gros',
        "Service e-commerce": 'Informatique & communication',
        "Fournisseur de cadeaux d'entreprise": 'Ventes & marketing',
        "Boutique de mariage": 'Associations & centres',
        "Magasin de souvenirs": 'Commerce de gros',
        "Entreprise de logiciels de comptabilité": 'Informatique & communication',
        "Agence de marketing en ligne": 'Ventes & marketing',
        "Concepteur de sites web": 'Informatique & communication',
        "Services aux entreprises": 'Administration & services',
        "Magasin de pièces et d'accessoires pour motos": 'Commerce de gros',
        "Fournisseur d'énergie": 'Informatique & communication',
        "Fournisseur d'énergie verte": 'Informatique & communication',
        "Courtier d'affaires": 'Ventes & marketing',
        "Centre d'appel": 'Informatique & communication',
        "Consultant média": 'Ventes & marketing',
        "Librairie": 'Ventes & marketing',
        "Bureau d'enregistrement": 'Informatique & communication',
        "Grossiste en accessoires électroniques": 'Commerce de gros',
        "Fabricant d'autocollants": 'Impression & design graphique',
        "Agence de talents": 'Ressources humaines & recrutement',
        "Entreprise de télécommunications": 'Informatique & communication',
        "Magasin de téléphonie mobile": 'Commerce de gros',
        "Fournisseur de service de courriel": 'Informatique & communication',
        "Grossiste en matériel de construction": 'Commerce de gros',
        "Fournisseur de matériel de bureau": 'Locaux & fournitures de bureau',
        "Magasin de matériel de bureau": 'Locaux & fournitures de bureau',
        "Centre de stockage": 'Transport & logistique',
        "Service de préparation des déclarations fiscales": 'Administration & services',
        "Magasin de fournitures de bureau": 'Locaux & fournitures de bureau',
        "Boutique de cartes de vœux": 'Impression & design graphique',
        "Service de visioconférence": 'Informatique & communication',
        "Imprimeur d'étiquettes personnalisées": 'Impression & design graphique',
        "Magasin d'impressions et de signalisation" : 'Impression & design graphique',
        "Magasin de portes" : 'Commerce de gros',
        "Graveur" : 'Impression & design graphique',
        "Imprimeur" : 'Impression & design graphique',
        "Espace de coworking" : 'Ventes & marketing',
        "Fournisseur de pierres": 'Commerce de gros',
        "Lapidaire": 'Commerce de gros',
        "Grossiste en pierres naturelles": 'Commerce de gros',
        "Magasin d'articles de loisirs": 'Commerce de gros',
        "Magasin de jeux": 'Commerce de gros',
        "Magasin d'informatique": 'Informatique & communication',
        "Fournisseur de composants électroniques": 'Commerce de gros',
        "Services de stockage d'archives": 'Administration & services',
        "Service de sécurité informatique": 'Informatique & communication',
        "Fournisseur de matériel de bureau": 'Locaux & fournitures de bureau',
        "Boutique de cartes de vœux": 'Impression & design graphique',
        "Service de visioconférence": 'Informatique & communication',
        "Agence de talents": 'Ressources humaines & recrutement',
        "Service de divertissement en entreprise": 'Associations & centres',
        "Société d'événementiel": 'Associations & centres',
        "Fournisseur de cadeaux d'entreprise": 'Ventes & marketing',
        "Boutique de souvenirs pour mariages": 'Commerce de gros',
        "Fabricant de souvenirs": 'Impression & design graphique',
        "Entreprise de logiciels": 'Informatique & communication',
        "Imprimeur d'étiquettes personnalisées": 'Impression & design graphique',
        "Magasin d'articles d'emballage": 'Commerce de gros',
        "Magasin de portes": 'Commerce de gros',
        "Graveur": 'Impression & design graphique',
        "Imprimeur": 'Impression & design graphique',
        "Centre de stockage": 'Transport & logistique',
        "Entrepôt": 'Transport & logistique',
        "Logiciel de préparation de déclaration des taxes": 'Informatique & communication',
        "Expert immobilier": 'Administration & services',
        "Service de détection d'amiante": 'Administration & services',
        "Centre de diagnostic": 'Administration & services',
        "Inspecteur en immobilier d'entreprise": 'Administration & services',
        "Inspecteur immobilier": 'Administration & services',
        "Service de paiement": 'Informatique & communication',
        "Service de marketing affilié": 'Ventes & marketing',
        "Service de transfert d'argent": 'Informatique & communication',
        "Plateforme de collaboration en ligne": 'Informatique & communication',
        "Magasin d'imprimantes et de scanners": 'Informatique & communication',
        "Fournisseur de cartouches d'encre": 'Commerce de gros',
        "Fournisseur de photocopieurs": 'Commerce de gros',
        "Entreprise de fabrication de plastique": 'Commerce de gros',
        "Fabricant de résine plastique": 'Commerce de gros',
        "Fournisseur de produits en plastique": 'Commerce de gros',
        "Grossiste en plastique": 'Commerce de gros',
        "Industrie plastique": 'Commerce de gros',
        "Fournisseur de feuilles de polyéthylène et de plastique": 'Commerce de gros',
    }

    subcategories = [mapping.get(category, 'Autre') for category in categories if category in mapping]
    return ', '.join(set(subcategories)) if subcategories else 'Autre'

# Assignation des sous-catégories
df['sous-categorie'] = df['nom_des_categories'].apply(assign_subcategory)

# Suppression de la colonne 'nom_des_categories'
df = df.drop(columns=['nom_des_categories'])

# Chemin du fichier CSV de sortie
output_csv_path = "/home/jben/Desktop/ProjetDS/CDE_Satisfaction2023/data/processed/L4_processed.csv"

# Exporter le DataFrame vers le fichier CSV
df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
