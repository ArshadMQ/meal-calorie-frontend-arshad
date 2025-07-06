# 🍽️ Calories Backend (FastAPI)

This is the backend service for the Meal Calorie Count Generator, built using **FastAPI**. It exposes APIs for user inputs, fetches nutritional info from the USDA API, and performs calorie calculations.

---

## 🚀 Tech Stack

- 🐍 Python 3.10+
- ⚡ FastAPI
- 🧪 Uvicorn + Gunicorn
- 📦 SQLite / PostgreSQL
- 🔐 Pydantic for validation
- 🧾 USDA FoodData Central API

---

## 🔧 Local Development

### 1. Clone and Setup Environment

```bash

git clone https://github.com/ArshadMQ/calories-app.git
cd calories-app/calories-be
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```