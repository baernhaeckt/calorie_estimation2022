from mask_rcnn.config import Config
from food_dataset import clusters


class FoodConfig(Config):
    NAME: str = "custom-food"
    GPU_COUNT: int = 1
    IMAGES_PER_GPU: int = 1
    NUM_CLASSES: int = 1 + len(clusters)
    STEPS_PER_EPOCH: int = 50
    VALIDATION_STEPS: int = 50
    DETECTION_MIN_CONFIDENCE: float = 0.8
    USE_MINI_MASK: bool = False
    BACKBONE = "resnet50"

    # Custom settings for the TF Lite model
    OUTPUT_MASK = "mrcnn_mask"
    OUTPUT_DETECTION = "mrcnn_detection"