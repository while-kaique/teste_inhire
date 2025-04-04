import zipfile
import pdfplumber
import pandas as pd

zip_path = "../etapa1/pdf_comprimido.zip"
pdf_name = "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
csv_output = "Teste_KaiqueBrenoGeronimoMedeiros.csv"

# Dicionário de substituições
substituicoes = {
    "OD": "Odontológica",
    "AMB": "Ambulatorial",
    "HCO": "Hospitalar Com Obstetrícia",
    "HSO": "Hospitalar Sem Obstetrícia",
    "REF": "Referência",
    "PAC": "Procedimento de Alta Complexidade",
    "DUT": "Diretriz de Utilização"
}

with zipfile.ZipFile(zip_path, "r") as zip_ref:
    with zip_ref.open(pdf_name) as pdf_file:
        with pdfplumber.open(pdf_file) as pdf:
            tabelas = []
            for page in pdf.pages:
                tabela = page.extract_table()
                if tabela:
                    tabelas.extend(tabela)

print("tabela criada, falta substituir")
# Criação do DataFrame
df = pd.DataFrame(tabelas[1:], columns=tabelas[0])
df.rename(columns=substituicoes, inplace=True)

# 3. Substituição INTELIGENTE (apenas onde os valores existem)
for col in df.columns:
    valores_unicos = df[col].unique()
    # Verifica se algum valor do dicionário existe na coluna
    if any(valor in substituicoes.keys() for valor in valores_unicos if pd.notna(valor)):
        print(f"\nColuna '{col}': {[v for v in valores_unicos if v in substituicoes]}")
        df[col] = df[col].replace(substituicoes)

# 4. Verificação FINAL
print("\n✅ Valores únicos DEPOIS da substituição:")
for col in df.columns:
    if any(original in df[col].values for original in substituicoes.keys()):
        print(f"Coluna '{col}': {df[col].unique()}")

# 5. Exportação
df.to_csv(csv_output, index=False, encoding="utf-8-sig")
print(f"\nArquivo salvo em: {csv_output}")