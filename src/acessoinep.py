from selenium import webdriver
import time

# search_string = search_string

PATH = "/Users/FernandoZanchitta/Documents/chromedriver"
driver = webdriver.Chrome(PATH)
def acessoinep(escola,cidade):
    qedu_url = pesquisa_google(escola,cidade)
    print("Url da escola QEDU: "+ qedu_url)
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
    return inep, city
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
    print("\n\n\n")
    for link in links:
        print(link)
        if "https://www.qedu.org.br/escola/" in link:
            qedu_url = link
            if "/sobre" in link:
                return qedu_url
        if "http://www.qedu.org.br/escola/" in link:
            qedu_url = link
            if "/sobre" in link:
                return qedu_url
    return qedu_url
# driver.exit(driver)
def ExitDriver():
    driver.close()
