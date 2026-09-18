"""Módulo para la persistencia de datos mediante lectura y escritura en formato JSON."""

import json
import os


def cargar_citas(ruta_archivo: str) -> list:
    """Deserializa el archivo JSON y retorna la lista de citas."""
    if not os.path.exists(ruta_archivo):
        return []

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def guardar_citas(ruta_archivo: str, datos: list) -> bool:
    """Serializa la lista de citas y la guarda en el archivo JSON."""
    try:
        directorio = os.path.dirname(ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        return True
    except Exception as error:
        print(f"Error al guardar los datos: {error}")
        return False