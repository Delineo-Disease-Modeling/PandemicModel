# updateTimeseries.py
# by Jiawei Peng

# Note: should run "pip install PyGithub" at first if you have not installed PyGithub on your machine

import os
from github import Github
import pandas as pd
from io import BytesIO
import base64
from datetime import datetime, time

# create a Github instance
# using an access token
g = Github("0ae92af1288db5103f6d02f9ad20649e603ec791")

# get into the root directory of the repo
repo = g.get_repo("CSSEGISandData/COVID-19")

# get into the tarageted directory which stores all data we need
contents = repo.get_contents("csse_covid_19_data/csse_covid_19_daily_reports")


a = datetime(2020, 4, 1)

for content_file in contents:
    # select the csv files of date after 4/1/2020
    if content_file.name.endswith('.csv') and datetime.strptime(content_file.name, '%m-%d-%Y.csv') > a:
        # convert byte string into bytes
        b_content = base64.decodebytes(bytes(content_file.content, 'utf-8'))
        
        # opens an IO stream to the bytes
        with BytesIO(b_content) as f:
            # read into dataframe
            df = pd.read_csv(f)
        
        # get the date information from the content_file and 
        # formatting(corresponds with other columns' name in *_timeseries.csv)
        d = datetime.strptime(content_file.name, '%m-%d-%Y.csv')
        string = str(d.month) + '/' + str(d.day) + '/' + str(d.year) 
        
        # select the data of US (the rows where 'Country_Region' == 'US')
        us_data = df.loc[df['Country_Region'] == 'US']
    
        # select subsets of the dataframe which are used for merge 
        update_deaths = us_data[['FIPS', 'Deaths']]
        update_confirms = us_data[['FIPS', 'Confirmed']]

        with open('Desktop/deaths_timeseries.csv') as dt:
            death_ts = pd.read_csv(dt)
            
            # innner join two dataframes on FIPS
            update_death_ts = pd.merge(left = death_ts, right = update_deaths, on = 'FIPS')
            
            # rename the newly added column by its date
            new_death_ts = update_death_ts.rename(columns = {'Deaths': string})
            
            # remove columns of duplicate names
            new_death_ts = new_death_ts.loc[:,~new_death_ts.columns.duplicated()]
            
            new_death_ts.to_csv('desktop/deaths_timeseries.csv', index = False)

        
        with open('Desktop/infections_timeseries.csv') as it:
            infection_ts = pd.read_csv(it)
            update_infection_ts = pd.merge(left = infection_ts, right = update_confirms, on = 'FIPS')
            new_infection_ts = update_infection_ts.rename(columns = {'Confirmed' : string})
            new_infection_ts = new_infection_ts.loc[:,~new_infection_ts.columns.duplicated()]
            new_infection_ts.to_csv('desktop/infections_timeseries.csv', index = False)