import chardet

# Lendo o arquivo em modo binário para análise
with open("tabela_extraida.csv", "rb") as file:
    raw_data = file.read()

# Detectando a codificação
result = chardet.detect(raw_data)
print(result)
