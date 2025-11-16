Here's a sample `README.md` that you can use for your Git repository:

````markdown
# Personalized Diet Planner

A personalized diet planner API that generates a custom weekly diet plan based on user input. The app calculates the user's Basal Metabolic Rate (BMR), Total Daily Energy Expenditure (TDEE), and recommends daily caloric intake according to the user's goal (weight loss, maintenance, or muscle gain). 

This project uses **FastAPI** for the backend API and **Pydantic** models for input validation.

## Features

- **User Profile Input**: Allows users to input their age, gender, weight, height, activity level, and dietary goals.
- **Caloric Calculation**: Calculates BMR, TDEE, and daily caloric intake tailored to the user's profile.
- **Meal Plan Generation**: Generates a daily meal plan with macronutrient breakdown (carbs, protein, fat) based on the user's caloric target.
- **Weekly Plan**: Generates a full weekly meal plan with daily meal breakdowns.
- **Fallback and AI Meal Generation**: Option to generate meals using AI or fallback to a predefined meals database.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn (for running the FastAPI server)
- Pydantic
- Other dependencies (listed in `requirements.txt`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Turjoy01/Personalized-Diet-Planner.git
   cd Personalized-Diet-Planner
````

2. Create a virtual environment and activate it:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

2. Access the API at `http://127.0.0.1:8000`.

3. Make POST requests to `/profile` with a user profile in the following format:

   ```json
   {
     "name": "John Doe",
     "age": 30,
     "gender": "male",
     "country": "USA",
     "weight_kg": 75,
     "height_cm": 175,
     "activity_level": "moderate",
     "goal": "weight_loss",
     "allergies": ["nuts"],
     "preferences": ["vegetarian"]
   }
   ```

   The response will include the BMR, TDEE, daily target calories, and a breakdown of macronutrients (carbs, protein, fat).

## Folder Structure

```
diet-planner/
├── .venv/               # Virtual environment
├── calculator.py        # Logic for BMR, TDEE, and daily caloric calculations
├── main.py              # FastAPI app and API endpoints
├── meals.py             # Meal generation logic
├── models.py            # Pydantic models for input validation
├── requirements.txt     # List of dependencies
└── __pycache__/         # Compiled Python files
```

## Development

1. Fork the repository and create a feature branch.
2. Implement your changes and make sure to write tests.
3. Submit a pull request for review.

## License

This project is licensed under the MIT License.
