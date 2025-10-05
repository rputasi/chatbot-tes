# Comprehensive Streamlit Chatbot
# Combines features from all existing implementations with enhanced capabilities

import streamlit as st
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import io
from typing import Dict, List, Any, Optional

# AI Model Imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from google import genai

# Database tools
from database_tools import text_to_sql, init_database, get_database_info

# Page Configuration
st.set_page_config(
    page_title="🤖 Comprehensive AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-left: 20px;
        padding-right: 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<h1 class="main-header">🤖 Comprehensive AI Chatbot</h1>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <p style="font-size: 1.2rem; color: #666;">
        A powerful AI assistant with multiple models, database integration, file processing, and data visualization
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    # Model Selection
    st.subheader("🤖 AI Model")
    model_type = st.selectbox(
        "Choose AI Model",
        ["LangGraph ReAct Agent", "Google Gemini Direct", "SQL Assistant"],
        help="Select the AI model for your chatbot"
    )
    
    # API Key Input
    google_api_key = st.text_input(
        "Google AI API Key", 
        type="password",
        help="Enter your Google AI API key to use the chatbot"
    )
    
    # Model Parameters
    with st.expander("🎛️ Model Parameters"):
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
        max_tokens = st.slider("Max Tokens", 100, 2000, 1000, 50)
    
    # Database Controls
    st.subheader("🗄️ Database")
    if st.button("Initialize Database", help="Create and populate the database with sample data"):
        with st.spinner("Initializing database..."):
            result = init_database()
            st.success(result)
    
    # File Upload
    st.subheader("📁 File Upload")
    uploaded_file = st.file_uploader(
        "Upload a file",
        type=['txt', 'csv', 'json', 'pdf'],
        help="Upload files to analyze or process"
    )
    
    # Reset Controls
    st.subheader("🔄 Controls")
    if st.button("Reset Conversation", help="Clear all messages and start fresh"):
        for key in list(st.session_state.keys()):
            if key not in ['_last_key']:
                del st.session_state[key]
        st.rerun()
    
    # Export Chat
    if st.button("Export Chat History"):
        if "messages" in st.session_state and st.session_state.messages:
            chat_data = {
                "timestamp": datetime.now().isoformat(),
                "model_type": model_type,
                "messages": st.session_state.messages
            }
            json_str = json.dumps(chat_data, indent=2)
            st.download_button(
                label="Download Chat History",
                data=json_str,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# Main Content Area
if not google_api_key:
    st.info("🔑 Please add your Google AI API key in the sidebar to start chatting.", icon="🗝️")
    st.stop()

# Initialize AI Models
@tool
def execute_sql_tool(sql_query: str):
    """Execute a SQL query against the sales database."""
    result = text_to_sql(sql_query)
    formatted_result = f"```sql\n{sql_query}\n```\n\nQuery Results:\n{result}"
    return formatted_result

@tool
def get_schema_info_tool():
    """Get information about the database schema and sample data."""
    return get_database_info()

@tool
def analyze_uploaded_file(file_content: str, file_type: str):
    """Analyze uploaded file content."""
    try:
        if file_type == 'csv':
            df = pd.read_csv(io.StringIO(file_content))
            analysis = {
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "dtypes": df.dtypes.to_dict(),
                "head": df.head().to_dict(),
                "summary": df.describe().to_dict()
            }
        elif file_type == 'json':
            data = json.loads(file_content)
            analysis = {
                "type": type(data).__name__,
                "keys": list(data.keys()) if isinstance(data, dict) else f"List with {len(data)} items",
                "sample": str(data)[:500] + "..." if len(str(data)) > 500 else str(data)
            }
        else:
            analysis = {
                "content_length": len(file_content),
                "lines": len(file_content.split('\n')),
                "preview": file_content[:500] + "..." if len(file_content) > 500 else file_content
            }
        return f"File Analysis:\n{json.dumps(analysis, indent=2)}"
    except Exception as e:
        return f"Error analyzing file: {str(e)}"

# Initialize models based on selection
if ("current_model" not in st.session_state) or (st.session_state.current_model != model_type) or (getattr(st.session_state, "_last_key", None) != google_api_key):
    try:
        if model_type == "LangGraph ReAct Agent":
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=google_api_key,
                temperature=temperature
            )
            st.session_state.agent = create_react_agent(
                model=llm,
                tools=[analyze_uploaded_file],
                prompt="You are a helpful, friendly assistant. Respond concisely and clearly. You can analyze uploaded files and help with various tasks."
            )
        elif model_type == "Google Gemini Direct":
            st.session_state.genai_client = genai.Client(api_key=google_api_key)
        elif model_type == "SQL Assistant":
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=google_api_key,
                temperature=temperature
            )
            st.session_state.agent = create_react_agent(
                model=llm,
                tools=[get_schema_info_tool, execute_sql_tool],
                prompt="""You are a helpful assistant that can answer questions about sales data using SQL.
                
                IMPORTANT: When a user asks a question about sales data, follow these steps:
                1. FIRST, use the get_schema_info_tool to understand the database structure
                2. THEN, write a SQL query based on the user's question and execute it
                3. Explain the results in a clear and concise way
                
                When writing SQL queries:
                - Use proper SQL syntax for SQLite
                - Use appropriate JOINs when querying across multiple tables
                - Use aliases for table names in complex queries
                - Use aggregation functions when appropriate
                """
            )
        
        st.session_state.current_model = model_type
        st.session_state._last_key = google_api_key
        st.session_state.pop("messages", None)
        
    except Exception as e:
        st.error(f"❌ Error initializing model: {e}")
        st.stop()

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# File Processing
if uploaded_file is not None:
    file_content = uploaded_file.read().decode('utf-8')
    file_type = uploaded_file.type.split('/')[-1]
    
    st.success(f"📁 File uploaded: {uploaded_file.name}")
    
    # Store file info in session state
    st.session_state.uploaded_file = {
        "name": uploaded_file.name,
        "content": file_content,
        "type": file_type
    }

# Main Chat Interface
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📊 Data Visualization", "🗄️ Database Explorer", "📈 Analytics"])

with tab1:
    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Chat input
    prompt = st.chat_input("Type your message here...")
    
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        try:
            with st.spinner("🤔 Thinking..."):
                if model_type == "LangGraph ReAct Agent":
                    messages = []
                    for msg in st.session_state.messages:
                        if msg["role"] == "user":
                            messages.append(HumanMessage(content=msg["content"]))
                        elif msg["role"] == "assistant":
                            messages.append(AIMessage(content=msg["content"]))
                    
                    response = st.session_state.agent.invoke({"messages": messages})
                    answer = response["messages"][-1].content
                
                elif model_type == "Google Gemini Direct":
                    if "chat" not in st.session_state:
                        st.session_state.chat = st.session_state.genai_client.chats.create(model="gemini-2.5-flash")
                    
                    response = st.session_state.chat.send_message(prompt)
                    answer = response.text if hasattr(response, "text") else str(response)
                
                elif model_type == "SQL Assistant":
                    messages = []
                    for msg in st.session_state.messages:
                        if msg["role"] == "user":
                            messages.append(HumanMessage(content=msg["content"]))
                        elif msg["role"] == "assistant":
                            messages.append(AIMessage(content=msg["content"]))
                    
                    response = st.session_state.agent.invoke({"messages": messages})
                    answer = response["messages"][-1].content
                    
                    # Extract and display SQL queries
                    for msg in response["messages"]:
                        if hasattr(msg, "tool_calls") and msg.tool_calls:
                            for tool_call in msg.tool_calls:
                                if tool_call.get("name") == "execute_sql_tool":
                                    sql_query = tool_call["args"]["sql_query"]
                                    st.code(sql_query, language="sql")
        
        except Exception as e:
            answer = f"❌ An error occurred: {e}"
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(answer)
        
        # Add assistant message to history
        st.session_state.messages.append({"role": "assistant", "content": answer})

with tab2:
    st.header("📊 Data Visualization")
    
    if "uploaded_file" in st.session_state:
        file_data = st.session_state.uploaded_file
        
        if file_data["type"] == "csv":
            try:
                df = pd.read_csv(io.StringIO(file_data["content"]))
                
                st.subheader("📈 Data Overview")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rows", df.shape[0])
                with col2:
                    st.metric("Columns", df.shape[1])
                with col3:
                    st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
                
                # Column selection for visualization
                numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
                categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
                
                if numeric_columns:
                    st.subheader("📊 Numeric Data Visualization")
                    
                    chart_type = st.selectbox("Chart Type", ["Line Chart", "Bar Chart", "Histogram", "Scatter Plot"])
                    
                    if chart_type == "Line Chart":
                        selected_cols = st.multiselect("Select columns", numeric_columns, default=numeric_columns[:2])
                        if selected_cols:
                            st.line_chart(df[selected_cols])
                    
                    elif chart_type == "Bar Chart":
                        selected_col = st.selectbox("Select column", numeric_columns)
                        st.bar_chart(df[selected_col])
                    
                    elif chart_type == "Histogram":
                        selected_col = st.selectbox("Select column", numeric_columns)
                        fig, ax = plt.subplots()
                        ax.hist(df[selected_col].dropna(), bins=20, alpha=0.7)
                        ax.set_xlabel(selected_col)
                        ax.set_ylabel("Frequency")
                        st.pyplot(fig)
                    
                    elif chart_type == "Scatter Plot":
                        col1, col2 = st.columns(2)
                        with col1:
                            x_col = st.selectbox("X-axis", numeric_columns)
                        with col2:
                            y_col = st.selectbox("Y-axis", numeric_columns)
                        
                        if x_col and y_col:
                            fig, ax = plt.subplots()
                            ax.scatter(df[x_col], df[y_col], alpha=0.6)
                            ax.set_xlabel(x_col)
                            ax.set_ylabel(y_col)
                            st.pyplot(fig)
                
                # Data table
                st.subheader("📋 Data Table")
                st.dataframe(df, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error processing CSV file: {e}")
        else:
            st.info("Please upload a CSV file to see visualizations.")
    else:
        st.info("📁 Upload a file to see data visualizations.")

with tab3:
    st.header("🗄️ Database Explorer")
    
    if st.button("🔄 Refresh Database Info"):
        st.rerun()
    
    try:
        db_info = get_database_info()
        
        st.subheader("📋 Database Schema")
        for table_name, schema in db_info["schema"].items():
            with st.expander(f"Table: {table_name}"):
                schema_df = pd.DataFrame(schema)
                st.dataframe(schema_df, use_container_width=True)
        
        st.subheader("📊 Sample Data")
        for table_name, sample_data in db_info["sample_data"].items():
            if sample_data:
                with st.expander(f"Sample data from {table_name}"):
                    sample_df = pd.DataFrame(sample_data)
                    st.dataframe(sample_df, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error accessing database: {e}")

with tab4:
    st.header("📈 Analytics Dashboard")
    
    try:
        # Sales Analytics
        sales_data = text_to_sql("SELECT * FROM sales")
        if "results" in sales_data and sales_data["results"]:
            sales_df = pd.DataFrame(sales_data["results"])
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_sales = sales_df['total_amount'].sum()
                st.metric("Total Sales", f"${total_sales:,.2f}")
            
            with col2:
                avg_sale = sales_df['total_amount'].mean()
                st.metric("Average Sale", f"${avg_sale:,.2f}")
            
            with col3:
                total_transactions = len(sales_df)
                st.metric("Total Transactions", total_transactions)
            
            with col4:
                max_sale = sales_df['total_amount'].max()
                st.metric("Highest Sale", f"${max_sale:,.2f}")
            
            # Sales over time
            st.subheader("📈 Sales Over Time")
            sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
            monthly_sales = sales_df.groupby(sales_df['sale_date'].dt.to_period('M'))['total_amount'].sum()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            monthly_sales.plot(kind='line', ax=ax, marker='o')
            ax.set_title('Monthly Sales Trend')
            ax.set_xlabel('Month')
            ax.set_ylabel('Sales Amount ($)')
            plt.xticks(rotation=45)
            st.pyplot(fig)
            
            # Top customers
            st.subheader("👥 Top Customers")
            customer_sales = text_to_sql("""
                SELECT c.name, SUM(s.total_amount) as total_spent, COUNT(s.sale_id) as transaction_count
                FROM customers c
                JOIN sales s ON c.customer_id = s.customer_id
                GROUP BY c.customer_id, c.name
                ORDER BY total_spent DESC
                LIMIT 5
            """)
            
            if "results" in customer_sales and customer_sales["results"]:
                customer_df = pd.DataFrame(customer_sales["results"])
                st.dataframe(customer_df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error generating analytics: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🤖 Comprehensive AI Chatbot - Built with Streamlit, LangGraph, and Google Gemini</p>
    <p>Features: Multi-model AI, Database Integration, File Processing, Data Visualization</p>
</div>
""", unsafe_allow_html=True)
