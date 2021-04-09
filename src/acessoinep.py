from selenium import webdriver
import time

# search_string = search_string


def acessoinep(escola,cidade):
    qedu_url = pesquisa_google(escola,cidade)
    driver.get(url=qedu_url)

    inep = driver.find_elements_by_xpath('//*[@class="table table-striped"]/tbody/tr/td')[0].text
    city = driver.find_elements_by_xpath('//*[@class="subnav-title"]/ul/li [3]')[0].text
    #CodigoInep = incategory.find_element_by_tag_name("tbody").find_element_by_tag_name("tr").find_element_by_tag_name("td")

    print(inep + ' , ' + city)
    time.sleep(2)
    driver.close()
def pesquisa_google(escola,cidade):
    escola = escola.replace(' ', '+')
    cidade = cidade.replace(' ', '+')
    query = escola + "+" + cidade
    search_url = "https://www.google.com/search?q=" + query + "+qedu"
    driver.get(url=search_url)
    elems = driver.find_elements_by_css_selector(".yuRUbf [href]")
    links = [elem.get_attribute('href') for elem in elems]
    aux = 0
    while links[aux].find('http://www.qedu.org.br/escola/') == -1:
        aux += 1
    time.sleep(2)
    return(links[aux])
# driver.exit(driver)

escola = input("Nome da Escola:\n")
cidade = input("Cidade da escola\n")
PATH = "/Users/FernandoZanchitta/Documents/chromedriver"
driver = webdriver.Chrome(PATH)
acessoinep(escola,cidade)