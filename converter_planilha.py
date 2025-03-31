import zipfile
import pdfplumber
import pandas as pd

zip_path = "./etapa1/pdf_comprimido.zip"
pdf_name = "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
csv_output = "tabela_extraida.csv"

with zipfile.ZipFile(zip_path, "r") as zip_ref:
    with zip_ref.open(pdf_name) as pdf_file:
        with pdfplumber.open(pdf_file) as pdf:
            tabelas = []
            for page in pdf.pages:
                tabela = page.extract_table()
                if tabela:
                    tabelas.extend(tabela)

df = pd.DataFrame(tabelas[1:], columns=tabelas[0])
df.to_csv(csv_output, index=False, encoding="utf-8")

