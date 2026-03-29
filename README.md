# Projeto Integrado 6

Este repositório contém um projeto de análise de dados em Python com foco em um conjunto de dados de jogos.

## Descrição

O projeto realiza a leitura e o tratamento de dados de jogos, explorando padrões, estatísticas e visualizações para interpretar informações relevantes da base.

## Análise de dados

O notebook realiza uma análise exploratória de um conjunto de dados com 16.715 registros e 11 colunas, incluindo:

- `Name`, `Platform`, `Year_of_Release`, `Genre`
- vendas por região: `NA_sales`, `EU_sales`, `JP_sales`, `Other_sales`
- `Critic_Score`, `User_Score` e `Rating`

A análise foca em:

- limpeza e tratamento de valores faltantes em `Year_of_Release`, `Genre`, `Critic_Score`, `User_Score` e `Rating`
- conversão de notas de usuário para valores numéricos
- resumo estatístico das vendas e pontuações
- identificação de plataformas e gêneros mais frequentes

## Gráficos e visualizações

O notebook inclui gráficos para explorar padrões e tendências, como:

- distribuição de vendas por região
- top 10 gêneros e plataformas mais populares
- evolução de vendas por ano
- comparação de vendas entre regiões
- avaliação média de críticos e usuários por gênero
- mapas de calor ou gráficos de dispersão para entender correlações entre nota e vendas

## Conclusões principais

Algumas conclusões esperadas a partir da análise são:

- a maior parte das vendas está concentrada na América do Norte e Europa
- plataformas como PS2, DS, PS3, Wii e X360 aparecem frequentemente nos registros
- os gêneros mais comuns no conjunto de dados incluem Action, Sports, Misc, Role-Playing e Shooter
- Role-Playing e Strategy tendem a apresentar notas de críticos mais altas, enquanto Sports e Shooter aparecem com grande volume de vendas
- há presença relevante de valores faltantes em campos de notas e classificações, o que exige cuidados no pré-processamento
