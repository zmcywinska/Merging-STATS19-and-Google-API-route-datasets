import os
from qgis.core import QgsProject, QgsVectorLayer, QgsLayerTreeLayer

#Path to the folder containing the route shapefiles
root = r"F:\Dyski współdzielone\PHY346 Shared Drive\Data\Codes and datasets - James\Sheffield routes\SheffieldSecondaryCatchments"

#Current QGIS project
proj = QgsProject.instance().layerTreeRoot()

#Creating a group for the route layers
group = proj.insertGroup(0, 'RoutesSplit')

# Looping through each route file in the root folder
for file in os.listdir(root):
    if file.lower().endswith('.shp'):                   #Looks for files ending with .shp
        shp_path = os.path.join(root, file)
        layer = QgsVectorLayer(shp_path, file[:-4], 'ogr')
        if layer.isValid():
            QgsProject.instance().addMapLayer(layer, False)
            group.insertChildNode(0, QgsLayerTreeLayer(layer))
            print(f"Loaded: {file}")
        else:
            print(f"Invalid shapefile: {file}")
