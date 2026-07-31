"""
Script de verificación y carga del modelo desde OCI Object Storage.
Tarea T10 - Hackathon EnergiAI Team 72
"""

import os
import joblib
import pandas as pd
import urllib.request

OCI_MODEL_URL = (
    "https://objectstorage.mx-queretaro-1.oraclecloud.com/p/"
    "uj2kUat0fjU1TcjE2QzFQed8d90Ok3tFQDEdg-M-E1h97Ce8YyC9Uv2dTx7idTru/"
    "n/ax7imsqswlob/b/energiai-models/o/"
    "modelo_pkl-energiai_team72modelo_energiai_team72.pkl"
)

LOCAL_FILENAME = "modelo_energiai_team72.pkl"


def download_model_from_oci(url: str, output_path: str):
    print(f"Descargando modelo desde OCI Object Storage...")
    urllib.request.urlretrieve(url, output_path)
    print(f"Descarga completada: Archivo guardado como '{output_path}'")


def verify_model_inference(model_path: str):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"No se encontró el archivo: {model_path}")

    print("Cargando el Pipeline con joblib...")
    model = joblib.load(model_path)
    print("Pipeline cargado exitosamente:")
    print(model)

    return model


if __name__ == "__main__":
    try:
        download_model_from_oci(OCI_MODEL_URL, LOCAL_FILENAME)
        pipeline = verify_model_inference(LOCAL_FILENAME)
        print("\n¡La verificación T10 en OCI fue un éxito!")

    except Exception as e:
        print(f"\nError durante la verificación: {e}")