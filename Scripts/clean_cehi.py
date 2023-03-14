# %%
import pandas as pd
data_path = "../../data/"

# %%
read = False
if read:
    fips_codes = pd.read_csv(data_path + "census_code_mappers/fips_codes.csv")
    percent_cover_county = pd.read_csv(data_path + "greenspace_data/percent_cover_county.txt", sep = ",")
    urban_tree_canopy = pd.read_csv(data_path + "greenspace_data/urban_tree_canopy.csv")
    trees_us = pd.read_csv(data_path + "greenspace_data/5_million_trees_us_cities.csv")
# percent_cover_county
# urban_tree_canopy

# %% [markdown]
# cehi_inputs

# %%
cehi_inputs = pd.read_csv(data_path + "greenspace_data/CEHI_inputs.csv")
cehi_ouputs = pd.read_csv(data_path + "greenspace_data/CEHI_outputs.csv")

# %%
print(cehi_inputs.columns)

print((cehi_inputs.bgrp != cehi_inputs.GEOID10).sum())
del cehi_inputs["bgrp"]
del cehi_inputs["OBJECTID"] # same as index

print(cehi_inputs.columns)


print(cehi_ouputs.columns)

cehi_ouputs.rename(columns={cehi_ouputs.columns[0]: 'GEOID10'}, inplace=True)
cehi_ouputs.rename(columns={cehi_ouputs.columns[1]: 'enviro_atlas_community_abbr'}, inplace=True)
cols = cehi_ouputs.columns.tolist()
for c in cols:
    cehi_ouputs = cehi_ouputs.rename(columns={c: c.strip()})
print((cehi_ouputs.Objects != cehi_ouputs.GEOID10).sum())
del cehi_ouputs["Objects"]

print(cehi_ouputs.columns)

# %%
#get dataset summary
cehi_inputs.info()
# cehi_inputs.describe()
cehi_inputs.city_state.unique()

# %%
#get histograms
cehi_inputs.hist(bins=50, figsize=(20,15))

# %%
#plot histogram
cehi_inputs.enviro_atlas_community_abbr.hist(bins=50, figsize=(15,5))

# %%
#plot histogram
import matplotlib.pyplot as plt
plt.xticks(rotation=90)
cehi_inputs.city_state.hist(bins=50, figsize=(15,5))

# %%
#check for repeated values
cehi_inputs.GEOID10.value_counts().max()

# %% [markdown]
# cehi_outputs

# %%
#get summary
cehi_ouputs.info()
# cehi_ouputs.describe()
cehi_ouputs.columns

# %%
cehi_ouputs.hist(bins=50, figsize=(20,15))

# %%
cehi_ouputs.enviro_atlas_community_abbr.hist(bins=50, figsize=(15,5))

# %%
cehi_ouputs.GEOID10.value_counts().max()

# %%
#merge datasets
cehi_merged = pd.merge(cehi_inputs, cehi_ouputs, on=['GEOID10', 'enviro_atlas_community_abbr'], how='inner')

# %%
cehi_merged.info()
cehi_merged.columns

# %%
cehi_merged.hist(bins=50, figsize=(20,15))

# %%
# save all data
cehi_inputs.to_csv(data_path + "greenspace_data/cehi_inputs_cleaned.csv", index=False)
cehi_ouputs.to_csv(data_path + "greenspace_data/cehi_outputs_cleaned.csv", index=False)
cehi_merged.to_csv(data_path + "greenspace_data/cehi_merged.csv", index=False)

# %%



