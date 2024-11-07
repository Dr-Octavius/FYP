# components/home.py
import streamlit as st

def home():
    st.title("🌟 Welcome to StaffAny's Sales Tool! ")
    st.write("##### Select a tool from the sidebar or explore the options below to get started on enhancing your sales and communication.")

    st.markdown("---")
    st.subheader("🛠 Available Tools")
    st.write("##### Here’s a snapshot of each tool in your toolkit:")

    st.markdown("---")
    
    # Call Transcription Tool Section
    st.markdown("### 🎙️ Call Transcription")
    st.write("###### Record and/or Transcribe Now! ")
    st.write("Transcribe your call recordings or record a new one & transcribe 🚀 ")
    with st.expander("Learn more about Call Transcription"):
        st.write("This tool allows you to upload or record calls and get instant transcriptions with speaker identification. "
                 "Perfect for analyzing client conversations and gathering insights on tone and topics.")

    if st.button("📜 Explore Call Transcription", key="call_transcription"):
        st.session_state["selected_tool"] = "transcription-tool"
    
    st.markdown("---")

    # Dialogue Planner Tool Section
    st.markdown("### 📞 Dialogue Planner")
    st.write("###### Plan your cold call")
    st.write("Trained with HubSpot CRM & Call data 🚀 ")
    with st.expander("Learn more about Dialogue Planner"):
        st.write("This tool integrates with your HubSpot CRM to give you all the essential information about a client or company. "
                 "Ideal for preparing cold calls with personalized details, enhancing the effectiveness of your conversations.")

    if st.button("📄 Explore Dialogue Planner", key="dialogue_planner"):
        st.session_state["selected_tool"] = "planner-tool"
    
    st.markdown("---")

    # Live Call Helper Tool Section
    st.markdown("### 📈 Live Call Helper")
    st.write("###### Receive real-time suggestions and guidance during calls")
    st.write("Enhance cold call engagement & increase effectiveness 🚀 ")
    with st.expander("Learn more about Live Call Helper"):
        st.write("This tool provides real-time suggestions and reminders during ongoing calls. "
                 "It’s designed to improve your call flow, give you pointers based on live transcription, "
                 "and ensure you never miss an important question or topic during a call.")

    if st.button("💡 Explore Live Call Helper", key="live_call_helper"):
        st.session_state["selected_tool"] = "ai-tool"
    
    st.markdown("---")

    # Footer message
    st.write("Choose a tool to begin transforming your sales conversations!")