import geopandas as gpd
import os

#Path to the folder containing all the separated 
base_folder = r"C:\Users\zosia\OneDrive\Desktop\FINAL ANALYSIS\Sheffield\Secondary school analysis\separated routes"

#Looping through each school folder inside the base folder
for school_folder in os.listdir(base_folder):
    school_path = os.path.join(base_folder, school_folder)

    #Skipping if it's not a folder
    if not os.path.isdir(school_path):
        continue

    #Formatting the school name (e.g. "All Saints Catholic High" -> "all_saints_catholic_high")
    formatted_school_name = school_folder.lower().replace(" ", "_")

    #Getting all .gpkg files in the school folder
    gpkg_files = [f for f in os.listdir(school_path) if f.lower().endswith(".gpkg")]

    for gpkg_file in gpkg_files:
        file_path = os.path.join(school_path, gpkg_file)

        #Loading the GeoDataFrame
        gdf = gpd.read_file(file_path)

        #Removing file extension to get base name
        base_name = os.path.splitext(gpkg_file)[0]

        #Generating the route_id
        route_id = f"{formatted_school_name}_{base_name}"

        #Adding a route_id column
        gdf["route_id"] = route_id

        #Saving it back to the same file (overwrite)
        gdf.to_file(file_path, driver="GPKG")

        print(f"Updated '{gpkg_file}' in '{school_folder}' with route_id = '{route_id}'")

print("All route_id fields added successfully.")