import os
from qgis.core import (
    QgsVectorLayer, QgsProject
)
from qgis import processing  

#Defining roots
buffered_routes_root = r"C:\Users\zosia\OneDrive\Desktop\FINAL ANALYSIS\Sheffield\Secondary school analysis\buffered routes"
output_root = r"C:\Users\zosia\OneDrive\Desktop\FINAL ANALYSIS\Sheffield\Secondary school analysis\merged data"
#Loading the point layer from QGIS
point_layer = QgsProject.instance().mapLayersByName("stats19_1979_23_secondary_SY")
if not point_layer:
    print("Point layer 'stats19_combined' not found in QGIS!")
    exit()
point_layer = point_layer[0]

#Creating spatial index for the point layer
processing.run("native:createspatialindex", {'INPUT': point_layer})

#Looping through all school folders
for school_folder in os.listdir(buffered_routes_root):
    school_input_path = os.path.join(buffered_routes_root, school_folder)
    if not os.path.isdir(school_input_path):
        continue

    school_output_path = os.path.join(output_root, school_folder)
    os.makedirs(school_output_path, exist_ok=True)

    print(f"Processing school: {school_folder}")

    for filename in os.listdir(school_input_path):
        if not filename.lower().endswith(".gpkg"):
            continue

        input_file = os.path.join(school_input_path, filename)
        route_name = os.path.splitext(filename)[0]
        output_path = os.path.join(school_output_path, f"joined_{route_name}.gpkg")

        #Loading route layer
        route_layer = QgsVectorLayer(input_file, route_name, "ogr")
        if not route_layer.isValid():
            print(f"Error loading: {input_file}")
            continue

        #Creating spatial index for route layer
        processing.run("native:createspatialindex", {'INPUT': route_layer})

        #Reprojecting if needed
        if route_layer.crs() != point_layer.crs():
            route_layer = processing.run("native:reprojectlayer", {
                'INPUT': route_layer,
                'TARGET_CRS': point_layer.crs().authid(),
                'OUTPUT': 'memory:reprojected'
            })['OUTPUT']
            print(f"Reprojected '{route_name}' to match CRS.")

        #Joining points to routes using the "Join attributes by location"
        joined_result = processing.run("native:joinattributesbylocation", {
            'INPUT': point_layer,
            'JOIN': route_layer,
            'PREDICATE': [0, 1, 2],  #intersects, contains, within
            'METHOD': 1, #One-to-many
            'DISCARD_NONMATCHING': True,
            'OUTPUT': 'memory:joined'
        })['OUTPUT']

        #Keeping only accident_reference, route_id, and length_m
        all_fields = joined_result.fields().names()
        fields_to_keep = ['accident_reference', 'route_id', 'length_m']
        fields_to_drop = [f for f in all_fields if f not in fields_to_keep and f != 'geometry']

        cleaned = processing.run("native:deletecolumn", {
            'INPUT': joined_result,
            'COLUMN': fields_to_drop,
            'OUTPUT': output_path
        })['OUTPUT']

        print(f"Saved with accident_reference + route_id: {output_path}")

print("All routes joined with collision data and saved.")
