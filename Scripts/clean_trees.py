# %%
import pandas as pd
data_path = "../../data/"
trees_us = pd.read_csv(data_path + "greenspace_data/5_million_trees_us_cities.csv")
city_info = pd.read_csv(data_path + "census_code_mappers/us_cities_zips.csv")

# %%
print(trees_us.columns, city_info.columns)

# %%
print(len(trees_us), len(city_info))

# %%
#count number of nan values in each column
trees_us.isnull().sum()

# %%
del trees_us["tree_ID"] # all nan
del trees_us["percent_population"] # all nan
del trees_us["ward"] # seems useless, too many nans
del trees_us["district"] # seems useless, too many nans
del trees_us["city_ID"] # seems useless
del trees_us['address'] # seems useless
del trees_us['location_name'] # seems useless
del trees_us['neighborhood'] # seems useless
del trees_us['overhead_utility'] # seems useless
del trees_us['retired_date'] # too few values
del trees_us['most_recent_observation'] # seems useless
del trees_us['most_recent_observation_type'] # seems useless

# %%
#capture year from planted_date
pattern = r'(\d{4})'
trees_us['planted_year'] = trees_us['planted_date'].str.extract(pattern, expand=True)

#capture month from planted_date
pattern = r'(^\d{2}/)'
trees_us['planted_month'] = trees_us['planted_date'].str.extract(pattern, expand=True).replace(to_replace = r'/', value = '', regex = True)

#capture day from planted_date
pattern = r'(/\d{2}/)'
trees_us['planted_day'] = trees_us['planted_date'].str.extract(pattern, expand=True).replace(to_replace = r'/', value = '', regex = True)

del trees_us['planted_date']

# %%
# remove rows with nan values for city and state, too few, around 500
trees_us = trees_us.dropna(subset=['city', 'state'])

# %%
trees_us.longitude_coordinate = trees_us.longitude_coordinate.astype(float)
trees_us.latitude_coordinate = trees_us.latitude_coordinate.astype(float)

# fill mean values for longitude and latitude by city and state
trees_us.longitude_coordinate = trees_us.groupby(['city', 'state'])['longitude_coordinate'].transform(lambda x: x.fillna(x.mean()))
trees_us.latitude_coordinate = trees_us.groupby(['city', 'state'])['latitude_coordinate'].transform(lambda x: x.fillna(x.mean()))


city_crd = city_info[['city', 'latitude_centroid', 'longitude_centroid']]

# make dictionary of city and state to latitude and longitude
city_longitude = dict(zip(city_crd.city, city_crd.longitude_centroid))
city_latitude = dict(zip(city_crd.city, city_crd.latitude_centroid))

trees_us.fillna(value={'longitude_coordinate': trees_us.city.map(city_longitude), 'latitude_coordinate': trees_us.city.map(city_latitude)}, inplace=True)

# %%
trees_us.location_type.unique()
trees_us.location_type.fillna(value='no_info', inplace=True)
trees_us.location_type.replace(to_replace='nan', value='no_info', inplace=True)
trees_us.location_type.replace(to_replace='<null>', value='no_info', inplace=True)
trees_us.location_type = trees_us.location_type.astype(str)
trees_us.location_type.unique()

# %%
city_zip = city_info[['city', 'zip_code']]
city_zip = dict(zip(city_zip.city, city_zip.zip_code))

trees_us.zipcode.fillna(value=trees_us.city.map(city_zip), inplace=True)

# fill mode by city and state
trees_us.zipcode = trees_us.groupby(['city'])['zipcode'].transform(lambda x: x.fillna(x.mode()))

mask1 = trees_us.city == 'Washington DC'
mask2 = trees_us.city == 'St. Louis'
trees_us.loc[mask1, 'zipcode'] = 20001
trees_us.loc[mask2, 'zipcode'] = 63101

print(trees_us.zipcode.isnull().sum())
trees_us.dropna(subset=['zipcode'], inplace=True)
mask3 = trees_us.zipcode == 'None'
trees_us.drop(trees_us[mask3].index, inplace=True)
trees_us.zipcode = trees_us.zipcode.astype(int)

# %%
print(len(trees_us['common_name'].unique()), len(trees_us['scientific_name'].unique()))

names_1 = trees_us[['common_name', 'scientific_name']].drop_duplicates()
names_2 = trees_us[['scientific_name', 'common_name']].drop_duplicates()
#convert to dictionary
common_scientific = names_1.set_index('common_name').to_dict()['scientific_name']
scientific_common = names_2.set_index('scientific_name').to_dict()['common_name']

#fill na values
# trees_us.scientific_name.fillna(trees_us.common_name.map(common_scientific), inplace=True)
trees_us.common_name.fillna(trees_us.scientific_name.map(scientific_common), inplace=True)

trees_us.common_name = trees_us.common_name.str.lower().astype(str)
# trees_us.common_name.fillna("UNK", inplace=True)

trees_us.scientific_name = trees_us.scientific_name.str.lower().astype(str)
# trees_us.scientific_name.fillna("UNK", inplace=True)

# %%
# fill by binned mean
trees_us.diameter_breast_height_CM = trees_us.groupby(['diameter_breast_height_binned_CM'])['diameter_breast_height_CM'].transform(lambda x: x.fillna(x.mean()))

print(trees_us.diameter_breast_height_CM.isnull().sum())

# fill by common_name mean
trees_us.diameter_breast_height_CM = trees_us.groupby(['common_name'])['diameter_breast_height_CM'].transform(lambda x: x.fillna(x.mean()))

print(trees_us.diameter_breast_height_CM.isnull().sum())

# fill by overall mean
trees_us.diameter_breast_height_CM.fillna(value=trees_us.diameter_breast_height_CM.mean(), inplace=True)

print(trees_us.diameter_breast_height_CM.isnull().sum())

# %%
# do the same for height
trees_us.height_M = trees_us.groupby(['height_binned_M'])['height_M'].transform(lambda x: x.fillna(x.mean()))

print(trees_us.height_M.isnull().sum())

# fill by common_name mean
trees_us.height_M = trees_us.groupby(['common_name'])['height_M'].transform(lambda x: x.fillna(x.mean()))

print(trees_us.height_M.isnull().sum())

# fill by overall mean
trees_us.height_M.fillna(value=trees_us.height_M.mean(), inplace=True)

print(trees_us.height_M.isnull().sum())

# %%
del trees_us['diameter_breast_height_binned_CM'] # delete the binned columns
del trees_us['height_binned_M'] # delete the binned columns

# %%
trees_us.condition.fillna(value='unknown', inplace=True)

# %%
trees_us.info()

# %%
trees_us.isnull().sum()

# %%
df = trees_us.isnull().sum()
stringcols = [col for col in trees_us.columns if trees_us[col].dtype == 'object' and df[col] == 0]
print(stringcols)
# convert to string
trees_us[stringcols] = trees_us[stringcols].astype(str)

# %%
trees_us.to_csv(data_path + "greenspace_data/5_million_trees_us_cities_cleaned.csv", index=False)

# %%



