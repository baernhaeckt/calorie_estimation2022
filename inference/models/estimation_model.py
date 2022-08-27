from pydantic import BaseModel


class EstimationModel(BaseModel):
    class_name: str
    estimated_calories: float
    estimated_protein: float
    estimated_fat: float
    estimated_carbohydrates: float


