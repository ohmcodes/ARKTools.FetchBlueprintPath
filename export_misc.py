import unreal
import os
import json

project_path = "/Game/"
base_directory = 'D:/REPO/ARKTools.FetchBlueprintPath/'
output_path = base_directory + 'output.txt' #debugging

Maps = {
   'PrimalEarth',
   'ScorchedEarth',
   'Extinction',
   'Aberration'
}

Categories = {
   'Items',
   #'Resources',
  # 'Weapons',
   #'Dinos'
}

Excludes = {
   'Base',
   'Generic',
   'Craftable',
   'Impacts',
   'BoneModifiersContainer',
   'StartingNote', # Player Specimen
   #'SuperTestMeat',
   'PrimalItemConsumableSeed',
   'Test',
   'RecipeNote_Dye',
   'BeetlePoop',
   'SpeedHack',
   'DevKitMaster',
   'Buff'
}

NamesUnderscored = [
   {'Flag':'PrimalItemStructure_'},
   {'Tek':'PrimalItemStructure_'},
   {'CropPlot':'PrimalItemStructure_'},
   {'SleepingBag':'PrimalItemStructure_'},
   {'StorageBox':'PrimalItemStructure_'},
   {'BearTrap':'PrimalItemStructure_'}
]

def createBPPath(asset):
   # /Game/PrimalEarth/CoreBlueprints/Items/Consumables/PrimalItemConsumable_Berry_Amarberry
   path_components = str(asset.package_path).replace("/Game/", "").split('/')
   name_components = str(asset.package_name).replace("/Game/", "").split('/')

   # temp
   if 'Misc' not in str(asset.package_path): return ""

   if is_assets_in_exludes(str(asset.package_name)): return ""

   if "_" in str(asset.package_name):
      item_components = str(asset.package_name).split('_')
      item_name = item_components[-1]
   else:
      item_name = str(asset.package_name)

   # Extract map name
   map_name = path_components[0]

   category = path_components[2] if len(path_components)-1 > 1 else ""
   sub_category = path_components[3] if len(path_components)-1 > 2 else ""
   item_type = path_components[4] if len(path_components)-1 > 3 else ""

   print(item_name)
   item_name_fix, item_type_fix = get_underscored_names(asset)
   if item_name_fix != "":
      item_name = item_name_fix
   
   item_data = {
      "item_name": item_name,
      "category": category,
      "sub_category": sub_category,
      "type": item_type,
      "map": map_name,
      "class": f"{str(name_components[-1])}_C",
      "engram": f"EngramEntry_{item_name}_C",
      "blueprint_path": f"Blueprint'{str(asset.package_path)}/{str(name_components[-1])}.{str(name_components[-1])}'",
      "real_path": str(asset.package_name)
   }

   return item_data

def get_underscored_names(asset):
   name_components = str(asset.package_name).replace("/Game/", "").split('/')

   for item in NamesUnderscored:
       for key, value in item.items():
         if key in str(name_components[-1]):
            item_name = str(asset.package_name).split(value)[-1]
            item_type = key
            return item_name, item_type
   
   return "",""

def export_json(results):
  # Convert the nested dictionary to JSON with double quotes
  json_string = json.dumps(results, ensure_ascii=False, indent=2)
  # Write JSON data to a file
  with open(base_directory+'blueprints-misc.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_string)

def is_assets_in_exludes(package_path):
  for ex in Excludes:
      if ex in package_path:
          return True
  return False

def is_asset_in_maps(asset):
  package_path = str(asset.package_path)
  for map_name in Maps:
      if map_name in package_path:
          return True
  return False
  
def is_asset_in_category(asset):
  package_path = str(asset.package_path)
  for cat in Categories:
      if cat in package_path:
          return True
  return False

def LoopUEAssets():
  asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
  all_assets = asset_registry.get_assets_by_path(project_path, recursive=True)
  counter = 0
  results = []

  for asset in all_assets:
    if is_asset_in_maps(asset) and is_asset_in_category(asset) and asset.asset_class_path.asset_name=='Blueprint':
      res = createBPPath(asset)
      if res != "": results.append(res) 
      
    counter+=1
    #if(counter == 1000): break

  export_json(results)
        
# Call Entry point
LoopUEAssets()
