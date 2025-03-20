import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta

from scrapers.sofascore_scraper import SofaScoreScraper
from utils.save_response_json import save_response_to_json
from utils.save_dataframe_csv import save_dataframe_to_csv

def get_lineups(match_id):
        """
        Busca as escalações de uma partida específica.
        """
        scraper = SofaScoreScraper()
        url = f"https://www.sofascore.com/api/v1/event/{match_id}/lineups"
        return scraper._make_request(url)

def extract_lineups(match_id):
    '''
    Extrair a resposta do servidor para as escalações

    :param scraper: Classe do SofaScoreScraper
    :return: A resposta do servidor para as escalações
    '''
    try:
        response_lineups = [{
            'match_id': match_id,
            'lineups': get_lineups(match_id)
        }]
    except:
        response_lineups = None
        print(f"Erro na Match_id: {match_id}")
        pass

    return response_lineups

def transform_lineups(response_matches):
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
    list_player_rating_sofascore = []
    for match in response_matches:
        match_id = match["match_id"]

        for team_key in ["home", "away"]:
            team = match["lineups"].get(team_key, {})
            formation = team['formation']
            if team:  # Verifica se o time existe (não está vazio)
                # Relacionados
                for player in team.get("players", []):
                    list_match_id.append(match_id)
                    list_home_or_away.append(team_key)  # "home" ou "away"
                    list_formation.append(formation)
                    list_player_id.append(player["player"]["id"])
                    list_player_out_reason.append(None)

                    try:
                        list_player_market_currency.append(player["player"]["proposedMarketValueRaw"]["currency"])
                        list_player_market_value.append(player["player"]["proposedMarketValueRaw"]["value"])
                    except:
                        list_player_market_currency.append(None)
                        list_player_market_value.append(None)

                    try:
                        list_player_position.append(player["player"]["position"])
                    except:
                        list_player_position.append(None)

                    try:
                        list_player_name.append(player["player"]["name"])
                    except:
                        list_player_name.append(None)

                    try:
                        list_player_slug.append(player["player"]["slug"])
                    except:
                        list_player_slug.append(None)

                    try:
                        list_player_country.append(player["player"]["country"]["name"])
                    except:
                        list_player_country.append(None)

                    try:
                        brithdate = datetime.fromtimestamp(player["player"]["dateOfBirthTimestamp"], tz=timezone.utc)
                        list_player_brithdate.append(brithdate)
                    except:
                        list_player_brithdate.append(None)

                    try:
                        list_player_number.append(player["player"]["jerseyNumber"])
                    except:
                        list_player_number.append(None)

                    try:
                        list_player_substitute.append(player["substitute"])
                    except:
                        list_player_substitute.append(None)

                    try:
                        list_player_captain.append(player["captain"]) # Apenas os capitães tem esse campo
                    except:
                        list_player_captain.append(None)

                    try:
                        list_player_rating_sofascore.append(player["statistics"]['rating'])
                    except:
                        list_player_rating_sofascore.append(None)

                # Afastados
                for player in team.get("missingPlayers", []):
                    list_match_id.append(match_id)
                    list_home_or_away.append(team_key)  # "home" ou "away"
                    list_formation.append(formation)
                    list_player_id.append(player["player"]["id"])
                    list_player_out_reason.append(None)
                    try:
                        list_player_market_currency.append(player["player"]["proposedMarketValueRaw"]["currency"])
                        list_player_market_value.append(player["player"]["proposedMarketValueRaw"]["value"])
                    except:
                        list_player_market_currency.append(None)
                        list_player_market_value.append(None)

                    try:
                        list_player_name.append(player["player"]["name"])
                    except:
                        list_player_name.append(None)

                    try:
                        list_player_slug.append(player["player"]["slug"])
                    except:
                        list_player_slug.append(None)

                    try:
                        list_player_country.append(player["player"]["country"]["name"])
                    except:
                        list_player_country.append(None)

                    try:
                        brithdate = datetime.fromtimestamp(player["player"]["dateOfBirthTimestamp"], tz=timezone.utc)
                        list_player_brithdate.append(brithdate)
                    except:
                        list_player_brithdate.append(None)

                    try:
                        list_player_position.append(player["player"]["position"])
                    except:
                        list_player_position.append(None)

                    try:
                        list_player_number.append(player["player"]["jerseyNumber"])
                    except:
                        list_player_number.append(None)

                    try:
                        list_player_substitute.append(player["substitute"])
                    except:
                        list_player_substitute.append(None)

                    try:
                        list_player_captain.append(player["captain"]) # Apenas os capitães tem esse campo
                    except:
                        list_player_captain.append(None)

                    try:
                        list_player_rating_sofascore.append(player["statistics"]['rating'])
                    except:
                        list_player_rating_sofascore.append(None)

    df_lineups = pd.DataFrame({
        "match_id": list_match_id,
        "home_or_away": list_home_or_away,
        "formation": list_formation,
        "player_id": list_player_id,
        "player_name": list_player_name,
        "player_slug": list_player_slug,
        "list_country": list_player_country,
        "list_market_currency": list_player_market_currency,
        "list_market_value": list_player_market_value,
        "list_brithdate": list_player_brithdate,
        "player_position": list_player_position,
        "player_number": list_player_number,
        "player_substitute": list_player_substitute,
        "player_captain": list_player_captain,
        "player_out_reason": list_player_out_reason,
        "player_rating_sofascore": list_player_rating_sofascore
    })

    return df_lineups

def load_lineups(search_match_id, save_path, datetime_now):
    response_lineups_agg = []
    df_lineups_agg = pd.DataFrame()
    for match_id in search_match_id:
        title = f"Lineups - {match_id} - {datetime_now}"
        print(f"Extraindo: {title}")
        response_lineups = extract_lineups(match_id)

        if response_lineups != None:
            df_lineups = transform_lineups(response_lineups)

            # Salvar
            save_response_to_json(response_lineups, save_path, title)
            save_dataframe_to_csv(df_lineups, save_path, title)

            # Agrupar
            response_lineups_agg.append(response_lineups)
            df_lineups_agg = pd.concat([df_lineups_agg, df_lineups], ignore_index=True)

    return response_lineups_agg, df_lineups_agg

if __name__ == "__main__":
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_path = r'data\outputs'
    search_match_id = ["12146574", "12146576"]

    response_lineups_agg, df_lineups_agg = load_lineups(search_match_id, save_path, datetime_now)

   