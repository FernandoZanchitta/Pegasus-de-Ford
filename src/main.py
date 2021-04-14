from selenium import webdriver
import re
def checarPalavra(url):
    driver.get(url = url)
    src = driver.page_source
    text_found = re.search(r'poliedro|Poliedro|POLIEDRO|Sistema Poliedro|SISTEMA POLIEDRO', src)
    sistemaEnsino = ''
    if(text_found != None):
        sistemaEnsino = 'Poliedro'
    text_found = re.search(r'Bilíngue|bilíngue|Bilingue|BILINGUE', src)
    if (text_found != None):
        sistemaEnsino = sistemaEnsino+';'+'Bilíngue' if sistemaEnsino != '' else 'Bilíngue'
    text_found = re.search(r'Objetivo|objetivo|OBJETIVO', src)
    if (text_found != None):
        sistemaEnsino = sistemaEnsino + ';' + 'Objetivo' if sistemaEnsino != '' else 'Objetivo'
    print(sistemaEnsino)
    return sistemaEnsino

PATH = "/Users/FernandoZanchitta/Documents/chromedriver"
driver = webdriver.Chrome(PATH)
driver.delete_all_cookies()
url = 'http://colegioieprol.com.br/'
checarPalavra(url)
driver.close()