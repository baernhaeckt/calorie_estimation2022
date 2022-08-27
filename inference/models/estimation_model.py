from pydantic import BaseModel


class EstimationModel(BaseModel):
    estimated_calories: float

