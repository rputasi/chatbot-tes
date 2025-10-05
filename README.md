# 🤖 Simple Health Assistant for People 30+

A user-friendly Streamlit chatbot application that provides direct health and wellness advice for individuals aged 30 and above.

## ✨ Features

### 🌱 **Health & Wellness Assistant**
- **Specialized for People 30+**: Tailored advice for mature adults.
- **Direct AI Advice**: Utilizes Google Gemini for concise, actionable health guidance.
- **Personalized Context**: Considers user's age, gender, activity level, and health goals for relevant responses.

### 🎨 **Enhanced UI/UX**
- **Clean, Focused Design**: A single chat interface for ease of use.
- **Health-Themed Styling**: Green color scheme for a calming and informative experience.
- **Responsive Layout**: Optimized for clear communication on various devices.

### 📁 **Chat History Export**
- **Downloadable Chat Logs**: Export your conversation history for future reference.

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.9+ installed. It is recommended to use `miniconda` or `conda` for environment management.

### Installation

1. **Install Miniconda (if not already installed)**

   Download and install Miniconda from the official website: [Miniconda Installer](https://docs.conda.io/en/latest/miniconda.html)

2. **Create a Conda Environment**

   Open your terminal or Anaconda Prompt and create a new environment:

   ```bash
   conda create -n chatbot-env python=3.9
   conda activate chatbot-env
   ```

3. **Install Requirements**

   Navigate to the project directory and install the necessary packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Get Google AI API Key**

   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key for use in the application

5. **Run the Application**

   ```bash
   # Run the simple health chatbot (recommended)
   python run_health_chatbot.py
   
   # Or directly using Streamlit
   streamlit run streamlit_health_chatbot.py
   
   # You can still run the more complex chatbots if desired:
   # streamlit run streamlit_comprehensive_chatbot.py  # Comprehensive AI Chatbot
   # streamlit run streamlit_react_tools_app.py        # SQL Assistant
   # streamlit run streamlit_react_app.py              # Basic LangGraph
   # streamlit run streamlit_chat_app.py               # Direct Gemini (older version)
   ```

   The application will open in your web browser at `http://localhost:8501`.

## 📖 Usage Guide

### 🌱 **Simple Health Assistant Usage**

#### 1. **Setup Your Profile**
- Enter your Google AI API key in the sidebar.
- Set your age (30+), gender, activity level, and health goals.
- These inputs provide context for the AI's advice.

#### 2. **Start Chatting**
- Ask questions about nutrition, exercise, sleep, or general wellness.
- The AI will provide direct and concise advice, tailored for people 30 and older.

#### 3. **Reset Conversation**
- Use the 'Reset Conversation' button in the sidebar to clear chat history and start fresh.

#### 4. **Export Chat History**
- Click 'Export Chat History' to download your conversation as a JSON file.

## 🏗️ Project Structure

```
chatbot-tes/
├── streamlit_health_chatbot.py         # 🌱 Simple Health Assistant (Main App)
├── run_health_chatbot.py               # Launcher script for Simple Health Assistant
├── health_database_tools.py            # (Optional) Database utilities for health data
├── streamlit_comprehensive_chatbot.py  # (Previous) Comprehensive AI Chatbot
├── streamlit_react_tools_app.py        # (Previous) SQL Assistant with LangGraph
├── streamlit_react_app.py              # (Previous) Basic LangGraph chatbot
├── streamlit_chat_app.py               # (Previous) Direct Gemini integration
├── streamlit_app_basic.py              # (Previous) Streamlit tutorial
├── database_tools.py                   # (Previous) Sales database utilities
├── requirements.txt                    # Python dependencies
├── Dockerfile                          # Docker configuration
└── README.md                          # This file
```

## 🔧 Configuration

### Model Parameters
- **Temperature**: Controls randomness (0.0-1.0). Lower values for more deterministic responses.

### User Profile
- **Age**: Input your age (30-80) for age-specific advice.
- **Gender**: Select your gender for tailored recommendations.
- **Activity Level**: Choose your activity level to get appropriate exercise advice.
- **Health Goals**: Select your primary health goals to guide the AI's focus.

## 🐳 Docker Support

### Build and Run with Docker

1. **Build the Docker Image**

   ```bash
   docker build -t simple-health-chatbot .
   ```

2. **Run the Docker Container**

   ```bash
   docker run -p 8501:8501 simple-health-chatbot
   ```

   The application will be accessible at `http://localhost:8501`.

## 🛠️ Development

### Customization

- **AI Model**: The chatbot currently uses a direct Google Gemini model. For more advanced features or tools, you can uncomment and adapt the `LangGraph ReAct Agent` or `Nutrition & Fitness Coach` sections in `streamlit_health_chatbot.py`, and re-introduce the `health_database_tools.py` functionality.
- **UI Styling**: Modify the CSS in the `st.markdown()` sections within `streamlit_health_chatbot.py` to change the visual theme.
- **Prompt Engineering**: Adjust the system instruction for the Gemini model in `streamlit_health_chatbot.py` to fine-tune its advice.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the existing issues
2. Create a new issue with detailed description
3. Include error messages and steps to reproduce

## 🔄 Updates

### Version 2.1 (Current)
- **Simplified Health Assistant**: User-friendly chatbot for people 30+.
- Removed complex features like advanced analytics and database explorer tabs.
- Streamlined AI to direct Google Gemini for concise advice.
- Enhanced UI/UX for a single-chat experience.

### Version 2.0
- Comprehensive chatbot with multiple models.
- Enhanced UI/UX with modern design.
- Added file processing capabilities.
- Integrated data visualization.
- Added analytics dashboard.

### Version 1.0
- Basic chatbot implementations.
- Database integration.
- LangGraph support.
