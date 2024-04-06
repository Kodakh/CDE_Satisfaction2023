from scripts.extract.E5 import scrap_reviews, update_csv_with_new_data
import pandas as pd
import scripts.transform.T5 as T5
import scripts.transform.T6 as T6 
import scripts.transform.T7 as T7
import scripts.load.L7 as L7

def main():
    scrap_reviews()
    update_csv_with_new_data()
    T5.main()
    T6.main()
    T7.main()
    L7.main()
    
    print("Processus ETL terminé avec succès !")