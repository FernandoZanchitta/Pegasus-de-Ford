import pandas
from selenium import webdriver
import time
from scrapping import checarsistemaensino

PATH = "/Users/FernandoZanchitta/Documents/chromedriver"
driver = webdriver.Chrome(PATH)
input = "negocioshub"
driver.delete_all_cookies()
data = pandas.read_csv('/Users/FernandoZanchitta/PycharmProjects/Pegasus de ford/%s.csv'%(input))
data.columns = [col.replace(' ', '_').lower() for col in data.columns]
data.insert(3,"sistema_de_ensino_encontrado","Sem site")
for i in range(data['dominio_(url_do_site_da_escola)'].count()):
    if "https://" not in data.loc[i,'dominio_(url_do_site_da_escola)'] and "http://" not in data.loc[i,'dominio_(url_do_site_da_escola)']:
        data.loc[i, 'dominio_(url_do_site_da_escola)'] = "http://" +data.loc[i, 'dominio_(url_do_site_da_escola)']
    data.loc[i,"sistema_de_ensino_encontrado"] = checarsistemaensino(driver,data.loc[i,'dominio_(url_do_site_da_escola)'])
    time.sleep(0.5)
csvoutput = data.to_csv('/Users/FernandoZanchitta/PycharmProjects/Pegasus de ford/output/%s_SisEns.csv'%(input))
driver.close()
