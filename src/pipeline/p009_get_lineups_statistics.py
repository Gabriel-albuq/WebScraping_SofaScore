import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta

from scrapers.sofascore_scraper import SofaScoreScraper
from utils.save_response_json import save_response_to_json
from utils.save_dataframe_csv import save_dataframe_to_csv

def get_lineups_statistics(scraper, match_id):
        """
        Busca as escalações de uma partida específica.
        """
        url = f"https://www.sofascore.com/api/v1/event/{match_id}/lineups"
        return scraper._make_request(url)

def extract_lineups_statistics(scraper, search_match):
    '''
    Extrair a resposta do servidor para as escalações

    :param scraper: Classe do SofaScoreScraper
    :return: A resposta do servidor para as escalações
    '''
    response_lineups = []
    for match_id in search_match:
        try:
            response_lineups.append({
                'match_id': match_id,
                'lineups': get_lineups_statistics(scraper, match_id)
            })
        except:
            print(f"Erro na Match_id: {match_id}")
            pass

    return response_lineups

def transform_lineups_statistics(response_matches):
    '''
    Pegar os dados de overview das partidas

    :param response_matches: A resposta do servidor ao scraper Matches
    :return: Um dataframe com o overview das partidas
    '''
    list_match_id = []
    list_home_or_away = [] 
    list_formation = []
    list_player_id = []
    list_player_name = []
    list_player_slug = []
    list_player_position = []
    list_player_number = []
    list_player_substitute = []
    list_player_captain = []
    list_player_out_reason = [] # 1: Machucado / 2: / 3: Suspenso
    list_player_country = []
    list_player_market_currency = []
    list_player_market_value = [] 
    list_player_brithdate = []
    list_player_statistic_name = []   
    list_player_statistic_value = []
    for match in response_matches:
        match_id = match["match_id"]

        for team_key in ["home", "away"]:
            team = match["lineups"].get(team_key, {})
            formation = team['formation']
            if team:  # Verifica se o time existe (não está vazio)
                # Relacionados
                for player in team.get("players", []):
                    home_or_away = (team_key)  # "home" ou "away"
                    formation = (formation)
                    player_id = (player["player"]["id"])
                    player_out_reason = (None)
                    try:
                        player_market_currency = (player["player"]["proposedMarketValueRaw"]["currency"])
                        player_market_value = (player["player"]["proposedMarketValueRaw"]["value"])
                    except:
                        player_market_currency = (None)
                        player_market_value = (None)

                    try:
                        player_position = player["player"]["position"]
                    except:
                        player_position = None

                    try:
                        player_name = player["player"]["name"]
                    except:
                        player_name = None

                    try:
                        player_slug = player["player"]["slug"]
                    except:
                        player_slug = None

                    try:
                        player_country = player["player"]["country"]["name"]
                    except:
                        player_country = None

                    try:
                        brithdate = datetime.fromtimestamp(player["player"]["dateOfBirthTimestamp"], tz=timezone.utc)
                        player_brithdate = brithdate
                    except:
                        player_brithdate = None

                    try:
                        player_number = (player["player"]["jerseyNumber"])
                    except:
                        player_number = (None)

                    try:
                        player_substitute = (player["substitute"])
                    except:
                        player_substitute = (None)

                    try:
                        player_captain = (player["captain"]) # Apenas os capitães tem esse campo
                    except:
                        player_captain = (None)

                    try:
                        for stat_name, stat_value in player["statistics"].items():
                            list_match_id.append(match_id)
                            list_home_or_away.append(home_or_away)  # "home" ou "away"
                            list_formation.append(formation)
                            list_player_id.append(player_id)
                            list_player_name.append(player_name)
                            list_player_slug.append(player_slug)
                            list_player_market_currency.append(player_market_currency)
                            list_player_market_value.append(player_market_value)
                            list_player_position.append(player_position)
                            list_player_number.append(player_number)
                            list_player_country.append(player_country)
                            list_player_brithdate.append(player_brithdate)
                            list_player_substitute.append(player_substitute)
                            list_player_captain.append(player_captain)
                            list_player_out_reason.append(player_out_reason) 
                            list_player_statistic_name.append(stat_name)     
                            list_player_statistic_value.append(stat_value)
                    except:
                        list_match_id.append(match_id)
                        list_home_or_away.append(home_or_away)  # "home" ou "away"
                        list_formation.append(formation)
                        list_player_id.append(player_id)
                        list_player_name.append(player_name)
                        list_player_slug.append(player_slug)
                        list_player_market_currency.append(player_market_currency)
                        list_player_market_value.append(player_market_value)
                        list_player_position.append(player_position)
                        list_player_number.append(player_number)
                        list_player_country.append(player_country)
                        list_player_brithdate.append(player_brithdate)
                        list_player_substitute.append(player_substitute)
                        list_player_captain.append(player_captain)
                        list_player_out_reason.append(player_out_reason) 
                        list_player_statistic_name.append(None)     
                        list_player_statistic_value.append(None)               

                # Afastados não tem estatísticas

    df_lineups_statistics = pd.DataFrame({
        "match_id": list_match_id,
        "home_or_away": list_home_or_away,
        "formation": list_formation,
        "player_id": list_player_id,
        "player_name": list_player_name,
        "player_slug": list_player_slug,
        "list_player_country": list_player_country,
        "list_player_market_currency": list_player_market_currency,
        "list_player_market_value": list_player_market_value,
        "list_player_brithdate": list_player_brithdate,
        "player_position": list_player_position,
        "player_number": list_player_number,
        "player_substitute": list_player_substitute,
        "player_captain": list_player_captain,
        "player_out_reason": list_player_out_reason,
        "player_statistic_name": list_player_statistic_name,
        "player_statistic_value": list_player_statistic_value,
    })

    return df_lineups_statistics

def load_lineups_statistics(search_match):
    scraper = SofaScoreScraper()

    response_lineups = extract_lineups_statistics(scraper, search_match)
    df_lineups = transform_lineups_statistics(response_lineups)

    return response_lineups, df_lineups

if __name__ == "__main__":
    save_path = r'data\outputs'
    input_path = r"data\outputs\silver\Matches 390-49058_390-59015_325-58766_325-48982 - 2025-03-15_14-14-26.csv"

    df_input = pd.read_csv(input_path)
    df_input = df_input.replace({np.nan: None})
    df_interest = df_input
    search_tournament_seasons = list(df_interest[['unique_tournament_id', 'season_id']].apply(tuple, axis=1))
    search_match = df_interest['match_id']
    
    # print("------ Campeonatos/Temporadas/Rodadas Escolhidas ------")
    # for _, match in df_interest.iterrows():
    #     print(match['match_id'])  

    response_lineups, df_lineups_statistics = load_lineups_statistics(search_match)

    # Salvar
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    text_search_match = "_".join(set([f"{unique_tournament_id}-{season_id}" for unique_tournament_id, season_id in search_tournament_seasons]))
    title = f"Lineups Statistics {text_search_match} - {datetime_now}"
    save_response_to_json(response_lineups, save_path, title)
    save_dataframe_to_csv(df_lineups_statistics, save_path, title)
