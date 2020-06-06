'''
    Last Updated: 2020/06/05
    By Steven Tan
    To run this script you need to install pymongo as well dnspython module
    Documentation for PyMongo API can be found at: https://api.mongodb.com/python/current/tutorial.html
'''

import pandas as pd
import numpy as np
# import pymongo
from pymongo import MongoClient
from pprint import pprint
from collections import defaultdict


if __name__ == "__main__":
    print('-'*100)
    print('Start to connect to the Atlas MongoDB')
    # connect to the client using atlas uri
    client = MongoClient('mongodb+srv://admin:covid19@covid19-g8npp.mongodb.net/covid19?retryWrites=true&w=majority')

    # connect to our covid 19 database
    db = client['covid19']

    #connect to the specific collections under the covid-19 database
    demographic = db['demographics']
    timeserie = db['timeseries']

    # use pprint to get document so that it's more organized and informative
    # pprint(demographic.find_one())
    # pprint(timeserie.find_one())

    # -------------------------------------------- Database Query --------------------------------------------#
    # TODO: add different methods if necessary
    # for now I'm only providing query function since database update should be handled by architecture team

    demo_data = demographic.find() # the find method could be customized here
    temp = defaultdict(list)

    # The problem with the DB is that each document does not necessarily have the same colums
    # manually retrieve the keys first
    all_keys = []
    # each demo is a document inside the demographics collection
    for demo in demo_data:
        keys= demo.keys()
        for ele in keys:
            if not ele in all_keys:
                all_keys.append(ele)
    # print(all_keys)

    # initialization of dictionary to be turned into dataframe
    demo_dict = dict()
    for ele in all_keys:
        demo_dict[ele] = []

    # need to reconnect once demo_data is accessed!!!!!!
    demo_data = demographic.find()
    for demo in demo_data:
        size = -1
        for k, v in demo.items():
            demo_dict[k].append(v)
            if size == -1: 
                size = len(demo_dict[k]) # get the updated size
                
        for k, v in demo_dict.items():
            if len(demo_dict[k]) < size:
                demo_dict[k].append(None)


    print('-'*100)
    print('Display dataframe converted from demographics below:')
    df = pd.DataFrame.from_dict(demo_dict)

    print(df.head())
    print(len(df.index))
    
    