import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from datetime import datetime

from scrapers.sofascore_scraper import SofaScoreScraper
from utils.save_response_json import save_response_to_json
from utils.save_dataframe_csv import save_dataframe_to_csv

def get_seasons(tournament_id):
    """
    Busca os dados das seasons disponíveis no torneio.
    """
    scraper = SofaScoreScraper()
    url = f"https://www.sofascore.com/api/v1/unique-tournament/{tournament_id}/seasons"
    return scraper._make_request(url)

def extract_seasons(tournament_id):
    '''
    Extrair a resposta do servidor ao scraper das Temporadas

    :param scraper: Classe do SofaScoreScraper
    :return: A resposta do servidor ao scraper das Temporadas
    '''
    response_seasons = [{
        'unique_tournament_id': tournament_id,
        'seasons': get_seasons(tournament_id)
    }]

    return response_seasons

def transform_seasons(response_seasons):
    '''
    Transformar os dados do response_seasons em um dataframe

    :param response_seasons: A resposta do servidor ao scraper seasons
    :return: Um dataframe com as temporadas
    '''
    list_unique_tournament_id = []
    list_tournament_season_name = []
    list_season_year = []
    list_season_id = []
    for tournament_id in response_seasons:
        for season in tournament_id['seasons']['seasons']:
            list_unique_tournament_id.append(tournament_id['unique_tournament_id'])
            list_tournament_season_name.append(season['name'])
            list_season_year.append(season['year'])
            list_season_id.append(season['id'])

    # Criar DataFrame
    df_seasons = pd.DataFrame({
        'unique_tournament_id': list_unique_tournament_id,
        'tournament_season_name': list_tournament_season_name,
        'season_year': list_season_year,
        'season_id': list_season_id 
    })

    return df_seasons

def load_seasons(search_tournaments_id, save_path, datetime_now):
    response_seasons_agg = []
    df_seasons_agg = pd.DataFrame()
    for tournament_id in search_tournaments_id:
        title = f"Seasons - {tournament_id} - {datetime_now}"
        print(f"Extraindo: {title}")
        response_seasons = extract_seasons(tournament_id)
        df_seasons = transform_seasons(response_seasons)

        # Salvar
        save_response_to_json(response_seasons, save_path, title)
        save_dataframe_to_csv(df_seasons, save_path, title)

        # Agrupar
        response_seasons_agg.append(response_seasons)
        df_seasons_agg = pd.concat([df_seasons_agg, df_seasons], ignore_index=True)

    return response_seasons_agg, df_seasons_agg

if __name__ == "__main__":
    # Input
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_path = r'data\outputs'
    search_tournaments_id = ['390']

    response_seasons_agg, df_seasons_agg = load_seasons(search_tournaments_id, save_path, datetime_now)
