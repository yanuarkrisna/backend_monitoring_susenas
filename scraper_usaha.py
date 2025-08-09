import requests
import pandas as pd

# Bounding box Luwu (min_lat, min_lon, max_lat, max_lon)
bbox = (-3.6975, 120.0043, -2.9470, 121.3587)

query = f"""
[out:json][timeout:90];
(
  node["shop"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  way["shop"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  relation["shop"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});

  node["office"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  way["office"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  relation["office"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});

  node["amenity"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  way["amenity"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
  relation["amenity"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
);
out center;
"""

response = requests.get("https://overpass-api.de/api/interpreter", params={"data": query})
data = response.json()

results = []
for el in data["elements"]:
    tags = el.get("tags", {})
    lat = el.get("lat")
    lon = el.get("lon")
    if not lat or not lon:
        center = el.get("center", {})
        lat = center.get("lat")
        lon = center.get("lon")
    results.append({
        "Nama": tags.get("name", ""),
        "Shop": tags.get("shop", ""),
        "Amenity": tags.get("amenity", ""),
        "Office": tags.get("office", ""),
        "Latitude": lat,
        "Longitude": lon
    })

df = pd.DataFrame(results)
df.to_excel("usaha_luwu_bbox.xlsx", index=False)
print(f"Berhasil disimpan! Total data: {len(df)}")
