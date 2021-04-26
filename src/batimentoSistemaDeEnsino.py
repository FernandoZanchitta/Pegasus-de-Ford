from selenium import webdriver
import pandas as pd
import re

def checarSistemaEnsino(url):
    if url != "":
        print("Acessando o link:" + url)
        try:
            driver.get(url = url)
        except:
            out = "Pagedown"
            return out
        src = driver.page_source
        textfoundPoli = re.search(r'poliedro|Poliedro|Ensino Poliedro|Sistema Poliedro|SISTEMA POLIEDRO|Portal Edros', src)
        textfoundBili = re.search(r'Ensino Bilíngue|bilíngue|Bilingue|BILINGUE|Internacional|Ensino de inglês', src)
        textfoundBernou = re.search(r'Bernoulli|bernoulli|BERNOULLI', src)
        textfoundAri = re.search(r'Ari de Sá|ari de Sá|Ari de Sa|Plataforma SAS|Ensino SAS', src)
        textfoundAnglo = re.search(r'Sistema Anglo|Ensino ANGLO|', src)
        textfoundEtapa = re.search(r'Ensino Etapa|Colégio Etapa|Sistema Etapa|Etapa Sistema', src)
        textfoundCOC = re.search(r'Sistema COC|Ensino COC|Colegio COC|COC ensino|Colégio COC', src)
        textfoundGoogle = re.search(r'Google For Education|Google pela Educação', src)
        textfoundUnesco = re.search(r'Comunidade Unesco|Unesco', src)
        sistemaEnsino = ''
        if (textfoundPoli != None):
            sistemaEnsino = 'Poliedro'
        if (textfoundBili != None):
            sistemaEnsino = sistemaEnsino + ';' + 'Bilíngue' if sistemaEnsino != '' else 'Bilíngue'
        if (textfoundBernou != None):
            sistemaEnsino = sistemaEnsino + ';' + 'Bernoulli' if sistemaEnsino != '' else 'Bernoulli'
        if (textfoundAri != None):
            sistemaEnsino = sistemaEnsino + ';' + 'Ari de Sá' if sistemaEnsino != '' else 'Ari de Sá'
        if (textfoundAnglo != None):
            sistemaEnsino = sistemaEnsino + ';' + 'Anglo' if sistemaEnsino != '' else 'Anglo'
        if (textfoundEtapa != None):
            sistemaEnsino = sistemaEnsino + ';' + 'Etapa' if sistemaEnsino != '' else 'Etapa'
        if (textfoundCOC != None):
            sistemaEnsino = sistemaEnsino + ';' + 'COC' if sistemaEnsino != '' else 'COC'
        if (textfoundGoogle != None):
            sistemaEnsino = sistemaEnsino + ';' + 'Google for Education' if sistemaEnsino != '' else 'Google for Education'
        if (textfoundUnesco != None):
            sistemaEnsino = sistemaEnsino + ';' + 'Unesco' if sistemaEnsino != '' else 'Unesco'
        print("Sistema de Ensino: " + sistemaEnsino)
        return sistemaEnsino
    else:
        return ""
PATH = "/Users/FernandoZanchitta/Documents/chromedriver"
driver = webdriver.Chrome(PATH)
driver.delete_all_cookies()
data = pd.read_csv('/Users/FernandoZanchitta/PycharmProjects/Pegasus de ford/testepoli.csv')
data.columns = [col.replace(' ', '_').lower() for col in data.columns]
data.insert(13,"sistema_de_ensino_encontrado","Sem site")
for i in range(data['dominio_(url_do_site_da_escola)'].count()):
    if "https://" not in data.loc[i,'dominio_(url_do_site_da_escola)'] and "http://" not in data.loc[i,'dominio_(url_do_site_da_escola)']:
        data.loc[i, 'dominio_(url_do_site_da_escola)'] = "http://" +data.loc[i, 'dominio_(url_do_site_da_escola)']
    data.loc[i,"sistema_de_ensino_encontrado"] = checarSistemaEnsino(data.loc[i,'dominio_(url_do_site_da_escola)'])

csvoutput = data.to_csv('/Users/FernandoZanchitta/PycharmProjects/Pegasus de ford/output/Resultadopoliedro.csv')
driver.close()
