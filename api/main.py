from fastapi import FastAPI, HTTPException
from schemas import PredictInventoryRequest
from model_utils import train_model, predict_inventory

app = FastAPI(
    title="Retail Demand Forecasting API",
    description="Demand Forecasting & Inventory Optimization System",
    version="1.0"
)


@app.get("/")
def health_check():
    return {"status": "API is running successfully"}


@app.post("/train")
def train():
    return train_model()


@app.post("/predict-inventory")
def predict(request: PredictInventoryRequest):
    try:
        return predict_inventory(
            request.store_id,
            request.product_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
