# Brno Buildings Tools
<img src="img/interface.png" alt="">

1. It is an add-on to <a target="blank" href="https://www.blender.org/">Blender</a> 
2. The tool is used to import, and grouping downloaded 3D data of Brno into Blender

3.  Add-on is composed of two tools:
   - <img src="img/main_tools.png" alt="">
   - <b>Import 3D data (Import Buildings)</b>
      - Used to import data into Blender to 0,0 coordinates
      - Creating collections based on the name of individual squares (grid_cell) 
      - Uploading individual parts of buildings (Pitched_roofs, Horizontal_roofs, Vertical_walls,  Base_plate) and terrain into these collections
      - <img src="img/outliner_import_cz.png" alt="">
   - <b>Group Layers (Groups Layer)</b>
      - Create two collections: Buildings (Pitched_roofs, Horizontal_roofs, Vertical_walls,  Base_plate) and Terrain
      - Group all data based on their category
      - <img src="img/outliner_group_cz.png" alt="">

# Instruction - preprocessing

1. If you don't have it, install <a target="blank" href="https://www.blender.org/">Blender</a> version 4.0.0 or higher
2. Download 3D data in ".obj" format from <a target="blank" href="https://webmaps.kambrno.cz/DTM_and_3d_buildings_download/">download app</a>

<img src="img/download_app.png" alt="">

3. Unzip downloaded 3D data

# Instruction - installing

1. Download script from <a target="blank" href="Brno_Buildings_Tools.py">repository</a>
2. Open blender and navigate to <b>Edit -> Preferences -> Add-ons</b>
3. Press <b>Install</b> button
4. Navigate to script folder and chose script and Install Add-on
5. If it's disabled, enable <b>Brno Building Tools</b>
- <img src="img/add_ons.png" alt="">
6. After the instalation the tools are available on the right (N) side bar
- <img src="img/side_bar.png" alt="">

# Instruction - using

1. Import buildings

   - <img src="img/import_buildings.png" alt="">
   - <b>Directory</b> - set directory of unzipped downloaded 3D data
   - <b>Grid Cell</b> - select grid cell which will be placed in Blender at coordinates 0,0
      - the other grid cells will be placed relative to this grid cell
   - <b>Import buildings</b> - the button to start the import process
   - <i>Warning: The tool is only used for importing data from specific data structure. In other cases, this tool may not work</i>

2. Group layers
- <img src="img/group_layers.png" alt="">
- <b>Group layers</b> - button to start the grouping process
- <i>Warning: The tool is only used for grouping data prepared using the import script. In other cases, this tool may not work</i>




   










