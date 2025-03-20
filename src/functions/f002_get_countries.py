import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from datetime import datetime

from scrapers.sofascore_scraper import SofaScoreScraper
from utils.save_response_json import save_response_to_json
from utils.save_dataframe_csv import save_dataframe_to_csv

def get_countries(sport):
        """
        Busca os dados de todos os países disponíveis.
        """
        scraper = SofaScoreScraper()
        url = f"https://www.sofascore.com/api/v1/config/default-unique-tournaments/BR/{sport}"
        return scraper._make_request(url)

def extract_countries(sport):
    '''
    Extrair a resposta do servidor ao scraper dos dos Países

    :param scraper: Classe do SofaScoreScraper
    :return: A resposta do servidor ao scraper dos Países
    '''
    response_countries = [{
        'sport': sport,
        'countries': get_countries(sport)
    }]

    return response_countries

def transform_countries(response_countries):
    '''
    Transformar os dados do response_countries em um dataframe

    :param response_countries: A resposta do servidor ao scraper countries
    :return: Um dataframe com os Torneios
    '''
    list_sport = []
    list_country_name = []
    list_sport_country_id = []
    for sport_countries in response_countries:
        for country in sport_countries['countries']['uniqueTournaments']:
            list_sport.append(sport_countries['sport'])
            list_country_name.append(country['category']['name'])
            list_sport_country_id .append(country['category']['id'])

    # Criar DataFrame
    df_countries = pd.DataFrame({
        'sport': list_sport,
        'country_name': list_country_name,
        'sport_country_id': list_sport_country_id ,
    })

    return df_countries

def load_countries(search_sports, save_path, datetime_now):
    response_countries_agg = []
    df_countries_agg = pd.DataFrame()
    for sport in search_sports:
        title = f"Countries - {sport} - {datetime_now}"
        print(f"Extraindo: {title}")
        response_countries = extract_countries(sport)
        df_countries = transform_countries(response_countries)
        df_countries = df_countries.drop_duplicates()

        # Salvar
        save_response_to_json(response_countries, save_path, title)
        save_dataframe_to_csv(df_countries, save_path, title)

        # Agrupar
        response_countries_agg.append(response_countries)
        df_countries_agg = pd.concat([df_countries_agg, df_countries], ignore_index=True)
        
    return response_countries_agg, df_countries_agg

if __name__ == "__main__":
    # Input
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_path = r'data\outputs'
    search_sports = ['football'] # Escolher o Esporte

    response_countries_agg, df_countries_agg = load_countries(search_sports, save_path, datetime_now)

        