# Ce script vise à nous donner un aperçu rapide du comportement des différents scripts (extraction, traitement) grâce à un affichage de différents dataframes
import pandas as pd 





# Création du dataframe noms_entreprises, trust_scores, nombres_d_avis et noms_des_categories
df_entreprises_page = pd.DataFrame(list(zip(noms_entreprises,urls_entreprises, trust_scores, nombres_d_avis,noms_des_categories)), columns = ["nom de l'entreprise",'URL', 'Note', "Nombre d'avis", "nom des catérogies"])
df_entreprises_page["Nombre d'avis"] = sorted(df_entreprises_page["Nombre d'avis"], key=tri_personnalisé)


df_entreprise_page = pd.DataFrame(list(zip(urls_entreprises, star_labels_entreprises,star_percentages_entreprises )), columns = ["URL", "star labels", "star percentages"])
df_entreprises_avec_toutes_infos_demandées = pd.merge(df_entreprises_page, df_entreprise_page, on = ['URL'], how = 'inner' )
df_entreprises_avec_toutes_infos_demandées