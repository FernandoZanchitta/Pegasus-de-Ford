import pandas
from selenium import webdriver
import time
from scrapping import checarsistemaensino

PATH = "/Users/FernandoZanchitta/Documents/chromedriver"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(10)
input = "Pegasus - Negócios - Sem site - 04_05_Tel_site_qedu"
driver.delete_all_cookies()
data = pandas.read_csv('/Users/FernandoZanchitta/PycharmProjects/Pegasus de ford/output/%s.csv'%(input))
data.columns = [col.replace(' ', '_').lower() for col in data.columns]

if "dominio_(url_do_site_da_escola)" in data.columns:
    data.rename(columns={'dominio_(url_do_site_da_escola)': 'dominio'}, inplace=True)

if "sistema_de_ensino_encontrado" in data.columns:
    data.rename(columns={'sistema_de_ensino_encontrado': 'sistema_de_ensino'}, inplace=True)

if "sistema_de_ensino" not in data.columns:
    data.insert(2, "sistema_de_ensino", "-")

if "Escola é Blíngue?" not in data.columns:
    data.insert(3, "Escola é Blíngue?","-")

if "Comunidade que a escola pertence" not in data.columns:
    data.insert(3, "Comunidade que a escola pertence"," ")

for i in range(data['dominio'].count()):
    if "https://" not in data.loc[i,'dominio'] and "http://" not in data.loc[i,'dominio']:
        data.loc[i, 'dominio'] = "http://" +data.loc[i, 'dominio']
    data.loc[i,"sistema_de_ensino"],data.loc[i,"Escola é Blíngue?"], data.loc[i,"Comunidade que a escola pertence"] = checarsistemaensino(driver,data.loc[i,'dominio'])
    time.sleep(0.5)
csvoutput = data.to_csv('/Users/FernandoZanchitta/PycharmProjects/Pegasus de ford/output/%s_SisEns.csv'%(input))
driver.close()
