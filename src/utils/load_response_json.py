import os
import json

def load_response_json(file_path):
    file_path = os.path.join(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)