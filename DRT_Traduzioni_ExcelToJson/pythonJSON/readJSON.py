import json

#Map(Brand, Map(country, Map(language, Map(privacy))))
with open('test.json') as f:
    data = json.load(f)
"""
for brand, countryMap in data.items():
    print(brand)
    for country, privacyMap in countryMap.items():
        print(country)
        for privacy, keyMap in privacyMap.items():
            print(privacy)
            for key, value in keyMap.items():
                print(key, value)
"""
countries = list(data.get("2_20").keys())
print(countries)

