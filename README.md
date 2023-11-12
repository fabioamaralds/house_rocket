<picture class= "imagem">
    <img src="images/photo-house-sales.jpg" alt="imagem flexível">
</picture>

# Insights House Rocket

O Objetivo desse projeto é indicar melhores imóveis para compra e venda a partir de uma analise de dados.

Passos que serão executados:
* Recebimento da Questão de Negócio
* Definição de Escopo e entendimento do Problema de Negócio
* Coleta de Dados
* Limpeza dos Dados
* Exploração dos dados


# 1. Problema de Negócio
## Contexto do Problema

A **House Rocket** é uma plataforma digital que tem como modelo de negócio, a compra e a venda de imóveis usando tecnologia. O CEO da House Rocket gostaria de maximizar a receita da empresa encontrando boas oportunidades de negócio.

Sua principal estratégia é comprar boas casas em ótimas localizações com preços baixos e depois revendê-las posteriormente à preços mais altos.

Dessa forma, o objetivo desse projeto é indicar quais são os melhores imóveis para compra e venda com seus respectivos valores utilizando Análise Exploratória de Dados.


# 2. Premissas de Negócio
## 2.1. Os dados

A base de dados utilizada na construção desse projeto pode ser encontrada dentro da plataforma [Kaggle](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction).

As colunas da base de dados são:

| Nome da Coluna | Descrição da Coluna                                                                                                                                                                                                                                                                                                                                                |
| :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id             | ID único de cada imóvel na base de dados                                                                                                                                                                                                                                                                                                                           |
| date           | Data da venda do imóvel                                                                                                                                                                                                                                                                                                                                            |
| price          | Preço de venda do imóvel                                                                                                                                                                                                                                                                                                                                           |
| bedrooms       | Número de quartos                                                                                                                                                                                                                                                                                                                                                  |
| bedrooms       | Número de banheiros. Onde 0.5 representa um quarto com vaso sanitário, mas sem chuveiro; 0.75 representa um banheiro que contém uma pia, uma privada, um chuveiro ou uma banheira. Um banheiro completo tradicionalmente possui uma pia, uma privada, um chuveiro e uma banheira, dessa forma, 0.75 representa que o banheiro tem, ou um chuveiro, ou uma banheira |
| sqft_living    | Metragem quadrada (em pés) do espaço interior do imóvel                                                                                                                                                                                                                                                                                                            |
| sqft_lot       | Metragem quadrada (em pés) do espaço terrestre do imóvel                                                                                                                                                                                                                                                                                                           |
| floors         | Número de andares do imóvel                                                                                                                                                                                                                                                                                                                                        |
| waterfront     | Coluna que representa se o imóvel possui vista para o mar/lago ou não. 0 representa sem vista para a água e 1 representa vista para a água                                                                                                                                                                                                                         |
| view           | Índice de 0 a 4 de quão boa é a vista do imóvel. 0 é a pior vista e 4 é a melhor vista                                                                                                                                                                                                                                                                             |
| condition      | Índice de 1 a 5 sobre a condição (usado) do imóvel. 1 é a pior condição e 5 é a melhor                                                                                                                                                                                                                                                                             |
| grade          | Índice de 1 a 13 sobre a condição da construção e design do imóvel. 1 é a pior nota e 13 é a melhor nota                                                                                                                                                                                                                                                           |
| sqft_above     | Metragem quadrada (em pés) do espaço interno do imóvel que está acima do nível do solo                                                                                                                                                                                                                                                                             |
| sqft_basement  | Metragem quadrada (em pés) do espaço interno do imóvel que está abaixo do nível do solo (porão)                                                                                                                                                                                                                                                                    |
| yr_built       | Ano em que o imóvel foi construído                                                                                                                                                                                                                                                                                                                                 |
| yr_renovated   | Ano da última reforma do imóvel                                                                                                                                                                                                                                                                                                                                    |
| zipcode        | Código postal do imóvel                                                                                                                                                                                                                                                                                                                                            |
| lat            | Ponto de latitude do imóvel                                                                                                                                                                                                                                                                                                                                        |
| long           | Ponto de longitude do imóvel                                                                                                                                                                                                                                                                                                                                       |
| sqft_living15  | Metragem quadrada (em pés) do espaço habitacional interior para os 15 vizinhos mais próximos                                                                                                                                                                                                                                                                       |
| sqft_lot15     | A metragem quadrada (em pés) dos terrenos (lotes vazios) dos 15 vizinhos mais próximos                                                                                                                                                                                                                                                                             |
## 2.2. Premissas
* ID duplicados serão removidos da base de dados.
* Imóveis que não possuem quartos ou banheiros foram removidos da base de dados
* Para definição da compra dos imóveis foram utilizadas duas condições:
    * O imóvel deve estar em boa condição de compra. O indicador é representado pela coluna condição, sendo consideradas as condições boas como 3 a 5.
    * O valor de compra do imóvel deve ser menor do que o valor mediano da região (Código Postal)
* Para definição da venda dos imóveis selecionados anteriormente foram utilizadas duas condições:
    * Caso o imóvel tenha sido adquirido por um preço de menor que a mediana da localidade, o preço de venda sugerido será 30% em cima do valor de compra.
    * Caso o imóvel tenha sido adquirido por um preço de maior que a mediana da localidade, o preço de venda sugerido será 10% em cima do valor de compra.

## 2.3. Estratégia de Resolução
01. **Entender o problema de Negócio:** O objetivo desta etapa é compreender corretamente o que é pedido, ajustar as expectativas e demonstrar exemplos de como serão os resultados.
02. **Descrição dos Dados:** O objetivo é utilizar ferramentas estatísticas de localização e dispersão para possuir um entendimento melhor dos dados.
03. **Filtragem dos Dados:** O objetivo desta etapa é remover as linhas que possam conter dados incorretos ou dados que possam prejudicar a análise de alguma forma.
04. **Análise Exploratória dos Dados:** O objetivo desta etapa é realizar uma exploração dos dados validando hipóteses de negócio, para melhor entender o comportamento das variáveis na base de dados.

## 2.4. Ferramentas e Métodos Utilizados
- Python 3.8.13
- Jupyter Notebook
- Git
- Streamlit

# 3. Resultado de Negócio
## 3.1. Pergunta de Negócio
### 3.1.1. Quais são os imóveis que a House Rocket deveria comprar e por qual preço ?
Foi realizado o agrupamento dos imóveis por código postal e calculado o valor mediano do preço de venda de cada código postal. A partir disso, foram selecionados os imóveis que possuiam o valor de venda menor que o valor mediano e que estavam em boa condições, gerando assim uma lista com **10495** imóveis elegíveis para compra.

Caso a sugestão de valores de venda seja acatada, o lucro previsto com a venda dos imóveis será de **$ 851.326.331,60**

### 3.1.3. Exibição das Análises
Foi criado uma aplicação web utilizando o framework web Streamlit para facilitar o consumo das análises feitas pelo CEO.

Link para acesso à aplicação: [Análises](https://house-rocket.streamlit.app/)

# 4. Lições Aprendidas
Foi constatado que poderíamos verificar e selecionar oportunidades de negócio para o CEO da empresa House Rocket somente utilizando técnicas de manipulação de dados e ferramentas estatísticas, podendo entregar resultados sem a necessidade de utilizar técnicas e ferramentas mais complexas.

# 5. Próximos Passos
* Realizar mais análises a fim de melhorar o entendimento dos dados da base de dados.
* Utilizar algoritmos de Machine Learning para melhorar a precificação dos imóvies, conseguindo assim melhorar os lucros previstos.
* Melhorar a estrutura da aplicação Web, utilizando seções para a exibição das análises.
* Adicionar testes automatizados para deixar o código mais robusto.

# 6. Desenvolvedor

[<img src="https://avatars.githubusercontent.com/u/110738694" width=115><br><sub>Fábio Ladislau do Amaral</sub>](https://github.com/fabioamaralds/fabioamaralds)
