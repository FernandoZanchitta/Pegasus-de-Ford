from selenium import webdriver
from scrapping import exitdriver
import pandas
from mapsprototype import *
#Modelo de Pesquisa:
#'Escolas na Copacabana, Rio de janeiro'

query = input('Selecione uma Pesquisa de Query\n')

#Chave de Api - do Francisco Castro
api_key = 'AIzaSyCm6GpcJ806Z46MggMMKHSoCfTzEW4z7K0'

y, next_page = pesquisaportexto(query,api_key)
print("Query Pesquisada:" + query + '\n')

#Expansão de pesquisa ( de 20 para 60 escolas por pesquisa);
while next_page!= "":
    aux,next_page = pesquisanextpage(next_page,api_key)
    y = y + aux

print("Total de escolas encontradas: "+ str(len(y)))



# Inicializando o Webdriver para começar o Scrapping

PATH = "/Users/FernandoZanchitta/Documents/chromedriver"
driver = webdriver.Chrome(PATH)
driver.delete_all_cookies()

# data =  Escolas para adicionar, json de output
data = {}
for i in range((len(y))):
    data[str(i)] = {}
    data[str(i)] = inserirnovaescola(driver,data[str(i)], y[i],api_key)

#Formatação dos dados para Exportação.
json_data = json.dumps(data).encode('utf8')
pdObj = pandas.read_json(json_data, orient='index', encoding='utf8')
csvData = pdObj.to_csv('/Users/FernandoZanchitta/PycharmProjects/Pegasus de ford/output/%s.csv'%query ,index=False)
exitdriver(driver)