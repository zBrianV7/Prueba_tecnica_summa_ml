import pandas as pd
import requests

# 1. Configuración
API_URL = "http://127.0.0.1:8000/predict"
PATH_DATA = "data/to_predict.csv"  # Ajusta si es .xlsx o .csv

# 2. Cargar los datos a predecir
df_to_predict = pd.read_csv(PATH_DATA) 

# 3. Asignar las demandas que ya calculaste (Punto 1)
# Supongamos que tus predicciones fueron estas (reemplaza con tus valores reales):
predicciones_demanda = {
    "2022-05-01": 1300.06, 
    "2022-06-01": 1309.21, 
    "2022-07-01": 1709.79
}


demands = [1300.06, 1309.21, 1709.79] 
df_to_predict['Demand'] = demands


def get_api_classification(row):
    payload = {
        "SeniorCity": int(row['SeniorCity']),
        "Partner": str(row['Partner']),
        "Dependents": str(row['Dependents']),
        "Service1": str(row['Service1']),
        "Service2": str(row['Service2']),
        "Security": str(row['Security']),
        "OnlineBackup": str(row['OnlineBackup']),
        "DeviceProtection": str(row['DeviceProtection']),
        "TechSupport": str(row['TechSupport']),
        "Contract": str(row['Contract']),
        "PaperlessBilling": str(row['PaperlessBilling']),
        "PaymentMethod": str(row['PaymentMethod']),
        "Charges": float(row['Charges']),
        "Demand": float(row['Demand'])
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result['data']['classification']
        else:
            return f"Error API: {response.status_code}"
    except Exception as e:
        return f"Error Conexión: {str(e)}"

# 5. Ejecutar la clasificación
print("Consultando API para obtener clases Alpha/Betha...")
df_to_predict['Class'] = df_to_predict.apply(get_api_classification, axis=1)

# 6. Guardar el archivo FINAL de entrega
df_to_predict.to_csv("resultados_finales_brian.csv", index=False)

print("✅ Proceso completado exitosamente.")
print(df_to_predict[['autoID', 'Demand', 'Class']])