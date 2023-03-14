#!/usr/bin/env python
# coding: utf-8

# ---

# # Setting up some things

# In[1]:


import matplotlib.pyplot as plt
import geopandas
import pandas as pd
import locale
import os
import os.path as osp
from typing import List, Dict, Set, Callable
import missingno as msno

HOME = "../../"

# the input directories
DATA = osp.join(HOME, "data")
CODE = osp.join(HOME, "code")
GREENSPACE_DATA = osp.join(DATA, "greenspace_data")
CENSUS_DATA = osp.join(DATA, "census_code_mappers")

# the output directories
def safe_mkdir(folder):
    if(not osp.exists(folder)):
        os.mkdir(folder)

CLEAN_DATA = osp.join(HOME, "clean_data")
CLEAN_GREENSPACE_DATA = osp.join(CLEAN_DATA, "greenspace_data")
safe_mkdir(CLEAN_DATA)
safe_mkdir(CLEAN_GREENSPACE_DATA)


# In[2]:


def plot_on_US_map(fnc: Callable[[pd.Series], int], col_name: str):
    STATES[col_name] = STATES.apply(fnc, axis = 1)
    STATES.plot(column = col_name, legend = True)
    plt.title("How "+str(col_name)+" varies by state")
    plt.show()


# Getting all the locational dataframes

# In[3]:


blocks_df = pd.read_csv(osp.join(CENSUS_DATA, "us_blocks.csv"))
fips_df = pd.read_csv(osp.join(CENSUS_DATA, "fips_codes.csv"))
fips_df['geoid'] = fips_df.apply(lambda row: int(row.state_code+row.county_code), axis=1)
city_df = pd.read_csv(osp.join(CENSUS_DATA, "us_city_info.csv"))
zip_df = pd.read_csv(osp.join(CENSUS_DATA, "zcta_census_tract.csv"))

# Getting some dictionaries from the blocks_df
dc_block_geo_id_state_fip = dict(zip(blocks_df.block_geoid, blocks_df.state_fip))
dc_block_geo_id_county_fip = dict(zip(blocks_df.block_geoid, blocks_df.county_fip))
dc_block_geo_id_county_name = dict(zip(blocks_df.block_geoid, blocks_df.county_name))

# Getting dictionaries from the fips_df
dc_state_fip_to_state_abb = dict(zip(fips_df.state_code, fips_df.state))
dc_state_fip_to_state_name = dict(zip(fips_df.state_code, fips_df.state_name))
dc_county_fip_to_county_name = dict(zip(fips_df.county_code, fips_df.county))
dc_geoid_to_county_name = dict(zip(fips_df.geoid, fips_df.county))
dc_geoid_to_state_name = dict(zip(fips_df.geoid, fips_df.state_name))
dc_geoid_to_state_abb = dict(zip(fips_df.geoid, fips_df.state))

# Getting dictionaries from the city_df
dc_county_fips_to_state_abb =  dict(zip(city_df.county_fips, city_df.state_abbr))
dc_county_fips_to_state_name =  dict(zip(city_df.county_fips, city_df.state_name))
dc_county_fips_to_county_name =  dict(zip(city_df.county_fips, city_df.county_name))
dc_city_name_to_state_name =  dict(zip(city_df.city, city_df.state_name))

# Getting dictionaries from zip_df
dc_zcta10_to_state_fip =  dict(zip(zip_df.ZCTA10, zip_df.state_fip))
dc_zcta10_to_county_fip =  dict(zip(zip_df.ZCTA10, zip_df.county_fip))


# ---

# # Cleaning the Percent Cover Data
# 
# There are 4 percent cover datasets to consider. We load them all.

# In[4]:


pcc = pd.read_csv(osp.join(GREENSPACE_DATA, "percent_cover_county.txt"))
pctnb = pd.read_csv(osp.join(GREENSPACE_DATA, "percent_cover_tracts_no_buffer.txt"))
pctwb = pd.read_csv(osp.join(GREENSPACE_DATA, "percent_cover_tracts_with_buffer.txt"))
pczta = pd.read_csv(osp.join(GREENSPACE_DATA, "percent_cover_zipcode_tabulated_areas.txt"))
apc = [pcc, pctnb, pctwb, pczta]
apc_names = ["percent_cover_county", "percent_cover_tracts_no_buffer", "percent_cover_tracts_with_buffer", "percent_cover_zipcode_tabulated_areas"]


# ### Counting Nan Values
# 
# Turns out to have no NAN values initially

# In[5]:


for pc in apc:
    print(pc.isnull().sum(axis = 0) / len(pc))


# ## Counting Zero Values
# 
# Debatable if they need to be removed. Ask Yash once before going ahead.

# In[6]:


for pc, pc_name in zip(apc, apc_names):
    print(pc_name + " " + str(len(pc[pc['pc_park'] == 0]) /(len(pc))))


# ## Adding Other Columns
# So that these dataframes are easily accessible

# In[7]:


for pc in [pctnb, pctwb]:
    pc['state'] = pc['STATEFP'].map(dc_state_fip_to_state_abb)
    pc['state_name'] = pc['STATEFP'].map(dc_state_fip_to_state_name)    
    pc['county_name'] = pc['COUNTYFP'].map(dc_county_fip_to_county_name)


# In[8]:


pcc['state'] = pcc['GEOID'].map(dc_county_fips_to_state_abb)
pcc['state_name'] = pcc['GEOID'].map(dc_county_fips_to_state_name)
pcc['county_name'] = pcc['GEOID'].map(dc_county_fips_to_county_name)


# In[9]:


pczta['state_fip'] = pczta['ZCTA5CE10'].map(dc_zcta10_to_state_fip)
pczta['state_abb'] = pczta['state_fip'].map(dc_state_fip_to_state_abb)
pczta['state_name'] = pczta['state_fip'].map(dc_state_fip_to_state_name)
pczta['county_fip'] = pczta['ZCTA5CE10'].map(dc_zcta10_to_county_fip)
pczta['county_name'] = pczta['county_fip'].map(dc_county_fip_to_county_name)


# In[11]:


for pc, nm in zip(apc, apc_names):
    tpc = pc.dropna()
    tpc.to_csv(osp.join(CLEAN_GREENSPACE_DATA, nm+str(".txt")), index=False)


# ---

# # Cleaning the Urban Tree Canopy Dataframe
# 
# Just the one dataframe this time, however it is significantly more complicated than the percent cover datasets. Starting off by loading the dataset and plotting a heatmap

# In[12]:


utcdf = pd.read_csv(osp.join(GREENSPACE_DATA, "urban_tree_canopy.csv"))


# ### Adding some columns
# 
# This dataset has the city name in a different format. Furthermore it does not have state or county so I am adding the same to the dataframe using the census block column. Furthermore I am taking rounding down the census block column as it should always be an int

# In[13]:


utcdf = utcdf.astype({'census_block':'int'})
utcdf['state_fip'] = utcdf['census_block'].map(dc_block_geo_id_state_fip)
utcdf['state'] = utcdf['state_fip'].map(dc_state_fip_to_state_abb)
utcdf['state_name'] = utcdf['state_fip'].map(dc_state_fip_to_state_name)
utcdf['county_fip'] = utcdf['census_block'].map(dc_block_geo_id_county_fip)
utcdf['county_name'] = utcdf['census_block'].map(dc_block_geo_id_county_name)


# ### Counting Nan Values
# 
# After adding the state and county columns. 99.77% of the data is present

# In[14]:


print(1- (utcdf.isnull().sum(axis = 0) / len(utcdf)))


# Washington DC seems to be missing from blocks_df. I think we can skip it is comparatively rare

# In[15]:


utcdf[utcdf['state_fip'].isnull()]['city_name'].unique()


# In[16]:


tutcdf = utcdf.dropna()
tutcdf.to_csv(osp.join(CLEAN_GREENSPACE_DATA, "urban_tree_canopy.csv"), index=False)

