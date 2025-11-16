# meals.py
from typing import List, Dict
import google.generativeai as genai
from models import Meal, UserProfile

# --- Gemini setup -------------------------------------------------
GEMINI_API_KEY = "AIzaSyDcnFt7Ad5fivHtK-kG3oNbsU-mPNrb9uE"
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

# --- Fallback static meals ----------------------------------------
FALLBACK_MEALS_DB: Dict[str, List[Meal]] = {
    "breakfast": [
        Meal(name="Oatmeal with Berries", calories=350, carbs_g=60, protein_g=10, fat_g=5, category="breakfast"),
        Meal(name="Greek Yogurt Parfait", calories=300, carbs_g=30, protein_g=20, fat_g=10, category="breakfast"),
    ],
    "lunch": [
        Meal(name="Grilled Chicken Salad", calories=450, carbs_g=20, protein_g=40, fat_g=15, category="lunch"),
        Meal(name="Veggie Stir-Fry with Tofu", calories=400, carbs_g=50, protein_g=25, fat_g=12, category="lunch"),
    ],
    "dinner": [
        Meal(name="Baked Salmon with Quinoa", calories=500, carbs_g=40, protein_g=35, fat_g=20, category="dinner"),
        Meal(name="Lentil Soup with Bread", calories=450, carbs_g=60, protein_g=20, fat_g=8, category="dinner"),
    ],
    "snack": [
        Meal(name="Apple with Almond Butter", calories=200, carbs_g=25, protein_g=5, fat_g=10, category="snack"),
        Meal(name="Protein Shake", calories=250, carbs_g=10, protein_g=30, fat_g=5, category="snack"),
    ]
}

def _filter(meals: List[Meal], profile: UserProfile) -> List[Meal]:
    allergies = {a.lower() for a in profile.allergies}
    return [m for m in meals if not any(a in m.name.lower() for a in allergies)]

def _ai_meal(category: str, target_cal: int, profile: UserProfile) -> Meal:
    try:
        goal_desc = {
            "weight_loss": "low-calorie, high-protein",
            "maintenance": "balanced",
            "muscle_gain": "high-protein, carb-rich"
        }[profile.goal.value]

        prompt = f"""
        Create ONE {category} meal for a {profile.goal.value} diet.
        Target calories: {target_cal}.
        Focus: {goal_desc}.
        Avoid allergies: {', '.join(profile.allergies) or 'none'}.
        Preferences: {', '.join(profile.preferences) or 'none'}.
        Return exactly: "Meal Name — X cal, Cg carbs, Pg protein, Fg fat"
        Example: "Quinoa Buddha Bowl — 420 cal, 55g carbs, 25g protein, 12g fat"
        """

        resp = gemini_model.generate_content(prompt)
        line = resp.text.strip()

        name, rest = line.split(" — ")
        cal_str, carb_str, prot_str, fat_str = [p.split()[0] for p in rest.split(", ")]
        return Meal(
            name=name,
            calories=int(cal_str),
            carbs_g=int(carb_str.rstrip("g")),
            protein_g=int(prot_str.rstrip("g")),
            fat_g=int(fat_str.rstrip("g")),
            category=category
        )
    except Exception:
        pool = _filter(FALLBACK_MEALS_DB[category], profile)
        fallback = pool[0] if pool else Meal(
            name=f"{category.title()} (default)",
            calories=target_cal,
            carbs_g=30, protein_g=20, fat_g=10,
            category=category
        )
        return fallback

def generate_daily_plan(calorie_target: int, profile: UserProfile, use_ai: bool = False) -> List[Meal]:
    selected = []
    per_meal = calorie_target // 4
    for cat in ("breakfast", "lunch", "dinner", "snack"):
        if use_ai:
            meal = _ai_meal(cat, per_meal, profile)  # ← FIXED
        else:
            pool = _filter(FALLBACK_MEALS_DB[cat], profile)
            meal = pool[0] if pool else Meal(
                name=f"{cat.title()} (default)",
                calories=per_meal,
                carbs_g=30, protein_g=20, fat_g=10,
                category=cat
            )
        selected.append(meal)
    return selected