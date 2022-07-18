import csv 
import json 
import collections
orderedDict = collections.OrderedDict()
from collections import OrderedDict

def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
    x = OrderedDict([('index', { "_index" : "mir" })])      
    jsonString = json.dumps(x)  
    with open(csvFilePath, encoding='utf-8') as csvf: 
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            csvReader = csv.DictReader(csvf) 
            for row in csvReader: 
                jsonf.write(jsonString)
                jsonf.write("\n")
                row.pop('')
                row.pop('cleaned_tweets')
                row.pop('lemmatized_tweets')
                row.pop('Text_words_joined')
                y = json.dumps(row)
                jsonf.write(y)
                jsonf.write("\n")
          
csvFilePath = r'../data_final.csv'
jsonFilePath = r'es_data.json'
csv_to_json(csvFilePath, jsonFilePath)

