from datetime import datetime
import sys
import os
import pandas as pd
import logging

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.pipeline.p001_extract.utils.u001_get_sports import load_sports
from src.pipeline.p001_extract.utils.u002_get_countries import load_countries
from src.pipeline.p001_extract.utils.u003_get_tournaments import load_tournaments
from src.pipeline.p001_extract.utils.u004_get_seasons import load_seasons
from src.pipeline.p001_extract.utils.u005_get_rounds import load_rounds
from src.pipeline.p001_extract.utils.u006_get_matches import load_matches
from src.pipeline.p001_extract.utils.u007_get_matches_statistics import load_matches_statistics
from src.pipeline.p001_extract.utils.u008_get_lineups import load_lineups
from src.pipeline.p001_extract.utils.u009_get_lineups_statistics import load_lineups_statistics

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

if __name__ == "__main__":
    '''
    Pegar os dados iniciais, comuns para toda extração

    '''
    # Inputs
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_path = r'data\outputs'
    search_sports=['football']
    search_sports_countries_id = ['13']
    search_tournaments_id = [
                            '14659', # Acreano
                            '10294', # Alagoano
                            '13668', # Amapazão
                            '11702', # Amazonense
                            '374', # Baiano
                            '325', # BrasileirÃ£o Betano
                            '390', # BrasileirÃ£o Série B
                            '11682', # Brasiliense
                            '14650', # Capixaba
                            '92', #	Carioca
                            '376', # Catarinense
                            '378', # Cearense
                            '373', # Copa Betano do Brasil
                            '1596', # Copa do Nordeste
                            '377', # GaÃºcho
                            '381', # Goiano
                            '11664', # Maranhense
                            '11669', # Paraense
                            '10295', # Paraibano
                            '382', # Paranaense
                            '372', # Paulista Série A1
                            '380', # Pernambucano
                            '13353', # Piauiense
                            '11663', # Potiguar, 1 Divisão 
                            '14658', # Rondoniense
                            '14733', # Roraimense
                            '11665', # Sergipano
                            '11679', # Sul-Mato-Grossense
                            '14602', # Supercopa do Brasil
                            '14686', # Tocantinense
    ]



    search_tournament_seasons_id = [
                                        ('390', '59015'),
                                        ('390', '49058'),
                                        ('390', '40560'),
                                        ('390', '36162'),
                                        ('390', '27593'),
                                        ('390', '22932')
    ]
    
    # Extract
    response_sports_agg, df_sports_agg = load_sports(save_path, datetime_now)
    response_countries_agg, df_countries_agg = load_countries(search_sports, save_path, datetime_now)
    response_tournaments_agg, df_tournaments_agg = load_tournaments(search_sports_countries_id, save_path, datetime_now)
    response_seasons_agg, df_seasons_agg = load_seasons(search_tournaments_id, save_path, datetime_now)
    
    response_rounds_agg, df_rounds_agg = load_rounds(search_tournament_seasons_id, save_path, datetime_now)
    search_tournament_seasons_round_slug = [(str(int(row["unique_tournament_id"])), 
                                        str(int(row["season_id"])), 
                                        str(int(row["round"])), 
                                        None if pd.isna(row["slug"]) else str(row["slug"])
                                        ) for _, row in df_rounds_agg.iterrows()]

    response_matches_agg, df_matches_agg = load_matches(search_tournament_seasons_round_slug, save_path, datetime_now)
    search_match_id = df_matches_agg['match_id'].astype(int).astype(str).tolist()
    
    response_matches_statistics_agg, df_matches_statistics_agg = load_matches_statistics(search_match_id, save_path, datetime_now)
    response_lineups_agg, df_lineups_agg = load_lineups(search_match_id, save_path, datetime_now)
    response_lineups_statistics_agg, df_lineups_statistics_agg = load_lineups_statistics(search_match_id, save_path, datetime_now)

