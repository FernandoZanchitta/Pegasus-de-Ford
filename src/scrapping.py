from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import re
import time


# funçoes de Webscrapping

# chama uma pesquisaGoogleQedu -> Procura o Link de dominio qedu e
# realiza o Scrapping do Código Inep e Batimento de Cidade.
def acessoqedu(driver, escola, cidade):
    qedu_url = pesquisagoogleqedu(driver, escola, cidade)
    if qedu_url != "":
        driver.get(url=qedu_url)
        time.sleep(1)
        try:
            inep = driver.find_elements_by_xpath('//*[@class="table table-striped"]/tbody/tr/td')[0].text
        except IndexError:
            inep = ""
        try:
            city = driver.find_elements_by_xpath('//*[@class="subnav-title"]/ul/li [3]')[0].text
        except IndexError:
            city = cidade
    else:
        inep = ""
        city = cidade
    return inep, city, qedu_url


# chama uma Pesquisa do Google: "Nome da Escola + Cidade + 'qedu' "
def pesquisagoogleqedu(driver, escola, cidade):
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


# chama uma Pesquisa do Google: "Nome da Escola + Cidade e Pega o primeiro Link e o Telefone
def pesquisagooglesitetelefone(driver, escola, cidade):
    try:
        escola = escola.replace(' ', '+')
        cidade = cidade.replace(' ', '+')
    except:
        telefone = ""
        domain_url = ""
        return domain_url, telefone
    query = escola + "+" + cidade
    search_url = "https://www.google.com/search?q=" + query
    driver.get(url=search_url)
    time.sleep(1)
    elems = driver.find_elements_by_css_selector(".yuRUbf [href]")
    try:
        telefone = driver.find_elements_by_xpath('//*[@class="LrzXr zdqRlf kno-fv"]/a/span')[0].text
    except IndexError:
        telefone = '-'
    links = [elem.get_attribute('href') for elem in elems]
    domain_url = links[0]

    return domain_url, telefone


# Entra no url, e procura as palavras chave representando
# os sistemas de ensino no Código Fonte da página
def checarsistemaensino(driver, url):
    if url != "":
        print("Acessando o link:" + url)
        try:
            driver.get(url=url)
            src = driver.page_source
        except:
            out = "Pagedown"
            return out

        textfoundPoli = re.search(
            r'poliedro|Poliedro|Ensino Poliedro|Sistema Poliedro|SISTEMA POLIEDRO|Portal Edros|Poliedro Sistema|p4ed',
            src)
        textfoundBili = re.search(r'Ensino Bilíngue|bilíngue|Bilingue|BILINGUE|Internacional|Ensino de inglês', src)
        textfoundBernou = re.search(r'Bernoulli|bernoulli|BERNOULLI', src)
        textfoundAri = re.search(r'Ari de Sá|ari de Sá|Ari de Sa|Plataforma SAS|Ensino SAS|portalsas.com.br|"SAS"', src)
        textfoundAnglo = re.search(r'Sistema Anglo|anglo|Ensino ANGLO|Ecossistema Anglo|Anglo sistema', src)
        textfoundEtapa = re.search(r'Ensino Etapa|Colégio Etapa|Sistema Etapa|Etapa Sistema', src)
        textfoundCOC = re.search(
            r'coc-| coc|Plataforma coc|Sistema COC|COC Sistema|Ensino COC|Colegio COC|COC ensino|Colégio COC|SISTEMA COC|coc.com.br|Portal COC|Portal Coc|coc.png',
            src)
        textfoundGoogle = re.search(
            r'Google For Education|Google pela Educação|Google for Education|Google.png|Google.jgp|Google.jpeg', src)
        textfoundUnesco = re.search(r'Comunidade Unesco|Unesco|UNESCO|unesco.png', src)
        textfoundMack = re.search(r'mackenzie|Mackenzie', src)
        textfoundgeekie = re.search(r'geekie|Geekie', src)
        textfoundPositivo = re.search(
            r'Sistema Positivo|Positivo Ensino|Editora Positivo|Positivo English Solution|editorapositivo', src)
        textfoundSales = re.search(r'Salesiano|salesiano', src)
        textfoundMaple = re.search(r'MapleBear|Maple Bear', src)
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
        if (textfoundMack != None):
            sistemaEnsino = sistemaEnsino + ';' + 'Mackenzie' if sistemaEnsino != '' else 'Mackenzie'
        if (textfoundgeekie != None):
            sistemaEnsino = sistemaEnsino + ';' + 'Geekie' if sistemaEnsino != '' else 'Geekie'
        if (textfoundPositivo != None):
            sistemaEnsino = sistemaEnsino + ';' + 'Positivo' if sistemaEnsino != '' else 'Positivo'
        if (textfoundSales != None):
            sistemaEnsino = sistemaEnsino + ';' + 'Salesiano' if sistemaEnsino != '' else 'Salesiano'
        if (textfoundMaple != None):
            sistemaEnsino = sistemaEnsino + ';' + 'Maple Bear' if sistemaEnsino != '' else 'Maple Bear'
        print("Sistema de Ensino: " + sistemaEnsino)
        return sistemaEnsino
    else:
        return ""


# fecha o driver
def exitdriver(driver):
    driver.delete_all_cookies()
    driver.quit()


# nao uso em nada atualmente, deleta o cache da página.
def delete_cache(driver):
    driver.execute_script("window.open('');")
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)
    driver.get('chrome://settings/clearBrowserData')  # for old chromedriver versions use cleardriverData
    time.sleep(1)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 3 + Keys.DOWN * 3)  # send right combination
    actions.perform()
    time.sleep(1)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 4 + Keys.ENTER)  # confirm
    actions.perform()
    time.sleep(3)  # wait some time to finish
    driver.close()  # close this tab
    driver.switch_to.window(driver.window_handles[0])  # switch back

# delete_cache()
