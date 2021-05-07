=======
# Pegasus-de-Ford
O projeto tem por viés ajudar na obtenção de Listas de Escola para Ataque comercial do Time de Marketing de Vendas.
São Extraidos somente dados Públicos e Abertos, sem qualquer quebra da legislação. O objetivo principal é encontrar novas

##Detalhamento do Código:
O ambiente é dividido em três operações semelhantes:
- Procura de Listas do 0, usando MAPs API, procurando código inep pelo site do Qedu
  e Entrando nos Sites procurando Sistema de Ensino.
- Procura Telefone, site e Código Inep, dada uma lista de escolas e cidades
- Procura Sistema de Ensino, dada uma lista de escolas, cidades e Links
### Procura por Listas do 0
Utilizamos o Google Maps API para encontrar resultados de pesquisa a partir de um texto.
Esse pode ser iniciado rodando o main.py e escrevendo o Input query.

Ex: "Escolas particulares de Vila Madalena SP"

Com isso, é gerado uma pesquisa por nextpagetoken, ampliando o resultado da pesquisa para até 60 resultados.

Um Json é criado de forma a armazenar somente as informações relevantes (Nome, telefone, website, endereço), e chama as funções
de Webscrapping para encontrar o Resultado do Código Inep e Sistema de Ensino.
- Codigo inep:
    - Faz a pesquisa no google com o nome + cidade + qedu, procurando os resultados com o domínio qedu e entrando;
    - Procura nas classes do Html o Código Inep e a Cidade (para Batimento)
- Sistema de Ensino:
    - Entra no Website encontrado no Maps API e procura no Page source as palavras chave referentes aos principais Sistemas de Ensino;

Depois disso, pega o Json Gerado e armazena num csv na pasta output

### Procura o Código Inep, telefone e site dada uma lista - procurainepporlista.

Habilita a entrada de listas prontas. Procura no google "Nome + cidade" e pega o primeiro link relacionado
além de procurar o Telefone automático relacionado ao estabelecimento.

Gera um output em csv com os valores, para fins de backup.

Apos isso, realiza a pesquisa no google "Nome + cidade + qedu" procurando os sites do domínio qedu, de forma a entrar neles e procurar o código
Inep e a cidade( para efeitos de conferência) oriundos do código fonte da página. Gera-se o csv dos resultados encontrados

### Verifica o sistema de ensino das escolas - batimentoSistemadDeEnsino
Dada uma lista de escolas com um link atrelado, procure por palavras chave em cada link de forma que indique o seu sistema
de ensino, se possui sistema de ensino 
## Instalação do Software:
Para ter o Pegasus pronto em seu pc devemos seguir os seguintes passos:

instalar o python3 no seu computador:
Para verificar se já consta, digite "python3" no seu terminal ou powershell. Caso não esteja instalado siga esses tutoriais:
https://phoenixnap.com/kb/how-to-install-python-3-windows

Instale o chrome driver e certifique-se de que ele esteja na mesma pasta do projeto. Caso queira alterar a pasta em que o
chromedriver se encontra, é preciso alterar a variável PATH dos códigos: main.py, procurainepporlista.py batimentoSistemaDeEnsino.py

tutorial, instale a versão mais nova completa (nao a versão beta):
https://chromedriver.chromium.org/downloads

Instale os requisitos para rodar:
```
python3 install requirements.txt 
```

Caso a linha acima dê errado:
```
pip3 install selenium 
pip3 install pandas
```

Para rodar o código, faça:
```
python3 main.py
python3 procurainepporlista.py
python3 batimentoSistemadDeEnsino.py
```

