# sheets2json.py


import os
import os.path as ospath
import sys
import csv
import json
try:
    import requests
except:
    print("'requests' module required\n")
    os.system('pause')
    sys.exit()


DEFAULT_TXT = """To get a google sheet's url, in the document go to File > \
Share > Publish to web. Be sure to select a specific sheet if there are multiple, \
Google will only output the first one if you choose Entire Document.\n
Add the urls to sheets.json as "name":"url" (don't forget to add commas \
for any item before the last). Set the output path for your generated json files \
under "output_path" (it's "output\\" by default - don't forget to escape backslashes).\n
In the sheets themselves, the first row is used as headers, so label them appropriately."""

DEFAULT_JSON = r"""{
    "output_path":"output\\",
    "sheets":{
        "example name":"example.url"
    }
}"""


#==============================================================
# a class for transfering a google sheet to a json file
#==============================================================

class JsonHolder():
    def __init__(
            self, 
            json_path #-- (str) path to json file
            ):
        self.sheets_json = self.load_file(json_path)
    
    def load_file(self, json_path): #== returns a json file as a dict
        if not ospath.exists(json_path):
            self.make_new_file(json_path)
        with open(json_path, 'r', encoding='utf-8-sig') as file:
            try:
                sheets_json = json.load(file)
                return sheets_json
            except:
                print('##############################################################################')
                print('Problem loading sheets.json.')
                print('Try fixing its syntax or just deleting it and let a default one get generated.')
                print('##############################################################################')

    def make_new_file(self, json_path): #== creates a default json file
        with open('README.txt', 'w', encoding='utf-8') as file:
            file.write(DEFAULT_TXT)
        with open(json_path, 'w', encoding='utf-8-sig') as file:
            file.write(DEFAULT_JSON)
    
    def get_output_path(self): #== returns self.sheets_json
        return self.sheets_json['output_path']
    
    def get_sheets(self): #== returns self.sheets_json
        sheets = {
                key:value for key, value 
                in self.sheets_json['sheets'].items() 
                if value != 'example.url'
                }
        return sheets


#==============================================================
# a class for converting google sheets from csv to json 
#==============================================================

class Sheet():
    def __init__(
            self, 
            name, #-- (str) name for saving json file
            output_path, #-- (str) path to save json file to
            csv_url #-- (str) url of google sheets csv document
            ):
        self.name = name
        self.output_path = output_path
        self.csv_url = csv_url
    
    def load_csv(self): #== loads csv from url and returns a dict
        csv_file = requests.get(self.csv_url)
        csv_path = self.output_path + self.name + '.csv'
        with open(csv_path, 'w', newline='', encoding='ISO-8859-1') as file:
            file.write(csv_file.text)
        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            dicts = list(csv.DictReader(file))
        csv_dict = {key:[] for key in dicts[0]}
        for dict in dicts:
            for (key, value) in dict.items():
                if value != '': csv_dict[key].append(value)
        os.remove(csv_path)
        return csv_dict
    
    def get_json(self): #== returns a string of json syntax created from a dict
        dict = self.load_csv()
        json_str = json.dumps(dict, ensure_ascii=False)
        return json_str
    
    def save_json(self): #== saves json file of sheet
        json_path = self.output_path + self.name + '.json'
        json_str = self.get_json()
        with open(json_path, 'w', encoding='utf-8-sig') as file:
            file.write(json_str)


#==============================================================
# a class for handling the sheet conversion process 
#==============================================================

class SheetsHandler():
    def __init__(self):
        sheets_json = JsonHolder('sheets.json')
        self.output_path = sheets_json.get_output_path()
        self.sheets = sheets_json.get_sheets()
    
    def save_sheets(self): #== saves all sheets in sheets.json as json files
        if self.sheets == {}: return
        if not ospath.exists(self.output_path): os.makedirs(self.output_path)
        for name, url in self.sheets.items():
            file = Sheet(name, self.output_path, url)
            file.save_json()


if __name__ == '__main__':
    handler = SheetsHandler()
    handler.save_sheets()
