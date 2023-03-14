#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np




df = pd.read_csv('../../data/health_datasets/big_cities_health_cdc.csv')

census = pd.read_csv('../../data/census_code_mappers/fips_codes.csv')

cities = pd.read_csv('../../data/census_code_mappers/us_city_info.csv')

# Optionally set this to false if you do not want the fips
ADD_FIPS=True


del df['Methods'] # Approx 75% NaN, not useful
del df['Notes'] # Approx 75% NaN, not useful


def ind_to_int(x):
    if '100,000' in x: return 100000
    if '1,000' in x: return 1000
    if 'Percent' in x: return 100
    if 'Rate' in x: return 100
    else: return 1


df['per'] = [ind_to_int(x) for x in df['Indicator']]


df['city'] = df['Place']\
    .str.extract(r'(.*), (.*)')[0]\
    .str.split('(')\
    .str.get(0)\
    .str.replace('County', '')\
    .str.strip()\
    .fillna('National')
df['state'] = df['Place']\
    .str.extract(r'(.*), (.*)')[1]\
    .str.strip()\
    .fillna('National')


def city_state_to_fips(row):
    if row['city'] == 'National':
        return 0
    else:
        return cities[(cities['city']==row['city']) & (cities['state_abbr'] == row['state'])]['county_fips'].iloc[0]


df['fips'] = df.apply(lambda x: city_state_to_fips(x), axis=1)


df.rename(columns={
    'Indicator Category': 'category',
    'Indicator': 'indicator',
    'Year': 'year',
    'Gender': 'gender',
    'Race/ Ethnicity': 'race',
    'Value': 'value',
    'Place': 'place',
    'BCHC Requested Methodology': 'methodology',
    'Source': 'source'
}, inplace=True)

df.to_csv('../../data/health_datasets/big_cities_health_cdc_clean.csv', index=False)

