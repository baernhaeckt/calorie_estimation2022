from typing import List, Tuple
from azureml.core import Run, Model

import mask_rcnn.model as modellib

from food_config import FoodConfig


def register_model(run_context: Run) -> str:
    run_log_files: List[str] = run_context.get_file_names()
    checkpoint_files = [f for f in run_log_files if "mask_rcnn_custom-food" in f]
    
    last_checkpoint: str = checkpoint_files[-1]
    register_model: Model = run_context.register_model(model_name="mask_rcnn_custom_food", model_path=last_checkpoint)
    print("[*] Register Model:", register_model)

    return last_checkpoint

def register_tflite_model(run_context: Run, model_path: str, base_model_version: int) -> str:
    register_model: Model = run_context.register_model(model_name="mask_rcnn_custom_food_tflite", model_path=model_path, tags={"base model version": base_model_version})
    print("[*] Register TF Lite Model:", register_model)

    return register_model.name

def create_mask_rcnn_model(mode: str) -> Tuple[modellib.MaskRCNN, FoodConfig]:
    config: FoodConfig = FoodConfig()
    model: modellib.MaskRCNN = modellib.MaskRCNN(
        mode=mode,
        config=config,
        model_dir="logs"
    )

    return model, config