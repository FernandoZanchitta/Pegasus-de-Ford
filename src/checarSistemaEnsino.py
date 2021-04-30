import re

def checarSistemaEnsino(url):
    if url != "":
        print("Acessando o link:" + url)
        try:
            driver.get(url = url)
            src = driver.page_source
        except:
            out = "Pagedown"
            return out

        textfoundPoli = re.search(r'poliedro|Poliedro|Ensino Poliedro|Sistema Poliedro|SISTEMA POLIEDRO|Portal Edros|Poliedro Sistema|p4ed', src)
        textfoundBili = re.search(r'Ensino Bilíngue|bilíngue|Bilingue|BILINGUE|Internacional|Ensino de inglês', src)
        textfoundBernou = re.search(r'Bernoulli|bernoulli|BERNOULLI', src)
        textfoundAri = re.search(r'Ari de Sá|ari de Sá|Ari de Sa|Plataforma SAS|Ensino SAS|portalsas.com.br|"SAS"', src)
        textfoundAnglo = re.search(r'Sistema Anglo|anglo|Ensino ANGLO|Ecossistema Anglo|Anglo sistema', src)
        textfoundEtapa = re.search(r'Ensino Etapa|Colégio Etapa|Sistema Etapa|Etapa Sistema', src)
        textfoundCOC = re.search(r'coc-| coc|Plataforma coc|Sistema COC|COC Sistema|Ensino COC|Colegio COC|COC ensino|Colégio COC|SISTEMA COC|coc.com.br|Portal COC|Portal Coc', src)
        textfoundGoogle = re.search(r'Google For Education|Google pela Educação|Google for Education', src)
        textfoundUnesco = re.search(r'Comunidade Unesco|Unesco|UNESCO', src)
        textfoundMack = re.search(r'mackenzie|Mackenzie', src)
        textfoundgeekie = re.search(r'geekie|Geekie', src)
        textfoundPositivo = re.search(r'Sistema Positivo|Positivo Ensino|Editora Positivo|Positivo English Solution|editorapositivo', src)
        textfoundSales = re.search(r'Salesiano|salesiano', src)
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
        print("Sistema de Ensino: " + sistemaEnsino)
        return sistemaEnsino
    else:
        return ""