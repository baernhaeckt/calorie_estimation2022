from typing import List

from food_config import FoodConfig
import mask_rcnn.model as modellib
from food_dataset import FoodDataset
from models.estimation_model import EstimationModel
from services.calorie_service import CalorieService


class PredictionService:
    masked_plate_pixels: float = 1130972
    real_plate_size: float = 12
    real_plate_area: float = 113.04
    pixels_per_sq_centimeter: float = masked_plate_pixels / real_plate_area

    def __init__(self, ):
        self.config: FoodConfig = FoodConfig()
        self.food_dataset: FoodDataset = FoodDataset()
        self.food_dataset.prepare()

        self.model: modellib = modellib.MaskRCNN(mode="inference", config=self.config, model_dir="./logs")
        self.model.load_weights("./weights/mask_rcnn_custom-food_0049.h5", by_name=True)

        self.calorie_service: CalorieService = CalorieService()

    def predict(self, image) -> List[EstimationModel]:
        estimations: List[EstimationModel] = list()
        results = self.model.detect([image])
        first_result = results[0]

        for i in range(first_result["masks"].shape[-1]):
            masked_food_pixels = first_result["masks"][:, :, i].sum()
            class_name: str = self.food_dataset.class_names[first_result["class_ids"][i]]
            real_food_area: float = masked_food_pixels / self.pixels_per_sq_centimeter

            estimations.append(EstimationModel(
                class_name=class_name,
                estimated_calories=self.calorie_service.get_calories_per_category(class_name, real_food_area),
                estimated_protein=self.calorie_service.get_protein_per_category(class_name, real_food_area),
                estimated_fat=self.calorie_service.get_fat_per_category(class_name, real_food_area),
                estimated_carbohydrates=self.calorie_service.get_carbohydrates_per_category(class_name, real_food_area)
            ))

        return estimations
