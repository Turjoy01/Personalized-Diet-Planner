from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"

class Goal(str, Enum):
    WEIGHT_LOSS = "weight_loss"
    MAINTENANCE = "maintenance"
    MUSCLE_GAIN = "muscle_gain"

class UserProfile(BaseModel):
    name: str
    age: int = Field(..., ge=18, le=100)
    gender: Gender
    country: str = Field(..., description="User's country (any string)")
    weight_kg: float = Field(..., ge=30, le=300)
    height_cm: int = Field(..., ge=100, le=250)
    activity_level: ActivityLevel
    goal: Goal
    allergies: Optional[List[str]] = []
    preferences: Optional[List[str]] = []

class Meal(BaseModel):
    name: str
    calories: int
    carbs_g: int
    protein_g: int
    fat_g: int
    category: str

class DailyPlan(BaseModel):
    day: int
    meals: List[Meal]
    total_calories: int
    total_carbs_g: int
    total_protein_g: int
    total_fat_g: int

class WeeklyPlan(BaseModel):
    user_name: str
    daily_calorie_target: int
    disclaimer: str = "Consult a healthcare professional before following any diet plan."
    days: List[DailyPlan]

class ProfileResponse(BaseModel):
    bmr: int
    tdee: int
    daily_target: int
    macros_g: dict