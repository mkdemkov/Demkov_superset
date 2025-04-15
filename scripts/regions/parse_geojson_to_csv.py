import json
import csv

with open('data/Russia_regions.geojson', 'r', encoding='utf-8') as f:
    data = json.load(f)

rows = []
for feature in data["features"]:
    reg_name = feature["properties"]["region"]
    geom = json.dumps(feature["geometry"])  # сериализация geometry в строку
    rows.append([reg_name, geom])

with open('regions.csv', 'w', encoding='utf-8', newline='') as out:
    writer = csv.writer(out, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(["region", "geometry"])
    writer.writerows(rows)


# import json
# import csv

# features = [
#     {
#         "region": "Алтайский край",
#         "geometry": {
#             "type": "Polygon",
#             "coordinates": [ ... ]
#         }
#     },
#     ...
# ]

# with open("regions.csv", "w", encoding="utf-8", newline="") as f:
#     writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
#     writer.writerow(["region", "geometry"])
#     for feat in features:
#         # сериализовать geometry в JSON (одна строка)
#         geom_json = json.dumps(feat["geometry"], ensure_ascii=False)
#         writer.writerow([feat["region"], geom_json])
