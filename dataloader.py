from typing import Tuple
import pandas as pd
import numpy as np

from azureml.core import Workspace, Dataset
from azureml.data import TabularDataset
from food_dataset import FoodDataset


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

    def load_dataset(self, workspace: Workspace, dataset_name: str) -> pd.DataFrame:
        # Mount dataset
        dataset: TabularDataset = Dataset.get_by_name(workspace=workspace, name=dataset_name)
        dataset.download("image_url", target_path=self.download_folder, overwrite=True)

        # to pandas
        df = dataset.to_pandas_dataframe()
        df["image_url"] = df["image_url"].astype(str)

        return df

    def create_train_valid_test_datasets(self, dataframe: pd.DataFrame) -> Tuple[FoodDataset, FoodDataset, FoodDataset]:
        # Create filter column
        for index, row in dataframe.iterrows():
            dataframe.loc[index, "filter_label"] = row.label[0]["label"]

        # Create Test Dataframe
        test_df: pd.DataFrame = pd.DataFrame()
        for label in set(dataframe.filter_label):
            filter_idx = np.where(dataframe.filter_label == label)[0]
            random_filter_idx = np.random.choice(filter_idx, 1)
            
            test_df = test_df.append(dataframe.iloc[random_filter_idx])
            dataframe.drop(random_filter_idx, inplace=True, axis=0)


        # Train / Test split
        train_df = dataframe.sample(frac=0.7, random_state=42)
        valid_df = dataframe.drop(train_df.index)

        # Train dataset
        dataset_train: FoodDataset = self._create_food_dataset(train_df, "Training")

        # Validation dataset
        dataset_validation: FoodDataset = self._create_food_dataset(valid_df, "Validation")

        # Test dataset
        dataset_test: FoodDataset = self._create_food_dataset(test_df, "Test")

        return dataset_train, dataset_validation, dataset_test