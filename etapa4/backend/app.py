from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="kaiquemedeiros08",
        database="estagio_intuitivecare"
    )

@app.route('/api/operadoras', methods=['GET'])
def buscar_operadoras():
    termo = request.args.get('q', '')
    pagina = int(request.args.get('page', 1))
    por_pagina = 10
    
    try:
        db = conectar_banco()
        cursor = db.cursor(dictionary=True)
        
        # Query para contar o total de resultados
        count_query = """
        SELECT COUNT(*) as total 
        FROM operadoras 
        WHERE nome_fantasia LIKE %s OR razao_social LIKE %s
        """
        parametro_busca = f"%{termo}%"
        cursor.execute(count_query, (parametro_busca, parametro_busca))
        total = cursor.fetchone()['total']
        
        # Query modificada para tratar nome_fantasia NULL/vazio
        data_query = """
        SELECT 
            registro_ans, 
            CASE 
                WHEN nome_fantasia IS NULL OR nome_fantasia = '' THEN 'Desconhecido/Não informado' 
                ELSE nome_fantasia 
            END as nome_fantasia,
            razao_social 
        FROM operadoras 
        WHERE nome_fantasia LIKE %s OR razao_social LIKE %s
        LIMIT %s OFFSET %s
        """
        offset = (pagina - 1) * por_pagina
        cursor.execute(data_query, (parametro_busca, parametro_busca, por_pagina, offset))
        
        resultados = cursor.fetchall()
        
        return jsonify({
            "data": resultados,
            "pagination": {
                "total": total,
                "per_page": por_pagina,
                "current_page": pagina,
                "total_pages": (total + por_pagina - 1) // por_pagina,
                "has_next": pagina * por_pagina < total,
                "has_prev": pagina > 1
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'db' in locals() and db.is_connected():
            db.close()

if __name__ == '__main__':
    app.run(debug=True)