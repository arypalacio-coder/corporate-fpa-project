import os
import zipfile
import requests

# URL oficial y actualizada del dataset trimestral (Q3 2024)
URL_SEC = "https://www.sec.gov/files/dera/data/financial-statement-data-sets/2024q3.zip"
OUTPUT_DIR = "data/raw"
ZIP_PATH = os.path.join(OUTPUT_DIR, "2024q3.zip")

# Cabecera requerida por la SEC (declaración de identidad y contacto)
HEADERS = {
    "User-Agent": "FinancialPortfolioAnalyst user.analyst@example.com",
    "Accept-Encoding": "gzip, deflate"
}

def descargar_y_descomprimir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Iniciando descarga desde: {URL_SEC}")
    response = requests.get(URL_SEC, headers=HEADERS, stream=True)
    
    if response.status_code == 200:
        with open(ZIP_PATH, "wb") as file:
            for chunk in response.iter_content(chunk_size=16384):
                file.write(chunk)
        print("Descarga finalizada. Descomprimiendo archivos...")
        
        with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
            zip_ref.extractall(OUTPUT_DIR)
            
        os.remove(ZIP_PATH)
        print("Archivos descomprimidos con éxito en la carpeta data/raw/")
    else:
        print(f"Error en la descarga. Código HTTP: {response.status_code}")

if __name__ == "__main__":
    descargar_y_descomprimir()