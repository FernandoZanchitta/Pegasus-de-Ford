from selenium import webdriver
import time





def pesquisa_google(escola,cidade):
    escola = escola.replace(' ', '+')
    cidade = cidade.replace(' ', '+')
    PATH = "/Users/FernandoZanchitta/Documents/chromedriver"
    driver = webdriver.Chrome(PATH)
    qedu_url = "https://www.qedu.org.br/escola/36163-upaon-educacional-ltda/censo-escolar"

    query = escola + "+" + cidade
    search_url = "https://www.google.com/search?q=" + query + "+qedu"
    driver.get(url=search_url)
    elems = driver.find_elements_by_css_selector(".yuRUbf [href]")
    links = [elem.get_attribute('href') for elem in elems]
    aux = 0;
    while links[aux].find('http://www.qedu.org.br/escola/') == -1:
        aux += 1

    print(links[aux])

    time.sleep(2)
    driver.close()

escola = input('digite nome da escola:\n');
cidade = input('digite nome da cidade:\n');

pesquisa_google(escola,cidade)