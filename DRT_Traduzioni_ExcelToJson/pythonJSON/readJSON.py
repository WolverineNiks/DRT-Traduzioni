import json
import copy

"""
    The SOURCE file should use TAGS and the rigid structure in able to be processed correctly:
    This script process the source file in blocks. To identify the end of a block, the script searches for the <ENDP> tag, so that whenever it reads <ENDP>, it knows that a block is completed and now it has all the info to save it.
    Every block must have a line that starts with:
        - <CONT> for Country
        - <LANG> for Language
        - <PARA> for the text
    Each must have only one tag for Country and one for lang, whereas it can have multiple <PARA> tags.
    <PARA> tags positions are important as it will read them sequently to map them correctly. 
    For this project, first <PARA> is mapped to marketing varibale, secondo one to pofiling variable and, if it exists, third and fourth to nam and sms respectively.
    The Source file must end with <ENDF> tag so that it defines the EOF (End of File). 

    Project requisites:
    This project has a folder with json files, each of it corresponds to a language. (e.g. it.json, en.json,...). The script import those jsons into a python dictionary with keys equivalent to the languages ("it", "de",...). After creating the python dict, it enters the loop to read the source file line by line. Due to the rigid structure of the file, the script can understand the content of every line. Once it reads the line that starts with <ENDP> tag, it saves that block's info into the json. The logic to save the content of a block is:
    Loop:
        read the line from source file
        if it's not blank, try to identify the tag:
            if tag is <CONT>: then the content of the file should be a country (e.g. "AT")
            if tag is <LANG>: then the content of the line should be a language (e.g. "en")
            if tag is <PARA>: 
                based on the position reading the file sequently, it will read the marketing, profiling, nam or sms respectively 
            if tag is <ENDP>: then save it by the following logic:
                Search for the language object in the python dict created early:
                    - if found: 
                        (*)Search for the country into that language object:
                            -if found country:
                                save the <PARA> tag's info into the corresponding key
                            if not found country:
                                create a new country into the language object
                                saves the <PARA> tag's info into te corresponding key
                    - if not found:
                        create a new object into the python dict with the new language as key, and copy the "en" lang object's content into it (a deepcopy)
                        *...
                Clean the variables for next block
            if tag is <ENDF>: 
                break the loop
    
    Dump the python dict into json files
"""
#CONSTANTS 
BRAND = "2_20"
COUNTRY_PH = "<CONT>"   #PH = Place holder
LANGUAGE_PH = "<LANG>"
PARA_PH = "<PARA>"
END_PH = "<ENDF>"
ENDPARA_PH = "<ENDP>"
MarketingJSON_PH = "FLAG_MARKETING_OPTIN_TEXT"
ProfilingJSON_PH = "FLAG_PROFILING_OPTIN_TEXT"
NamJSON_PH = "GENERAL_CONSENT_NAM"
smsJSON_PH = "FLAG_TEXT_MESSAGE"

def saveItToDict(langFilesMap, vars):
    if vars["lang"] in langFilesMap:    #JSON for this vars["lang"] already exists
        langObj = langFilesMap[vars["lang"]]
        if vars["country"] in langObj[BRAND]:   #JSON has also this country! #SAVE: update the json with new variables
            langObj[BRAND][vars["country"]]["PRIVACY"][MarketingJSON_PH] = vars["marketing"]
            langObj[BRAND][vars["country"]]["PRIVACY"][ProfilingJSON_PH] = vars["profiling"]
            if vars["nam"] != "" and vars["sms"] != "":
                print("Canada or USA are here!")
                langObj[BRAND][vars["country"]]["PRIVACY"][NamJSON_PH] = vars["nam"]
                langObj[BRAND][vars["country"]]["PRIVACY"][smsJSON_PH] = vars["sms"]
        else:   #New vars["country"] for the json
            print("Creating new country: " + vars["country"] + " for " + vars["lang"] + ".json")
            basicObj = {
                "HEADER": "PRIVACY PREFERENCES",
                "HEADER_SUB": "I confirm that I’m 16 years old and I have read the information notice provided by the Data Controllers in accordance with local applicable laws, I understand that providing the personal data for profiling and marketing purposes is optional and I:",
                "HEADER_SUB_1": "",
                NamJSON_PH: "",
                "HEADER_SUB_2": "",
                MarketingJSON_PH: vars["marketing"],
                ProfilingJSON_PH: vars["profiling"],
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
            if vars["nam"] != "" and vars["sms"] != "":
                basicObj[NamJSON_PH] = vars["nam"]
                basicObj[smsJSON_PH] = vars["sms"]
            privacyObj = {
                "PRIVACY":basicObj
            }
            langObj[BRAND][vars["country"]] = privacyObj    #SAVE: updates the lang json by creating a new country obj
    else:   #New JSON for the language
        print("Creating new file " + vars["lang"] + ".json")
        newLangObj = copy.deepcopy(langFilesMap["en"])  #a deepcopy of the en object as it's the default language
        if vars["country"] in newLangObj[BRAND]:   #JSON has also this vars["country"]
            newLangObj[BRAND][vars["country"]]["PRIVACY"][MarketingJSON_PH] = vars["marketing"]
            newLangObj[BRAND][vars["country"]]["PRIVACY"][ProfilingJSON_PH] = vars["profiling"]
            if vars["nam"] != "" and vars["sms"] != "":
                newLangObj[BRAND][vars["country"]]["PRIVACY"][NamJSON_PH] = vars["nam"]
                newLangObj[BRAND][vars["country"]]["PRIVACY"][smsJSON_PH] = vars["sms"]
        else:   #New vars["country"] for the json
            basicObj = {
                "HEADER": "PRIVACY PREFERENCES",
                "HEADER_SUB": "I confirm that I’m 16 years old and I have read the information notice provided by the Data Controllers in accordance with local applicable laws, I understand that providing the personal data for profiling and marketing purposes is optional and I:",
                "HEADER_SUB_1": "",
                NamJSON_PH: "",
                "HEADER_SUB_2": "",
                MarketingJSON_PH: vars["marketing"],
                ProfilingJSON_PH: vars["profiling"],
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
            if vars["nam"] != "" and vars["sms"] != "":
                basicObj[NamJSON_PH] = vars["nam"]
                basicObj[smsJSON_PH] = vars["sms"]
            privacyObj = {
                "PRIVACY":basicObj
            }
            newLangObj[BRAND][vars["country"]] = privacyObj
        langFilesMap[vars["lang"]] = newLangObj

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
langPerCountriesMap = {}
for key in langFilesMap.keys():
    langPerCountriesMap[key] = []
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
        elif line.startswith(ENDPARA_PH):
            if country != "" and lang != "" and marketing != "" and profiling != "":    #End of Paragraph: Let's save it
                print("Saving Country: " + country + " Language: " + lang)
                vars = {
                    "country":country,
                    "lang":lang, 
                    "marketing":marketing,
                    "profiling":profiling,
                    "nam":nam,
                    "sms":sms
                }
                saveItToDict(langFilesMap, vars)
                if lang in langPerCountriesMap:
                    langPerCountriesMap[lang].append(country)
                else:
                    langPerCountriesMap[lang] = [country]
                print("Cleaning varibales...")
                country = ""
                lang = "" 
                marketing = "" 
                profiling = ""
                nam = ""
                sms = ""
            else:
                print("ERROR MISSING VARIABLES: Country: " + country + " Lang: " + lang + " Marketing: " + marketing + " Profiling: " + profiling)
        elif line.startswith(END_PH):   #End of File
            print("File END")
            break

#Fill the remaining countries with default en translation
print("Country Per Languages Map: ")
print(langPerCountriesMap)

for lang in langFilesMap.keys():    #For each file to be created
    print("Completing {lang} object to save it into {lang}.json")
    for count in langFilesMap[lang][BRAND]: #For every country in the file 
        if count not in langPerCountriesMap[lang] and count in langPerCountriesMap['en']: #If we don't have a translation for that country AND there is a translation in english for this country
            enLangCountObj = copy.deepcopy(langFilesMap['en'][BRAND][count]['PRIVACY']) #Copy it's english translation
            langFilesMap[lang][BRAND][count]['PRIVACY'] = enLangCountObj    #Use that 
    path = "C:\\Users\\NikhilChander\\Documents\\OTB\\GIT-DRT_Traduzioni\\DRT_Traduzioni_ExcelToJson\\pythonJSON\\resultJsons\\" + lang + '.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(langFilesMap[lang], f, ensure_ascii=False, indent=4)



srcRead.close()

