from datetime import datetime
import sys
import os
import pandas as pd

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

if __name__ == "__main__":
    '''
    Pegar os dados iniciais, comuns para toda extração

    '''
    # Inputs
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_path = r'data\outputs'
    search_sports=['football']
    search_sports_countries_id = ['13']
    search_tournaments_id = ['390']
    search_tournament_seasons_id = [
                                        ('390', '72603'),
                                        ('390', '59015'),
                                        ('390', '49058'),
                                        ('390', '40560'),
                                        ('390', '36162'),
                                        ('390', '27593'),
                                        ('390', '22932'),
                                        ('390', '16184'),
                                        ('390', '13101'),
                                        ('390', '11430'),
                                        ('390', '10189'),
                                        ('390', '7780'),
                                        ('390', '6143'),
                                        ('390', '4480'),
                                        ('390', '3346'),
                                        ('390', '2685'),
                                        ('390', '2080'),
                                        ('390', '1224')
    ]
    search_tournament_seasons_id = [
                                        ('390', '59015'),
                                        ('390', '49058'),
                                        ('390', '40560'),
                                        ('390', '36162'),
                                        ('390', '27593'),
                                        ('390', '22932'),
                                        ('390', '16184'),
                                        ('390', '13101'),
                                        ('390', '11430'),
                                        ('390', '10189'),
                                        ('390', '7780')
    ]

    search_tournament_seasons_id = [('390', '59015')]
    
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

