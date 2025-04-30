from datetime import datetime
import sys
import os
import pandas as pd
import logging
from glob import glob
from tqdm import tqdm

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.utils.extract_df_agg_csv import extract_df_agg_csv
from src.utils.load_response_json import load_response_json
from src.utils.save_response_json import save_response_to_json
from src.utils.save_dataframe_csv import save_dataframe_to_csv

from src.pipeline.p001_extract_raw.utils.u001_get_sports import extract_sports, transform_sports
from src.pipeline.p001_extract_raw.utils.u002_get_countries import extract_countries, transform_countries
from src.pipeline.p001_extract_raw.utils.u003_get_tournaments import extract_tournaments, transform_tournaments
from src.pipeline.p001_extract_raw.utils.u004_get_seasons import extract_seasons, transform_seasons
from src.pipeline.p001_extract_raw.utils.u005_get_rounds import extract_rounds, transform_rounds
from src.pipeline.p001_extract_raw.utils.u006_get_matches import extract_matches, transform_matches
from src.pipeline.p001_extract_raw.utils.u007_get_matches_statistics import extract_matches_statistics, transform_matches_statistics
from src.pipeline.p001_extract_raw.utils.u008_get_lineups import extract_lineups, transform_lineups
from src.pipeline.p001_extract_raw.utils.u009_get_lineups_statistics import extract_lineups_statistics, transform_lineups_statistics

# Configuração do logging
log_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'logs'))
os.makedirs(log_folder, exist_ok=True)

log_file = os.path.join(log_folder, 'sports_scraper.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_all_tournaments_year(datetime_now, save_path, search_sports, search_sports_countries_id, ano, search_tournaments_id,
                             choice_extract_sports = 1, choice_transform_sports = 1,
                             choice_extract_countries = 1, choice_transform_countries = 1,
                             choice_extract_tournaments = 1, choice_transform_tournaments = 1,
                             choice_extract_seasons = 1, choice_transform_seasons = 1,
                             choice_extract_rounds = 1, choice_transform_rounds = 1,
                             choice_extract_matches = 1, choice_transform_matches = 1,
                             choice_extract_matches_statistics = 1, choice_transform_matches_statistics = 1,
                             choice_extract_lineups = 1, choice_transform_lineups = 1,
                             choice_extract_lineups_statistics = 1, choice_transform_lineups_statistics = 1,
                             ):
    # Sports
    if choice_extract_sports:
        for _ in tqdm(range(1), desc="Extraindo os dados dos esportes"):
            title = f"Sports - {datetime_now}"
            logging.info(f"Extraindo: {title}")

            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "raw", title_datetime, title_path)
            
            response_sports = extract_sports()
            if response_sports:
                save_response_to_json(response_sports, path, title)
            else:
                logging.error("Não foi possível extrair dados dos esportes.")

    if choice_transform_sports:
        for file_path in tqdm( glob(os.path.join(save_path, "raw", datetime_now, "Sports", "*.json")), desc="Transformando os dados dos esportes"):
            title = os.path.splitext(os.path.basename(file_path))[0]
            logging.info(f"Transformando: {title}")

            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "bronze", title_datetime, title_path)

            response_sports = load_response_json(file_path)
            if response_sports:
                df_sports = transform_sports(response_sports, title_datetime)
                save_dataframe_to_csv(df_sports, path, title)
            else:
                logging.error("Não foi possível transformar os dados dos esportes.")

    # Countries
    if choice_extract_countries:
        for sport in tqdm(search_sports, desc="Extraindo os países"):
            title = f"Countries - {sport} - {datetime_now}"
            logging.info(f"Extraindo: {title}")

            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "raw", title_datetime, title_path)
            
            response_countries = extract_countries(sport)
            if response_countries:
                save_response_to_json(response_countries, path, title)
            else:
                logging.error(f"Não foi possível extrair os dados dos países: {sport}")
                
    if choice_transform_countries:
        for file_path in tqdm( glob(os.path.join(save_path, "raw", datetime_now, "Countries", "*.json")), desc="Transformando os dados dos países"):
            title = os.path.splitext(os.path.basename(file_path))[0]
            logging.info(f"Transformando: {title}")

            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "bronze", title_datetime, title_path)

            response_countries = load_response_json(file_path)
            if response_countries:
                df_countries = transform_countries(response_countries, datetime_now)
                save_dataframe_to_csv(df_countries, path, title)
            else:
                logging.error("Não foi possível transformar os dados dos países.")

    # Tournaments
    if choice_extract_tournaments:
        for sport_country_id in tqdm(search_sports_countries_id, desc="Extraindo os torneios"):
            title = f"Tournaments - {sport_country_id} - {datetime_now}"
            logging.info(f"Extraindo: {title}")

            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "raw", title_datetime, title_path)
            
            response_tournaments = extract_tournaments(sport_country_id)
            if response_tournaments:
                save_response_to_json(response_tournaments, path, title)
            else:
                logging.error(f"Não foi possível extrair os dados para o país/ID: {sport_country_id}")

    if choice_transform_tournaments:
        for file_path in tqdm( glob(os.path.join(save_path, "raw", datetime_now, "Tournaments", "*.json")), desc="Transformando os dados dos torneios"):
            title = os.path.splitext(os.path.basename(file_path))[0]
            logging.info(f"Transformando: {title}")

            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "bronze", title_datetime, title_path)

            response_tournaments = load_response_json(file_path)
            if response_tournaments:
                df_tournaments = transform_tournaments(response_tournaments, datetime_now)
                save_dataframe_to_csv(df_tournaments, path, title)
            else:
                logging.error("Não foi possível transformar os dados dos países.")

    # Seasons
    if choice_extract_seasons:
        for tournament_id in tqdm(search_tournaments_id, desc="Extraindo as temporadas"):
            title = f"Seasons - {tournament_id} - {datetime_now}"
            logging.info(f"Extraindo: {title}")

            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "raw", title_datetime, title_path)

            response_seasons = extract_seasons(tournament_id)
            if response_seasons:
                save_response_to_json(response_seasons, path, title)
            else:
                logging.error(f"Não foi possível extrair os dados para o torneio: {tournament_id}")

    if choice_transform_seasons:
        for file_path in tqdm( glob(os.path.join(save_path, "raw", datetime_now, "Seasons", "*.json")), desc="Transformando os dados das temporadas"):
            title = os.path.splitext(os.path.basename(file_path))[0]
            logging.info(f"Transformando: {title}")

            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "bronze", title_datetime, title_path)

            response_seasons = load_response_json(file_path)
            if response_seasons:
                df_seasons = transform_seasons(response_seasons, datetime_now)
                save_dataframe_to_csv(df_seasons, path, title)
            else:
                logging.error("Não foi possível transformar os dados das temporadas.")

    # Rounds
    if choice_extract_rounds:
        df_extract = extract_df_agg_csv(os.path.join(save_path, "bronze", datetime_now, 'Seasons'))
        df_extract['season_year'] = df_extract['season_year'].astype(str)
        df_extract = df_extract[df_extract['season_year'] == ano]
        search_tournament_seasons_id = [tuple(map(str, raw)) for raw in df_extract[['unique_tournament_id', 'season_id']].drop_duplicates().to_numpy()]

        for tournament_id, season_id in tqdm(search_tournament_seasons_id, desc="Extraindo as rodadas"):    
            title = f"Rounds - {tournament_id} - {season_id} - {datetime_now}"
            logging.info(f"Extraindo: {title}")

            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "raw", title_datetime, title_path)

            response_rounds = extract_rounds(tournament_id, season_id)
            if response_rounds:
                save_response_to_json(response_rounds, path, title)
            else:
                logging.error(f"Não foi possível extrair os dados para o torneio e season: {tournament_id, season_id}")

    if choice_transform_rounds:
        for file_path in tqdm( glob(os.path.join(save_path, "raw", datetime_now, "Rounds", "*.json")), desc="Transformando os dados das rodadas"):
            title = os.path.splitext(os.path.basename(file_path))[0]
            logging.info(f"Transformando: {title}")

            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "bronze", title_datetime, title_path)

            response_rounds = load_response_json(file_path)
            if response_rounds:
                df_rounds = transform_rounds(response_rounds, datetime_now)
                save_dataframe_to_csv(df_rounds, path, title)
            else:
                logging.error("Não foi possível transformar os dados das rodadas.")

    # Matches
    if choice_extract_matches:
        df_extract = extract_df_agg_csv(os.path.join(save_path, "bronze", datetime_now, 'Rounds'))
        search_tournament_seasons_round_slug = [tuple(None if pd.isna(x) else str(x) for x in raw) for raw in df_extract[['unique_tournament_id', 'season_id', 'round', 'slug']].drop_duplicates().to_numpy()]
        for tournament_id, season_id, round, slug in tqdm(search_tournament_seasons_round_slug, desc="Extraindo as partidas"):  
            title = f"Matches - {tournament_id} - {season_id} - {round} - {slug} - {datetime_now}"
            logging.info(f"Extraindo: {title}")

            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "raw", title_datetime, title_path)
            
            response_matches = extract_matches(tournament_id, season_id, round, slug)
            if response_matches:
                save_response_to_json(response_matches, path, title)
            else:
                logging.error(f"Não foi possível extrair os dados para o torneio, temporada, rodada e slug: {tournament_id, season_id, round, slug}")

    if choice_transform_matches:
        for file_path in tqdm( glob(os.path.join(save_path, "raw", datetime_now, "Matches", "*.json")), desc="Transformando os dados das partidas"):
            title = os.path.splitext(os.path.basename(file_path))[0]
            logging.info(f"Transformando: {title}")

            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "bronze", title_datetime, title_path)

            response_matches = load_response_json(file_path)
            if response_matches:
                df_matches = transform_matches(response_matches, datetime_now)
                save_dataframe_to_csv(df_matches, path, title)
            else:
                logging.error("Não foi possível transformar os dados das partidas.")

    # Matches Statistics
    if choice_extract_matches_statistics:
        df_extract = extract_df_agg_csv(os.path.join(save_path, "bronze", datetime_now, 'Matches'))
        search_match_id = df_extract['match_id'].drop_duplicates()
        for match_id in tqdm(search_match_id, desc="Extraindo as estatísticas da partida"):  
            title = f"Matches Statistics - {match_id} - {datetime_now}"
            logging.info(f"Extraindo: {title}")

            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "raw", title_datetime, title_path)

            response_matches_statistics = extract_matches_statistics(match_id)
            if response_matches_statistics:
                save_response_to_json(response_matches_statistics, path, title)
            else:
                logging.error(f"Não foi possível extrair os dados para as estatísticas da partida")

    if choice_transform_matches_statistics:
        for file_path in tqdm( glob(os.path.join(save_path, "raw", datetime_now, "Matches Statistics", "*.json")), desc="Transformando os dados das estatísticas da partida"):
            title = os.path.splitext(os.path.basename(file_path))[0]
            logging.info(f"Transformando: {title}")

            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "bronze", title_datetime, title_path)

            response_matches_statistics = load_response_json(file_path)
            if response_matches_statistics:
                df_matches_statistics = transform_matches_statistics(response_matches_statistics, datetime_now)
                save_dataframe_to_csv(df_matches_statistics, path, title)
            else:
                logging.error("Não foi possível transformar os dados das estatísticas da partida.")

    # Lineups
    if choice_extract_lineups:
        df_extract = extract_df_agg_csv(os.path.join(save_path, "bronze", datetime_now, 'Matches'))
        search_match_id = df_extract['match_id'].drop_duplicates()
        for match_id in tqdm(search_match_id, desc="Extraindo os jogadores da partida"):
            title = f"Lineups - {match_id} - {datetime_now}"
            logging.info(f"Extraindo: Lineups - {match_id} - {datetime_now}")
            
            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "raw", title_datetime, title_path)

            response_lineups = extract_lineups(match_id)
            if response_lineups:
                save_response_to_json(response_lineups, path, title)
            else:
                logging.error(f"Não foi possível extrair os dados dos jogadores da partida")

    if choice_transform_lineups:
        for file_path in tqdm( glob(os.path.join(save_path, "raw", datetime_now, "Lineups", "*.json")), desc="Transformando os dados dos jogadores da partida"):
            title = os.path.splitext(os.path.basename(file_path))[0]
            logging.info(f"Transformando: {title}")

            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "bronze", title_datetime, title_path)

            response_lineups = load_response_json(file_path)
            if response_lineups:
                df_lineups = transform_lineups(response_lineups, datetime_now)
                save_dataframe_to_csv(df_lineups, path, title)
            else:
                logging.error("Não foi possível transformar os dados dos jogadores da partida.")

    # Lineups Statistics
    if choice_extract_lineups_statistics:
        df_extract = extract_df_agg_csv(os.path.join(save_path, "bronze", datetime_now, 'Matches'))
        search_match_id = df_extract['match_id'].drop_duplicates()
        for match_id in tqdm(search_match_id, desc="Extraindo as estatísticas dos jogadores da partida"):
            title = f"Lineups Statistics - {match_id} - {datetime_now}"
            logging.info(f"Extraindo: {title}")
            
            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "raw", title_datetime, title_path)

            response_lineups_statistics = extract_lineups_statistics(match_id)
            if response_lineups_statistics:
                save_response_to_json(response_lineups_statistics, path, title)
            else:
                logging.error(f"Não foi possível extrair os dados dos jogadores da partida")

    if choice_transform_lineups_statistics:
        for file_path in tqdm( glob(os.path.join(save_path, "raw", datetime_now, "Lineups Statistics", "*.json")), desc="Transformando os dados das estatísticas dos jogadores da partida"):
            title = os.path.splitext(os.path.basename(file_path))[0]
            logging.info(f"Transformando: {title}")

            title_path = title.split(" - ")[0]
            title_datetime = title.rsplit(" - ", 1)[-1]
            path = os.path.join(save_path, "bronze", title_datetime, title_path)

            response_lineups = load_response_json(file_path)
            if response_lineups:
                df_lineups = transform_lineups(response_lineups, datetime_now)
                save_dataframe_to_csv(df_lineups, path, title)
            else:
                logging.error("Não foi possível transformar os dados das estatísticas dos jogadores da partida.")

    # Marcar o fim
    end_time = datetime.now()
    
    # Calcular e exibir o tempo total
    total_time = end_time - start_time
    logging.info(f"Tempo total da extração: {total_time}")

if __name__ == "__main__":
    start_time = datetime.now() # Marcar o início

    ########## Inputs ##########
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    datetime_now = '2025-04-28_14-41-41'
    save_path = r'data\outputs'
    search_sports=['football']
    search_sports_countries_id = ['13']
    ano = "2023"
    search_tournaments_id = [
                            #'14659', # Acreano
                            #'10294', # Alagoano
                            #'13668', # Amapazão
                            #'11702', # Amazonense
                            #'374', # Baiano
                            '325', # BrasileirÃ£o Betano
                            #'390', # BrasileirÃ£o Série B
                            #'11682', # Brasiliense
                            #'14650', # Capixaba
                            #'92', #	Carioca
                            #'376', # Catarinense
                            #'378', # Cearense
                            '373' # Copa Betano do Brasil
                            #'1596', # Copa do Nordeste
                            #'377', # GaÃºcho
                            #'381', # Goiano
                            #'11664', # Maranhense
                            #'11669', # Paraense
                            #'10295', # Paraibano
                            #'382', # Paranaense
                            #'372', # Paulista Série A1
                            #'380', # Pernambucano
                            #'13353', # Piauiense
                            #'11663', # Potiguar, 1 Divisão 
                            #'14658', # Rondoniense
                            #'14733', # Roraimense
                            #'11665', # Sergipano
                            #'11679', # Sul-Mato-Grossense
                            #'14602', # Supercopa do Brasil
                            #'14686', # Tocantinense
    ]

    ########## Extract e Transform ########## 
    run_all_tournaments_year(datetime_now, save_path, search_sports, search_sports_countries_id, ano, search_tournaments_id,
                             choice_extract_sports = 0, choice_transform_sports = 0,
                             choice_extract_countries = 0, choice_transform_countries = 0,
                             choice_extract_tournaments = 0, choice_transform_tournaments = 0,
                             choice_extract_seasons = 0, choice_transform_seasons = 0,
                             choice_extract_rounds = 0, choice_transform_rounds = 0,
                             choice_extract_matches = 0, choice_transform_matches = 0,
                             choice_extract_matches_statistics = 0, choice_transform_matches_statistics = 0,
                             choice_extract_lineups = 0, choice_transform_lineups = 0,
                             choice_extract_lineups_statistics = 1, choice_transform_lineups_statistics = 1,
                             )