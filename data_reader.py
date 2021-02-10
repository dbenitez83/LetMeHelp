import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib
from pandas import Series
import numpy as np
import os

def pop_density_binning(return_colors=False):
	"""Return bins and color scheme for population density"""
	bins = np.array([0, 1, 2, 4, 6, 8, 10, 50, 100, 200, 500, 1000, 1500, 2000, 2500, 5000, 10000])
	cmap = plt.cm.get_cmap('Reds', len(bins)+1)
	if not return_colors:
		return bins, cmap
	else:
		colors = []
		for i in range(cmap.N):
			rgb = cmap(i)[:3] 
			colors.append(matplotlib.colors.rgb2hex(rgb))

		return bins, colors

def risk_binning(return_colors=False):
	"""Return bins and color scheme for relative median risk"""
	bins = np.arange(-10000,18000,2000)
	cmap = plt.cm.get_cmap('RdBu', len(bins))
	if not return_colors:
		return bins, cmap
	else:
		colors = []
		for i in range(cmap.N):
			rgb = cmap(i)[:3] 
			colors.append(matplotlib.colors.rgb2hex(rgb))

		return bins, colors
		
url="/Volumes/Disco Externo/municipios_ign.geojson"
keep_columns = ['nameunit', 'codigoine', 'geometry']
df=gpd.read_file(url)

df=df.loc[(df['codigoine'].isin(["25041","25068","25048","25052","25068","25093","25099","25113", 
	"25122","25135","25137","25158","25168","25205","25230","25248","25252",'250061',
'250096',
'250292',
'251706',
'250582',
'250560',
'250674',
'250735',
'250766',
'250812',
'250925',
'250978',
'251018',
'251057',
'251180',
'251193',
'251538',
'251692',
'251804',
'252069',
'252189',
'252249',
'252537',
'252555','430213',
'430290',
'430461',
'430542',
'430614',
'430733',
'430862',
'431016',
'431055',
'431074',
'431418',
'431303',
'431397',
'431423',
'431439',
'431460',
'431476',
'431589',
'431592',
'431687',
'431726',
'431763',
'250557',
'250729',
'250851',
'251039',
'251044',
'251109',
'251142',
'251327',
'251410',
'251431',
'251522',
'259118',
'259059',
'251919',
'251924',
'251977',
'251945',
'252167',
'252192',
'259078',
'252234',
'250030',
'250273',
'250463',
'250501',
'250707',
'250740',
'250962',
'251095',
'251305',
'251459',
'251543',
'251575',
'251765',
'251811',
'259025',
'252252',
'252173',
'252385',
'252424',
'252445',
'250557',
'250729',
'250851',
'251039',
'251044',
'251109',
'251142',
'251327',
'251410',
'251431',
'251522',
'259118',
'259059',
'251919',
'251924',
'251977',
'251945',
'252167',
'252192',
'259078',
'252234']))]

cols = list(df)
for col in keep_columns:
    cols.remove(col)
data=df.drop(columns=cols)

data.rename(columns={'nameunit': 'name','codigoine':'zip'}, inplace=True)
data.loc[:, 'pop2018'] = 100
data.loc[:, 'area'] = 100
data.loc[:, 'risk'] = 000
data['pop_density'] = data['pop2018']/data['area']
avg_risk = np.nanmean(data['risk'])
data['risk_relative'] = data['risk']-avg_risk


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


outfile = 'map_data_ES_filtered.json'
if os.path.isfile(outfile):
	os.remove(outfile)

data.to_file(outfile, driver='GeoJSON')
# ogr2ogr -f "GeoJSON" -lco COORDINATE_PRECISION=4 map_data_ES_filtered_reduced.json map_data_ES_filtered.json
