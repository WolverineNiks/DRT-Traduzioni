import json
import copy
import os

#BrandList
brands = {"Marni":"4_40", "Margiela":"5_80", "D2":"1_60", "JC":"1_130", "Diesel":"2_20", "JilSander":"6_90"}
langFilesMap = {"ca":{}, "da":{}, "de":{}, "el":{}, "en":{}, "en_GB":{}, "es":{}, "fi":{}, "fr":{}, "it":{}, "ja":{}, "ko":{}, "nl":{}, "no":{}, "pt":{}, "sv":{}, "zh":{}, "zh_HK":{}}
os.chdir(r'C:\\Users\\nikhi\\Documents\\GIT-DRT_Traduzioni\\DRT_Traduzioni_ExcelToJson\\pythonJSON')
for lang in langFilesMap.keys():
    path = 'testResultJsons\\' + lang + '.json'
    print("Processing: " + path)
    fRead = open(path, encoding="utf-8")
    data = json.load(fRead)
    langFilesMap[lang] = data
    fRead.close()

for langKey in langFilesMap.keys():
    