# main.py
from fastapi import FastAPI, HTTPException
from typing import List
from models import (UserProfile, WeeklyPlan, DailyPlan, Meal, ProfileResponse)
from calculator import calculate_bmr, calculate_tdee, get_daily_calories
from meals import generate_daily_plan, FALLBACK_MEALS_DB  # ← NO 'app'

app = FastAPI(title="Personalized Diet Planner", version="1.0")

@app.post("/profile", response_model=ProfileResponse)
async def profile_info(profile: UserProfile):
    bmr = calculate_bmr(profile.weight_kg, profile.height_cm, profile.age, profile.gender)
    tdee = calculate_tdee(bmr, profile.activity_level)
    daily = get_daily_calories(bmr, profile.activity_level, profile.goal)

    return {
        "bmr": round(bmr),
        "tdee": round(tdee),
        "daily_target": daily,
        "macros_g": {
            "carbs": round(daily * 0.50 / 4),
            "protein": round(daily * 0.25 / 4),
            "fat": round(daily * 0.25 / 9)
        }
    }

@app.post("/plan", response_model=WeeklyPlan)
async def weekly_plan(profile: UserProfile):
    bmr = calculate_bmr(profile.weight_kg, profile.height_cm, profile.age, profile.gender)
    daily_cal = get_daily_calories(bmr, profile.activity_level, profile.goal)
    days = []
    for day in range(1, 8):
        meals = generate_daily_plan(daily_cal, profile, use_ai=False)
        totals = {
            "total_calories": sum(m.calories for m in meals),
            "total_carbs_g": sum(m.carbs_g for m in meals),
            "total_protein_g": sum(m.protein_g for m in meals),
            "total_fat_g": sum(m.fat_g for m in meals),
        }
        days.append(DailyPlan(day=day, meals=meals, **totals))
    return WeeklyPlan(user_name=profile.name, daily_calorie_target=daily_cal, days=days)

@app.post("/plan-ai", response_model=WeeklyPlan)
async def weekly_plan_ai(profile: UserProfile):
    bmr = calculate_bmr(profile.weight_kg, profile.height_cm, profile.age, profile.gender)
    daily_cal = get_daily_calories(bmr, profile.activity_level, profile.goal)
    days = []
    for day in range(1, 8):
        meals = generate_daily_plan(daily_cal, profile, use_ai=True)
        totals = {
            "total_calories": sum(m.calories for m in meals),
            "total_carbs_g": sum(m.carbs_g for m in meals),
            "total_protein_g": sum(m.protein_g for m in meals),
            "total_fat_g": sum(m.fat_g for m in meals),
        }
        days.append(DailyPlan(day=day, meals=meals, **totals))
    return WeeklyPlan(user_name=profile.name, daily_calorie_target=daily_cal, days=days)

@app.get("/meals/{category}")
async def list_category(category: str):
    if category not in FALLBACK_MEALS_DB:
        raise HTTPException(status_code=404, detail="Category not found")
    return FALLBACK_MEALS_DB[category]