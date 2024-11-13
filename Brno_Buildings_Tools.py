bl_info = {
    "name": "Brno Buildings Tools",
    "author": "Josef Divín",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Toolbar > Brno Buildings Tools",
    "description": "Import and manipulate 3D Model Of Brno",
    "warning": "",
    "doc_url": "",
    "category": "Mesh"
}


import bpy
import os
# Clear console
os.system('cls' if os.name == 'nt' else 'clear')
def update_directory(self, context):
    # Get the absolute path of the selected directory
    directory = bpy.path.abspath(self.my_directory)
    if os.path.isdir(directory):
        bpy.data.scenes["Scene"].my_directory = directory
        # List all folders in the selected directory
        folders = [(folder, folder, "") for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
        bpy.types.Scene.my_folders_enum = bpy.props.EnumProperty(
            name="Folders",
            description="Choose a folder",
            items=folders 
        )

class BrnoBuildingTools(bpy.types.Panel):
    bl_label = "Import buildings"
    bl_idname = "PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Brno Buildings Tools'

    bpy.types.Scene.my_directory = bpy.props.StringProperty(
    name="Directory",
    description="Select a directory",
    subtype='DIR_PATH',
    update=update_directory  # Call this function when the directory is changed
)

    # Add a dynamic EnumProperty for the dropdown menu
    bpy.types.Scene.my_folders_enum = bpy.props.EnumProperty(
        name="Base Grid Cell",
        description="Chose bas grid cell",
        items=[('NONE', 'No Grid Cell', '')]  
    )

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Directory path selection
        layout.prop(scene, "my_directory")

        # Dropdown menu for folders
        layout.prop(scene, "my_folders_enum")

        layout.operator("object.import_building")
class ImportBuildingButton(bpy.types.Operator):
    bl_label = "Import Buildings"
    bl_idname = 'object.import_building'
    bl_description = "Import building and terain to scene. Make colection with name of grid (Grdi_Cell_121). These colection contain these object layer with number of Grid Cell: [Terrain_121, Svisle_steny_121, Sikme_strechy_121, Zakladova_deska_121, Vodorovne_strechy_121]."
    
    def execute(self, context):
        directory = bpy.data.scenes["Scene"].my_directory
        selectCell = bpy.data.scenes["Scene"].my_folders_enum
        importObjData(directory, selectCell)
        return {'FINISHED'}
class GroupLayers( bpy.types.Panel):
    bl_idname = "groupLayers"
    bl_label = "Group layers"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Object Adder'
    bl_parent_id = 'PT_MainPanel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.operator("object.group_laye")
        


class GroupLayersButton(bpy.types.Operator):
    bl_label = "Group Layers"
    bl_idname = 'object.group_laye'
    bl_description = "Group all grid layers to 5 layer [Terrain, Svisle_steny, Sikme_strechy, Zakladova_deska, Vodorovne_strechy] and set these layer in to two colection [Terrain,Buildings]."

    def execute(self, context):
        groupLayers()
        return {'FINISHED'}

# Get x, y, z coordinate from global.fwt file
def getFETdata(GridCell, base_dir):
    filePath = os.path.join(base_dir,GridCell, "global.fwt")
    file = open(filePath,'r')
    counter = 0
    arrayCoordi = ["x", "z", "y"]
    objectCordi = {}
    for x in file:
        objectCordi[arrayCoordi[counter]] = x[6:-1]
        counter +=1
    file.close
    return objectCordi

def calculateCoordinate(coordinats, GridCell, base_dir):
    baseCoordi = getFETdata(GridCell, base_dir)
    y_cord = float(baseCoordi["y"]) - float(coordinats["y"])
    x_cord = float(coordinats["x"]) - float(baseCoordi["x"])
    z_cord = float(coordinats["z"]) - float(baseCoordi["z"])
    return (x_cord, y_cord, z_cord)


def importObjs(GridCell, base_dir):
    gridPahPath = os.path.join(base_dir,GridCell)
    onlyfiles = [f for f in os.listdir(gridPahPath) if os.path.isfile(os.path.join(gridPahPath, f))]
    #Create new colection with folder name
    my_coll = bpy.data.collections.new(GridCell)
    bpy.context.scene.collection.children.link(my_coll)
    bpy.context.collection.get(GridCell)
    newCoordinate = None
    if(GridCell != bpy.data.scenes["Scene"].my_folders_enum):

        remoteCoordinate = getFETdata(GridCell,base_dir)
        newCoordinate = calculateCoordinate(remoteCoordinate, bpy.data.scenes["Scene"].my_folders_enum, base_dir)
    
    for fildir in onlyfiles:
        if(fildir[-3:] == "obj"):
            gridObjectPath = os.path.join(gridPahPath,fildir)
            #Import obj file to blender
            if(bpy.app.version[0] == 3):

                bpy.ops.import_scene.obj(filepath=gridObjectPath)
            if(bpy.app.version[0] == 4):
                bpy.ops.wm.obj_import(filepath=gridObjectPath)

            #Select object
            obj = bpy.context.selected_objects[0]

            if(newCoordinate):
                obj.location = newCoordinate

            #Prevent to add .001 to end of layer name
            obj.data.name = obj.data.name[:-4]
                
            # Add date to colection
            my_coll.objects.link(obj)
            # Get all colection
            collections = [col for col in obj.users_collection]
            for collection in collections:
                # Unlink colection
                if(collection.name[-4:] !=obj.name[-4:]):
                    collection.objects.unlink(obj)
            
def importObjData(base_dir, zeroGridValue):

    # Get folder name
    path = os.listdir(base_dir)

    # Remove zeroGridValue from folder dir
    path.remove(zeroGridValue)

    for folder in path:
        importObjs(folder, base_dir)    
    importObjs(zeroGridValue, base_dir)

def sortToColoection():
    values = bpy.data.objects.values()
    terrainColl = bpy.data.collections.new("Terrain")
    buildingColl = bpy.data.collections.new("Buildings")
    bpy.context.scene.collection.children.link(terrainColl)
    bpy.context.scene.collection.children.link(buildingColl)
    for objValue in values:
        collections = [col.name for col in objValue.users_collection]
        
        collectionUnlink = bpy.data.collections.get(collections[0])
        objValue.name = objValue.name[:-4]
        if(objValue.name[:7] == "Terrain"):
            terrainColl.objects.link(objValue)
        else:
            buildingColl.objects.link(objValue)

        collectionUnlink.objects.unlink(objValue)
            
def groupObjects(objectArray):
    
    bpy.context.view_layer.objects.active = objectArray[0]
    for obj in objectArray:
        obj.select_set(True)
    
    bpy.ops.object.join()
    
    for objekt in bpy.context.selected_objects:
        objekt.select_set(False)

def removeAllCollection():
    colections = bpy.data.collections
    for colection in colections:       
        if(colection.name != "Buildings" and colection.name != "Terrain"):
            colections.remove(colection)
            
def unselectAll():
    for objekt in bpy.context.selected_objects:
        objekt.select_set(False)    

def groupLayers():
    values = bpy.data.objects.values()
    terrain_OBJ_array = []
    svisle_steny_OBJ_array = []
    sikme_strechy_OBJ_array = []
    zakladova_deska_OBJ_array = []
    vodorovne_strechy_OBJ_array = []
    for objValue in values:
        if(objValue.name[:7] == "Terrain"):
            terrain_OBJ_array.append(objValue)
        elif(objValue.name[:12] == "Svisle_steny"):
            svisle_steny_OBJ_array.append(objValue)
        elif(objValue.name[:13] == "Sikme_strechy"):
            sikme_strechy_OBJ_array.append(objValue)
        elif(objValue.name[:15] == "Zakladova_deska"):
            zakladova_deska_OBJ_array.append(objValue)
        elif(objValue.name[:17] == "Vodorovne_strechy"):
            vodorovne_strechy_OBJ_array.append(objValue)

    unselectAll()
    groupObjects(terrain_OBJ_array)
    groupObjects(svisle_steny_OBJ_array)
    groupObjects(sikme_strechy_OBJ_array)
    groupObjects(zakladova_deska_OBJ_array)
    groupObjects(vodorovne_strechy_OBJ_array)
    sortToColoection()
    removeAllCollection()

# Register the panel and properties
def register():
    bpy.utils.register_class(BrnoBuildingTools)  
    bpy.utils.register_class(ImportBuildingButton)
    bpy.utils.register_class(GroupLayers)  
    bpy.utils.register_class(GroupLayersButton)  
    
# Unregister the panel and properties
def unregister():
    bpy.utils.unregister_class(BrnoBuildingTools)
    bpy.utils.unregister_class(ImportBuildingButton)
    bpy.utils.unregister_class(GroupLayers)
    bpy.utils.unregister_class(GroupLayersButton) 
   

if __name__ == "__main__":
    register()
