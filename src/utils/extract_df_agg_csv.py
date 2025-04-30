from glob import glob
import os   
import pandas as pd
import sys
import logging

# Configuração do logging
log_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'logs'))
os.makedirs(log_folder, exist_ok=True)

log_file = os.path.join(log_folder, 'sports_scraper.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def extract_df_agg_csv(files_dir):
    csv_files = glob(os.path.join(files_dir, "*.csv"))
    dfs = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            dfs.append(df)
        except Exception as e:
            print(f"Erro ao ler o arquivo {file}: {e}")

    if dfs:
        df_matches_agg = pd.concat(dfs, ignore_index=True)
        return df_matches_agg
    else:
        logging.warning(f"Nenhum DataFrame válido foi encontrado nos arquivos CSV")
        return None