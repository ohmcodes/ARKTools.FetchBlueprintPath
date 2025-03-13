import unreal
import os
import json

project_path = "/Game/"
base_directory = 'D:/REPO/ARKTools.FetchBlueprintPath/'
output_path = base_directory + 'output.txt'

Maps = {
   'PrimalEarth',
   'ScorchedEarth',
   'Extinction'
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
   'RecipeNote_Dye'
}

def createIconPath(results, asset):
  #if ("Icons" in str(asset.package_name) or "Icon" in str(asset.package_path)) or (asset.asset_class_path.asset_name=='Texture2D' or asset.asset_class_path.asset_name=='Blueprint') and "IconGenerator" not in str(asset.package_path) and "UltraDynamicSky" not in str(asset.package_path):
  current_dict = results
  path_components = str(asset.package_path).replace("/Game/","").split('/')
  for component in path_components:
    current_dict = current_dict.setdefault(component, {})

  current_dict[str(asset.asset_name)] = str(asset.package_name) + "." + str(asset.asset_name)

  return results



def createBPPath(asset):
  # /Game/PrimalEarth/CoreBlueprints/Items/Consumables/PrimalItemConsumable_Berry_Amarberry
  path_components = str(asset.package_path).replace("/Game/", "").split('/')
  name_components = str(asset.package_name).replace("/Game/", "").split('/')

  
  

  # temp
  if 'Consumables' not in str(asset.package_name): return ""

  if is_assets_in_exludes(str(asset.package_name)): return ""

  if "_" in str(asset.package_name):
    item_components = str(asset.package_name).split('_')
    item_name = item_components[-1]
  else:
    item_name = str(asset.package_name)

  # Extract map name
  map_name = path_components[0]

  #print(len(path_components))
  
  if path_components[1] == 'Dinos':
    category = path_components[1]
    sub_category = path_components[2] if len(path_components)-1 > 1 else ""
    item_type = path_components[3] if len(path_components)-1 > 2 else ""
  else:
    category = path_components[2] if len(path_components)-1 > 1 else ""
    sub_category = path_components[3] if len(path_components)-1 > 2 else ""
    item_type = path_components[4] if len(path_components)-1 > 3 else ""

  if sub_category == 'Artifacts':
     item_name = name_components[-1]

  #print(asset.package_path, file=open(output_path, "a"))
  #print(asset.package_name, file=open(output_path, "a"))

  if sub_category == '' and "PrimalItemStructure" in item_name:
     sub_category = 'Structure'

  if sub_category == 'Consumables' and "Berry" in str(name_components[-1]):
     item_type = "Berry"

  if 'CustomDrinkRecipe' in item_name and len(item_components)-1 > 1:
     item_name = item_name.split('PrimalItem_')[1]
     item_type = 'CustomDrinkRecipe'

  if 'RawMeat' in item_name and len(item_components)-1 > 1:
     item_type = 'RawMeat'
     item_name = item_name.split('PrimalItemConsumable_')[1]
  
  if 'RawPrimeMeat' in item_name and len(item_components)-1 > 1:
     item_type = 'RawPrimeMeat'
     item_name = item_name.split('PrimalItemConsumable_')[1]

  if 'MulticraftItem' in item_name and len(item_components)-1 > 1:
     item_type = 'MulticraftItem'
     item_name = item_name.split('PrimalItemConsumable_MulticraftItem_')[1]

  if 'Veggie' in item_name:
     item_type = 'Veggie'
  
  if 'Soup' in item_name:
     item_type = 'Soup'

  if "RecipeNote_Kibble" in item_name and len(item_components)-1 > 1:
     item_name = item_name.split('PrimalItem_')[1]
     item_type = 'Kibble'

  if "Consumable_Kibble" in item_name and len(item_components)-1 > 1:
     item_name = item_name.split('PrimalItemConsumable_Kibble')[1]
     item_type = 'Kibble'

  if "Dye" in item_name:
     if sub_category == "":
      sub_category = 'Dye' 
     else:
      item_type = 'Dye'

  if 'Egg_' in item_name and 'PrimalItemConsumable_' in item_name:
     item_name = item_name.split('PrimalItemConsumable_')[1]
     item_type = name_components[-1]

  #Egg_Small
  #Egg_XtraLarge
  #Fertilizer_Compost
  #Egg_XSmall
  #FE_Crafted_CandyCorn
  #Egg_Special
  #Egg_Medium
  #Egg_Large
  #DinoPoopMedium_OnFire
  #Crafted_FourthOfJulyDinoCandy
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
      "real_path": str(asset.package_name),
      "icon_path": ""
  }

  print(item_data, file=open(output_path, "a"))

  return item_data

def export_json(results):
  # Convert the nested dictionary to JSON with double quotes
  json_string = json.dumps(results, ensure_ascii=False, indent=2)
  # Write JSON data to a file
  with open(base_directory+'blueprints.json', 'w', encoding='utf-8') as json_file:
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

  # Filter unnecessary folders IconGenerator and UltraDynamicSky
  # for asset in all_assets:
  #   if (asset.asset_class_path.asset_name=='Blueprint'):

  #     print(asset.package_name)
  #     print(asset.package_path)
  #     print(asset.asset_class_path.asset_name)
  #     bp_path = createBPPath(results, asset)

  
  
        
# Call Entry point
LoopUEAssets()
