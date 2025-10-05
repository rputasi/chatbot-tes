# Health & Wellness Chatbot for People 30+
# Simple Streamlit chatbot focused on direct health advice

import streamlit as st
import os
from datetime import datetime
import json
from typing import Dict, List, Any, Optional


import google.genai as genai_core # Use an alias for the module


# Page Configuration
st.set_page_config(
    page_title="🌱 Simple Health Assistant",
    page_icon="🌱",
    layout="centered", # Simplified layout
    initial_sidebar_state="expanded"
)

# Custom CSS for health-focused styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .health-card {
        background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
    }
    .assistant-message {
        background-color: #E8F5E8;
        border-left: 4px solid #4CAF50;
    }
    /* Removed tab specific CSS as tabs are removed */
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<h1 class="main-header">🌱 Simple Health Assistant</h1>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <p style="font-size: 1.2rem; color: #666;">
        Your personal health companion for people 30+ - Get direct advice on nutrition, exercise, sleep, and wellness.
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
  
    model_type = "Google Gemini Direct" # Force direct Gemini for simplicity
    
    # API Key Input
    google_api_key = st.text_input(
        "Google AI API Key", 
        type="password",
        help="Enter your Google AI API key to use the chatbot"
    )
    
    # User Profile - Comprehensive health context
    st.subheader("👤 Your Health Profile")
    
    # Basic Demographics
    user_age = st.slider("Age", 30, 80, 35, 1)
    user_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    # Physical Measurements
    st.markdown("**📏 Physical Measurements**")
    col1, col2 = st.columns(2)
    with col1:
        user_height_cm = st.number_input("Height (cm)", 120, 220, 170, 1)
    with col2:
        user_height_ft = st.number_input("Height (ft)", 4.0, 7.5, 5.6, 0.1)
    
    col1, col2 = st.columns(2)
    with col1:
        user_weight_kg = st.number_input("Weight (kg)", 30, 200, 70, 1)
    with col2:
        user_weight_lbs = st.number_input("Weight (lbs)", 66, 440, 154, 1)
    
    # Health Metrics
    st.markdown("**💊 Health Metrics**")
    user_bmi = round(user_weight_kg / ((user_height_cm/100) ** 2), 1) if user_height_cm > 0 else 0
    st.metric("BMI", f"{user_bmi}", help="Body Mass Index")
    
    col1, col2 = st.columns(2)
    with col1:
        user_blood_pressure_sys = st.number_input("Systolic BP", 80, 200, 120, 1)
    with col2:
        user_blood_pressure_dia = st.number_input("Diastolic BP", 50, 120, 80, 1)
    
    user_resting_hr = st.number_input("Resting Heart Rate (bpm)", 40, 120, 70, 1)
    user_sleep_hours = st.slider("Average Sleep (hours)", 3.0, 12.0, 7.5, 0.5)
    
    # Lifestyle & Activity
    st.markdown("**🏃 Lifestyle & Activity**")
    user_activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    user_exercise_freq = st.selectbox("Exercise Frequency", ["None", "1-2 times/week", "3-4 times/week", "5-6 times/week", "Daily"])
    user_diet_type = st.selectbox("Diet Type", ["No specific diet", "Mediterranean", "Keto", "Vegetarian", "Vegan", "Paleo", "Low-carb", "Other"])
    
    # Health History & Conditions
    st.markdown("**🏥 Health History**")
    user_conditions = st.multiselect("Current Health Conditions", [
        "None", "Diabetes", "Hypertension", "Heart Disease", "Arthritis", 
        "Osteoporosis", "Depression/Anxiety", "Sleep Apnea", "High Cholesterol",
        "Thyroid Issues", "Digestive Issues", "Allergies", "Other"
    ])
    
    user_medications = st.text_area("Current Medications", placeholder="List any medications you're currently taking...", height=60)
    user_surgeries = st.text_area("Recent Surgeries/Procedures", placeholder="Any surgeries or medical procedures in the last 2 years...", height=60)
    
    # Health Goals & Concerns
    st.markdown("**🎯 Health Goals & Concerns**")
    user_goals = st.multiselect("Primary Health Goals", [
        "Weight Management", "Muscle Building", "Cardiovascular Health", 
        "Stress Reduction", "Better Sleep", "Energy Boost", "Joint Health",
        "Blood Pressure Control", "Blood Sugar Control", "Cholesterol Management",
        "Mental Health", "Digestive Health", "Immune System", "Bone Health"
    ])
    
    user_concerns = st.text_area("Specific Health Concerns", placeholder="Any specific health issues or questions you'd like to focus on...", height=60)
    
    # Family History
    st.markdown("**👨‍👩‍👧‍👦 Family History**")
    family_history = st.multiselect("Family Health History", [
        "None", "Heart Disease", "Diabetes", "Cancer", "High Blood Pressure",
        "Stroke", "Alzheimer's/Dementia", "Depression", "Osteoporosis",
        "Thyroid Disease", "Autoimmune Disorders", "Other"
    ])
    
    # Model Parameters
    with st.expander("🎛️ Model Parameters"):
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
        # max_tokens = st.slider("Max Tokens", 100, 2000, 1000, 50) # Removed for simpler model
    
    
    
    # Reset Controls
    st.subheader("🔄 Controls")
    if st.button("Reset Conversation", help="Clear all messages and start fresh"):
        for key in list(st.session_state.keys()):
            if key not in ['_last_key']:
                del st.session_state[key]
        st.rerun()
    
    # Export Health Data
    if st.button("Export Chat History"):
        if "messages" in st.session_state and st.session_state.messages:
            health_data = {
                "timestamp": datetime.now().isoformat(),
                "model_type": model_type,
                "user_profile": {
                    "demographics": {
                        "age": user_age,
                        "gender": user_gender
                    },
                    "physical_measurements": {
                        "height_cm": user_height_cm,
                        "height_ft": user_height_ft,
                        "weight_kg": user_weight_kg,
                        "weight_lbs": user_weight_lbs,
                        "bmi": user_bmi
                    },
                    "vital_signs": {
                        "blood_pressure_systolic": user_blood_pressure_sys,
                        "blood_pressure_diastolic": user_blood_pressure_dia,
                        "resting_heart_rate": user_resting_hr,
                        "sleep_hours": user_sleep_hours
                    },
                    "lifestyle": {
                        "activity_level": user_activity,
                        "exercise_frequency": user_exercise_freq,
                        "diet_type": user_diet_type
                    },
                    "health_history": {
                        "conditions": user_conditions,
                        "medications": user_medications,
                        "surgeries": user_surgeries,
                        "family_history": family_history
                    },
                    "goals_and_concerns": {
                        "health_goals": user_goals,
                        "specific_concerns": user_concerns
                    }
                },
                "messages": st.session_state.messages
            }
            json_str = json.dumps(health_data, indent=2)
            st.download_button(
                label="Download Chat History",
                data=json_str,
                file_name=f"health_chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# Main Content Area
if not google_api_key:
    st.info("🔑 Please add your Google AI API key in the sidebar to start your health journey.", icon="🗝️")
    st.stop()


# Initialize models based on selection
if "genai_client" not in st.session_state or getattr(st.session_state, "_last_key", None) != google_api_key:
    try:
        # Initialize the Google GenAI client
        st.session_state.genai_client = genai_core.Client(api_key=google_api_key)
        
        st.session_state.current_model = model_type
        st.session_state._last_key = google_api_key
        st.session_state.pop("messages", None)
        st.session_state.pop("chat_session", None) # Clear chat session if API key changes
        
    except Exception as e:
        st.error(f"❌ Error initializing model: {e}")
        st.stop()

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Only show the chat interface
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Ask about nutrition, exercise, sleep, or wellness for people 30+...")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    try:
        with st.spinner("🌱 Getting health advice..."):
            if "chat_session" not in st.session_state:
                # Initialize chat session with system instruction
                # Create comprehensive health profile for context
                health_conditions = ', '.join(user_conditions) if user_conditions and 'None' not in user_conditions else 'None'
                family_conditions = ', '.join(family_history) if family_history and 'None' not in family_history else 'None'
                
                system_instruction = f"""You are a helpful health and wellness assistant, specialized in giving advice to people 30 and older.

USER HEALTH PROFILE:
- Demographics: {user_age} years old, {user_gender}
- Physical: Height {user_height_cm}cm ({user_height_ft}ft), Weight {user_weight_kg}kg ({user_weight_lbs}lbs), BMI {user_bmi}
- Vital Signs: Blood Pressure {user_blood_pressure_sys}/{user_blood_pressure_dia}, Resting HR {user_resting_hr} bpm
- Sleep: {user_sleep_hours} hours average per night
- Activity: {user_activity} level, Exercise {user_exercise_freq}
- Diet: {user_diet_type}
- Health Conditions: {health_conditions}
- Medications: {user_medications if user_medications else 'None reported'}
- Recent Surgeries: {user_surgeries if user_surgeries else 'None reported'}
- Health Goals: {', '.join(user_goals) if user_goals else 'General wellness'}
- Specific Concerns: {user_concerns if user_concerns else 'None specified'}
- Family History: {family_conditions}

Provide personalized, evidence-based health advice considering this comprehensive profile. Always recommend consulting healthcare professionals for medical concerns."""
                
                # Create a chat session using the google.genai API
                st.session_state.chat_session = st.session_state.genai_client.chats.create(
                    model="gemini-2.5-flash",
                    config=genai_core.types.GenerateContentConfig(
                        temperature=temperature,
                        system_instruction=system_instruction
                    )
                )

                # Send the first message
                response = st.session_state.chat_session.send_message(prompt)
            else:
                # Send subsequent messages
                response = st.session_state.chat_session.send_message(prompt)
            
            # Extract the response text
            if hasattr(response, 'candidates') and response.candidates:
                answer = response.candidates[0].content.parts[0].text
            else:
                answer = str(response)
        
    except Exception as e:
        answer = f"❌ An error occurred: {e}"
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(answer)
    
    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🌱 Simple Health Assistant - Your direct source for health advice for people 30+</p>
    <p>Built with Streamlit and Google Gemini | Focused on concise, actionable wellness guidance</p>
</div>
""", unsafe_allow_html=True)
