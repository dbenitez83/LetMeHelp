import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib
from pandas import Series
import numpy as np
import os

def pop_density_binning(return_colors=False):
	"""Return bins and color scheme for population density"""
	# First bin is 0, next is 0.1-1, ..., final is > 10000
	bins = np.array([0, 1, 2, 4, 6, 8, 10, 50, 100, 200, 500, 1000, 1500, 2000, 2500, 5000, 10000])
	cmap = plt.cm.get_cmap('Reds', len(bins)+1)
	if not return_colors:
		return bins, cmap
	else:
		colors = []
		for i in range(cmap.N):
			rgb = cmap(i)[:3] # will return rgba, we take only first 3 so we get rgb
			colors.append(matplotlib.colors.rgb2hex(rgb))

		return bins, colors

def risk_binning(return_colors=False):
	"""Return bins and color scheme for relative median risk"""
	# First bin is -10 000..-8 000, next is -8 000..-6 000, ..., final is 14 000-16 000
	bins = np.arange(-10000,18000,2000)
	cmap = plt.cm.get_cmap('RdBu', len(bins))
	if not return_colors:
		return bins, cmap
	else:
		colors = []
		for i in range(cmap.N):
			rgb = cmap(i)[:3] # will return rgba, we take only first 3 so we get rgb
			colors.append(matplotlib.colors.rgb2hex(rgb))

		return bins, colors
		
# Get statistics from Statistics Finland portal for year 2018 keeping only the selected data columns
url="/Volumes/Disco Externo/LetMeHelp!/municipios_ign.geojson"
keep_columns = ['nameunit', 'codigoine', 'geometry']
df=gpd.read_file(url)
cols = list(df)
for col in keep_columns:
    cols.remove(col)
data=df.drop(columns=cols)
#data.rename(columns={'he_vakiy': 'pop2018', 'pinta_ala': 'area', 'nimi': 'name', 'hr_mtu': 'risk', 'posti_alue': 'zip'}, inplace=True)

data.rename(columns={'nameunit': 'name','codigoine':'zip'}, inplace=True)
data.loc[:, 'pop2018'] = 100
data.loc[:, 'area'] = 100
data.loc[:, 'risk'] = 000
data['pop_density'] = data['pop2018']/data['area']
data['risk_relative'] = data['risk']-avg_risk


# Assign alternative colors for population density
bins, cmap = pop_density_binning()
colors = []

for i, row in data.iterrows():
	index = bins.searchsorted(row['pop_density'])
	colors.append(matplotlib.colors.rgb2hex(cmap(index)[:3]))

data['fill_density'] = Series(colors, dtype='str', index=data.index)

	bins, cmap = risk_binning()
	colors = []

	for i, row in data.iterrows():
		index = bins.searchsorted(row['risk_relative'])
		colors.append(matplotlib.colors.rgb2hex(cmap(index)[:3]))

data['fill'] = Series(colors, dtype='str', index=data.index)

# Save data as GeoJSON
# Note the driver cannot overwrite an existing file,
# so we must remove it first
outfile = 'map_data_ES.json'
if os.path.isfile(outfile):
	os.remove(outfile)

data.to_file(outfile, driver='GeoJSON')