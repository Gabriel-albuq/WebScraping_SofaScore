import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta

from scrapers.sofascore_scraper import SofaScoreScraper
from utils.save_response_json import save_response_to_json
from utils.save_dataframe_csv import save_dataframe_to_csv

def get_matches(scraper, unique_tournament_id, season_id, round, slug=None):
    """
    Busca os dados de uma partida de uma rodada de um torneio específico e temporada.
    """
    if slug:
        url = f"https://www.sofascore.com/api/v1/unique-tournament/{unique_tournament_id}/season/{season_id}/events/round/{round}/slug/{slug}"
    else:
        url = f"https://www.sofascore.com/api/v1/unique-tournament/{unique_tournament_id}/season/{season_id}/events/round/{round}"
    return scraper._make_request(url)

def extract_matches(scraper, search_tournament_seasons_round_slug):
    '''
    Extrair a resposta do servidor ao scraper das Partidas

    :param scraper: Classe do SofaScoreScraper
    :return: A resposta do servidor ao scraper das Partidas
    '''
    
    response_matches = []
    for unique_tournament_id, season_id, round, slug in search_tournament_seasons_round_slug:
        response_matches.append({
            'unique_tournament_id': unique_tournament_id,
            'season_id': season_id,
            'round': round,
            'slug': slug,
            'matches': get_matches(scraper, unique_tournament_id, season_id, round, slug)
        })

    return response_matches

def transform_matches(response_matches):
    '''
    Transformar os dados do response_matches em um dataframe

    :param response_matches: A resposta do servidor ao scraper matches
    :return: Um dataframe com as partidas
    '''
    list_unique_tournament_id = []
    list_season_id = []
    list_round = []
    list_slug = []
    list_tournament_name = []
    list_tournament_name = []
    list_match_id = []
    list_match_slug = []
    list_match_timestamp = []
    list_match_datetime = []
    list_home_team_id = []
    list_home_team_name = []
    list_home_score = []
    list_away_team_id = []
    list_away_team_name = []
    list_away_score = []
    list_cup_round_type = []
    for match in response_matches:
        unique_tournament_id = match["unique_tournament_id"]
        season_id = match["season_id"]
        round = match['round']
        slug = match['slug']
        for match_data in match['matches']['events']:
            tournament_name = match_data['tournament']['name']
            match_id = match_data['id']
            match_slug = match_data['slug']
            match_timestamp = int(match_data['startTimestamp'])
            match_datetime_utc = datetime.fromtimestamp(match_timestamp, tz=timezone.utc)
            match_datetime_br = match_datetime_utc.astimezone(timezone(timedelta(hours=-3)))
            home_team_id = match_data['homeTeam']['id']
            home_team_name = match_data['homeTeam']['name']
            away_team_id = match_data['awayTeam']['id']
            away_team_name = match_data['awayTeam']['name']

            try:
                home_score = match_data['homeScore']['current']
            except:
                home_score = None

            try:
                away_score = match_data['awayScore']['current']
            except:
                away_score = None

            try:
                cup_round_type = str(match_data['roundInfo']['cupRoundType'])
            except:
                cup_round_type = None
            
            list_unique_tournament_id.append(unique_tournament_id)
            list_season_id.append(season_id)
            list_round.append(round)
            list_slug.append(slug)
            list_tournament_name.append(tournament_name)
            list_match_id.append(match_id)
            list_match_slug.append(match_slug)
            list_match_timestamp.append(match_timestamp) # Não está pegando corretamente
            list_match_datetime.append(match_datetime_br) # # Não está pegando corretamente
            list_home_team_id.append(home_team_id)
            list_home_team_name.append(home_team_name)
            list_home_score.append(home_score)
            list_away_team_id.append(away_team_id)
            list_away_team_name.append(away_team_name)
            list_away_score.append(away_score)
            list_cup_round_type.append(cup_round_type)

    # Criar DataFrame
    df_matches = pd.DataFrame({
        'unique_tournament_id': list_unique_tournament_id,
        'season_id': list_season_id,
        'round': list_round,
        'slug': list_slug,
        'tournament_name': list_tournament_name,
        'match_id': list_match_id,
        'cup_round_type': list_cup_round_type,
        'match_slug': list_match_slug,
        'match_timestamp': list_match_timestamp,
        'match_datatime': list_match_datetime,
        'home_team_id': list_home_team_id,
        'home_team_name': list_home_team_name,
        'home_score': list_home_score,
        'away_score': list_away_score,
        'away_team_name': list_away_team_name,
        'away_team_id': list_away_team_id,
    })

    return df_matches

def load_matches(search_tournament_seasons_round_slug):
    scraper = SofaScoreScraper()

    response_matches = extract_matches(scraper, search_tournament_seasons_round_slug)
    df_matches = transform_matches(response_matches)

    return response_matches, df_matches

if __name__ == "__main__":
    # Input
    save_path = r'data\outputs'
    input_path = r"data\outputs\silver\Rounds 325-58766_325-48982_390-59015_390-49058 - 2025-03-15_14-10-35.csv"

    df_input = pd.read_csv(input_path)
    df_input = df_input.replace({np.nan: None})
    df_interest = df_input
    search_rounds = list(df_interest[['unique_tournament_id', 'season_id', 'round', 'slug']].apply(tuple, axis=1))
    
    print("------ Campeonatos/Temporadas/Rodadas Escolhidas ------")
    for _, tournament_season in df_interest.iterrows():
        print(tournament_season['unique_tournament_id'], "-", tournament_season['season_id'], "-", tournament_season['round'], "-", tournament_season['slug'])
    print("------------------------------------")

    response_matches, df_matches = load_matches(search_rounds)

    # Salvar
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    text_search_tournaments_seasons = "_".join(set([f"{unique_tournament_id}-{season_id}" for unique_tournament_id, season_id, round, slug in search_rounds]))
    title = f"Matches {text_search_tournaments_seasons} - {datetime_now}"
    save_response_to_json(response_matches, save_path, title)
    save_dataframe_to_csv(df_matches, save_path, title)
