import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from datetime import datetime

from scrapers.sofascore_scraper import SofaScoreScraper
from utils.save_response_json import save_response_to_json
from utils.save_dataframe_csv import save_dataframe_to_csv

def get_tournaments(scraper, sport_country_id):
    """
    Busca os dados dos torneios disponíveis no esporte.
    """
    url = f"https://www.sofascore.com/api/v1/category/{sport_country_id}/unique-tournaments"
    return scraper._make_request(url)

def extract_tournaments(scraper, search_sports_countries):
    '''
    Extrair a resposta do servidor ao scraper dos Torneios

    :param scraper: Classe do SofaScoreScraper
    :return: A resposta do servidor ao scraper Torneios
    '''
    response_tournaments = []
    for sport_country_id in search_sports_countries:
        response_tournaments.append({
            'sport_country_id': sport_country_id,
            'tournaments': get_tournaments(scraper, sport_country_id)
        })

    return response_tournaments

def transform_tournaments(response_tournaments):
    '''
    Transformar os dados do response_tournaments em um dataframe

    :param response_tournaments: A resposta do servidor ao scraper Tournaments
    :return: Um dataframe com os Torneios
    '''
    list_sport_country_id = []
    list_tournament_name = []
    list_tournament_id = []
    list_category_name = []
    for sport_tournaments in response_tournaments:
        for group in sport_tournaments['tournaments']['groups']:
            for tournament in group['uniqueTournaments']:
                list_sport_country_id.append(sport_tournaments['sport_country_id'])
                list_tournament_name.append(tournament['name'])
                list_tournament_id.append(tournament['id'])
                list_category_name.append(tournament['category']['name'])

    # Criar DataFrame
    df_tournaments = pd.DataFrame({
        'sport_country_id': list_sport_country_id,
        'tournament_name': list_tournament_name,
        'tournament_id': list_tournament_id,
        'category_name': list_category_name
    })

    return df_tournaments

def load_tournaments(search_sports_countries):
    scraper = SofaScoreScraper()

    response_tournaments = extract_tournaments(scraper, search_sports_countries)
    df_tournaments = transform_tournaments(response_tournaments)

    return response_tournaments, df_tournaments

if __name__ == "__main__":
    # Input
    save_path = r'data\outputs'
    list_countries = ['13'] # Escolher o ID país. 1 = Inglaterra, 13 = Brasil

    response_tournaments, df_tournaments = load_tournaments(list_countries)
    text_tournaments = "-".join(list_countries)

    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    title = f"Tournaments {text_tournaments} - {datetime_now}"
    save_response_to_json(response_tournaments, save_path, title)
    save_dataframe_to_csv(df_tournaments, save_path, title)