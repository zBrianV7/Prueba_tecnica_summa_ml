import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import joblib
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "src" / "models" / "rf_model.pkl"
PROC_PATH = BASE_DIR / "src" / "models" / "preprocessor.pkl"
LE_PATH = BASE_DIR / "src" / "models" / "label_encoder.pkl"

class SupplyData(BaseModel):
    SeniorCity: int = Field(..., example=0)
    Partner: str = Field(..., example="Yes")
    Dependents: str = Field(..., example="No")
    Service1: str = Field(..., example="No")
    Service2: str = Field(..., example="No phone service")
    Security: str = Field(..., example="No")
    OnlineBackup: str = Field(..., example="Yes")
    DeviceProtection: str = Field(..., example="No")
    TechSupport: str = Field(..., example="No")
    Contract: str = Field(..., example="Month-to-month")
    PaperlessBilling: str = Field(..., example="Yes")
    PaymentMethod: str = Field(..., example="Electronic check")
    Charges: float = Field(..., example=29.85)
    Demand: float = Field(..., example=1200.50)

app = FastAPI(title="Servicio de Abastecimiento IA")

CLASSIFICATION_THRESHOLD = 0.35

def load_artifacts():
    try:
        model = joblib.load(MODEL_PATH)
        proc = joblib.load(PROC_PATH)
        le = joblib.load(LE_PATH)
        logger.info("Artefactos cargados exitosamente.")
        return model, proc, le
    except Exception as e:
        logger.error(f"Error crítico cargando modelos: {e}")
        raise RuntimeError("No se pudieron cargar los modelos.")

rf_model, preprocessor, le = load_artifacts()

@app.post("/predict")
async def predict_class(data: SupplyData):
    try:
        input_data = pd.DataFrame([data.model_dump()])
        
        X_transformed = preprocessor.transform(input_data)
        
        probs = rf_model.predict_proba(X_transformed)
        prob_betha = float(probs[0][1])
        
        prediction_int = 1 if prob_betha >= CLASSIFICATION_THRESHOLD else 0
        prediction_label = le.inverse_transform([prediction_int])[0]
        
        return {
            "status": "success",
            "data": {
                "classification": str(prediction_label),
                "confidence": round(prob_betha, 4),
                "metadata": {
                    "threshold_used": CLASSIFICATION_THRESHOLD,
                    "model_version": "1.0.0"
                }
            }
        }

    except ValueError as ve:
        logger.warning(f"Error de validación de categorías: {ve}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "Unprocessable Entity",
                "message": "Uno o más valores categóricos no son válidos para el modelo.",
                "technical_details": str(ve)
            }
        )

    except Exception as e:
        logger.error(f"Error inesperado en el servidor: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": "Ocurrió un error inesperado al procesar la predicción."
            }
        )
