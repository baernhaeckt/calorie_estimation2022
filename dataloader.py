import os
import random
import pandas as pd
import numpy as np

from azureml.core import Workspace, Dataset
from azureml.data import TabularDataset, FileDataset
from food_dataset import FoodDataset

from typing import Tuple, List


class Dataloader:
    def __init__(self, download_folder: str = "download") -> None:
        self.download_folder: str = download_folder

    def _create_food_dataset(self, df: np.ndarray, dataset_name: str) -> FoodDataset:
        dataset: FoodDataset = FoodDataset()
        dataset.load_food(df, self.download_folder)
        dataset.prepare()

        print(f"[*] {dataset_name} dataset:")
        print(" ", "Image Count: {}".format(len(dataset.image_ids)))
        print(" ", "Class Count: {}".format(dataset.num_classes))
        print(" ", "Classes:", dataset.class_names)

        return dataset

    def load_test_dataset(self, workspace: Workspace, dataset_name: str) -> List[str]:
        dataset: FileDataset = Dataset.get_by_name(workspace=workspace, name=dataset_name)
        test_image_list: List[str] = dataset.download(target_path=os.path.join(self.download_folder, "test"))

        return random.sample(test_image_list, 20)

    def load_dataset(self, workspace: Workspace, dataset_name: str) -> pd.DataFrame:
        # Mount dataset
        dataset: TabularDataset = Dataset.get_by_name(workspace=workspace, name=dataset_name)
        dataset.download("image_url", target_path=self.download_folder, overwrite=True)

        # to pandas
        df = dataset.to_pandas_dataframe()
        df["image_url"] = df["image_url"].astype(str)

        return df

    def create_train_valid_explain_datasets(self, dataframe: pd.DataFrame) -> Tuple[FoodDataset, FoodDataset, FoodDataset]:
        # Create filter column
        for index, row in dataframe.iterrows():
            dataframe.loc[index, "filter_label"] = row.label[0]["label"]

        # Create Explain Dataframe
        explain_df: pd.DataFrame = pd.DataFrame()
        for label in set(dataframe.filter_label):
            filter_idx = np.where(dataframe.filter_label == label)[0]
            random_filter_idx = np.random.choice(filter_idx, 1)
            
            explain_df = explain_df.append(dataframe.iloc[random_filter_idx])
            dataframe.drop(random_filter_idx, inplace=True, axis=0)


        # Train / Test split
        train_df = dataframe.sample(frac=0.7, random_state=42)
        valid_df = dataframe.drop(train_df.index)

        # Train dataset
        dataset_train: FoodDataset = self._create_food_dataset(train_df, "Training")

        # Validation dataset
        dataset_validation: FoodDataset = self._create_food_dataset(valid_df, "Validation")

        # Explain dataset
        dataset_explain: FoodDataset = self._create_food_dataset(explain_df, "Test")

        return dataset_train, dataset_validation, dataset_explain