import os
import sys
import pandas as pd
from datetime import datetime, timezone, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from scrapers.sofascore_scraper import SofaScoreScraper
from utils.save_response_json import save_response_to_json
from utils.save_dataframe_csv import save_dataframe_to_csv

def get_rounds(unique_tournament_id, season_id):
    """
    Busca os dados dos rounds de um torneio específico e temporada.
    """
    scraper = SofaScoreScraper()
    url = f"https://www.sofascore.com/api/v1/unique-tournament/{unique_tournament_id}/season/{season_id}/rounds"
    return scraper._make_request(url)

def extract_rounds(tournament_id, season_id):
    '''
    Extrair a resposta do servidor ao scraper das Rodadas

    :param scraper: Classe do SofaScoreScraper
    :return: A resposta do servidor ao scraper das Rodadas
    '''
    response_rounds= [{
        'unique_tournament_id': tournament_id,
        'season_id': season_id,
        'rounds': get_rounds(tournament_id, season_id)
    }]

    return response_rounds

def transform_rounds(response_rounds, datetime_now):
    '''
    Transformar os dados do response_rounds em um dataframe

    :param response_rounds: A resposta do servidor ao scraper rounds
    :return: Um dataframe com as temporadas
    '''
    list_unique_tournament_id = []
    list_season_id = []
    list_round = []
    list_slug = []
    list_updated_at = []
    list_season_id_round_slug = []
    for tournament_season in response_rounds:
        unique_tournament_id = tournament_season["unique_tournament_id"]
        season_id = tournament_season["season_id"]
        for round_data in tournament_season['rounds']['rounds']:
            round = round_data['round']
            try:
                slug = round_data['slug'] # Para jogos de copa é necessário pegar pelo slug, pois o round se repete
            except:
                 slug = None

            list_unique_tournament_id.append(unique_tournament_id)
            list_season_id.append(season_id)
            list_round.append(round)
            list_slug.append(slug)
            list_updated_at.append(datetime_now)

            if slug == None:
                list_season_id_round_slug.append(f"{season_id}{round}")
            else:
                list_season_id_round_slug.append(f"{season_id}{round}{slug}")

    # Criar DataFrame
    df_rounds = pd.DataFrame({
        'season_id_round_slug': list_season_id_round_slug,
        'unique_tournament_id': list_unique_tournament_id,
        'season_id': list_season_id,
        'round': list_round,
        'slug': list_slug,
        'updated_at': list_updated_at,
    })

    return df_rounds

def load_rounds(search_tournament_seasons_id, save_path, datetime_now):
    response_rounds_agg = []
    df_rounds_agg = pd.DataFrame()
    for tournament_id, season_id in search_tournament_seasons_id:
        title = f"Rounds - {tournament_id} - {season_id} - {datetime_now}"
        table = title.split(" - ")[0].lower()
        print(f"Extraindo: {title}")

        response_rounds = extract_rounds(tournament_id, season_id)
        df_rounds = transform_rounds(response_rounds, datetime_now)

        # Salvar
        save_response_to_json(response_rounds, save_path, title)
        save_dataframe_to_csv(df_rounds, save_path, title)

        # Agrupar
        response_rounds_agg.append(response_rounds)
        df_rounds_agg = pd.concat([df_rounds_agg, df_rounds], ignore_index=True)

    return response_rounds_agg, df_rounds_agg

if __name__ == "__main__":
    # Input
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_path = r'data\outputs'
    search_tournament_seasons_id = [("390", "49058")]

    response_rounds_agg, df_rounds_agg = load_rounds(search_tournament_seasons_id, save_path, datetime_now)

    

