import json
import copy
import os

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

    -update: 26/02/2021
        All files lang.json must have all countries available per brand. And if the there isn't any translation for that country in that lang, english translation must be used. 
        Code logic:
            Every time a new country is been saved (basically, every time there's a <ENDP>), that country is added to a map which register's the language as KEY and a list of countries that have the translation in that lang. (e.g. 
            {
                'en' = ['at', 'de', 'fr',...], 
                'de' = ['at', 'de', ...], 
                ...
            })
            Before saving dumping every lang obj into the json file, iterate over every lang in python lang dict by the following logic:
            for every lang in pythonLangDict
                for every country in that lang obj (iterating over the new map created early)
                    if the country is not present in map created early (that means, it has not got a translation in this language) AND if it has a translation in engilish
                        fill all the countries that have not the transaltion for this language with the translation in english
            ... (the rest is same, just to save the file)

    -update: 01/03/2021
        New countries, such as Bulgaria and Croazie (BG and HR), are only present in en.json. 
        This is because, when the loop before comes to see if the

    -TODO:  08/03/2021
        Create a check on if a block ends without <ENDP>
"""
#CONSTANTS 
BRAND = "1_60"
COUNTRY_PH = "<CONT>"   #PH = Place holder
LANGUAGE_PH = "<LANG>"
PARA_PH = "<PARA>"
END_PH = "<ENDF>"
ENDPARA_PH = "<ENDP>"
MarketingJSON_PH = "FLAG_MARKETING_OPTIN_TEXT"
ProfilingJSON_PH = "FLAG_PROFILING_OPTIN_TEXT"
NamJSON_PH = "GENERAL_CONSENT_NAM"
smsJSON_PH = "FLAG_TEXT_MESSAGE"
ComunicationJSON_PH = "COMMUNICATION_DATA"

MarketingLinkValue = "FOR DETAILS ABOUT MARKETING PURPOSES CLICK HERE"
ProfilingLinkValue = "FOR DETAILS ABOUT PROFILING PURPOSES CLICK HERE"
PrivacyLinkValue = "FOR FULL TEXT OF INFORMATION NOTICE CLICK HERE"

def saveItToDict(langFilesMap, vars):
    if vars["lang"] in langFilesMap:    #JSON for this vars["lang"] already exists (Langugage)
        langObj = langFilesMap[vars["lang"]]
        if vars["country"] in langObj[BRAND]:   #JSON has also this country! #SAVE: update the json with new variables (Country)
            langObj[BRAND][vars["country"]]["PRIVACY"][MarketingJSON_PH] = vars["marketing"]
            langObj[BRAND][vars["country"]]["PRIVACY"][ProfilingJSON_PH] = vars["profiling"]
            langObj[BRAND][vars["country"]]["PRIVACY"][ComunicationJSON_PH] = vars["comunication"]
        else:   #New vars["country"] for the json (New Country)
            print("Creating new country: " + vars["country"] + " for " + vars["lang"] + ".json")
            basicObj = {
                "HEADER": "AUTHORIZATION FOR DATA PROCESSING",
                "HEADER_SUB_1": "I confirm I’m over 16 years old and I have read the Privacy Policy provided by the Data Controllers in accordance with local applicable laws, and I",
                "GENERAL_CONSENT_NAM": "",
                "HEADER_SUB_2": "",
                MarketingJSON_PH: vars["marketing"],
                ProfilingJSON_PH: vars["profiling"],
                "HEADER_SUB_3": "",
                "FOOTER_SUB_1": "I understand that providing the personal data for profiling and marketing purposes is optional.",
                "FLAG_TEXT_MESSAGE": "",
                ComunicationJSON_PH: vars["comunication"],
                "PRIVACY_MARKETING_LINK": MarketingLinkValue,
                "PRIVACY_PROFILING_LINK": ProfilingLinkValue,
                "PRIVACY_TERMCOND_LINK": PrivacyLinkValue,
                "PRIVACY_LINK": "I confirm that I have read privacy policy.",
                "PRIVACY_LINK_DCB": "I confirm that I have read privacy policy.",
                "AGREE": ""
            }
            privacyObj = {
                "PRIVACY":basicObj
            }
            langObj[BRAND][vars["country"]] = privacyObj    #SAVE: updates the lang json by creating a new country obj
    else:   #New JSON for the language (New Language)
        print("Creating new file " + vars["lang"] + ".json")
        newLangObj = copy.deepcopy(langFilesMap["en"])  #a deepcopy of the en object as it's the default language
        if vars["country"] in newLangObj[BRAND]:   #JSON has also this vars["country"]
            newLangObj[BRAND][vars["country"]]["PRIVACY"][MarketingJSON_PH] = vars["marketing"]
            newLangObj[BRAND][vars["country"]]["PRIVACY"][ProfilingJSON_PH] = vars["profiling"]
            newLangObj[BRAND][vars["country"]]["PRIVACY"][ComunicationJSON_PH] = vars["comunication"]
        else:   #New vars["country"] for the json
            basicObj = {
                "HEADER": "AUTHORIZATION FOR DATA PROCESSING",
                "HEADER_SUB_1": "I confirm I’m over 16 years old and I have read the Privacy Policy provided by the Data Controllers in accordance with local applicable laws, and I",
                "GENERAL_CONSENT_NAM": "",
                "HEADER_SUB_2": "",
                MarketingJSON_PH: vars["marketing"],
                ProfilingJSON_PH: vars["profiling"],
                "HEADER_SUB_3": "",
                "FOOTER_SUB_1": "I understand that providing the personal data for profiling and marketing purposes is optional.",
                "FLAG_TEXT_MESSAGE": "",
                ComunicationJSON_PH: vars["comunication"],
                "PRIVACY_MARKETING_LINK": MarketingLinkValue,
                "PRIVACY_PROFILING_LINK": ProfilingLinkValue,
                "PRIVACY_TERMCOND_LINK": PrivacyLinkValue,
                "PRIVACY_LINK": "I confirm that I have read privacy policy.",
                "PRIVACY_LINK_DCB": "I confirm that I have read privacy policy.",
                "AGREE": ""
            }
            privacyObj = {
                "PRIVACY":basicObj
            }
            newLangObj[BRAND][vars["country"]] = privacyObj
        langFilesMap[vars["lang"]] = newLangObj

#Map(Brand, Map(country, Map(language, Map(privacy))))
langFilesMap = {"da":{}, "de":{}, "el":{}, "en":{}, "en_GB":{}, "es":{}, "fi":{}, "fr":{}, "it":{}, "ja":{}, "ko":{}, "nl":{}, "no":{}, "pt":{}, "sv":{}, "zh":{}, "zh_HK":{}}
print("Retrieving jsons from files...")
os.chdir(r'C:\Users\Chander\Documents\DRT Traduzioni\DRT_Traduzioni_ExcelToJson\pythonJSON')
for defJson in langFilesMap.keys():
    #path = "C:\\Users\\NikhilChander\\Documents\\OTB\\GIT-DRT_Traduzioni\\DRT_Traduzioni_ExcelToJson\\pythonJSON\\jsons\\" + defJson + ".json"
    path = 'jsons\\' + defJson + '.json'
    print("Processing: " + path)
    fRead = open(path, encoding="utf-8")
    data = json.load(fRead)
    langFilesMap[defJson] = data
    fRead.close()
print("JSON files stored successfuly!")
sourceFile = 'fixD2.html'
srcRead = open(sourceFile, 'r', encoding="utf-8")
lang = ""
country = ""
marketing = ""
profiling = ""
comunication = ""
foot_marketing = ""
foot_profiling = ""

comunication = ""
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
            elif foot_marketing == "": #Marketing Footer
                foot_marketing = line[6:]
            elif profiling == "":   #Profiling
                profiling = line[6:]
            elif foot_profiling == "": #Profiling Footer
                foot_profiling = line[6:]
            elif comunication == "": #Comunication Data
                comunication = line[6:]
            else:   #ERROR
                marketing = "ERROR_PARA: Not enough PARA for the VARIABLES " + line
                profiling = marketing
                foot_profiling = marketing
                foot_profiling = marketing
                comunication = marketing
        elif line.startswith(ENDPARA_PH):
            if country != "" and lang != "" and marketing != "" and profiling != "" and foot_profiling != "" and foot_marketing != "" and comunication != "":    #End of Paragraph: Let's save it
                print("Saving Country: " + country + " Language: " + lang)
                vars = {
                    "country":country,
                    "lang":lang, 
                    "marketing":marketing,
                    "profiling":profiling,
                    "comunication": comunication
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
                comunication = ""
                foot_profiling = ""
                foot_marketing = ""
            else:
                print("ERROR MISSING VARIABLES: Country: " + country + " Lang: " + lang + " Marketing: " + marketing + " Profiling: " + profiling + " Comunication: " + comunication + " Footer Marketing: " + foot_marketing + " Footer Profiling: " + foot_profiling)
        elif line.startswith(END_PH):   #End of File
            print("File END")
            break

#Fill the remaining countries with default en translation
print("Country Per Languages Map: ")
print(langPerCountriesMap)

for lang in langFilesMap.keys():    #For each file to be created
    print("Completing " + lang + " object to save it into " + lang + ".json")
    for count in langPerCountriesMap['en']: #For every country that has translation in english
        if count not in langPerCountriesMap[lang]:  #To not ovveride the original translations, only if it doesn't have a translation for that country in that langauge
            enLangCountObj = copy.deepcopy(langFilesMap['en'][BRAND][count]['PRIVACY']) #Copy it's english translation
            basicObj = enLangCountObj    #If the country hasn't got an object in that lang, it will create one  
            privacyObj = {"PRIVACY" : basicObj}
            langFilesMap[lang][BRAND][count] = privacyObj
    if lang != 'en_GB':
        langFilesMap[lang][BRAND]['GB']['PRIVACY'] = langFilesMap['en_GB'][BRAND]['GB']['PRIVACY']
    path = "resultJsons\\D2_" + lang + '.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(langFilesMap[lang], f, ensure_ascii=False, indent=4)
srcRead.close()

