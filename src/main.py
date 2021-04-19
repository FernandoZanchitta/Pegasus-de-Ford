from selenium import webdriver
import re
def checarPalavra(url):
    driver.get(url = url)
    src = driver.page_source
    text_found1= re.search(r'poliedro|Poliedro|POLIEDRO|Sistema Poliedro|SISTEMA POLIEDRO', src)
    text_found2 = re.search(r'Bilíngue|bilíngue|Bilingue|BILINGUE', src)
    text_found3 = re.search(r'Bernoulli|bernoulli|BERNOULLI|', src)
    sistemaEnsino = ''
    if(text_found1 != None):
        sistemaEnsino = 'Poliedro'
    if (text_found2 != None):
        sistemaEnsino = sistemaEnsino+';'+'Bilíngue' if sistemaEnsino != '' else 'Bilíngue'
    if (text_found3 != None):
        sistemaEnsino = sistemaEnsino + ';' + 'Bernoulli' if sistemaEnsino != '' else 'Bernoulli'
    print("Sistema de Ensino: "+ sistemaEnsino)
    return sistemaEnsino

PATH = "/Users/FernandoZanchitta/Documents/chromedriver"
driver = webdriver.Chrome(PATH)
driver.delete_all_cookies()
url = 'http://colegioieprol.com.br/'
checarPalavra(url)
driver.close()