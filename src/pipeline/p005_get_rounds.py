import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from datetime import datetime

from scrapers.sofascore_scraper import SofaScoreScraper
from utils.save_response_json import save_response_to_json
from utils.save_dataframe_csv import save_dataframe_to_csv

def get_rounds(scraper, unique_tournament_id, season_id):
    """
    Busca os dados dos rounds de um torneio específico e temporada.
    """
    url = f"https://www.sofascore.com/api/v1/unique-tournament/{unique_tournament_id}/season/{season_id}/rounds"
    return scraper._make_request(url)

def extract_rounds(scraper, search_tournament_seasons):
    '''
    Extrair a resposta do servidor ao scraper das Rodadas

    :param scraper: Classe do SofaScoreScraper
    :return: A resposta do servidor ao scraper das Rodadas
    '''
    response_rounds = []
    for unique_tournament_id, season_id in search_tournament_seasons:
        response_rounds.append({
            'unique_tournament_id': unique_tournament_id,
            'season_id': season_id,
            'rounds': get_rounds(scraper, unique_tournament_id, season_id)
        })

    return response_rounds

def transform_rounds(response_rounds):
    '''
    Transformar os dados do response_rounds em um dataframe

    :param response_rounds: A resposta do servidor ao scraper rounds
    :return: Um dataframe com as temporadas
    '''
    list_unique_tournament_id = []
    list_season_id = []
    list_round = []
    list_slug = []
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

    # Criar DataFrame
    df_rounds = pd.DataFrame({
        'unique_tournament_id': list_unique_tournament_id,
        'season_id': list_season_id,
        'round': list_round,
        'slug': list_slug
    })

    return df_rounds

def load_rounds(search_tournament_seasons):
    scraper = SofaScoreScraper()

    response_rounds = extract_rounds(scraper, search_tournament_seasons)
    transform_rounds(response_rounds)
    df_rounds = transform_rounds(response_rounds)

    return response_rounds, df_rounds

if __name__ == "__main__":
    # Input
    save_path = r'data\outputs'
    input_path = r"data\outputs\silver\Seasons 325_390 - 2025-03-15_14-09-28.csv"
    search_interest_tournaments = ["Brasileirão Betano",
                                "Brasileirão Série A",
                                "Brasileiro Serie B"] # Lista com torneios de interesse
    search_interest_seasons = ["2023", 
                                "2024"]
    
    df_input = pd.read_csv(input_path)
    df_interest = df_input[df_input['tournament_season_name'].str.contains("|".join(search_interest_tournaments), case=False, na=False)]
    df_interest = df_input[df_input['season_year'].str.contains("|".join(search_interest_seasons), case=False, na=False)]
    search_tournament_seasons = list(df_interest[['unique_tournament_id', 'season_id']].apply(tuple, axis=1))

    print("------ Campeonatos Escolhidos ------")
    for _, tournament_season in df_interest.iterrows():
        print(tournament_season['unique_tournament_id'], "-", tournament_season['tournament_season_name'], "-", tournament_season['season_year'], "-", tournament_season['season_id'])
    print("------------------------------------")

    response_rounds, df_rounds = load_rounds(search_tournament_seasons)
    
    # Salvar
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    text_search_tournaments_seasons = "_".join([f"{tournament}-{season}" for tournament, season in search_tournament_seasons])
    title = f"Rounds {text_search_tournaments_seasons} - {datetime_now}"
    save_response_to_json(response_rounds, save_path, title)
    save_dataframe_to_csv(df_rounds, save_path, title)
