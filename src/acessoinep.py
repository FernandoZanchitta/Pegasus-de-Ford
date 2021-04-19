from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import re
import time

# search_string = search_string

def acessoinep(escola,cidade):
    qedu_url = pesquisa_google(escola,cidade)
    #print("Url da escola QEDU: "+ qedu_url)
    if qedu_url != "":
        driver.get(url= qedu_url)
        time.sleep(1)
        try:
            inep = driver.find_elements_by_xpath('//*[@class="table table-striped"]/tbody/tr/td')[0].text
        except IndexError:
            inep = ""
        try:
            city = driver.find_elements_by_xpath('//*[@class="subnav-title"]/ul/li [3]')[0].text
        except IndexError:
            city = cidade
        #CodigoInep = incategory.find_element_by_tag_name("tbody").find_element_by_tag_name("tr").find_element_by_tag_name("td")
    else:
        inep = ""
        city = cidade
    return inep, city, qedu_url
def pesquisa_google(escola,cidade):
    escola = escola.replace(' ', '+')
    cidade = cidade.replace(' ', '+')
    query = escola + "+" + cidade
    search_url = "https://www.google.com/search?q=" + query + "+qedu"
    driver.get(url=search_url)
    time.sleep(1)
    elems = driver.find_elements_by_css_selector(".yuRUbf [href]")
    links = [elem.get_attribute('href') for elem in elems]
    qedu_url = ""
    for link in links:
        print(link)
        if "http://qedu.org.br/escola/" in link:
            qedu_url = link
            if "/sobre" in link:
                return qedu_url
            if "/censo-escolar" in link:
                return qedu_url
        if "http://www.qedu.org.br/escola/" in link:
            qedu_url = link
            if "/sobre" in link:
                return qedu_url
            if "/censo-escolar" in link:
                return qedu_url
        if "https://www.qedu.org.br/escola/" in link:
            qedu_url = link
            if "/sobre" in link:
                return qedu_url
            if "/censo-escolar" in link:
                return qedu_url
        if "https://qedu.org.br/escola/" in link:
            qedu_url = link
            if "/sobre" in link:
                return qedu_url
            if "/censo-escolar" in link:
                return qedu_url

    return qedu_url
# driver.exit(driver)
def checarSistemaEnsino(url):
    if url != "":
        driver.get(url=url)
        print("Acessando o link:"+ url)
        src = driver.page_source
        textfoundPoli = re.search(r'poliedro|Poliedro|POLIEDRO|Sistema Poliedro|SISTEMA POLIEDRO', src)
        textfoundBili = re.search(r'Bilíngue|bilíngue|Bilingue|BILINGUE', src)
        textfoundBernou = re.search(r'Bernoulli|bernoulli|BERNOULLI', src)
        textfoundAri = re.search(r'Ari de Sá|Ari|ari de Sá|Ari de Sa|Plataforma SAS', src)
        textfoundAnglo = re.search(r'Sistema Anglo|anglo|ANGLO|Anglo', src)
        textfoundEtapa = re.search(r'Etapa|Sistema Etapa|Etapa Sistema', src)
        textfoundCOC = re.search(r'Sistema COC|Ensino COC|Colegio COC', src)
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
        print("Sistema de Ensino: " + sistemaEnsino)
        return sistemaEnsino
    else:
        return ""
def ExitDriver():
    driver.close()
def delete_cache():
    driver.execute_script("window.open('');")
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)
    driver.get('chrome://settings/clearBrowserData') # for old chromedriver versions use cleardriverData
    time.sleep(1)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 3 + Keys.DOWN * 3) # send right combination
    actions.perform()
    time.sleep(1)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 4 + Keys.ENTER) # confirm
    actions.perform()
    time.sleep(3) # wait some time to finish
    driver.close() # close this tab
    driver.switch_to.window(driver.window_handles[0]) # switch back


PATH = "/Users/FernandoZanchitta/Documents/chromedriver"
driver = webdriver.Chrome(PATH)
driver.delete_all_cookies()
#delete_cache()
