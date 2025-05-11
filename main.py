
import os
from dotenv import load_dotenv
from scraper.download_file import download_file
from scraper.process_file import process_file
from scraper.upload_file import upload_file



def main():
    #Cargar variables de entorno
    load_dotenv()

    API_KEY = os.getenv("ALPHACAST_API_KEY")
    REPO_ID = os.getenv("REPO_ID")
    DATASET_NAME = os.getenv("DATASET_NAME")
    DATASET_DESCRIPTION = os.getenv("DATASET_DESCRIPTION")
    EXCEL_URL = os.getenv("EXCEL_URL")
    SHEET_NAME = os.getenv("SHEET_NAME")

    if not API_KEY:
        raise ValueError("No se encontro ALPHACAST_API_KEY")


    #Descargar archivo Excel
    archivo_excel = download_file(EXCEL_URL)

    #Procesar archivo
    df_result = process_file(archivo_excel, SHEET_NAME)

    #Subir a Alphacast
    upload_file(
        alphacast_api_key=API_KEY,
        df=df_result,
        repo_id=REPO_ID,
        dataset_name=DATASET_NAME,
        description=DATASET_DESCRIPTION
    )

if __name__ == "__main__":
    main()
