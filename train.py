import argparse
import os
import pandas as pd

from azureml.core import Run, Workspace

import experiment_utils
from experiment_train import Train
from experiment_eval import Eval
from dataloader import Dataloader

import mask_rcnn.utils as utils


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Train Mask R-CNN to detect food.")
    parser.add_argument("--dataset_name", type=str, dest="dataset_name", required=True)
    parser.add_argument("--download_folder", type=str, dest="download_folder", required=True)
    parser.add_argument("--epochs", type=int, dest="epochs", required=True)
    args = parser.parse_args()

    print(f"[*] Dataset Name: {args.dataset_name}")
    print(f"[*] Download Folder: {args.download_folder}")
    print(f"[*] Epochs: {args.epochs}")

    # Get workspace
    run_context: Run = Run.get_context()
    ws: Workspace = run_context.experiment.workspace

    # Load and create food dataset
    dataloader: Dataloader = Dataloader(args.download_folder)
    df: pd.DataFrame = dataloader.load_dataset(ws, args.dataset_name)
    dataset_train, dataset_validation, dataset_test = dataloader.create_train_valid_test_datasets(df)

    # Create Mask R-CNN Model
    model, config = experiment_utils.create_mask_rcnn_model("training")

    # Download and load weigths
    weights_path: str = "./mask_rcnn_coco.h5"
    if not os.path.exists(weights_path):
        utils.download_trained_weights(weights_path)

    model.load_weights(weights_path, by_name=True, exclude=["mrcnn_class_logits", "mrcnn_bbox_fc", "mrcnn_bbox", "mrcnn_mask"])
    
    trainer: Train = Train()
    trained_model_name = trainer.execute_train(dataset_train, dataset_validation, model, config, args.epochs)

    model_trained, _ = experiment_utils.create_mask_rcnn_model("inference")

    print("[*] Load weights from path: ", trained_model_name)
    model_trained.load_weights(trained_model_name, by_name=True)

    evaluator: Eval = Eval()
    evaluator.execute_eval(dataset_test, model_trained)
