import requests
import zipfile
import os
from concurrent.futures import ThreadPoolExecutor

def downloader_file(url, file_path):
    response = requests.get(url, stream=True)
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=4096):
            file.write(chunk)   

urls = [
    "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf",

    "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"
    ]

pdf_paths = ['Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf', 'Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf']

with ThreadPoolExecutor() as executor:
    executor.map(downloader_file, urls, pdf_paths)

zip_path = 'pdf_comprimido.zip'

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for pdf_path in pdf_paths:
        zipf.write(pdf_path, os.path.basename(pdf_path))

for pdf_path in pdf_paths:
    if (os.path.exists(pdf_path)):
        os.remove(pdf_path)