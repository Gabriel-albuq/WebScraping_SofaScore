import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta

from scrapers.sofascore_scraper import SofaScoreScraper
from utils.save_response_json import save_response_to_json
from utils.save_dataframe_csv import save_dataframe_to_csv

def get_matches_statistics(scraper, match_id):
        """
        Busca os dados de uma partida de uma rodada de um torneio específico e temporada.
        """
        url = f"https://www.sofascore.com/api/v1/event/{match_id}/statistics"
        return scraper._make_request(url)

def extract_matches_statistics(scraper, search_match):
    '''
    Extrair a resposta do servidor para as estatísticas

    :param scraper: Classe do SofaScoreScraper
    :return: A resposta do servidor para as estatísticas
    '''
    
    response_statistics = []
    for match_id in search_match:
        try:
            response_statistics.append({
                'match_id': match_id,
                'statistics': get_matches_statistics(scraper, match_id)
            })
        except:
            print(f"Erro na Match_id: {match_id}")
            pass

    return response_statistics

def transform_matches_statistics(response_matches):
    '''
    Pegar os dados de overview das partidas

    :param response_matches: A resposta do servidor ao scraper Matches
    :return: Um dataframe com o overview das partidas
    '''
    list_match_id = []
    list_period = [] 
    list_groupname = [] 
    list_name = [] 
    list_home = [] 
    list_away = [] 
    list_statisticstype = [] 
    list_key = []
    for match in response_matches:
        match_id = match["match_id"]
        statistics = match["statistics"]["statistics"]

        for stat in statistics:
            period = stat["period"]

            for group in stat["groups"]: 
                group_name = group["groupName"]

                for item in group["statisticsItems"]:
                    name = item["name"]
                    home = item["home"]
                    away = item["away"]
                    statistics_type = item["statisticsType"]
                    key = item["key"]

                    list_match_id.append(match_id)
                    list_period .append(period)
                    list_groupname.append(group_name) 
                    list_name.append(name) 
                    list_home.append(home) 
                    list_away.append(away) 
                    list_statisticstype.append(statistics_type) 
                    list_key.append(key)

    df_statistics = pd.DataFrame({
        'match_id' : list_match_id,
        'period' : list_period,
        'groupname' : list_groupname,
        'name' : list_name,
        'home' : list_home,
        'away' : list_away,
        'statistics' : list_statisticstype,
        'key' : list_key
    })

    return df_statistics

def load_matches_statistics(search_matc):
    scraper = SofaScoreScraper()

    response_matches_statistics = extract_matches_statistics(scraper, search_match)
    df_matches_statistics = transform_matches_statistics(response_matches_statistics)

    return response_matches_statistics, df_matches_statistics

if __name__ == "__main__":
    # Input
    save_path = r'data\outputs'
    input_path = r"data\outputs\silver\Matches 390-49058_390-59015_325-58766_325-48982 - 2025-03-15_14-14-26.csv"

    df_input = pd.read_csv(input_path)
    df_input = df_input.replace({np.nan: None})
    df_interest = df_input
    search_tournament_seasons = list(df_interest[['unique_tournament_id', 'season_id']].apply(tuple, axis=1))
    search_match = df_interest['match_id']

    print("------ Campeonatos/Temporadas/Rodadas Escolhidas ------")
    for _, tournament_season in df_interest.iterrows():
        print(tournament_season['unique_tournament_id'], "-", tournament_season['season_id'], "-", tournament_season['round'], "-", tournament_season['slug'])
    print("------------------------------------")

    response_matches_statistics, df_matches_statistics = load_matches_statistics(search_match)

    # Salvar
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    text_search_match = "_".join(set([f"{unique_tournament_id}-{season_id}" for unique_tournament_id, season_id in search_tournament_seasons]))
    title = f"Matches Statistics {text_search_match} - {datetime_now}"
    save_response_to_json(response_matches_statistics, save_path, title)
    save_dataframe_to_csv(df_matches_statistics, save_path, title)
   
