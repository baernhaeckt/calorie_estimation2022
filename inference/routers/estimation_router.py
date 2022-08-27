from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

import config
from models.estimation_model import EstimationModel

router = APIRouter()


@router.get("/", tags=["api test"])
def touch():
    return f"Model API is running on ENV {config.settings.ENV}"


@router.get("/calories", response_model=EstimationModel, status_code=200, tags=["estimation"])
async def get_calories():
    result: EstimationModel = EstimationModel(
        estimated_calories=100
    )

    return JSONResponse(content=jsonable_encoder(result))
