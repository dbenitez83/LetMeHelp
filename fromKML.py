from fastkml import kml
import shapely.geometry
import shapely.ops
import json
import geojson
from geojson import Feature, FeatureCollection, dump

with open('zones_potencialment_inundables.kml') as myfile:
    doc=myfile.read()
k = kml.KML()
k.from_string(doc.encode('utf-8'))

outerFeature = list(k.features())
innerFeature = list(outerFeature[0].features())
features = []
#print(help(innerFeature[0]))
for i in innerFeature:
#    print('[{\"name\":\"',i.name)
    features.append(geojson.Feature(geometry=shapely.geometry.asShape(i.geometry), properties={"name":i.name}))
#print( shapely.geometry.asShape(i.geometry))

    #for p in i.geometry:
    #    print(p)
#placemarks = list(innerFeature[0].geometry)
feature_collection = FeatureCollection(features)

with open('myfile.geojson', 'w') as f:
   dump(feature_collection, f)
