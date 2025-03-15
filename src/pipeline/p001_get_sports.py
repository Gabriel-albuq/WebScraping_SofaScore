import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from datetime import datetime

from scrapers.sofascore_scraper import SofaScoreScraper
from utils.save_response_json import save_response_to_json
from utils.save_dataframe_csv import save_dataframe_to_csv

def get_sports(scraper):
    """
    Busca os dados dos esportes disponíveis.
    """
    url = f"https://www.sofascore.com/api/v1/sport/-10800/event-count"
    return scraper._make_request(url)

def extract_sports(scraper):
    '''
    Extrair a resposta do servidor ao scraper dos Esportes

    :param scraper: Classe do SofaScoreScraper
    :return: A resposta do servidor ao scraper Sports
    '''
    response_sports = get_sports(scraper)

    return response_sports

def transform_sports(response_sports):
    '''
    Transformar os dados do response_sports em um dataframe

    :param response_sports: A resposta do servidor ao scraper Sports
    :return: Um dataframe com os esportes
    '''
    list_live = []
    list_total = []
    list_sports = []
    if response_sports:
        for sport_name, data_sport in response_sports.items():
            list_sports.append(sport_name)
            list_live.append(data_sport['live'])
            list_total.append(data_sport['total'])

    # Criar DataFrame
    df_sports = pd.DataFrame({
        'sport': list_sports,
        'live': list_live,
        'total': list_total
    })

    return df_sports

def load_sports():
    scraper = SofaScoreScraper()
    response_sports = extract_sports(scraper)
    df_sports = transform_sports(response_sports)

    return response_sports, df_sports

if __name__ == "__main__":
    # Inputs
    save_path = r'data\outputs'

    response_sports, df_sports = load_sports()
    
    # Salvar
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    title = f"Sports - {datetime_now}"
    save_response_to_json(response_sports, save_path, title)
    save_dataframe_to_csv(df_sports, save_path, title)
    

