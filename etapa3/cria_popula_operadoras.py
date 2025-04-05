import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = r'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\Relatorio_cadop.csv'

# Conectar ao banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),     
        password=os.getenv('DB_PASSWORD'),     
        database=os.getenv('DB_NAME', 'estagio_intuitivecare')
    )

def criar_tabela_operadoras():
    db = conectar_banco()
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
    
    try:
        cursor.execute(create_table_sql)
        db.commit()
        print("Tabela 'operadoras' criada com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabela operadoras: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close()

def criar_indices():
    db = conectar_banco()
    cursor = db.cursor()
    
    try:
        # Índice composto para trimestre e descrição
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_despesas_trimestre_descricao 
        ON despesas(trimestre, descricao(50))
        """)
        
        # Índice para reg_ans (chave estrangeira)
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_despesas_reg_ans 
        ON despesas(reg_ans)
        """)
        
        db.commit()
        print("Índices criados/verificados com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro MySQL ao criar índices: {err}")
        db.rollback()
    except Exception as e:
        print(f"Erro geral ao criar índices: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close()

# Ler o arquivo CSV com pandas
df = pd.read_csv(CSV_PATH, delimiter=';', quotechar='"', encoding='utf-8')
def popular_tabela_operadoras():
    db = conectar_banco()
    cursor = db.cursor()
    
    try:
        # Ler o arquivo CSV com pandas
        df = pd.read_csv(CSV_PATH, delimiter=';', quotechar='"', encoding='utf-8')
        
        total_linhas = len(df)
        print(f"Iniciando importação de {total_linhas} registros...")
        
        for i, row in enumerate(df.iterrows(), 1):
            _, data = row
            cursor.execute("""
                INSERT INTO operadoras (
                    registro_ans, cnpj, razao_social, nome_fantasia, modalidade,
                    logradouro, numero, complemento, bairro, cidade, uf, cep,
                    ddd, telefone, fax, endereco_eletronico, representante,
                    cargo_representante, regiao_comercializacao, data_registro_ans
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, tuple(data))
            
            if i % 1000 == 0:
                db.commit()
                print(f"Registros processados: {i}/{total_linhas}")
        
        db.commit()
        print(f"Concluída! {total_linhas} registros inseridos.")
        
    except Exception as e:
        print(f"Erro ao popular: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close()

def main():
    # Configuração inicial do banco
    criar_tabela_operadoras()
    criar_indices()
    popular_tabela_operadoras()

if __name__ == "__main__":
    main()