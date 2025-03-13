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
   'SpeedHack'
}

def createBPPath(asset):
   # /Game/PrimalEarth/CoreBlueprints/Items/Consumables/PrimalItemConsumable_Berry_Amarberry
   path_components = str(asset.package_path).replace("/Game/", "").split('/')
   name_components = str(asset.package_name).replace("/Game/", "").split('/')

   # temp
   if 'Consumables' not in str(asset.package_path): return ""

   if is_assets_in_exludes(str(asset.package_name)): return ""

   if "_" in str(asset.package_name):
      item_components = str(asset.package_name).split('_')
      item_name = item_components[-1]
   else:
      item_name = str(asset.package_name)

   # Extract map name
   map_name = path_components[0]

  #print(len(path_components))
  
   category = path_components[2] if len(path_components)-1 > 1 else ""
   sub_category = path_components[3] if len(path_components)-1 > 2 else ""
   item_type = path_components[4] if len(path_components)-1 > 3 else ""

   if sub_category == 'Consumables' and "Berry" in str(name_components[-1]):
      item_name = str(asset.package_name).split('PrimalItemConsumable_')[1]
      item_type = "Berry"

   if 'CustomDrinkRecipe' in str(asset.package_name) and len(item_components)-1 > 1:
      item_name = str(asset.package_name).split('PrimalItem_')[1]
      item_type = 'CustomDrinkRecipe'

   if 'RawMeat' in str(asset.package_name) and len(item_components)-1 > 1:
      item_type = 'RawMeat'
      item_name = str(asset.package_name).split('PrimalItemConsumable_')[1]

   if 'RawPrimeMeat' in str(asset.package_name) and len(item_components)-1 > 1:
      item_type = 'RawPrimeMeat'
      item_name = str(asset.package_name).split('PrimalItemConsumable_')[1]

   if 'MulticraftItem' in str(asset.package_name) and len(item_components)-1 > 1:
      item_type = 'MulticraftItem'
      item_name = str(asset.package_name).split('PrimalItemConsumable_MulticraftItem_')[1]

   if 'Veggie' in str(asset.package_name):
      item_type = 'Veggie'

   if 'Soup' in str(asset.package_name):
      item_type = 'Soup'

   if "Consumable_Kibble" in str(asset.package_name) and len(item_components)-1 > 1:
      item_name = str(asset.package_name).split('PrimalItemConsumable_')[1]
      item_type = 'Kibble'
      

   if 'Egg_' in str(asset.package_name) and 'PrimalItemConsumable_' in str(asset.package_name):
      itm_split = str(asset.package_name).split('PrimalItemConsumable_')
      item_name = itm_split[1]
      item_type = name_components[-1]

   if 'PrimalItemConsumable_MulticraftItem_' in str(asset.package_name):
      itm_split = str(asset.package_name).split('PrimalItemConsumable_MulticraftItem_')
      item_name = itm_split[1]
      item_type = item_components[1]

   if 'OnFire' in str(asset.package_name):
      itm_split = str(asset.package_name).split('PrimalItemConsumable_')
      item_name = itm_split[1]
      item_type = item_components[1]

   if 'Crafted' in str(asset.package_name):
      item_type = 'Crafted'
      
   if 'CookedPrimeMeat' in str(asset.package_name):
      itm_split = str(asset.package_name).split('PrimalItemConsumable_')
      item_name = itm_split[1]
   
   if 'CookedMeat' in str(asset.package_name):
      itm_split = str(asset.package_name).split('PrimalItemConsumable_')
      item_name = itm_split[1]

   if 'UnlockEmote' in str(asset.package_name):
      itm_split = str(asset.package_name).split('PrimalItemConsumable_')
      item_name = itm_split[1]
   
   if 'SpeedHack' in str(asset.package_name):
      itm_split = str(asset.package_name).split('PrimalItemConsumable_')
      item_name = itm_split[1]
      
   # if 'PrimalItemCustomFoodRecipe' in str(asset.package_name):
   #    itm_split = str(asset.package_name).split('PrimalItem')
   #    item_name = itm_split[1]

   print(item_name)

   #CookedPrimeMeat_Jerky
   #CookedPrimeMeat_Fish
   #CookedPrimeMeat
   #CookedMeat_Jerky
   #CookedMeat_Fish
   #UnlockEmote_Touchdown
   #UnlockEmote_FE_Sniff
   #Seed_Verdberry_SpeedHack
   #PrimalItemConsumable_Seed_Mejoberry_SpeedHack

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

   #print(item_data, file=open(output_path, "a"))
   #print(item_data)

   return item_data

def export_json(results):
  # Convert the nested dictionary to JSON with double quotes
  json_string = json.dumps(results, ensure_ascii=False, indent=2)
  # Write JSON data to a file
  with open(base_directory+'blueprints-consumables.json', 'w', encoding='utf-8') as json_file:
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
