from enum import Enum
from models import Gender, ActivityLevel, Goal

class ActivityMultiplier(Enum):
    sedentary = 1.2
    light = 1.375
    moderate = 1.55
    active = 1.725
    very_active = 1.9

class GoalAdjustment(Enum):
    weight_loss = -500
    maintenance = 0
    muscle_gain = 500

def calculate_bmr(weight_kg: float, height_cm: int, age: int, gender: Gender) -> float:
    if gender == Gender.MALE:
        return 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)

def calculate_tdee(bmr: float, activity_level: ActivityLevel) -> float:
    return bmr * ActivityMultiplier[activity_level.value].value

def get_daily_calories(bmr: float, activity_level: ActivityLevel, goal: Goal) -> int:
    tdee = calculate_tdee(bmr, activity_level)
    adjustment = GoalAdjustment[goal.value].value
    return int(max(1200, tdee + adjustment))