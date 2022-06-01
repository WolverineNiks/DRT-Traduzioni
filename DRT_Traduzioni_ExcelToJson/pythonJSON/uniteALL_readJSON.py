import json
import copy
import os

#BrandList
brands = {"Marni":"4_40", "Margiela":"5_80", "D2":"1_60", "JC":"1_130", "Diesel":"2_20", "Sander":"6_90"}

#Map(Brand, Map(country, Map(language, Map(privacy))))
langFilesMap = {"ca":{}, "da":{}, "de":{}, "el":{}, "en":{}, "en_GB":{}, "es":{}, "fi":{}, "fr":{}, "it":{}, "ja":{}, "ko":{}, "nl":{}, "no":{}, "pt":{}, "sv":{}, "zh":{}, "zh_HK":{}}
print("Retrieving jsons from files...")
os.chdir(r'C:\\Users\\nikhi\\Documents\\GIT-DRT_Traduzioni\\DRT_Traduzioni_ExcelToJson\\pythonJSON')
for defJson in langFilesMap.keys():
    path = 'jsons\\' + defJson + '.json'
    print("Processing: " + path)
    fRead = open(path, encoding="utf-8")
    data = json.load(fRead)
    langFilesMap[defJson] = data
    fRead.close()
print("JSON files stored successfuly!")

for brand in brands.keys():
    print("Processing " + brand + " " + brands[brand])
    brandCode = brands[brand]
    for lang in langFilesMap.keys():
        sourceFile = 'resultJsons\\' + brand + '_' + lang + '.json'
        fRead = open(sourceFile, encoding="utf-8")
        print("Source file: " + sourceFile)
        allObjectData = json.load(fRead)
        langFilesMap[lang][brandCode] = allObjectData[brandCode]
        fRead.close()

for lang in langFilesMap.keys():    #For each file to be created
    print("Completing " + lang + " object to save it into " + lang + ".json")
    path = "testResultJsons\\" + lang + '.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(langFilesMap[lang], f, ensure_ascii=False, indent=4)