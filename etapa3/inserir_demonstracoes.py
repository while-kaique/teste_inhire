
import pandas as pd
import mysql.connector

CSV_FILES = {
    r'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\2023\1T2023.csv': '1T2023',
    r'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\2023\2T2023.csv': '2T2023',
    r'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\2023\3T2023.csv': '3T2023',
    r'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\2023\4T2023.csv': '4T2023',
    r'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\2024\1T2024.csv': '1T2024',
    r'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\2024\2T2024.csv': '2T2024',
    r'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\2024\3T2024.csv': '3T2024',
    r'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\2024\4T2024.csv': '4T2024',
}

# Conectar ao banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="kaiquemedeiros08",
        database="estagio_intuitivecare"
    )

def criar_tabela_despesas():
    db = conectar_banco()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS despesas (
                data DATE NOT NULL,
                reg_ans VARCHAR(20) NOT NULL,
                cd_conta_contabil VARCHAR(20) NOT NULL,
                descricao VARCHAR(255) NOT NULL,
                vl_saldo_inicial DECIMAL(15,2),
                vl_saldo_final DECIMAL(15,2),
                trimestre VARCHAR(6) NOT NULL,
                PRIMARY KEY (data, reg_ans, cd_conta_contabil, trimestre),
                FOREIGN KEY (reg_ans) REFERENCES operadoras(registro_ans)
            );
        """)
        db.commit()
        print("Tabela criada com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabela despesas: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close()

def obter_registros_ans():
    db = conectar_banco()
    cursor = db.cursor()
    
    try:
        cursor.execute("SELECT registro_ans FROM operadoras")
        return {row[0] for row in cursor.fetchall()}
    except Exception as e:
        print(f"Erro ao obter registros ANS: {e}")
        return set()
    finally:
        cursor.close()
        db.close()

def processar_arquivo_csv(csv_file, trimestre, reg_ans_existentes):
    db = conectar_banco()
    cursor = db.cursor()
    
    try:

        df = pd.read_csv(csv_file, delimiter=';', quotechar='"', encoding='utf-8')
        df.columns = df.columns.str.lower()
        
        # Transformações
        df['reg_ans'] = df['reg_ans'].astype(str)
        df["vl_saldo_inicial"] = df["vl_saldo_inicial"].astype(str).str.replace(",", ".")
        df["vl_saldo_final"] = df["vl_saldo_final"].astype(str).str.replace(",", ".")
        df['data'] = pd.to_datetime(df['data'], dayfirst=True).dt.strftime('%Y-%m-%d')
        
        # Filtrar registros
        df = df[df['reg_ans'].isin(reg_ans_existentes)]
        
        if df.empty:
            print(f"Nenhum registro válido. Pulando...")
            return
        
        # Preparar valores para inserção
        valores = [tuple(row) + (trimestre,) for _, row in df.iterrows()]
        total_registros = len(valores)
        
        # Inserir em lotes
        batch_size = 10000
        for i in range(0, total_registros, batch_size):
            batch = valores[i:i + batch_size]
            cursor.executemany("""
                INSERT INTO despesas (
                    data, reg_ans, cd_conta_contabil, 
                    descricao, vl_saldo_inicial, vl_saldo_final, trimestre
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, batch)
            db.commit()
            print(f"  Lote {i//batch_size + 1}: {min(i + batch_size, total_registros)}/{total_registros} registros inseridos")
            
        print(f"{total_registros} registros processados com sucesso para {trimestre}")
        
    except Exception as e:
        print(f"Erro ao processar {csv_file}: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close()

def carregar_dados_despesas():
    reg_ans_existentes = obter_registros_ans()
    
    if not reg_ans_existentes:
        print("Nenhum registro ANS encontrado na tabela operadoras.")
        return
    
    for csv_file, trimestre in CSV_FILES.items():
        processar_arquivo_csv(csv_file, trimestre, reg_ans_existentes)
        
def main():
    # Configuração inicial
    criar_tabela_despesas()
    
    # Inserção de dados
    carregar_dados_despesas()
    
    print("\nProcessamento concluído com sucesso!")

if __name__ == "__main__":
    main()
