import os
import sys
import pandas as pd
import logging
from datetime import datetime, timezone, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from scrapers.sofascore_scraper import SofaScoreScraper
from utils.save_response_json import save_response_to_json
from utils.save_dataframe_csv import save_dataframe_to_csv

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
        # Requisita os dados de estatísticas
        response = get_matches_statistics(match_id)
        
        # Verifica se a resposta contém a chave "statistics" válida
        if "statistics" not in response or not (isinstance(response["statistics"], dict) or isinstance(response["statistics"], list)):
            logging.warning(f"Match_id {match_id} não contém estatísticas válidas. Resposta: {response}")
            return None
        
        response_statistics = [{
            'match_id': match_id,
            'statistics': response
        }]
        
    except Exception as e:
        response_statistics = None
        logging.error(f"Erro ao buscar estatísticas para Match_id: {match_id}. Erro: {str(e)}")
    
    return response_statistics

def transform_matches_statistics(response_matches, datetime_now):
    '''
    Pegar os dados de overview das partidas

    :param response_matches: A resposta do servidor ao scraper Matches
    :return: Um dataframe com o overview das partidas
    '''
    list_match_id_key = []
    list_match_id = []
    list_key = []
    list_period = [] 
    list_groupname = [] 
    list_name = [] 
    list_home = [] 
    list_away = [] 
    list_statisticstype = [] 
    list_updated_at = []
    for match in response_matches:
        match_id = match["match_id"]
        
        # Verifica se existe a chave 'statistics' e se está estruturada corretamente
        statistics = match.get("statistics", {}).get("statistics", [])
        if not statistics:
            logging.warning(f"Match_id {match_id} não contém estatísticas válidas.")
            continue

        for stat in statistics:
            period = stat.get("period", "")

            for group in stat.get("groups", []):
                group_name = group.get("groupName", "")

                for item in group.get("statisticsItems", []):
                    name = item.get("name", "")
                    home = item.get("home", 0)
                    away = item.get("away", 0)
                    statistics_type = item.get("statisticsType", "")
                    key = item.get("key", "")

                    list_match_id.append(match_id)
                    list_period.append(period)
                    list_groupname.append(group_name) 
                    list_name.append(name) 
                    list_home.append(home) 
                    list_away.append(away) 
                    list_statisticstype.append(statistics_type) 
                    list_key.append(key)
                    list_match_id_key.append(f"{match_id}{key}")
                    list_updated_at.append(datetime_now)

    df_statistics = pd.DataFrame({
        'match_id_key': list_match_id_key,
        'match_id': list_match_id,
        'period': list_period,
        'groupname': list_groupname,
        'name': list_name,
        'home': list_home,
        'away': list_away,
        'statistics': list_statisticstype,
        'key': list_key,
        'updated_at': list_updated_at,
    })

    return df_statistics

def load_matches_statistics(search_match_id, save_path, datetime_now):
    response_matches_statistics_agg = []
    df_matches_statistics_agg = pd.DataFrame()
    for match_id in search_match_id:
        title = f"Matches Statistics - {match_id} - {datetime_now}"
        logging.info(f"Extraindo: {title}")
        
        response_matches_statistics = extract_matches_statistics(match_id)
        if response_matches_statistics:
            df_matches_statistics = transform_matches_statistics(response_matches_statistics)

            # Salvar
            save_response_to_json(response_matches_statistics, save_path, title)
            save_dataframe_to_csv(df_matches_statistics, save_path, title)

            # Agrupar
            response_matches_statistics_agg.append(response_matches_statistics)
            df_matches_statistics_agg = pd.concat([df_matches_statistics_agg, df_matches_statistics], ignore_index=True)
        else:
            logging.error(f"Não foi possível extrair dados para a partida: {match_id}")

    return response_matches_statistics_agg, df_matches_statistics_agg

if __name__ == "__main__":
    # Input
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_path = r'data\outputs'
    search_match_id = ["12146274"]

    response_matches_statistics_agg, df_matches_statistics_agg = load_matches_statistics(search_match_id, save_path, datetime_now)
