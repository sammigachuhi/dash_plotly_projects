# Load the wide table of human_waste
import pandas as pd
data = pd.read_csv('D:\gachuhi\dash-projects\human_waste_filtered.csv')

data_long = pd.melt(data, id_vars='County', var_name='indicator', value_name='value', ignore_index='False')

print(data_long.head())

data_long.to_csv('sanitation_long.csv', sep=',')



















