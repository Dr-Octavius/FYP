import streamlit as st
import atexit
import time
from utils.app_helper import initialize_flask_app, run_flask , shutdown_flask
from threading import Thread

# Main App Layout with Two Columns
st.set_page_config(layout="wide")

# Initialize and start the Flask app
flask_app = initialize_flask_app()
if "flask_thread" not in st.session_state:
    st.session_state["flask_thread"] = Thread(target=run_flask, daemon=True)
    st.session_state["flask_thread"].start()

# Register shutdown function to stop Flask when Streamlit stops
atexit.register(shutdown_flask)

from components.home import home
from components.transcription_tool import transcription_tool
from components.hubspot_tool import hubspot_tool
from components.aircall_tool import aircall_tool

# Initialize session state for tool selection
if "selected_tool" not in st.session_state:
    st.session_state["selected_tool"] = "home"

if st.sidebar.button(
    "Home", 
    key="home", 
    use_container_width=True, 
    type="secondary",
    help="Home"
    ):
    st.session_state["selected_tool"] = "home"

st.markdown("---")

# Sidebar Navigation - Sidebar buttons for tool selection
st.sidebar.markdown("<h2 style='text-align: center;'>🛠AI Powered Toolkit🛠</h2>", unsafe_allow_html=True)

# Sidebar Selections
if st.sidebar.button(
    "Call Transcription", 
    key="transcription", 
    use_container_width=True, 
    type="secondary",
    help="Transcribe your call recordings"
    ):
    st.session_state["selected_tool"] = "transcription-tool"
if st.sidebar.button(
    "Dialogue Planner", 
    key="hubspot", 
    use_container_width=True, 
    type="secondary",
    help="Plan a Cold Call"
    ):
    st.session_state["selected_tool"] = "planner-tool"
if st.sidebar.button(
    "Live Call Helper", 
    key="aircall", 
    use_container_width=True, 
    type="secondary",
    help="Sharpen your call with suggestions"
    ):
    st.session_state["selected_tool"] = "ai-tool"

# Display the selected tool in the main area
if st.session_state["selected_tool"] == "transcription-tool":
    transcription_tool()
elif st.session_state["selected_tool"] == "planner-tool":
    hubspot_tool()
elif st.session_state["selected_tool"] == "ai-tool":
    aircall_tool()
elif st.session_state["selected_tool"] == "home":
    home()