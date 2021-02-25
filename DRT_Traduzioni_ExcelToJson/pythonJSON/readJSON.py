import json
import copy

#CONSTANTS 
BRAND = "2_20"
COUNTRY_PH = "<CONT>"   #PH = Place holder
LANGUAGE_PH = "<LANG>"
PARA_PH = "<PARA>"
END_PH = "<END>"
MarketingJSON_PH = "FLAG_MARKETING_OPTIN_TEXT"
ProfilingJSON_PH = "FLAG_PROFILING_OPTIN_TEXT"
NamJSON_PH = "GENERAL_CONSENT_NAM"
smsJSON_PH = "FLAG_TEXT_MESSAGE"

#Map(Brand, Map(country, Map(language, Map(privacy))))
langFilesMap = {"de":{}, "en":{}, "en_GB":{}, "es":{}, "fr":{}, "it":{}, "ja":{}, "ko":{}, "pt":{}, "zh":{}, "zh_HK":{}}
print("Retrieving jsons from files...")
for defJson in langFilesMap.keys():
    path = "C:\\Users\\NikhilChander\\Documents\\OTB\\GIT-DRT_Traduzioni\\DRT_Traduzioni_ExcelToJson\\pythonJSON\\jsons\\" + defJson + ".json"
    print("Processing: " + path)
    fRead = open(path, encoding="utf-8")
    data = json.load(fRead)
    langFilesMap[defJson] = data
    fRead.close()
print("JSON files stored successfuly!")
sourceFile = 'fixDiesel.html'
srcRead = open(sourceFile, 'r', encoding="utf-8")
lang = ""
country = ""
marketing = ""
profiling = ""
nam = ""
sms = ""
print("Reading the source file...")
while True:
    line = srcRead.readline().strip()
    if len(line) > 0:
        if line.startswith(COUNTRY_PH): #Country
            if country == "":
                country = line[6:]
            else:
                country = "ERROR_COUNTRY " + line
        elif line.startswith(LANGUAGE_PH):  #Language
            if lang == "":
                lang = line[6:]
            else:
                lang = "ERROR_LANG " + line 
        elif line.startswith(PARA_PH):
            if marketing == "": #Marketing
                marketing = line[6:]
            elif profiling == "":   #Profiling
                profiling = line[6:]
            else:
                if country == "CA" or country == "US":
                    if nam == "":   #Canada NAM
                        nam = line[6:]
                    elif sms == "": #Canada SMS
                        sms = line[6:]
                    else:
                        nam = "ERROR_PARA_NAM " + line
                        sms = "ERROR_PARA_SMS " + line 
                else:
                    marketing = "ERROR_PARA " + line
                    profiling = marketing
    if country != "" and lang != "" and marketing != "" and profiling != "":
        print("Processing Country: " + country + " Language: " + lang)
        if lang in langFilesMap:    #JSON for this lang already exists
            langObj = langFilesMap[lang]
            if country in langObj[BRAND]:   #JSON has also this country
                langObj[BRAND][country]["PRIVACY"][MarketingJSON_PH] = marketing
                langObj[BRAND][country]["PRIVACY"][ProfilingJSON_PH] = profiling
                if nam != "" and sms != "":
                    print("Canada or USA are here!")
                    langObj[BRAND][country]["PRIVACY"][NamJSON_PH] = nam
                    langObj[BRAND][country]["PRIVACY"][smsJSON_PH] = sms
            else:   #New country for the json
                print("Creating new country: " + country + " for " + lang + ".json")
                basicObj = {
                    "HEADER": "PRIVACY PREFERENCES",
                    "HEADER_SUB": "I confirm that I’m 16 years old and I have read the information notice provided by the Data Controllers in accordance with local applicable laws, I understand that providing the personal data for profiling and marketing purposes is optional and I:",
                    "HEADER_SUB_1": "",
                    NamJSON_PH: "",
                    "HEADER_SUB_2": "",
                    MarketingJSON_PH: marketing,
                    ProfilingJSON_PH: profiling,
                    "HEADER_SUB_3": "",
                    "FOOTER_SUB_1": "",
                    smsJSON_PH: "",
                    "PRIVACY_LINK": "for full text of information notice click here",
                    "PRIVACY_LINK_DCB": "I confirm that I have read privacy policy.",
                    "PRIVACY_MARKETING_LINK": "for full details about marketing purposes click here",
                    "PRIVACY_PROFILING_LINK": "for details about profiling purposes click here",
                    "PRIVACY_TERMCOND_LINK": "full text of T&Cs please click here",
                    "AGREE": "Agree"
                }
                if nam != "" and sms != "":
                    basicObj[NamJSON_PH] = nam
                    basicObj[smsJSON_PH] = sms
                privacyObj = {
                    "PRIVACY":basicObj
                }
                langObj[BRAND][country] = privacyObj
        else:   #New JSON for the language
            print("Creating new file " + lang + ".json")
            newLangObj = copy.deepcopy(langFilesMap["en"])
            if country in newLangObj[BRAND]:   #JSON has also this country
                newLangObj[BRAND][country]["PRIVACY"][MarketingJSON_PH] = marketing
                newLangObj[BRAND][country]["PRIVACY"][ProfilingJSON_PH] = profiling
                if nam != "" and sms != "":
                    newLangObj[BRAND][country]["PRIVACY"][NamJSON_PH] = nam
                    newLangObj[BRAND][country]["PRIVACY"][smsJSON_PH] = sms
            else:   #New country for the json
                basicObj = {
                    "HEADER": "PRIVACY PREFERENCES",
                    "HEADER_SUB": "I confirm that I’m 16 years old and I have read the information notice provided by the Data Controllers in accordance with local applicable laws, I understand that providing the personal data for profiling and marketing purposes is optional and I:",
                    "HEADER_SUB_1": "",
                    NamJSON_PH: "",
                    "HEADER_SUB_2": "",
                    MarketingJSON_PH: marketing,
                    ProfilingJSON_PH: profiling,
                    "HEADER_SUB_3": "",
                    "FOOTER_SUB_1": "",
                    smsJSON_PH: "",
                    "PRIVACY_LINK": "for full text of information notice click here",
                    "PRIVACY_LINK_DCB": "I confirm that I have read privacy policy.",
                    "PRIVACY_MARKETING_LINK": "for full details about marketing purposes click here",
                    "PRIVACY_PROFILING_LINK": "for details about profiling purposes click here",
                    "PRIVACY_TERMCOND_LINK": "full text of T&Cs please click here",
                    "AGREE": "Agree"
                }
                if nam != "" and sms != "":
                    basicObj[NamJSON_PH] = nam
                    basicObj[smsJSON_PH] = sms
                privacyObj = {
                    "PRIVACY":basicObj
                }
                newLangObj[BRAND][country] = privacyObj
            langFilesMap[lang] = newLangObj
        marketing = "" 
        profiling = "" 
        lang = "" 
        country = ""
        nam = ""
        sms = ""
    if line == END_PH:
        break

for lang in langFilesMap.keys():
    path = "C:\\Users\\NikhilChander\\Documents\\OTB\\GIT-DRT_Traduzioni\\DRT_Traduzioni_ExcelToJson\\pythonJSON\\resultJsons\\" + lang + '.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(langFilesMap[lang], f)

srcRead.close()
"""
megaStr = ""

data = langFilesMap["ja"]

for brand, countryMap in data.items():
    megaStr = megaStr + "Brand: " + str(brand) + "\n"
    for country, privacyMap in countryMap.items():
        megaStr = megaStr + "Country: " + str(country) + "\n"
        for privacy, keyMap in privacyMap.items():
            megaStr = megaStr + "Privacy: " + str(privacy) + "\n"
            for key, value in keyMap.items():
                megaStr = megaStr + "KEY: " + str(key) + "VALUE: " + str(value) + "\n"
with open('test.txt', 'w', encoding="utf-8") as writer:
    writer.writelines(megaStr)

"""



