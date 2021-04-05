from selenium import webdriver
import time

search_string = input("Input da pesquisa: ")
search_string = search_string.replace(' ', '+')
PATH = "/Users/FernandoZanchitta/Documents/chromedriver"
driver = webdriver.Chrome(PATH)
for i in range(1):
    matched_elements = browser.get("https://www.google.com/search?q=" +
                                     search_string + "&start=" + str(i))

driver.get(url="https://www.qedu.org.br/escola/279164-morumbi-escola-unidade-moema/sobre")

incategory = driver.find_elements_by_xpath('//*[@class="table table-striped"]/tbody/tr/td')[0].text

#CodigoInep = incategory.find_element_by_tag_name("tbody").find_element_by_tag_name("tr").find_element_by_tag_name("td")

print(incategory)
time.sleep(5)
driver.close()
driver.exit(driver)
