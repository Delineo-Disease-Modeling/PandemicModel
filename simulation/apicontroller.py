import json
import traceback

file_path = "testAPI.json"

language_settings = {}

class apicontroller:
    with open(file_path, encoding="UTF-8") as file:
        values = json.load(file)

class innercontroller:
    def __init__(self):
    
    @staticmethod
    def get(line):
        return apicontroller.values[line]