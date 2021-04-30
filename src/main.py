from selenium import webdriver
from scrapping import ExitDriver
import pandas
from mapsprototype import *

#query = 'Escolas na Copacabana, Rio de janeiro'
query = input('Selecione uma Pesquisa de Query\n')

PATH = "/Users/FernandoZanchitta/Documents/chromedriver"
driver = webdriver.Chrome(PATH)
driver.delete_all_cookies()
api_key = 'AIzaSyCm6GpcJ806Z46MggMMKHSoCfTzEW4z7K0'

y, next_page = pesquisaportexto(query,api_key)
print("Query Pesquisada:" + query + '\n')

while next_page!= "":
    aux,next_page = pesquisanextpage(next_page,api_key)
    y = y + aux

data = {}
print("Total de escolas encontradas: "+ str(len(y)))
for i in range((len(y))):
    data[str(i)] = {}
    data[str(i)] = inserirnovaescola(data[str(i)], y[i],api_key)

json_data = json.dumps(data).encode('utf8')
#print(json_data)
pdObj = pandas.read_json(json_data, orient='index', encoding='utf8')
#print(pdObj)
csvData = pdObj.to_csv('output/%s.csvoutput/%s.csv'%query ,index=False)
ExitDriver()