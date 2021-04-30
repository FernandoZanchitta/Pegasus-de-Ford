import pandas
from selenium import webdriver
import time
from checarSistemaEnsino import *

PATH = "/Users/FernandoZanchitta/Documents/chromedriver"
driver = webdriver.Chrome(PATH)
input = "Geduq-Pagina3_Tel_site_qedu"
driver.delete_all_cookies()
data = pandas.read_csv('/Users/FernandoZanchitta/PycharmProjects/Pegasus de ford/output/%s.csv'%(input))
data.columns = [col.replace(' ', '_').lower() for col in data.columns]
data.loc[27,'company_domain_name'] = ""
data.insert(3,"sistema_de_ensino_encontrado","Sem site")
for i in range(data['company_domain_name'].count()):
    if "https://" not in data.loc[i,'company_domain_name'] and "http://" not in data.loc[i,'company_domain_name']:
        data.loc[i, 'company_domain_name'] = "http://" +data.loc[i, 'company_domain_name']
    data.loc[i,"sistema_de_ensino_encontrado"] = checarSistemaEnsino(driver,data.loc[i,'company_domain_name'])
    time.sleep(0.5)
csvoutput = data.to_csv('/Users/FernandoZanchitta/PycharmProjects/Pegasus de ford/output/%s_SisEns.csv'%(input))
driver.close()
