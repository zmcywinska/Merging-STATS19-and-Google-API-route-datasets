import geopandas as gpd
import os

input_root = r"C:\Users\zosia\OneDrive\Desktop\FINAL ANALYSIS\Sheffield\Secondary school analysis\separated routes"
output_root = r"C:\Users\zosia\OneDrive\Desktop\FINAL ANALYSIS\Sheffield\Secondary school analysis\buffered routes"

#Creating output root folder if it doesn't exist
os.makedirs(output_root, exist_ok=True)

#Walking through each school folder
for school_folder in os.listdir(input_root):
    school_input_path = os.path.join(input_root, school_folder)

    if not os.path.isdir(school_input_path):
        continue  # Skip if not a folder

    #Creating matching output folder
    school_output_path = os.path.join(output_root, school_folder)
    os.makedirs(school_output_path, exist_ok=True)

    #Processing each GPKG in the school folder
    for file_name in os.listdir(school_input_path):
        if not file_name.lower().endswith(".gpkg"):
            continue

        input_file_path = os.path.join(school_input_path, file_name)
        output_file_path = os.path.join(school_output_path, file_name)

        #Loading, buffer, and save
        gdf = gpd.read_file(input_file_path)
        buffered_gdf = gdf.copy()
        buffered_gdf['geometry'] = buffered_gdf['geometry'].buffer(0.000150)
        buffered_gdf.to_file(output_file_path, driver="GPKG")

        print(f"Buffers added and saved: {output_file_path}")

print("All buffers created succesfully.")