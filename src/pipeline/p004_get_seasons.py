import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from datetime import datetime

from scrapers.sofascore_scraper import SofaScoreScraper
from utils.save_response_json import save_response_to_json
from utils.save_dataframe_csv import save_dataframe_to_csv

def get_seasons(scraper, tournament_id):
    """
    Busca os dados das seasons disponíveis no torneio.
    """
    url = f"https://www.sofascore.com/api/v1/unique-tournament/{tournament_id}/seasons"
    return scraper._make_request(url)

def extract_seasons(scraper, search_tournaments):
    '''
    Extrair a resposta do servidor ao scraper das Temporadas

    :param scraper: Classe do SofaScoreScraper
    :return: A resposta do servidor ao scraper das Temporadas
    '''
    response_seasons = []
    for unique_tournamen_id in search_tournaments:
        response_seasons.append({
            'unique_tournament_id': unique_tournamen_id,
            'seasons': get_seasons(scraper, unique_tournamen_id)
        })

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

def load_seasons(search_tournaments):
    scraper = SofaScoreScraper()
    response_seasons = extract_seasons(scraper, search_tournaments)
    df_seasons = transform_seasons(response_seasons)

    return response_seasons, df_seasons

if __name__ == "__main__":
    # Input
    save_path = r'data\outputs'
    input_path = r"data\outputs\silver\Tournaments 13 - 2025-03-15_13-36-34.csv" # Caminho para o arquivo com a lista de torneios
    search_interest_tournaments = ["Brasileirão Betano",
                                   "Brasileirão Série B"] # Lista com torneios de interesse
    
    df_input = pd.read_csv(input_path)
    df_interest = df_input[df_input['tournament_name'].str.contains('|'.join(search_interest_tournaments), case=False, na=False)]
    search_tournaments_id = df_interest['tournament_id']

    print("------ Campeonatos Escolhidos ------")
    for _, tournament in df_interest.iterrows():
        print(tournament['tournament_name'], "-", tournament['tournament_id'])
    print("------------------------------------")

    response_seasons, df_seasons = load_seasons(search_tournaments_id)

    # Salvar
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    text_search_tournaments = "_".join(df_interest['tournament_id'].astype(str).tolist())
    title = f"Seasons {text_search_tournaments} - {datetime_now}"
    save_response_to_json(response_seasons, save_path, title)
    save_dataframe_to_csv(df_seasons, save_path, title)
