from selenium import webdriver
import time


PATH = "/Users/FernandoZanchitta/Documents/chromedriver"
driver = webdriver.Chrome(PATH)
qedu_url = "https://www.qedu.org.br/escola/36163-upaon-educacional-ltda/censo-escolar"
driver.get(url=qedu_url)

inep = driver.find_elements_by_xpath('//*[@class="table table-striped"]/tbody/tr/td')[0].text
city = driver.find_elements_by_xpath('//*[@class="subnav-title"]/ul/li [3]')[0].text
#CodigoInep = incategory.find_element_by_tag_name("tbody").find_element_by_tag_name("tr").find_element_by_tag_name("td")

print(inep + ' , ' + city)
time.sleep(2)
driver.close()
# driver.exit(driver)
# TODO:Comparar o nome da escola procurada
#TODO: Comparar o nome da cidade