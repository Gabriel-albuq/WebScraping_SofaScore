import os
import sys
import pandas as pd
from datetime import datetime, timezone, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from scrapers.sofascore_scraper_playwright import SofaScoreScraper
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
    Extrair a resposta do servidor ao scraper dos Países

    :param sport: Nome do esporte para buscar os países
    :return: A resposta do servidor ao scraper dos Países
    '''
    try:
        response_countries = [{
            'sport': sport,
            'countries': get_countries(sport)
        }]
        if not isinstance(response_countries[0]['countries'], dict):
            print(f"Erro ao buscar países para o esporte {sport}: resposta inválida.")
            return None
    except Exception as e:
        print(f"Erro ao buscar dados dos países para o esporte {sport}: {str(e)}")
        response_countries = None
    
    return response_countries

def transform_countries(response_countries, datetime_now):
    '''
    Transformar os dados do response_countries em um dataframe

    :param response_countries: A resposta do servidor ao scraper countries
    :param datetime_now: Data e hora atuais
    :return: Um dataframe com os Países
    '''
    list_sport = []
    list_country_name = []
    list_sport_country_id = []
    list_updated_at = []
    
    if response_countries:
        for sport_countries in response_countries:
            if 'countries' in sport_countries:
                for country in sport_countries['countries'].get('uniqueTournaments', []):
                    if 'category' in country and 'name' in country['category'] and 'id' in country['category']:
                        list_sport.append(sport_countries['sport'])
                        list_country_name.append(country['category']['name'])
                        list_sport_country_id.append(country['category']['id'])
                        list_updated_at.append(datetime_now)
                    else:
                        print(f"Dados faltando ou inválidos para o país: {country}")
            else:
                print(f"Dados de países ausentes para o esporte: {sport_countries['sport']}")
    else:
        print("Resposta dos países está vazia ou inválida.")

    # Criar DataFrame
    df_countries = pd.DataFrame({
        'sport_country_id': list_sport_country_id,
        'sport': list_sport,
        'country_name': list_country_name,
        'updated_at': list_updated_at
    })

    return df_countries

def load_countries(search_sports, save_path, datetime_now):
    response_countries_agg = []
    df_countries_agg = pd.DataFrame()
    
    for sport in search_sports:
        title = f"Countries - {sport} - {datetime_now}"
        table = title.split(" - ")[0].lower()
        print(f"Extraindo: {title}")
        
        response_countries = extract_countries(sport)
        if response_countries:
            df_countries = transform_countries(response_countries, datetime_now)

            # Salvar
            save_response_to_json(response_countries, save_path, title)
            save_dataframe_to_csv(df_countries, save_path, title)

            # Agrupar
            response_countries_agg.append(response_countries)
            df_countries_agg = pd.concat([df_countries_agg, df_countries], ignore_index=True)
        else:
            print(f"Não foi possível extrair dados para o esporte: {sport}")
        
    return response_countries_agg, df_countries_agg

if __name__ == "__main__":
    # Input
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_path = r'data\outputs'
    search_sports = ['football']  # Escolher o Esporte

    response_countries_agg, df_countries_agg = load_countries(search_sports, save_path, datetime_now)
