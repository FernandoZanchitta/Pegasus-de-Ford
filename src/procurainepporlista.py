from selenium import webdriver
import time
import pandas as pd


def pesquisa_google(escola,cidade):
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

    return domain_url,telefone
def pesquisa_google_qedu(escola,cidade):
    try:
        escola = escola.replace(' ', '+')
        cidade = cidade.replace(' ', '+')
    except:
        telefone = ""
        domain_url = ""
        return domain_url, telefone
    query = escola + "+" + cidade
    search_url = "https://www.google.com/search?q=" + query + "+qedu"
    driver.get(url=search_url)
    time.sleep(0.5)
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
def acessoinep(escola,cidade):
    qedu_url = pesquisa_google_qedu(escola,cidade)
    if qedu_url != "":
        try:
            driver.get(url= qedu_url)
        except:
            inep = ""
            city = cidade
            qedu_url = "INVALIDO"
            return inep, city, qedu_url
        time.sleep(0.5)
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
PATH = "/Users/FernandoZanchitta/Documents/chromedriver"
driver = webdriver.Chrome(PATH)
input = input("Nome do Arquivo:\n")
data = pd.read_csv('/Users/FernandoZanchitta/PycharmProjects/Pegasus de ford/%s.csv'%(input))
data.columns = [col.replace(' ', '_').lower() for col in data.columns]
if "telefone" not in data.columns:
    data.insert(2,"telefone","-")
if "company_domain_name" not in data.columns:
    data.insert(2, "company_domain_name", False)
for i in range(data['name'].count()):
    if data.loc[i,'company_domain_name'] == False or pd.isna(data.loc[i,'company_domain_name']):
        data.loc[i,'company_domain_name'], data.loc[i,'telefone']  = pesquisa_google(data.loc[i,'name'],data.loc[i,'city'])

csvoutput = data.to_csv('/Users/FernandoZanchitta/PycharmProjects/Pegasus de ford/output/%s_site.csv'%(input))
data.insert(1,"inep",False)
data.insert(5,"link_qedu",False)
for i in range(data['name'].count()):
        if data.loc[i, "inep"] == False:
            data.loc[i, 'inep'] ,data.loc[i,'cidade_encontrada'], data.loc[i, 'link_qedu'] = acessoinep(data.loc[i,'name'],data.loc[i,'city'])
csvoutput = data.to_csv('/Users/FernandoZanchitta/PycharmProjects/Pegasus de ford/output/%s_Tel_site_qedu.csv'%(input))
driver.delete_all_cookies()



driver.close()