import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta

from scrapers.sofascore_scraper import SofaScoreScraper
from utils.save_response_json import save_response_to_json
from utils.save_dataframe_csv import save_dataframe_to_csv

def get_matches_statistics(match_id):
        """
        Busca os dados de uma partida de uma rodada de um torneio específico e temporada.
        """
        url = f"https://www.sofascore.com/api/v1/event/{match_id}/statistics"
        scraper = SofaScoreScraper()
        return scraper._make_request(url)

def extract_matches_statistics(match_id):
    '''
    Extrair a resposta do servidor para as estatísticas

    :param scraper: Classe do SofaScoreScraper
    :return: A resposta do servidor para as estatísticas
    '''
    
    try:
        response_statistics = [{
            'match_id': match_id,
            'statistics': get_matches_statistics(match_id)
        }]
    except:
        response_statistics = None
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

def load_matches_statistics(search_match_id, save_path, datetime_now):
    response_matches_statistics_agg = []
    df_matches_statistics_agg = pd.DataFrame()
    for match_id in search_match_id:
        title = f"Matches Statistics - {match_id} - {datetime_now}"
        print(f"Extraindo: {title}")
        response_matches_statistics = extract_matches_statistics(match_id)
        if response_matches_statistics != None:
            df_matches_statistics = transform_matches_statistics(response_matches_statistics)

            # Salvar
            save_response_to_json(response_matches_statistics, save_path, title)
            save_dataframe_to_csv(df_matches_statistics, save_path, title)

            # Agrupar
            response_matches_statistics_agg.append(response_matches_statistics)
            df_matches_statistics_agg = pd.concat([df_matches_statistics_agg, df_matches_statistics], ignore_index=True)

    return response_matches_statistics_agg, df_matches_statistics_agg

if __name__ == "__main__":
    # Input
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_path = r'data\outputs'
    search_match_id = ["12146574", "12146576"]

    response_matches_statistics_agg, df_matches_statistics_agg = load_matches_statistics(search_match_id, save_path, datetime_now)
    
    

   
