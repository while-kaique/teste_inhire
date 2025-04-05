# 📊 Projeto de Análise de Dados de Operadoras de Saúde
Esse é o projeto final do Teste de Nivelamento da vaga de estágio da IntuitiveCare, cujo objetivo é criar/povoar tabelas MySQL por dados preparados/baixados, criar queries otimizadas para consulta de informações gerais (uso de íncides para otimização) e apresentação de dados via requisição de API em Python através de aplicação em Vue.

# Apresentação do projeto:
## Página Principal
![image](https://github.com/user-attachments/assets/501ea575-f736-4dee-8fc2-557e4397060f)


## Pesquisa Geral
![image](https://github.com/user-attachments/assets/90a3a17b-d2c8-4dc8-a083-3daabacdc81d)
![image](https://github.com/user-attachments/assets/15ebd026-84ba-4db1-b716-a0dd5a15b536)


## Pesquisa sem resultados
![image](https://github.com/user-attachments/assets/ed2b86a2-425f-43c8-add0-87c041733e14)



## 🏗️ Estrutura do Projeto

├── 📂 etapa1/            # Download e compactação de arquivos  
├── 📂 etapa2/            # Conversão para CSV  
├── 📂 etapa3/            # Criação do banco de dados e consultas SQL  
└── 📂 etapa4/            # API (Flask) + Frontend (Vue.js)  

## 🚀 Etapas do Projeto
### 1️⃣ Etapa 1: Download dos Dados
Objetivo: Automatizar o download e compactação de arquivos de dados públicos.

Script: baixar_arquivos.py

Funcionalidades: 
- Baixa 2 arquivos do site https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-dasociedade/atualizacao-do-rol-de-procedimentos.

- Compacta os arquivos em .zip dentro da pasta etapa1.

### 2️⃣ Etapa 2: Conversão para CSV
Objetivo: Transformar um arquivo baixado em formato tabular (.csv).

Script: converte_para_csv.py

Saída: Gera tabela_extraida.csv na pasta etapa2.

### 3️⃣ Etapa 3: Banco de Dados e Consultas
Objetivo: Criar e popular tabelas no banco de dados MySQL local.

Scripts:
- cria_popula_operadoras.py: Cria a tabela Operadoras e insere dados do CSV.
- cria_popula_despesas.py: Cria a tabela Despesas com dados trimestrais.

consulta_sql.py: Responde às perguntas:
- Top 10 operadoras com maiores despesas em "EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MÉDICO-HOSPITALAR" no último trimestre
- Quais as 10 operadoras com maiores despesas nessa categoria no último ano?

 ////////////////////////////
 ////////////////////////////
 ////////////////////////////
 ////////////////////////////
 #
 ////////////////////////////
 ////////////////////////////
 ////////////////////////////
 ////////////////////////////
 
# 4️⃣ Etapa 4: API e Frontend
Objetivo: Criar uma interface para consulta dinâmica dos dados.

 
## Backend (Flask)
API: app.py
Rota: GET /api/operadoras?q=<termo>

Funcionalidade: busca operadoras por nome fantasia ou razão social (case-insensitive).

Retorna resultados paginados.

## Frontend (Vue.js)
Componente principal: SearchOperadoras.vue
- Campo de pesquisa em tempo real.
- Exibe resultados dinâmicos da API.

# 🛠️ Tecnologias Utilizadas
## Backend:	
- Python (Flask)
- MySQL
  
## Frontend	
- Vue.js
- fetch
- Design Moderno

## Tecnologias Secundárias
- Processamento	Pandas (ETL), SQL
- Ferramentas	Postman (testes de API), Git

#
# 📥 Instalação e Execução
Pré-requisitos
- Python 3.8+
- Javascript
- MySQL
- Node.js (para o frontend)

# Passo a Passo
## AVISO: Caso queira executar o código por completo, remova os arquivos pré-baixados que já estão no repositório para não have conflito na hora de fazer download.
## AVISO 2: Caso queira executar especificamente os scripts da etapa3, adicione os arquivos necessários no caminho: C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\seu_arquivo, ou ocorrerá um erro

## 1- Clone o repositório:
- git clone https://github.com/seu-usuario/projeto_operadoras.git  
## 2- Configure e consulte o banco de dados:
Execute os scripts SQL em "/etapa3" NA EXATA SEQUÊNCIA:
- 1- cria_popula_operadoras.py,
- 2- cria_popula_despesas.py,
- 3- consulta_sql.py.
## 3- Inicie a API Flask:
 - cd etapa4/backend
 - python app.py
## 4- Inicie o Frontend em Vue:
- cd etapa4/frontend  
- npm install  
- npm run dev  

#
# 🔍 Como Testar
## Via Postman:
- Importe a coleção "API_Operadoras.postman_collection.json" que está dentro da pasta "/docs".
- Teste a rota: GET http://localhost:5000/api/operadoras?q=saúde
  
## Via Frontend:
- Acesse http://localhost:5173 (ou o que o Vue utilizar na sua máquina) e digite no campo de busca.

# 📌 Destaques do Projeto
✅ Extração automatizada de dados públicos.

✅ Processamento eficiente com Pandas.

✅ Consultas SQL otimizadas para análise estratégica.

✅ Interface amigável com busca em tempo real.

# ✉️ Contato
Desenvolvedor: [Kaique Breno / KaiCode]

Email: whilekaique@alu.ufc.br

<p align="center"> *"Decida o tipo de pessoa que quer ser. Prove isso para si mesmo com pequenas vitórias."* </p>
<p align="center"> "- Hábitos Atômicos, de James Clear!" </p>

<p align="center"> <img src="https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D" /> </p>
