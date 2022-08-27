import os
from typing import List

import config
import tempfile
import skimage.io
import shutil

from fastapi import APIRouter, File, UploadFile
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from pathlib import Path

from models.estimation_model import EstimationModel
from services.prediction_service import PredictionService

router = APIRouter()
prediction_service: PredictionService = PredictionService()


@router.get("/", tags=["api test"])
def touch():
    return f"Model API is running on ENV {config.settings.ENV}"


@router.post("/calories", response_model=EstimationModel, status_code=200, tags=["estimation"], )
async def get_calories(image: UploadFile = File(...)):
    suffix = Path(image.filename).suffix
    result: List[EstimationModel] = list()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        try:
            shutil.copyfileobj(image.file, tmp)
            temp_file_path = Path(tmp.name)
            pred_image = skimage.io.imread(temp_file_path)
            result = prediction_service.predict(pred_image)
        except ValueError:
            os.unlink(tmp.name)

    return JSONResponse(content=jsonable_encoder(result))
