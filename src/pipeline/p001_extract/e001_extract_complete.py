from datetime import datetime
import sys
import os

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

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
    search_tournament_seasons_id = [("390", "59015")]
    search_tournament_seasons_round_slug = [("390", "59015", "38", None)]
    search_match_id = ["12146271"]
    
    # Extract
    response_sports, df_sports = load_sports(save_path, datetime_now)
    response_countries, df_countries = load_countries(search_sports, save_path, datetime_now)
    response_tournaments, df_tournaments = load_tournaments(search_sports_countries_id, save_path, datetime_now)
    response_seasons, df_seasons = load_seasons(search_tournaments_id, save_path, datetime_now)
    response_rounds, df_rounds = load_rounds(search_tournament_seasons_id, save_path, datetime_now)
    response_matches_agg, df_matches_agg = load_matches(search_tournament_seasons_round_slug, save_path, datetime_now)
    response_matches_statistics_agg, df_matches_statistics_agg = load_matches_statistics(search_match_id, save_path, datetime_now)
    response_lineups_agg, df_lineups_agg = load_lineups(search_match_id, save_path, datetime_now)
    response_lineups_agg, df_lineups_agg = load_lineups_statistics(search_match_id, save_path, datetime_now)

