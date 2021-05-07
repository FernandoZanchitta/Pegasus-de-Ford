from selenium import webdriver
import pandas as pd
from scrapping import pesquisagooglesitetelefone
from scrapping import acessoqedu
from scrapping import exitdriver

PATH = "../chromedriver"

input = input("Nome do Arquivo:\n")

driver = webdriver.Chrome(PATH)

data = pd.read_csv('/Users/FernandoZanchitta/PycharmProjects/Pegasus de ford/%s.csv' % input)
data.columns = [col.replace(' ', '_').lower() for col in data.columns]

if "dominio_(url_do_site_da_escola)" in data.columns:
    data.rename(columns={'dominio_(url_do_site_da_escola)': 'dominio'}, inplace=True)
if "telefone" not in data.columns:
    data.insert(2, "telefone", "-")
if "dominio" not in data.columns:
    data.insert(2, "dominio", False)
if "name" in data.columns:
    data.rename(columns={'name': 'deal_name'}, inplace=True)

for i in range(data['deal_name'].count()):
    if not pd.isna(data.loc[i,'cidade']):
        if data.loc[i, 'dominio'] == False or pd.isna(data.loc[i, 'dominio']):
            data.loc[i, 'dominio'], data.loc[i, 'telefone'] = pesquisagooglesitetelefone(driver, data.loc[i, 'deal_name'], data.loc[i, 'cidade'])

csvoutput = data.to_csv('/Users/FernandoZanchitta/PycharmProjects/Pegasus de ford/output/%s_site.csv' % input)
data.insert(1, "inep", False)
data.insert(5, "link_qedu", False)
for i in range(data['deal_name'].count()):
    if not pd.isna(data.loc[i,'cidade']):
        if data.loc[i, "inep"] == False:
            data.loc[i, 'inep'], data.loc[i, 'cidade_encontrada'], data.loc[i, 'link_qedu'] = acessoqedu(driver, data.loc[i, 'deal_name'], data.loc[i, 'cidade'])

if "deal_id" in data.columns:
    data.rename(columns={'deal_id': 'Deal ID'}, inplace=True)

if "company_id" in data.columns:
    data.rename(columns={'company_id': 'Company ID'}, inplace=True)

csvoutput = data.to_csv('/Users/FernandoZanchitta/PycharmProjects/Pegasus de ford/output/%s_Tel_site_qedu.csv' % input)
exitdriver(driver)
