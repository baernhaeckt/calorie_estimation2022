from azureml.core import Run
from matplotlib import pyplot as plt

import mask_rcnn.utils as utils
import mask_rcnn.visualize as visualize
from mask_rcnn.model import MaskRCNN

from food_dataset import FoodDataset


class Eval:
    def execute_eval(self, dataset_test: FoodDataset, model: MaskRCNN):
        # Get workspace
        run_context: Run = Run.get_context()

        for image_id in dataset_test.image_ids:
            eval_image = dataset_test.load_image(image_id)

            # Execute and visualize detection
            results = model.detect([eval_image])
            r = results[0]
            visualize.display_instances(
                eval_image,
                r["rois"],
                r["masks"],
                r["class_ids"],
                dataset_test.class_names,
                r["scores"]
            )

            run_context.log_image(f"Eval {image_id}", plot=plt)