<<<<<<< HEAD
# Prueba_tecnica_summa_ml
Punto 1 de la prueba
=======
# 📦 Servicio de Abastecimiento IA - API de Clasificación

Esta API es una solución robusta basada en **FastAPI** para la clasificación inteligente de clientes en categorías **Alpha** y **Betha**. Utiliza un modelo de Machine Learning (Random Forest) entrenado para optimizar el proceso de abastecimiento basándose en el comportamiento de compra y características demográficas.

---

## 🚀 Características
* **Predicción en Tiempo Real:** Endpoint optimizado para recibir datos y devolver clasificaciones instantáneas.
* **Umbral Personalizado:** Implementa un `CLASSIFICATION_THRESHOLD` de **0.35** para ajustar la sensibilidad de la clasificación hacia la clase Betha.
* **Validación de Datos:** Uso de **Pydantic** para garantizar que los datos de entrada cumplan con el formato y tipos requeridos.
* **Registro de Auditoría:** Sistema de logs integrado para monitorear peticiones y posibles errores técnicos.

---

## 🛠️ Estructura del Proyecto
```text
.
├── main.py              # Código principal de la API
├── requirements.txt     # Dependencias del proyecto
└── src/
    └── models/
        ├── rf_model.pkl      # Modelo Random Forest entrenado
        ├── preprocessor.pkl  # Pipeline de transformación (Scaler/Encoder)
        └── label_encoder.pkl # Codificador de etiquetas (Alpha/Betha)


## 🏃 Ejecución del Servidor
Para iniciar la API en modo de desarrollo, ejecuta el siguiente comando:

```Bash

uvicorn main:app --reload
La API estará disponible en: http://127.0.0.1:8000

📖 Documentación de la API
FastAPI genera documentación interactiva automáticamente:

Swagger UI: http://127.0.0.1:8000/docs (Para probar el endpoint directamente).

Redoc: http://127.0.0.1:8000/redoc

Endpoint: POST /predict
Recibe los datos del cliente y devuelve la clasificación predicha.

Cuerpo de la petición (Ejemplo JSON):

```JSON

{
  "SeniorCity": 0,
  "Partner": "Yes",
  "Dependents": "No",
  "Service1": "No",
  "Service2": "No phone service",
  "Security": "No",
  "OnlineBackup": "Yes",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "Charges": 29.85,
  "Demand": 1200.50
}

##⚠️ Manejo de Errores
422 Unprocessable Entity: Los datos enviados son válidos en formato pero contienen valores categóricos que el modelo no conoce.

500 Internal Server Error: Error inesperado en el procesamiento de la lógica del servidor.

Desarrollado por: Brian - Prueba Técnica de IA Año: 2026
>>>>>>> 3f7e4f6 (Initial commit: API de Abastecimiento y Modelos de Demanda)
