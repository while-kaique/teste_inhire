import pandas as pd
import mysql.connector

# Conectar ao banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kaiquemedeiros08",
    database="estagio_intuitivecare"
)

cursor = db.cursor()

create_table_sql = """
CREATE TABLE IF NOT EXISTS operadoras (
    registro_ans VARCHAR(20) PRIMARY KEY, 
    cnpj VARCHAR(18) NOT NULL UNIQUE,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    cep VARCHAR(10),
    ddd CHAR(5),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    regiao_comercializacao VARCHAR(255),
    data_registro_ans DATE
);
"""

cursor.execute(create_table_sql)

# Ler o arquivo CSV com pandas
df = pd.read_csv(r'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\Relatorio_cadop.csv', delimiter=';', quotechar='"')

# Inserir os dados na tabela
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO operadoras (registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, representante, cargo_representante, regiao_comercializacao, data_registro_ans)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

db.commit()
cursor.close()
db.close()
