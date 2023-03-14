#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np

census_designated_places = pd.read_csv('PLACES_2022_census_designated_places.csv')
census_tract = pd.read_csv('PLACES_2022_census_tract.csv')
county = pd.read_csv('PLACES_2022_county.csv')
zcta = pd.read_csv('PLACES_2022_zcta.csv')

print(census_designated_places.columns, census_tract.columns, county.columns, zcta.columns)

print(len(census_designated_places), len(census_tract), len(county), len(zcta))

census_designated_places.head()

census_designated_places.isnull().sum()

print(census_designated_places.Data_Value_Footnote_Symbol.unique())
print(census_designated_places.Data_Value_Footnote.unique())
print(census_designated_places.DataSource.unique())

print(census_designated_places.CategoryID.unique())
print(census_designated_places.MeasureId.unique())
print(census_designated_places.DataValueTypeID.unique()) # could be replaced with binary

del census_designated_places['StateDesc'] # repitition of previous column
del census_designated_places['Data_Value_Footnote_Symbol'] # all nan
del census_designated_places['Data_Value_Unit'] # everything is % in this column
del census_designated_places['Data_Value_Footnote'] # all nan
del census_designated_places['DataSource'] # only 1 value
del census_designated_places['Data_Value_Type'] # DataValueTypeID columns same but provides simplification
del census_designated_places['States'] # repeat data, also not even included in the table pdf they gave
del census_designated_places['Counties'] # repeat data, also not even included in the table pdf they gave
del census_designated_places['LocationID'] # not helpful
del census_designated_places['Short_Question_Text'] # repeat of measureID
del census_designated_places['Category'] # repeat in categoryID
del census_designated_places['Measure'] # measureID summarizes it

census_designated_places['ConfidenceLimit'] = census_designated_places[['Low_Confidence_Limit', 'High_Confidence_Limit']].apply(tuple, axis=1)
del census_designated_places['Low_Confidence_Limit']
del census_designated_places['High_Confidence_Limit']

census_designated_places = census_designated_places[census_designated_places['Data_Value'].notna()]
census_designated_places = census_designated_places.rename(columns={'StateAbbr': 'State', 'Data_Value': 'DataValue', 'Short_Question_Text':'ShortQuestionText', 'MeasureId':'MeasureID', 'Geolocation':'GeoLocation'})

census_designated_places.isnull().sum() # now left with no NA values

census_designated_places

del census_tract['StateDesc'] # repitition of previous column
del census_tract['Data_Value_Footnote_Symbol'] # all nan
del census_tract['Data_Value_Unit'] # everything is % in this column
del census_tract['Data_Value_Footnote'] # all nan
del census_tract['DataSource'] # only 1 value
del census_tract['Data_Value_Type'] # DataValueTypeID columns same but provides simplification
del census_tract['States'] # repeat data, also not even included in the table pdf they gave
del census_tract['Counties'] # repeat data, also not even included in the table pdf they gave
del census_tract['LocationID'] # not helpful
del census_tract['Short_Question_Text'] # repeat of measureID
del census_tract['Category'] # repeat in categoryID
del census_tract['Measure'] # measureID summarizes it

del census_tract['CountyFIPS']

census_tract['ConfidenceLimit'] = census_tract[['Low_Confidence_Limit', 'High_Confidence_Limit']].apply(tuple, axis=1)
del census_tract['Low_Confidence_Limit']
del census_tract['High_Confidence_Limit']

census_tract = census_tract[census_tract['Data_Value'].notna()]
census_tract = census_tract.rename(columns={'StateAbbr': 'State', 'Data_Value': 'DataValue', 'Short_Question_Text':'ShortQuestionText', 'MeasureId':'MeasureID', 'Geolocation':'GeoLocation'})

census_tract.isnull().sum() # now left with no NA values

census_tract

del zcta['Data_Value_Footnote_Symbol'] # all nan
del zcta['Data_Value_Unit'] # everything is % in this column
del zcta['Data_Value_Footnote'] # all nan
del zcta['DataSource'] # only 1 value
del zcta['Data_Value_Type'] # DataValueTypeID columns same but provides simplification

# OPT NOT TO DELETE STATES AND COUNTIES IN THIS CASE

#del zcta['States'] # repeat data, also not even included in the table pdf they gave
#del zcta['Counties'] # repeat data, also not even included in the table pdf they gave

del zcta['LocationID'] # not helpful
del zcta['Short_Question_Text'] # repeat of measureID
del zcta['Category'] # repeat in categoryID
del zcta['Measure'] # measureID summarizes it

zcta['ConfidenceLimit'] = zcta[['Low_Confidence_Limit', 'High_Confidence_Limit']].apply(tuple, axis=1)
del zcta['Low_Confidence_Limit']
del zcta['High_Confidence_Limit']

zcta = zcta[zcta['Data_Value'].notna()]
zcta = zcta[zcta['States'].notna()]
zcta = zcta[zcta['Counties'].notna()] # dropping 870 rows
zcta = zcta.rename(columns={'StateAbbr': 'State', 'Data_Value': 'DataValue', 'Short_Question_Text':'ShortQuestionText', 'MeasureId':'MeasureID', 'Geolocation':'GeoLocation'})

zcta.isnull().sum() # now left with no NA values

zcta

del county['LocationID'] # not helpful
del county['Short_Question_Text'] # repeat of measureID
del county['Category'] # repeat in categoryID
del county['Measure'] # measureID summarizes it

county['ConfidenceLimit'] = county[['Low_Confidence_Limit', 'High_Confidence_Limit']].apply(tuple, axis=1)
del county['Low_Confidence_Limit']
del county['High_Confidence_Limit']

del county['Data_Value_Unit']
del county['StateDesc']
del county['Data_Value_Footnote_Symbol']
del county['Data_Value_Footnote']
del county['Data_Value_Type']

county = county[county['Data_Value'].notna()]

county = county[county['LocationName'].notna()] # dropping 60 rows
county = county.rename(columns={'StateAbbr': 'State', 'Data_Value': 'DataValue', 'Short_Question_Text':'ShortQuestionText', 'MeasureId':'MeasureID', 'Geolocation':'GeoLocation'})

county.isnull().sum() # now left with no NA values

county

census_designated_places.to_csv('health_data/PLACES_2022_census_designated_places_cleaned.csv', index=False)
census_tract.to_csv('health_data/PLACES_2022_census_tract_cleaned.csv', index=False)
county.to_csv('health_data/PLACES_2022_county_cleaned.csv', index=False)
zcta.to_csv('health_data/PLACES_2022_zcta_cleaned.csv', index=False)

