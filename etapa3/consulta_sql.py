import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

def conectar_banco():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'), 
        user=os.getenv('DB_USER', 'root'),    
        password=os.getenv('DB_PASSWORD'),      
        database=os.getenv('DB_NAME', 'estagio_intuitivecare')
    )

def consultar_top_operadoras_ultimo_ano():
    db = conectar_banco()
    cursor = db.cursor(dictionary=True)
    
    try:
        # Consulta para obter o último ano disponível nos dados
        cursor.execute("""
        SELECT 
            SUBSTRING(trimestre, LOCATE('T', trimestre) + 1) AS ultimo_ano
        FROM despesas 
        ORDER BY 
            CAST(SUBSTRING(trimestre, LOCATE('T', trimestre) + 1) AS UNSIGNED) DESC
        LIMIT 1
        """)
        
        resultado = cursor.fetchone()
        if not resultado:
            raise ValueError("Não foram encontrados dados na tabela despesas")
            
        ultimo_ano = resultado['ultimo_ano']
        print(f"Último ano encontrado: {ultimo_ano}")
        
        # Consulta das top operadoras no último ano
        cursor.execute("""
        SELECT 
            d.reg_ans,
            o.nome_fantasia AS operadora,
            SUM(d.vl_saldo_final - d.vl_saldo_inicial) AS total_gasto
        FROM despesas d
        JOIN operadoras o ON d.reg_ans = o.registro_ans
        WHERE SUBSTRING(d.trimestre, LOCATE('T', d.trimestre) + 1) = %s
        GROUP BY d.reg_ans, o.nome_fantasia
        ORDER BY total_gasto DESC
        LIMIT 10
        """, (ultimo_ano,))
        
        resultados = cursor.fetchall()
        
        if resultados:
            df = pd.DataFrame(resultados)
            print(f"\nTop 10 operadoras com maior gasto no ano {ultimo_ano}:")
            print(df.to_string(index=False))
        else:
            print(f"Nenhum dado encontrado para o ano {ultimo_ano}")

    except Exception as e:
        print(f"Erro na consulta: {e}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def consultar_top_operadoras_eventos_sinistros():
    
    db = conectar_banco()
    cursor = db.cursor(dictionary=True)

    try:
        # Primeiro obtém o último trimestre
        cursor.execute("SELECT MAX(trimestre) as ultimo_trimestre FROM despesas")
        ultimo_trimestre = cursor.fetchone()['ultimo_trimestre']
        print(ultimo_trimestre)

        # Consulta principal
        query = """
        SELECT 
            d.reg_ans,
            o.nome_fantasia AS operadora,
            SUM(d.vl_saldo_final - d.vl_saldo_inicial) AS total_despesas,
            d.trimestre
        FROM 
            despesas d
        JOIN 
            operadoras o ON d.reg_ans = o.registro_ans
        WHERE 
            d.descricao = %s
            AND d.trimestre = %s
        GROUP BY 
            d.reg_ans, o.nome_fantasia, d.trimestre
        ORDER BY 
            total_despesas DESC
        LIMIT 10
        """
        
        descricao_pattern = 'EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA À SAÚDE'
        cursor.execute(query, (descricao_pattern, ultimo_trimestre))
        
        resultados = cursor.fetchall()
        
        if resultados:
            df = pd.DataFrame(resultados)
            print(f"\nTop 10 operadoras com maiores despesas em Eventos/Sinistros ({ultimo_trimestre}):")
            print(df.to_string(index=False))
        else:
            print(f"Nenhum resultado encontrado para o trimestre {ultimo_trimestre}")

    except Exception as e:
        print(f"Erro: {e}")

def main():
    consultar_top_operadoras_eventos_sinistros()
    print('//////////////////')
    print('//////////////////')
    consultar_top_operadoras_ultimo_ano()

if __name__ == "__main__":
    main()