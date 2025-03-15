# WebScraping SofaScore

Este projeto tem como objetivo a extração de dados esportivos utilizando a API do SofaScore. O processo é realizado em 9 scripts, cada um responsável por uma etapa diferente da extração, transformação e armazenamento de dados. A cada etapa, os dados são extraídos, processados e salvos em dois formatos: **JSON** (Camada Bronze) e **CSV** (Camada Silver).

## Aviso Importante sobre a Extração de API

**⚠️ Atenção:** Ao utilizar a extração de dados da API, **use com cuidado**. Não selecione **vários campeonatos e temporadas ao mesmo tempo**, pois isso pode sobrecarregar a API e causar falhas na extração ou atrasos significativos. Para evitar problemas, **limite a quantidade de campeonatos e temporadas selecionadas em uma única execução**.

---

## Sumário

1. [Introdução](#introdução)
2. [Estrutura dos Scripts](#estrutura-dos-scripts)
3. [Execução dos Scripts](#execução-dos-scripts)
4. [Arquivos Gerados](#arquivos-gerados)
5. [Exemplo de Saída](#exemplo-de-saída)

---

## Introdução

O projeto visa coletar dados esportivos de diversos níveis e armazená-los de maneira estruturada para posterior análise. A seguir, estão os 9 scripts que compõem o processo de extração e armazenamento de dados:

1. **p_001_get_sports.py**: Obtém dados sobre os esportes disponíveis na API do SofaScore.
2. **p_002_get_countries.py**: Obtém dados sobre os países disponíveis, com base nos esportes selecionados.
3. **p_003_get_tournaments.py**: Obtém dados sobre os torneios disponíveis para os países selecionados.
4. **p_004_get_seasons.py**: Obtém dados sobre as temporadas dos torneios selecionados.
5. **p_005_get_rounds.py**: Obtém dados sobre as rodadas das temporadas selecionadas.
6. **p_006_get_matches.py**: Obtém dados sobre as partidas de rodadas específicas.
7. **p_007_get_matches_statistics.py**: Obtém dados sobre as estatísticas das partidas.
8. **p_008_get_lineups.py**: Obtém dados sobre as formações dos jogadores nas partidas.
9. **p_009_get_lineups_statistics.py**: Obtém dados sobre as estatísticas dos jogadores nas partidas.

Cada script realiza a consulta à API do SofaScore, transforma os dados em um formato estruturado e os armazena localmente em duas camadas: **Camada Bronze** (JSON) e **Camada Silver** (CSV).

---

## Estrutura dos Scripts

### **1. p_001_get_sports.py**

#### **Objetivo**
Este script consulta a API do SofaScore para obter dados sobre os esportes disponíveis, transforma esses dados em um DataFrame e salva tanto a resposta bruta da API quanto os dados transformados.

#### **Entradas**
- **save_path**: O script solicita o caminho da pasta onde os arquivos serão salvos. O diretório de destino será utilizado para salvar tanto o arquivo JSON quanto o arquivo CSV.

#### **Saídas**
O script salva dois arquivos no diretório especificado:

- **Camada Bronze**: Um arquivo JSON contendo a resposta bruta da API.
- **Camada Gold**: Um arquivo CSV com os dados dos esportes.

---

### **2. p_002_get_countries.py**

#### **Objetivo**
Este script consulta a API do SofaScore para obter dados sobre os países disponíveis, transforma esses dados em um DataFrame e salva tanto a resposta bruta da API quanto os dados transformados.

#### **Entradas**
- **save_path**: O script solicita o caminho da pasta onde os arquivos serão salvos. O diretório de destino será utilizado para salvar tanto o arquivo JSON quanto o arquivo CSV.
- **search_sports**: O script solicita uma lista de Esportes que serão extraídos. Os Esportes disponíveis podem ser consultados na saída do script 1. p_001_get_sports.py na coluna sport.

#### **Saídas**
O script salva dois arquivos no diretório especificado:

- **Camada Bronze**: Um arquivo JSON contendo a resposta bruta da API.
- **Camada Gold**: Um arquivo CSV com os dados dos países.

---

### **3. p_003_get_tournaments.py**

#### **Objetivo**
Este script consulta a API do SofaScore para obter dados sobre os torneios disponíveis, transforma esses dados em um DataFrame e salva tanto a resposta bruta da API quanto os dados transformados.

#### **Entradas**
- **save_path**: O script solicita o caminho da pasta onde os arquivos serão salvos. O diretório de destino será utilizado para salvar tanto o arquivo JSON quanto o arquivo CSV.
- **list_countries**: O script solicita uma lista de IDs dos Países que serão extraídos. Os IDs dos Países disponíveis nos Esportes escolhidos podem ser consultados na saída do script 2. p_002_get_countries.py na coluna sport_country_id.

#### **Saídas**
O script salva dois arquivos no diretório especificado:

- **Camada Bronze**: Um arquivo JSON contendo a resposta bruta da API.
- **Camada Gold**: Um arquivo CSV com os dados dos torneios.

---

### **4. p_004_get_seasons.py**

#### **Objetivo**
Este script consulta a API do SofaScore para obter dados sobre as temporadas disponíveis, transforma esses dados em um DataFrame e salva tanto a resposta bruta da API quanto os dados transformados.

#### **Entradas**
- **save_path**: O script solicita o caminho da pasta onde os arquivos serão salvos. O diretório de destino será utilizado para salvar tanto o arquivo JSON quanto o arquivo CSV.
- **input_path**: O script solicita o caminho do arquivo csv retornado do script 3. p_003_get_tournaments.py contendo a lista de torneios para determinados países.
- **search_interest_tournaments**: O script solicita uma lista de Torneios que serão extraídos (Verifica se o texto da lista está contido em uma linha da tabela). Os torneios disponíveis no país podem ser consultados na saída do script 3. p_003_get_tournaments.py na coluna tournament_season_name.

#### **Saídas**
O script salva dois arquivos no diretório especificado:

- **Camada Bronze**: Um arquivo JSON contendo a resposta bruta da API.
- **Camada Gold**: Um arquivo CSV com os dados das temporadas.

---

### **5. p_005_get_rounds.py**

#### **Objetivo**
Este script consulta a API do SofaScore para obter dados sobre as rodadas disponíveis, transforma esses dados em um DataFrame e salva tanto a resposta bruta da API quanto os dados transformados.

#### **Entradas**
- **save_path**: O script solicita o caminho da pasta onde os arquivos serão salvos. O diretório de destino será utilizado para salvar tanto o arquivo JSON quanto o arquivo CSV.
- **input_path**: O script solicita o caminho do arquivo csv retornado do script 4. p_004_get_seasons.py contendo a lista de temporadas para determinados torneios.
- **search_interest_tournaments**: O script solicita uma lista de Torneios que serão extraídos (Verifica se o texto da lista está contido em uma linha da tabela). Os torneios disponíveis no país podem ser consultados na saída do script 4. p_004_get_seasons.py na coluna tournament_season_name.
- **search_interest_seasons**: O script solicita uma lista de temporadas que serão extraídas. As temporadas disponíveis no país e torneio podem ser consultados na saída do script 4. p_004_get_seasons.py na coluna season_year.

#### **Saídas**
O script salva dois arquivos no diretório especificado:

- **Camada Bronze**: Um arquivo JSON contendo a resposta bruta da API.
- **Camada Gold**: Um arquivo CSV com os dados das rodadas.

---

### **6. p_006_get_matches.py**

#### **Objetivo**
Este script consulta a API do SofaScore para obter dados sobre as partidas disponíveis, transforma esses dados em um DataFrame e salva tanto a resposta bruta da API quanto os dados transformados.

#### **Entradas**
- **save_path**: O script solicita o caminho da pasta onde os arquivos serão salvos. O diretório de destino será utilizado para salvar tanto o arquivo JSON quanto o arquivo CSV.
- **input_path**: O script solicita o caminho do arquivo csv retornado do script 5. p_005_get_rounds.py contendo a lista de rodadas para determinados torneios e temporadas.

#### **Saídas**
O script salva dois arquivos no diretório especificado:

- **Camada Bronze**: Um arquivo JSON contendo a resposta bruta da API.
- **Camada Gold**: Um arquivo CSV com os dados das partidas.

---

### **7. p_007_get_matches_statistics.py**

#### **Objetivo**
Este script consulta a API do SofaScore para obter dados sobre as estatísticas das partidas, transforma esses dados em um DataFrame e salva tanto a resposta bruta da API quanto os dados transformados.

#### **Entradas**
- **save_path**: O script solicita o caminho da pasta onde os arquivos serão salvos. O diretório de destino será utilizado para salvar tanto o arquivo JSON quanto o arquivo CSV.
- **input_path**: O script solicita o caminho do arquivo csv retornado do script 6. p_006_get_matches.py contendo a lista de partidas para determinados rodadas dos torneios e temporadas.

#### **Saídas**
O script salva dois arquivos no diretório especificado:

- **Camada Bronze**: Um arquivo JSON contendo a resposta bruta da API.
- **Camada Gold**: Um arquivo CSV com os dados das estatísticas das partidas.

OBS: Algumas partidas podem dar erro, geralmente quando um jogo é remarcado/cancelado.

---

### **8. p_008_get_lineups.py**

#### **Objetivo**
Este script consulta a API do SofaScore para obter dados sobre jogadores e formações, transforma esses dados em um DataFrame e salva tanto a resposta bruta da API quanto os dados transformados.

#### **Entradas**
- **save_path**: O script solicita o caminho da pasta onde os arquivos serão salvos. O diretório de destino será utilizado para salvar tanto o arquivo JSON quanto o arquivo CSV.
- **input_path**: O script solicita o caminho do arquivo csv retornado do script 6. p_006_get_matches.py contendo a lista de partidas para determinados rodadas dos torneios e temporadas.

#### **Saídas**
O script salva dois arquivos no diretório especificado:

- **Camada Bronze**: Um arquivo JSON contendo a resposta bruta da API.
- **Camada Gold**: Um arquivo CSV com os dados dos jogadores e formações.

OBS: Algumas partidas podem dar erro, geralmente quando um jogo é remarcado/cancelado.

---

### **9. p_009_get_lineups_statistics.py**

#### **Objetivo**
Este script consulta a API do SofaScore para obter dados sobre as estatísticas dos jogadores, transforma esses dados em um DataFrame e salva tanto a resposta bruta da API quanto os dados transformados.

#### **Entradas**
- **save_path**: O script solicita o caminho da pasta onde os arquivos serão salvos. O diretório de destino será utilizado para salvar tanto o arquivo JSON quanto o arquivo CSV.
- **input_path**: O script solicita o caminho do arquivo csv retornado do script 6. p_006_get_matches.py contendo a lista de partidas para determinados rodadas dos torneios e temporadas.

#### **Saídas**
O script salva dois arquivos no diretório especificado:

- **Camada Bronze**: Um arquivo JSON contendo a resposta bruta da API.
- **Camada Gold**: Um arquivo CSV com as estatísticas dos jogadores.

OBS: Algumas partidas podem dar erro, geralmente quando um jogo é remarcado/cancelado.

---

## Execução dos Scripts

Para rodar os scripts, basta executar cada um dos arquivos Python em sequência, fornecendo os parâmetros de entrada necessários. Certifique-se de ter as dependências necessárias instaladas no seu ambiente Python.

## Arquivos Gerados

Cada script gera dois arquivos:
1. **Camada Bronze**: Arquivo **JSON** com a resposta bruta da API.
2. **Camada Gold**: Arquivo **CSV** com os dados estruturados.

### Exemplo de Saída

A saída de cada script será salva no formato `YYYY-MM-DD_HH-MM-SS`, contendo o nome do conteúdo e podendo conter também algum ID de país, torneio e/ou temporada.
Os arquivos serão organizados em duas camadas:

- **Arquivo JSON** (Camada Bronze):  
  `bronze/<script_name> - 2025-03-15_14-30-00.json`
  
- **Arquivo CSV** (Camada Gold):  
  `silver/<script_name> - 2025-03-15_14-30-00.csv`

Por exemplo, após a execução do primeiro script `p_001_get_sports.py`, você verá:

- `bronze/Sports - 2025-03-15_14-30-00.json`
- `silver/Sports - 2025-03-15_14-30-00.csv`

---

## Contribuição

Se você deseja contribuir para o projeto, fique à vontade para enviar pull requests ou sugerir melhorias.
