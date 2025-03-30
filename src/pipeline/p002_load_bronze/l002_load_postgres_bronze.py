import pandas as pd
import sys
import os
import glob

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.pipeline.p002_load_bronze.utils.u001_update_postgres_bronze import update_json_postgres

if __name__ == "__main__":
    batch_dir = r'data\outputs\bronze\2025-03-30_11-20-03'
    schema = "s001_bronze"

    # Sport   
    path_table_name = 'Sports'
    table_name = 't001_sports'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    print(json_files)
    for json_path in json_files:
        update_json_postgres(table_name, schema, json_path)

    # Countries
    path_table_name = 'Countries'
    table_name = 't002_countries'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    print(json_files)
    for json_path in json_files:
        update_json_postgres(table_name, schema, json_path)

    # Tournaments
    path_table_name = 'Tournaments'
    table_name = 't003_tournaments'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    print(json_files)
    for json_path in json_files:
        update_json_postgres(table_name, schema, json_path)

    # Seasons
    path_table_name = 'Seasons'
    table_name = 't004_seasons'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    print(json_files)
    for json_path in json_files:
        update_json_postgres(table_name, schema, json_path)

    # Rounds
    path_table_name = 'Rounds'
    table_name = 't005_rounds'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    print(json_files)
    for json_path in json_files:
        update_json_postgres(table_name, schema, json_path)

    # Matches
    path_table_name = 'Matches'
    table_name = 't006_matches'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    print(json_files)
    for json_path in json_files:
        update_json_postgres(table_name, schema, json_path)

    # Matches Statistics
    path_table_name = 'Matches Statistics'
    table_name = 't007_matches_statistics'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    print(json_files)
    for json_path in json_files:
        update_json_postgres(table_name, schema, json_path)

    # Lineups
    path_table_name = 'Lineups'
    table_name = 't008_lineups'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    print(json_files)
    for json_path in json_files:
        update_json_postgres(table_name, schema, json_path)

    # Lineups Statistics
    path_table_name = 'Lineups Statistics'
    table_name = 't009_lineups_statistics'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    print(json_files)
    for json_path in json_files:
        update_json_postgres(table_name, schema, json_path)

    
