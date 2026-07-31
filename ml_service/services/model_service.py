import os
import joblib
import urllib.request

OCI_MODEL_URL = (
    "https://objectstorage.mx-queretaro-1.oraclecloud.com/p/"
    "uj2kUat0fjU1TcjE2QzFQed8d90Ok3tFQDEdg-M-E1h97Ce8YyC9Uv2dTx7idTru/"
    "n/ax7imsqswlob/b/energiai-models/o/"
    "modelo_pkl-energiai_team72modelo_energiai_team72.pkl"
)

LOCAL_FILENAME = "models/modelo_energiai_team72.pkl"

#descargar modelo desde oci
def download_model_from_oci(url: str, output_path: str):
    print(f"Descargando modelo desde OCI Object Storage...")
    urllib.request.urlretrieve(url, output_path)
    print(f"Descarga completada: Archivo guardado como '{output_path}'")

#guardar modelo localmente si no existe
def load_model():
    if not os.path.exists(LOCAL_FILENAME):
        download_model_from_oci(OCI_MODEL_URL, LOCAL_FILENAME)

    print("Cargando el Pipeline con joblib...")
    model = joblib.load(LOCAL_FILENAME)
    print("Pipeline cargado exitosamente:")
    #print(model)

    return model

model = load_model()