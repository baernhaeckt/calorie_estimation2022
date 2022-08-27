from azureml.core import Run

import experiment_utils
from food_config import FoodConfig
from food_dataset import FoodDataset
from azureml_logger import AzureMlLogger

from mask_rcnn.model import MaskRCNN

from imgaug import augmenters as iaa

class Train:
    def execute_train(self, dataset_train: FoodDataset, dataset_validation: FoodDataset, model: MaskRCNN, config: FoodConfig, epochs: int) -> str:
        # Get run context
        run_context: Run = Run.get_context()

        # Input augmentations
        augmentation = iaa.SomeOf((0, None), [
            iaa.Fliplr(0.5), # Left-right flip
            iaa.Flipud(0.5), # Up-down flip
            iaa.Add((-40, 40)), # Add delta value to brightness
            iaa.LinearContrast((0.8, 1.2)), # Transform contrast
            iaa.AddToSaturation((-40, 40)), # Add delta value to saturation
            iaa.AddToHue((-20, 20)) # Add delta value to hue
        ])

        # Create Azure ML Logger
        logger: AzureMlLogger = AzureMlLogger(run_context)

        # Train network heads
        print('[*] Training network heads.')
        model.train(
            dataset_train,
            dataset_validation,
            learning_rate=config.LEARNING_RATE,
            augmentation=augmentation,
            epochs=epochs,
            layers="heads",
            logger=logger
        )

        return experiment_utils.register_model(run_context)