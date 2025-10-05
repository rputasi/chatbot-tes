# health_database_tools.py
import sqlite3
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

# Database file path
DB_PATH = "health_wellness.db"

def init_database():
    """
    Initialize the database with health and wellness tables for people 30+
    """
    # Create the database file if it doesn't exist
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT,
        height_cm REAL,
        weight_kg REAL,
        activity_level TEXT,
        health_goals TEXT,
        created_date TEXT NOT NULL
    )
    """)
    
    # Create nutrition_log table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nutrition_log (
        log_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        date TEXT NOT NULL,
        meal_type TEXT NOT NULL,
        food_name TEXT NOT NULL,
        calories INTEGER,
        protein_g REAL,
        carbs_g REAL,
        fat_g REAL,
        fiber_g REAL,
        sugar_g REAL,
        sodium_mg REAL,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    """)
    
    # Create exercise_log table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercise_log (
        exercise_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        date TEXT NOT NULL,
        exercise_type TEXT NOT NULL,
        duration_minutes INTEGER,
        calories_burned INTEGER,
        intensity_level TEXT,
        notes TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    """)
    
    # Create health_metrics table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_metrics (
        metric_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        date TEXT NOT NULL,
        weight_kg REAL,
        body_fat_percentage REAL,
        blood_pressure_systolic INTEGER,
        blood_pressure_diastolic INTEGER,
        resting_heart_rate INTEGER,
        sleep_hours REAL,
        stress_level INTEGER,
        energy_level INTEGER,
        mood_score INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    """)
    
    # Create wellness_tips table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wellness_tips (
        tip_id INTEGER PRIMARY KEY,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        age_group TEXT,
        difficulty_level TEXT,
        time_required TEXT
    )
    """)
    
    # Create health_articles table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_articles (
        article_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        content TEXT NOT NULL,
        author TEXT,
        publish_date TEXT,
        read_time_minutes INTEGER,
        tags TEXT
    )
    """)
    
    # Insert sample data only if tables are empty
    if cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        # Insert sample users (30+ years old)
        cursor.executemany(
            "INSERT INTO users (name, age, gender, height_cm, weight_kg, activity_level, health_goals, created_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ("Sarah Johnson", 35, "Female", 165.0, 68.0, "Moderately Active", "Weight Management, Energy Boost", "2024-01-15"),
                ("Michael Chen", 42, "Male", 178.0, 85.0, "Very Active", "Muscle Building, Cardiovascular Health", "2024-01-20"),
                ("Emily Rodriguez", 38, "Female", 160.0, 62.0, "Lightly Active", "Stress Reduction, Better Sleep", "2024-02-01"),
                ("David Thompson", 45, "Male", 182.0, 90.0, "Moderately Active", "Weight Loss, Joint Health", "2024-02-10"),
                ("Lisa Wang", 33, "Female", 158.0, 58.0, "Very Active", "Fitness, Mental Health", "2024-02-15")
            ]
        )
        
        # Insert sample nutrition logs
        nutrition_data = []
        for user_id in range(1, 6):
            for day in range(30):  # 30 days of data
                date = (datetime.now() - timedelta(days=day)).strftime("%Y-%m-%d")
                # Breakfast
                nutrition_data.append((user_id, date, "Breakfast", "Oatmeal with berries", 350, 12.0, 65.0, 8.0, 10.0, 15.0, 200))
                nutrition_data.append((user_id, date, "Breakfast", "Greek yogurt", 150, 15.0, 8.0, 2.0, 0.0, 6.0, 50))
                # Lunch
                nutrition_data.append((user_id, date, "Lunch", "Grilled chicken salad", 400, 35.0, 20.0, 15.0, 8.0, 5.0, 300))
                # Dinner
                nutrition_data.append((user_id, date, "Dinner", "Salmon with vegetables", 450, 40.0, 15.0, 25.0, 6.0, 8.0, 400))
                # Snacks
                if random.random() > 0.5:
                    nutrition_data.append((user_id, date, "Snack", "Mixed nuts", 200, 6.0, 8.0, 18.0, 3.0, 2.0, 100))
        
        cursor.executemany(
            "INSERT INTO nutrition_log (user_id, date, meal_type, food_name, calories, protein_g, carbs_g, fat_g, fiber_g, sugar_g, sodium_mg) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            nutrition_data
        )
        
        # Insert sample exercise logs
        exercise_data = []
        exercise_types = ["Running", "Weight Training", "Yoga", "Swimming", "Cycling", "Walking", "HIIT", "Pilates"]
        intensity_levels = ["Low", "Moderate", "High"]
        
        for user_id in range(1, 6):
            for day in range(30):
                date = (datetime.now() - timedelta(days=day)).strftime("%Y-%m-%d")
                if random.random() > 0.3:  # 70% chance of exercise
                    exercise_type = random.choice(exercise_types)
                    duration = random.randint(20, 90)
                    calories = random.randint(150, 600)
                    intensity = random.choice(intensity_levels)
                    exercise_data.append((user_id, date, exercise_type, duration, calories, intensity, f"Good {exercise_type.lower()} session"))
        
        cursor.executemany(
            "INSERT INTO exercise_log (user_id, date, exercise_type, duration_minutes, calories_burned, intensity_level, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
            exercise_data
        )
        
        # Insert sample health metrics
        metrics_data = []
        for user_id in range(1, 6):
            base_weight = 70.0 if user_id % 2 == 0 else 80.0
            for day in range(30):
                date = (datetime.now() - timedelta(days=day)).strftime("%Y-%m-%d")
                weight = base_weight + random.uniform(-2, 2)
                body_fat = random.uniform(15, 25)
                bp_systolic = random.randint(110, 140)
                bp_diastolic = random.randint(70, 90)
                heart_rate = random.randint(55, 75)
                sleep = random.uniform(6.5, 8.5)
                stress = random.randint(1, 10)
                energy = random.randint(3, 10)
                mood = random.randint(4, 10)
                
                metrics_data.append((user_id, date, weight, body_fat, bp_systolic, bp_diastolic, heart_rate, sleep, stress, energy, mood))
        
        cursor.executemany(
            "INSERT INTO health_metrics (user_id, date, weight_kg, body_fat_percentage, blood_pressure_systolic, blood_pressure_diastolic, resting_heart_rate, sleep_hours, stress_level, energy_level, mood_score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            metrics_data
        )
        
        # Insert wellness tips
        wellness_tips = [
            ("Nutrition", "Hydration for 30+", "Drink at least 8 glasses of water daily. As we age, our thirst sensation decreases, so set reminders to stay hydrated.", "30+", "Easy", "5 minutes"),
            ("Exercise", "Strength Training Benefits", "Include resistance training 2-3 times per week to maintain muscle mass and bone density, which naturally decline after 30.", "30+", "Moderate", "45 minutes"),
            ("Sleep", "Quality Sleep Routine", "Maintain a consistent sleep schedule. Adults 30+ need 7-9 hours of quality sleep for optimal health and recovery.", "30+", "Easy", "30 minutes"),
            ("Stress Management", "Mindfulness Practice", "Practice 10 minutes of daily meditation or deep breathing to reduce stress and improve mental clarity.", "30+", "Easy", "10 minutes"),
            ("Nutrition", "Anti-Inflammatory Foods", "Include omega-3 rich foods like salmon, walnuts, and flaxseeds to combat age-related inflammation.", "30+", "Easy", "15 minutes"),
            ("Exercise", "Cardiovascular Health", "Aim for 150 minutes of moderate cardio weekly to maintain heart health and reduce disease risk.", "30+", "Moderate", "30 minutes"),
            ("Mental Health", "Social Connections", "Maintain strong social relationships as they're crucial for mental health and longevity in your 30s and beyond.", "30+", "Easy", "60 minutes"),
            ("Nutrition", "Protein Intake", "Consume 1.2-1.6g protein per kg body weight to support muscle maintenance and recovery.", "30+", "Moderate", "20 minutes"),
            ("Exercise", "Flexibility & Mobility", "Include stretching or yoga 2-3 times weekly to maintain flexibility and prevent injury.", "30+", "Easy", "20 minutes"),
            ("Sleep", "Sleep Environment", "Keep your bedroom cool (65-68°F), dark, and quiet for optimal sleep quality.", "30+", "Easy", "5 minutes")
        ]
        
        cursor.executemany(
            "INSERT INTO wellness_tips (category, title, content, age_group, difficulty_level, time_required) VALUES (?, ?, ?, ?, ?, ?)",
            wellness_tips
        )
        
        # Insert health articles
        health_articles = [
            ("The 30+ Fitness Guide", "Exercise", "Comprehensive guide to staying fit and healthy in your 30s and beyond, including workout routines and recovery strategies.", "Dr. Sarah Miller", "2024-01-15", 8, "fitness,30s,workout"),
            ("Nutrition for Mature Adults", "Nutrition", "Essential nutrition guidelines for people 30+ focusing on metabolism changes and nutrient needs.", "Dr. Michael Chen", "2024-01-20", 10, "nutrition,metabolism,health"),
            ("Sleep Optimization After 30", "Sleep", "How to improve sleep quality and duration as you age, including common sleep issues and solutions.", "Dr. Emily Davis", "2024-02-01", 6, "sleep,aging,recovery"),
            ("Stress Management Techniques", "Mental Health", "Effective stress management strategies for busy professionals in their 30s and 40s.", "Dr. Lisa Johnson", "2024-02-10", 7, "stress,mental-health,wellness"),
            ("Hormonal Changes in Your 30s", "Health", "Understanding hormonal changes that occur in your 30s and how to manage them naturally.", "Dr. Robert Smith", "2024-02-15", 9, "hormones,aging,health")
        ]
        
        cursor.executemany(
            "INSERT INTO health_articles (title, category, content, author, publish_date, read_time_minutes, tags) VALUES (?, ?, ?, ?, ?, ?, ?)",
            health_articles
        )
    
    conn.commit()
    conn.close()
    
    return "Health and wellness database initialized with empty tables."

def execute_sql_query(query: str) -> List[Dict[str, Any]]:
    """
    Execute an SQL query and return the results as a list of dictionaries
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query)
        
        if query.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            result = [{k: row[k] for k in row.keys()} for row in rows]
        else:
            result = [{"affected_rows": cursor.rowcount}]
            conn.commit()
            
        conn.close()
        return result
    
    except sqlite3.Error as e:
        return [{"error": str(e)}]

def get_table_schema() -> Dict[str, List[Dict[str, str]]]:
    """
    Get the schema of all tables in the database
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        schema = {}
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            schema[table_name] = [
                {
                    "name": col[1],
                    "type": col[2],
                    "notnull": bool(col[3]),
                    "pk": bool(col[5])
                }
                for col in columns
            ]
        
        conn.close()
        return schema
    
    except sqlite3.Error as e:
        return {"error": str(e)}

def text_to_sql(sql_query: str) -> Dict[str, Any]:
    """
    Execute a SQL query against the health database
    
    Args:
        sql_query: The SQL query to execute
        
    Returns:
        Dictionary with SQL query and results
    """
    if not os.path.exists(DB_PATH):
        init_database()
    
    try:
        results = execute_sql_query(sql_query)
        return {
            "query": sql_query,
            "results": results
        }
    except Exception as e:
        return {
            "query": sql_query,
            "results": [{"error": str(e)}]
        }

def get_database_info() -> Dict[str, Any]:
    """
    Get information about the database schema to help with query construction
    
    Returns:
        Dictionary with database schema and sample data
    """
    if not os.path.exists(DB_PATH):
        init_database()
    
    schema = get_table_schema()
    
    sample_data = {}
    for table_name in schema.keys():
        if isinstance(table_name, str):
            try:
                sample_data[table_name] = execute_sql_query(f"SELECT * FROM {table_name} LIMIT 3")
            except:
                pass
    
    return {
        "schema": schema,
        "sample_data": sample_data
    }

def get_health_recommendations(user_id: int = None) -> Dict[str, Any]:
    """
    Get personalized health recommendations based on user data
    """
    if not os.path.exists(DB_PATH):
        init_database()
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        recommendations = {}
        
        # Get user's latest health metrics
        if user_id:
            cursor.execute("""
                SELECT * FROM health_metrics 
                WHERE user_id = ? 
                ORDER BY date DESC 
                LIMIT 1
            """, (user_id,))
            latest_metrics = cursor.fetchone()
            
            if latest_metrics:
                recommendations["latest_metrics"] = dict(latest_metrics)
                
                # Generate recommendations based on metrics
                if latest_metrics["sleep_hours"] < 7:
                    recommendations["sleep_tip"] = "Consider improving your sleep routine. Aim for 7-9 hours nightly."
                
                if latest_metrics["stress_level"] > 7:
                    recommendations["stress_tip"] = "High stress detected. Try meditation or deep breathing exercises."
                
                if latest_metrics["energy_level"] < 6:
                    recommendations["energy_tip"] = "Low energy levels. Consider reviewing your nutrition and exercise routine."
        
        # Get wellness tips
        cursor.execute("SELECT * FROM wellness_tips WHERE age_group = '30+' ORDER BY RANDOM() LIMIT 5")
        tips = cursor.fetchall()
        recommendations["wellness_tips"] = [dict(tip) for tip in tips]
        
        conn.close()
        return recommendations
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print(init_database())
    print("Health and wellness database created with empty tables.")
