from pydantic import BaseModel

class PredictInventoryRequest(BaseModel):
    store_id: str
    product_id: str
 