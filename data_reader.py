import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib
from pandas import Series
import numpy as np
import os

def pop_density_binning(return_colors=False):
	"""Return bins and color scheme for population density"""
	bins = np.array([0, 1, 2, 4, 6, 8, 10, 50, 100, 200, 500, 1000, 1500, 2000, 2500, 5000, 10000])
	cmap = plt.cm.get_cmap("Reds", len(bins)+1)
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
	cmap = plt.cm.get_cmap("RdBu", len(bins))
	if not return_colors:
		return bins, cmap
	else:
		colors = []
		for i in range(cmap.N):
			rgb = cmap(i)[:3] 
			colors.append(matplotlib.colors.rgb2hex(rgb))

		return bins, colors
		
url="/Volumes/Disco Externo/municipios_ign.geojson"
keep_columns = ["nameunit", "codigoine", "geometry"]
df=gpd.read_file(url)

df=df.loc[(df["codigoine"].isin(["25041","25068","25048","25052","25068","25093","25099","25113", 
	"25122","25135","25137","25158","25168","25205","25230","25248","25252","250061",\
"25009",\
"25029",\
"25170",\
"25058",\
"25056",\
"25067",\
"25073",\
"25076",\
"25081",\
"25092",\
"25097",\
"25101",\
"25105",\
"25118",\
"25119",\
"25153",\
"25169",\
"25180",\
"25206",\
"25218",\
"25224",\
"25253",\
"25255",\
"43021",\
"43029",\
"43046",\
"43054",\
"43061",\
"43073",\
"43086",\
"43101",\
"43105",\
"43107",\
"43141",\
"43130",\
"43139",\
"43142",\
"43143",\
"43146",\
"43147",\
"43158",\
"43159",\
"43168",\
"43172",\
"43176",\
"25055",\
"25072",\
"25085",\
"25103",\
"25104",\
"25110",\
"25114",\
"25132",\
"25141",\
"25143",\
"25152",\
"25911",\
"25905",\
"25191",\
"25192",\
"25197",\
"25194",\
"25216",\
"25219",\
"25907",\
"25223",\
"25003",\
"25027",\
"25046",\
"25050",\
"25070",\
"25074",\
"25096",\
"25109",\
"25130",\
"25145",\
"25154",\
"25157",\
"25176",\
"25181",\
"25902",\
"25225",\
"25217",\
"25238",\
"25242",\
"25244",\
"25055",\
"25072",\
"25085",\
"25103",\
"25104",\
"25110",\
"25114",\
"25132",\
"25141",\
"25143",\
"25152",\
"25911",\
"25905",\
"25191",\
"25192",\
"25197",\
"25194",\
"25216",\
"25219",\
"25907",\
"25223"]))]

cols = list(df)
for col in keep_columns:
    cols.remove(col)
data=df.drop(columns=cols)

data.rename(columns={"nameunit": "name","codigoine":"zip"}, inplace=True)
data.loc[:, "pop2018"] = 100
data.loc[:, "area"] = 100
data.loc[:, "risk"] = 000
data["pop_density"] = data["pop2018"]/data["area"]
avg_risk = np.nanmean(data["risk"])
data["risk_relative"] = data["risk"]-avg_risk


bins, cmap = pop_density_binning()
colors = []

for i, row in data.iterrows():
	index = bins.searchsorted(row["pop_density"])
	colors.append(matplotlib.colors.rgb2hex(cmap(index)[:3]))

data["fill_density"] = Series(colors, dtype="str", index=data.index)

bins, cmap = risk_binning()
colors = []

for i, row in data.iterrows():
	index = bins.searchsorted(row["risk_relative"])
	colors.append(matplotlib.colors.rgb2hex(cmap(index)[:3]))

data["fill"] = Series(colors, dtype="str", index=data.index)


outfile = "map_data_ES_filtered.json"
if os.path.isfile(outfile):
	os.remove(outfile)

data.to_file(outfile, driver="GeoJSON")
# ogr2ogr -f "GeoJSON" -lco COORDINATE_PRECISION=4 map_data_ES_filtered_reduced.json map_data_ES_filtered.json
