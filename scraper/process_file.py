import pandas as pd
import re

def process_file(excel_file, sheet_name):

    """
    Procesa el archivo Excel y retorna un DataFrame plano con columnas:
    Date, Region, Product, Unit, Price.
    """

    #Leo hoja cruda
    df_raw = pd.read_excel(excel_file, sheet_name=sheet_name, engine="xlrd", header=None)

    #Detecto las filas donde están los encabezados
    fila_anios = df_raw.iloc[2].ffill()
    fila_meses = df_raw.iloc[3]

    #Armo nombres de columnas
    nuevas_columnas = []
    for i in range(len(fila_anios)):
        anio = str(fila_anios[i]).strip()
        mes = str(fila_meses[i]).strip()

        if i == 0:
            nuevas_columnas.append("Región")
        elif i == 1:
            nuevas_columnas.append("Productos seleccionados")
        elif i == 2:
            nuevas_columnas.append("Unidad de medida")
        else:
            anio = re.sub(r"[^\d]", "", anio)
            if anio and mes and mes.lower() != "nan":
                nuevas_columnas.append(f"{anio}-{mes}")
            else:
                nuevas_columnas.append(None)

    #Aplico nombres de columnas
    df_raw.columns = nuevas_columnas
    df_raw = df_raw.iloc[5:].reset_index(drop=True)

    #Convierto a formato largo
    df_largo = convertir_a_largo(df_raw)
    return df_largo


def limpiar_y_traducir_fecha(fecha_str):
    meses = {
        "enero": "January", "febrero": "February", "marzo": "March",
        "abril": "April", "mayo": "May", "junio": "June",
        "julio": "July", "agosto": "August", "septiembre": "September",
        "octubre": "October", "noviembre": "November", "diciembre": "December"
    }

    if not isinstance(fecha_str, str):
        return None
    fecha_str = fecha_str.strip().lower()
    fecha_str = re.sub(r"[áéíóú]", lambda x: {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}[x.group()], fecha_str)
    match = re.match(r"(\d{4})[\s\-]*([a-z]+)", fecha_str)
    if not match:
        return None
    anio, mes_esp = match.groups()
    mes_eng = meses.get(mes_esp)
    return f"{anio}-{mes_eng}" if mes_eng else None


def convertir_a_largo(df_raw):
    columnas_fijas = ['Región', 'Productos seleccionados', 'Unidad de medida']
    columnas_fecha = [col for col in df_raw.columns if col not in columnas_fijas and col is not None]

    df_largo = df_raw.melt(
        id_vars=columnas_fijas,
        value_vars=columnas_fecha,
        var_name="Date",
        value_name="Price"
    )

    df_largo = df_largo.rename(columns={
        "Productos seleccionados": "Product",
        "Unidad de medida": "Unit",
        "Región": "Region"
    })

    df_largo["Date"] = df_largo["Date"].apply(limpiar_y_traducir_fecha)
    df_largo["Date"] = pd.to_datetime(df_largo["Date"], format="%Y-%B", errors="coerce")

    df_largo = df_largo[pd.to_numeric(df_largo["Price"], errors="coerce").notnull()]
    df_largo["Price"] = df_largo["Price"].astype(float)

    return df_largo[["Date", "Region", "Product", "Unit", "Price"]]