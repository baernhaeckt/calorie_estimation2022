import os
from typing import Dict, List, Set
import numpy as np
import skimage.io
import skimage.draw
import numpy as np

from mask_rcnn import utils

cluster_dict: Dict[str, str] = {
    "potatoes": "potatoes",
    "pasta": "pasta",
    "pizza": "pizza",
    "fruit": "fruit",
    "beef": "beef",
    "yogurt": "yogurt",
    "bread": "bread",
    "pie": "pie",
    "vegetable": "vegetable",
    "fish": "fish",
    "pudding": "pudding",
    "chicken": "chicken",
    "salad": "salad",
    "soup": "soup",
    "rice": "rice",
    "pork": "pork",
    "packaged": "packaged",
    "cake": "cake",
    "cheese": "cheese"
}
clusters: List[str] = list(set(val for val in cluster_dict.values())) 
clusters.sort() # To keep the same order across all executions
class_id_map: Dict[int, str] = {c: i + 1 for i, c in enumerate(clusters)} # Map each cluster to an integer label

class FoodDataset(utils.Dataset):
    def __init__(self, class_map=None):
        super().__init__(class_map)
        
        # Add class with the id
        for index, class_name in enumerate(clusters):
            self.add_class("custom-food", index + 1, class_name)
    
    def load_food(self, dataframe, download_folder: str):
        # For each image in the dataset add its path and annotations
        for index, row in dataframe.iterrows():
            image_path: str = os.path.join(download_folder, row.image_url)

            try:
                image: np.ndarray = skimage.io.imread(image_path)
            except FileNotFoundError:
                print("[!] Image", image_path, "was not found.")
                continue

            image_height, image_width = image.shape[:2]

            # Unpack polygon coordinates in a list
            polygons: list = list()
            for label in row.label:
                all_points_x: List[float] = list()
                all_points_y: List[float] = list()

                for p in label["polygon"]:
                    for i in range(0, len(p), 2):
                        all_points_x.append(p[i] * image_width)
                        all_points_y.append(p[i + 1] * image_height)
                
                polygons.append({
                    "type": label["label"],
                    "all_points_x": all_points_x,
                    "all_points_y": all_points_y
                })

            self.add_image(
                "custom-food",
                image_id=os.path.basename(row.image_url),
                path=os.path.join(download_folder, row.image_url),
                width=image_width,
                heigth=image_height,
                polygons=polygons
            )

    def load_mask(self, image_id: int):
        image_info: list = self.image_info[image_id]
        if image_info["source"] != "custom-food":
            return super().load_mask(image_id)

        mask = np.zeros([image_info["heigth"], image_info["width"], len(image_info["polygons"])], dtype=np.float32)
        class_ids = np.zeros(len(image_info["polygons"]), dtype=np.int32)

        for index, polygon in enumerate(image_info["polygons"]):
            row_coord, column_coord = skimage.draw.polygon(polygon["all_points_y"], polygon["all_points_x"])
            mask[row_coord, column_coord, index] = 1
            class_ids[index] = class_id_map[polygon["type"]]

        return mask.astype(np.bool), class_ids

    def image_reference(self, image_id):
        image_info = self.image_info[image_id]
        if image_info["source"] != "custom-food":
            return super().load_mask(image_id)
        else:
            return image_info["path"]