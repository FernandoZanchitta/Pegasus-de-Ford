# coding: utf-8
import requests, json
import pandas as pd


def pesquisaDetalhada(school_json):
    api_key = 'AIzaSyCm6GpcJ806Z46MggMMKHSoCfTzEW4z7K0'
    # realizamos uma pesquisa detalhada para cada elemento encontrado na pesquisa por texto
    print("Entramos numa pesquisa detalhada.")
    url_details = ''' 
https://maps.googleapis.com/maps/api/place/details/json?
placeid=%s&
key=%s
''' % (school_json['place_id'], api_key)
    url_details = url_details.replace('\n', '')
    r_details = requests.get(url_details)
    x = r_details.json()
    z = x['result']
    return z


def inserirNovaEscola(data, school_json):
    # chamamos a pesquisa detalhada e inserimos as informações que precisamos da escola lá dentro
    z = pesquisaDetalhada(school_json)
    data['place_id'] = school_json['place_id'] if 'place_id' in school_json else ''
    data['name'] = school_json['name'] if 'name' in y[i] else ''
    data['formatted_address'] = school_json['formatted_address'] if 'formatted_address' in school_json else ''
    data['website'] = z['website'] if 'website' in z else ''
    data['formatted_phone_number'] = z['formatted_phone_number'] if 'formatted_phone_number' in z else ''
    return data


def checarEscolaExiste(data,school_json):
    for i in range(len(data)):
        if data[i]['place_id'] == school_json['place_id']:
            return 1
    return 0

def pesquisaPorTexto(query):
    api_key = 'AIzaSyCm6GpcJ806Z46MggMMKHSoCfTzEW4z7K0'
    query = query.replace(' ', '+')
    url = '''
https://maps.googleapis.com/maps/api/place/textsearch/json?
key=%s&
query=%s
''' % (api_key, query)
    url = url.replace('\n', '')
    print("Acessando o endereço: " + url)

    r = requests.get(url)
    x = r.json()
    y = x["results"]
    print("Query Pesquisada:" + query + '\n')
    print("Escolas encontradas: " + str(len(y))+'\n')
    return y



Entrada = input('Selecione uma Pesquisa de Query\n')
palavras_chave_pesquisa = ['Escolas de ','Escolas particulares de ', 'Colegios de ','Colegios particulares de ','Melhores escolas de ']
y = {}
for i in range(len(palavras_chave_pesquisa)):
    query = palavras_chave_pesquisa[i] + Entrada
    aux = pesquisaPorTexto(query)
    if y == {}:
        y = aux
    for j in range(len(aux)):
        if checarEscolaExiste(y,aux[i]) == 0:
            print("Escola nova adicionada\n")
            y[len(y)] = aux[i]

data = {}
for i in range((len(y))):
    data[str(i)] = {}
    data[str(i)] = inserirNovaEscola(data[str(i)], y[i])

json_data = json.dumps(data).encode('utf8')
# print(json_data)
pdObj = pd.read_json(json_data, orient='index', encoding='utf8')
# print(pdObj)
csvData = pdObj.to_csv('%s.csv' % Entrada, index=False)
