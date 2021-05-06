=======
# Pegasus-de-Ford
O projeto tem por viés ajudar na obtenção de Listas de Escola para Ataque comercial do Time de Marketing de Vendas.
São Extraidos somente dados Públicos e Abertos, sem qualquer quebra da legislação. O objetivo principal é encontrar novas

##Detalhamento do Código:
O ambiente é dividido em duas operações:
- Procura de Listas do 0, usando MAPs API, procurando código inep pelo site do Qedu e Entrando nos Sites procurando Sistema de Ensino.
### Procura por Listas do 0
Utilizamos o Google Maps API para encontrar resultados de pesquisa a partir de um texto.
Esse pode ser iniciado rodando o main.py e escrevendo o Input query.

Ex:"Escolas particulares de Vila Madalena SP"

Com isso, é gerado uma pesquisa por nextpagetoken, ampliando o resultado da pesquisa para até 60 resultados.

Um Json é criado de forma a armazenar somente as informações relevantes (Nome, telefone, website, endereço), e chama as funções
de Webscrapping para encontrar o Resultado do Código Inep e Sistema de Ensino.
- Codigo inep:
    - Faz a pesquisa no google com o nome + cidade + qedu, procurando os resultados com o domínio qedu e entrando;
    - Procura nas classes do Html o Código Inep e a Cidade (para Batimento)
- Sistema de Ensino:
    - Entra no Website encontrado no Maps API e procura no Page source as palavras chave referentes aos principais Sistemas de Ensino;

Depois disso, pega o Json Gerado e armazena num csv

###Procura o Código Inep, telefone e site dada uma lista.
