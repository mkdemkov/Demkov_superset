import json

def get_regions_from_geojson(file_path):
    """
    Reads a GeoJSON file and returns a list of region names
    based on the property 'region'.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    res = []
    for feature in data["features"]:
        region_name = feature["properties"]["region"]
        res.append(region_name)
    
    return res

def get_geosjon_keys(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    res = []
    for feature in data["features"]:
        print(feature.keys())
    



if __name__ == "__main__":
    geojson_file = "data/Russia_regions.geojson"
    regions_list = get_regions_from_geojson(geojson_file)
    # get_geosjon_keys(geojson_file)
    print(regions_list)

