import os
from qgis.core import QgsProject, QgsVectorLayer
import processing

#Directory to the output folder - separate subfolder will be created for each school 
output_base = r"C:\Users\zosia\OneDrive\Desktop\FINAL ANALYSIS\Sheffield\Secondary school analysis\separated routes"

#Name of the group in QGIS containing the route layers
group_name = "RoutesSplit"

#Getting the group node
group_node = QgsProject.instance().layerTreeRoot().findGroup(group_name)

if not group_node:
    print(f"Group '{group_name}' not found.")
else:
    #Looping through all route layers in the group
    for child in group_node.children():
        if hasattr(child, 'layer'):
            layer = child.layer()
            layer_name = layer.name()

            #Creating output directory for this layer
            output_folder = os.path.join(output_base, layer_name)
            os.makedirs(output_folder, exist_ok=True)

            #Running "Split vector layer" tool
            processing.run("native:splitvectorlayer", {
                'INPUT': layer,
                'FIELD': 'id',
                'OUTPUT': output_folder,
                'PREFIX_FIELD': False
            })

            print(f"Split completed for layer: {layer_name}")
