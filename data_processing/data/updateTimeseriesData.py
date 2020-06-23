# updateTimeseriesData.py
# by Jiawei Peng


import pandas as pd
import pymongo
from pymongo import MongoClient
from datetime import datetime, date
from github import Github
import pytz
import json as js
import base64
from io import BytesIO


# connect to the client using atlas url
client = MongoClient(#Enter the url here#)
    
# connect to covid19 database
db = client['covid19']
    
# connect to the timeseries collection
collection = db['timeseries']


# fetch the latest date from the existing documents
for obj in collection.find({}, {'date': 1}).sort('date', pymongo.DESCENDING).limit(1):
    latest_date = obj['date']



with open('interventions.json') as json_file:
    interventions = js.load(json_file)

def convert_boolean(cur_date, ordinan_date):
    if ordinan_date != None:
        start_date = date.fromordinal(ordinan_date)
        cur_date =  datetime.date(cur_date)
        return start_date <= cur_date
    else:
        return ""

    
# create a Github instance
# using an access token (should generate in the developer setting in your Github account settings or 
# you can just use your Github account when you just run this code on your own machine)
g = Github('5253f359f6caae28d18d0227c223d404f1515123')

# get into the root directory of the repo
repo = g.get_repo("CSSEGISandData/COVID-19")

# get into the tarageted directory which stores all data we need
contents = repo.get_contents("csse_covid_19_data/csse_covid_19_daily_reports")


for content_file in contents: 
    # select the csv files of date after the existing latest date
    if content_file.name.endswith('.csv') and datetime.strptime(content_file.name, '%m-%d-%Y.csv') > latest_date:
        # convert byte string into bytes
        b_content = base64.decodebytes(bytes(content_file.content, 'utf-8'))
        
        # opens an IO stream to the bytes
        with BytesIO(b_content) as f:
            # read into dataframe
            df = pd.read_csv(f)
        
        # get the date information and set it into UTC timezone
        d = datetime.strptime(content_file.name, '%m-%d-%Y.csv').replace(tzinfo = pytz.UTC)
        
        
        # select the rows which have corresponding FIPS
        us_data = df.loc[df['FIPS'].notnull()]
        us_data = us_data.loc[us_data['FIPS'] >= 1000]
    
        # select subsets of the dataframe and rename the columns
        update_info = us_data[['FIPS', 'Confirmed', 'Combined_Key', 'Deaths']]
        update_info = update_info.rename(columns = {'Deaths': 'death', 'Confirmed': 'infected', 'Combined_Key': 'Ckey'})
        
        # convert the values of 'FIPS' column to string of integer
        update_info = update_info.astype({'FIPS': int})
        update_info = update_info.astype({'FIPS': str})
    
        # formatting the strings of 'Ckey' column
        update_info['Ckey'] = update_info['Ckey'].str.replace(',', ' -')
        
        # make the 'FIPS' values as the new columns
        update_info = update_info.T
        update_info = update_info.rename(columns = update_info.iloc[0])
        update_info = update_info.drop(update_info.index[0])
    
        # convert the dataframe to python dictionary used for inserting
        post = update_info.to_dict()
        
        # update the policies
        for key in post:
            for item in interventions:
                if str(item['FIPS']) == key:
                    post[key]['stay at home'] = convert_boolean(d, item['stay at home'])
                    post[key]['>50 gatherings'] = convert_boolean(d, item['>50 gatherings'])
                    post[key]['>500 gatherings'] = convert_boolean(d, item['>500 gatherings'])
                    post[key]['public schools'] = convert_boolean(d, item['public schools'])
                    post[key]['restaurant dine-in'] = convert_boolean(d, item['restaurant dine-in'])
                    post[key]['entertainment/gym'] = convert_boolean(d, item['entertainment/gym'])
                    post[key]['federal guidelines'] = convert_boolean(d, item['federal guidelines'])
                    post[key]['foreign travel ban'] = convert_boolean(d, item['foreign travel ban'])
        
        # update the date object
        post['date'] = d
        
        # insert the dictionary to the collection
        collection.insert_one(post)
        
