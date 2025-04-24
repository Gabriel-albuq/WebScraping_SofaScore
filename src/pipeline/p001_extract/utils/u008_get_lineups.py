import os
import sys
import pandas as pd
from datetime import datetime, timezone
from scrapers.sofascore_scraper_playwright import SofaScoreScraper
from utils.save_response_json import save_response_to_json
from utils.save_dataframe_csv import save_dataframe_to_csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

def get_lineups(match_id):
    """Busca as escalações de uma partida específica."""
    scraper = SofaScoreScraper()
    url = f"https://www.sofascore.com/api/v1/event/{match_id}/lineups"
    return scraper._make_request(url)

def extract_lineups(match_id):
    """Extrai a resposta do servidor para as escalações"""
    try:
        return [{
            'match_id': match_id,
            'lineups': get_lineups(match_id)
        }]
    except:
        print(f"Erro na Match_id: {match_id}")
        return None

def transform_lineups(response_matches):
    """Transforma os dados das escalações em um dataframe"""
    data = {
        'match_id_player_id': [], 'match_id': [], 'home_or_away': [], 'formation': [],
        'player_id': [], 'player_name': [], 'player_slug': [], 'list_country': [],
        'list_market_currency': [], 'list_market_value': [], 'list_brithdate': [], 
        'player_position': [], 'player_number': [], 'player_substitute': [],
        'player_captain': [], 'player_out_reason': [], 'player_rating_sofascore': []
    }

    for match in response_matches:
        match_id = match["match_id"]
        for team_key in ["home", "away"]:
            team = match["lineups"].get(team_key, {})
            formation = team['formation']
            if team:
                for player in team.get("players", []):
                    data['match_id_player_id'].append(f"{match_id}{player['player']['id']}")
                    data['match_id'].append(match_id)
                    data['home_or_away'].append(team_key)
                    data['formation'].append(formation)
                    data['player_id'].append(player["player"]["id"])
                    data['player_name'].append(player["player"].get("name"))
                    data['player_slug'].append(player["player"].get("slug"))
                    data['list_country'].append(player["player"].get("country", {}).get("name"))
                    data['list_market_currency'].append(player["player"].get("proposedMarketValueRaw", {}).get("currency"))
                    data['list_market_value'].append(player["player"].get("proposedMarketValueRaw", {}).get("value"))
                    data['list_brithdate'].append(datetime.fromtimestamp(player["player"].get("dateOfBirthTimestamp", 0), tz=timezone.utc))
                    data['player_position'].append(player["player"].get("position"))
                    data['player_number'].append(player["player"].get("jerseyNumber"))
                    data['player_substitute'].append(player.get("substitute"))
                    data['player_captain'].append(player.get("captain"))
                    data['player_out_reason'].append(None)
                    data['player_rating_sofascore'].append(player["statistics"].get('rating'))

                # Afastados (missingPlayers)
                for player in team.get("missingPlayers", []):
                    data['match_id_player_id'].append(f"{match_id}{player['player']['id']}")
                    data['match_id'].append(match_id)
                    data['home_or_away'].append(team_key)
                    data['formation'].append(formation)
                    data['player_id'].append(player["player"]["id"])
                    data['player_name'].append(player["player"].get("name"))
                    data['player_slug'].append(player["player"].get("slug"))
                    data['list_country'].append(player["player"].get("country", {}).get("name"))
                    data['list_market_currency'].append(player["player"].get("proposedMarketValueRaw", {}).get("currency"))
                    data['list_market_value'].append(player["player"].get("proposedMarketValueRaw", {}).get("value"))
                    data['list_brithdate'].append(datetime.fromtimestamp(player["player"].get("dateOfBirthTimestamp", 0), tz=timezone.utc))
                    data['player_position'].append(player["player"].get("position"))
                    data['player_number'].append(player["player"].get("jerseyNumber"))
                    data['player_substitute'].append(player.get("substitute"))
                    data['player_captain'].append(player.get("captain"))
                    data['player_out_reason'].append(None)
                    data['player_rating_sofascore'].append(player["statistics"].get('rating'))

    return pd.DataFrame(data)

def load_lineups(search_match_id, save_path, datetime_now):
    """Carrega as escalações para múltiplos match_ids e salva em arquivos"""
    df_lineups_agg = pd.DataFrame()
    for match_id in search_match_id:
        print(f"Extraindo: Lineups - {match_id} - {datetime_now}")
        response_lineups = extract_lineups(match_id)

        if response_lineups:
            df_lineups = transform_lineups(response_lineups)
            save_response_to_json(response_lineups, save_path, f"Lineups - {match_id} - {datetime_now}")
            save_dataframe_to_csv(df_lineups, save_path, f"Lineups - {match_id} - {datetime_now}")
            df_lineups_agg = pd.concat([df_lineups_agg, df_lineups], ignore_index=True)

    return df_lineups_agg

if __name__ == "__main__":
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_path = r'data\outputs'
    search_match_id = ["12146574", "12146576"]

    df_lineups_agg = load_lineups(search_match_id, save_path, datetime_now)
