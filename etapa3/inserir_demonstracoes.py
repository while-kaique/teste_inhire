
import pandas as pd
import mysql.connector
import os

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
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kaiquemedeiros08",
    database="estagio_intuitivecare"
)

cursor = db.cursor()

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

cursor.execute("SELECT registro_ans FROM operadoras")
reg_ans_existentes = set(row[0] for row in cursor.fetchall())

for csv_file, trimestre in CSV_FILES.items():
    print(f"Processando: {csv_file} ({trimestre})")

    try:
        df = pd.read_csv(csv_file, delimiter=';', quotechar='"', encoding='utf-8')
        df.columns = df.columns.str.lower()
        df['reg_ans'] = df['reg_ans'].astype(str)
        df["vl_saldo_inicial"] = df["vl_saldo_inicial"].astype(str).str.replace(",", ".")
        df["vl_saldo_final"] = df["vl_saldo_final"].astype(str).str.replace(",", ".")
        df['data'] = pd.to_datetime(df['data'], dayfirst=True).dt.strftime('%Y-%m-%d')
        df = df[df['reg_ans'].isin(reg_ans_existentes)]

        if df.empty:
            print(f"⚠️ Nenhum registro válido para {csv_file}. Pulando...")
            continue

        valores = [tuple(row) + (trimestre,) for _, row in df.iterrows()]

        batch_size = 10000  # Insere 10.000 registros por vez

        for i in range(0, len(valores), batch_size):
            batch = valores[i:i + batch_size]
            cursor.executemany("""
                INSERT INTO despesas (data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final, trimestre)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, batch)
            db.commit()  # Confirma o lote antes de continuar
            print(f"Inseridos {i + len(batch)} registros...")
    except Exception as e:
        print(f"Erro ao processar {csv_file}: {e}")

cursor.close()
db.close()
print("Processamento concluído!")
