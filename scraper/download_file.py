import requests
from io import BytesIO

def download_file(url: str) -> BytesIO:
    
    """
    Descarga el archivo desde la URL y lo devuelve como un objeto en memoria.
    """

    print(f"🔄 Descargando archivo desde {url}...")

    response = requests.get(url)
    response.raise_for_status()

    print(f"✅ Archivo descargado correctamente.")

    return BytesIO(response.content)