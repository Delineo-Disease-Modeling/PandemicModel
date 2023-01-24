from dotenv import load_dotenv, find_dotenv
import requests
import pymongo
import urllib
import os
import certifi


def get_data():
    load_dotenv(find_dotenv())
    password = urllib.parse.quote_plus(os.environ.get("MONGO_PWD"))
    connection_string = f"mongodb+srv://root:{password}@cluster0.vnuo3wg.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(connection_string, tlsCAFile=certifi.where())
    delineo_db = client["delineo_disease_modeling"]
    simulation_data = delineo_db["simulation_data"]
    return simulation_data
