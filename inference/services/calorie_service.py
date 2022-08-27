from typing import Dict


class CalorieService:
    def __init__(self):
        self.calories_per_sq_centimeter: Dict = {
            "potatoes": 1.4778,
            "pasta": 3.5398,
            "pizza": 6.2477,
            "fruit": 0.7453,
            "beef": 4.4247,
            "bread": 2.6856,
            "pie": 6.9863,
            "vegetable": 0.7256,
            "fish": 0.4745,
            "chicken": 2.5736,
            "salad": 0.2567,
            "soup": 3.8753,
            "rice": 3.5398,
            "pork": 5.6383,
            "packaged": 6.9773,
            "cake": 10.9464,
            "cheese": 5.9763
        }

        self.protein_per_sq_centimeter: Dict = {
            "potatoes": 0.4567,
            "pasta": 0.5398,
            "pizza": 1.2477,
            "fruit": 0.7453,
            "beef": 7.4247,
            "bread": 2.6856,
            "pie": 6.9863,
            "vegetable": 0.7256,
            "fish": 0.4745,
            "chicken": 9.5736,
            "salad": 0.2567,
            "soup": 5.8753,
            "rice": 0.5398,
            "pork": 1.6383,
            "packaged": 0.9773,
            "cake": 0.9464,
            "cheese": 3.9763
        }

        self.fat_per_sq_centimeter: Dict = {
            "potatoes": 0.4567,
            "pasta": 0.5398,
            "pizza": 6.2477,
            "fruit": 0.7453,
            "beef": 4.4247,
            "bread": 1.6856,
            "pie": 8.9863,
            "vegetable": 0.7256,
            "fish": 0.4745,
            "chicken": 2.5736,
            "salad": 0.2567,
            "soup": 1.8753,
            "rice": 0.5398,
            "pork": 8.6383,
            "packaged": 4.9773,
            "cake": 4.9464,
            "cheese": 6.9763
        }

        self.carbohydrates_per_sq_centimeter: Dict = {
            "potatoes": 8.4567,
            "pasta": 7.5398,
            "pizza": 2.2477,
            "fruit": 0.7453,
            "beef": 2.4247,
            "bread": 8.6856,
            "pie": 5.9863,
            "vegetable": 0.7256,
            "fish": 0.4745,
            "chicken": 4.5736,
            "salad": 0.2567,
            "soup": 3.8753,
            "rice": 8.5398,
            "pork": 4.6383,
            "packaged": 2.9773,
            "cake": 2.9464,
            "cheese": 2.9763
        }

        self.calories_per_unit: Dict = {
            "yogurt": 102,
            "pudding": 130
        }

        self.protein_per_unit: Dict = {
            "yogurt": 50,
            "pudding": 20
        }

        self.fat_per_unit: Dict = {
            "yogurt": 20,
            "pudding": 50
        }

        self.carbohydrates_per_unit: Dict = {
            "yogurt": 10,
            "pudding": 15
        }

        def get_calories_per_category(category: str, food_area: float) -> float:
            if category in self.calories_per_unit:
                return self.calories_per_unit[category]
            else:
                return self.calories_per_sq_centimeter[category] * food_area

        def get_protein_per_category(category: str, food_area: float) -> float:
            if category in self.protein_per_unit:
                return self.protein_per_unit[category]
            else:
                return self.protein_per_sq_centimeter[category] * food_area

        def get_fat_per_category(category: str, food_area: float) -> float:
            if category in self.fat_per_unit:
                return self.fat_per_unit[category]
            else:
                return self.fat_per_sq_centimeter[category] * food_area

        def get_carbohydrates_per_category(category: str, food_area: float) -> float:
            if category in self.carbohydrates_per_unit:
                return self.carbohydrates_per_unit[category]
            else:
                return self.carbohydrates_per_sq_centimeter[category] * food_area
