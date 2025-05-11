# Merging-STATS19-and-Google-API-route-datasets
  This repository contains code for merging the UK Stats19 dataset with Google API route shapefiles, which was performed as a part of the PHY346 School Safety Project. Python was used to automate each step in the data processing integration in QGIS, allowing for large datasets to be processed efficiently and quickly. Below is a list stating in what order do the codes need to be ran, along with a short description of each step.
  
  1. Opening routes.py - The original route folders contain files with different file extensions. This code loops through the folder and opens all the .shp files in QGIS
  
  2. Splitting routes.py - Each layer contains all the routes to a given school. This code creates a folder with separate subfolders for every school, each one containing a distinct 
     geopackage file for every route, allowing for all routes to be studied individually.
 
  3. Add route id.py - Loops through all geopackage files and adds a unique route_id for each route based on the school name.
 
  4. Add buffer.py - Loops through all geopackage files and adds a buffer
 
  5. Merge with stats19.py - Executes "Join Attributes by Location" for every buffered route. The output files contain the route_id, as well as the accident_reference, allowing us to link     
     specific casualties to particular routes.
