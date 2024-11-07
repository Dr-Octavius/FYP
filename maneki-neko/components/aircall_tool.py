# components/aircall_tool.py

import os
import json
import streamlit as st
import time

# Initialize session state variables if they do not exist
if "transcription_data" not in st.session_state:
    st.session_state["transcription_data"] = []  # Cache for storing transcription data
if "updating" not in st.session_state:
    st.session_state["updating"] = False  # Control live updating
if "last_transcript_index" not in st.session_state:
    st.session_state["last_transcript_index"] = 0  # Track last processed index
if "last_utterance_index" not in st.session_state:
    st.session_state["last_utterance_index"] = 0  # Track last processed index

def read_from_file(filename="data/received_transcriptions_shared.json"):
    """Reads data from a JSON file and parses it as a JSON object."""
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)  # Parse JSON content into a dictionary
        except json.JSONDecodeError:
            st.error("Error parsing the JSON file.")
            return None
    return None

def aircall_tool():
    """Streamlit component to display real-time live transcription text from Aircall."""
    
    # Create two main columns: header in the first, buttons in the second
    col1, col2 = st.columns([3, 1])  # Adjust widths as necessary

    # Header in the first column
    with col1:
        st.markdown("<h1 style='margin-top: 0px;'>Live Call Helper</h1>", unsafe_allow_html=True)

    # Buttons in the second column, placed closer together
    with col2:
        # Nested columns within col2 for buttons side-by-side
        button_cols = st.columns([1, 1.5])

        # Start/Stop Updates button
        with button_cols[0]:
            if st.session_state["updating"]:
                if st.button("Stop Updates"):
                    st.session_state["updating"] = False
                    st.rerun()  # Rerun to update button state
            else:
                if st.button("Start Updates"):
                    st.session_state["updating"] = True
                    st.rerun()  # Rerun to update button state

        # Clear Transcription button
        with button_cols[1]:
            if st.button("Clear Transcription"):
                st.session_state["transcription_data"] = []
                st.session_state["last_transcript_index"] = 0  # Reset the last index
                if os.path.exists("data/received_transcriptions_shared.json"):
                    os.remove("data/received_transcriptions_shared.json")
                st.write("Transcription cleared.")

    # Placeholder for conversation
    conversation_placeholder = st.container()
    
    # Run live update loop if updating is enabled
    if st.session_state["updating"]:
        while st.session_state["updating"]:
            # Read the latest transcription data from the JSON file
            transcription_content = read_from_file()
            # Process only new transcriptions
            if transcription_content:
                # Check if there are new utterances beyond the last processed index
                if len(transcription_content) > st.session_state["last_transcript_index"]:
                    # Add only new utterances to the cached data
                    new_transcriptions = transcription_content[st.session_state["last_transcript_index"]:]
                    for transcription in new_transcriptions:
                        new_utterances = transcription['transcription']['utterances']
                        st.session_state["transcription_data"].extend(new_utterances)
                    # Display all cached transcriptions
                    display_transcriptions(st.session_state["transcription_data"][st.session_state["last_utterance_index"]:],conversation_placeholder)
                    # Update the last index to the new length
                    st.session_state["last_transcript_index"] = len(transcription_content)

            # Wait for 2 seconds before checking for updates again
            time.sleep(2)
    elif st.session_state["transcription_data"]:
        return
    else:
        display_empty_state(conversation_placeholder)

# Helper function to display transcriptions
def display_transcriptions(utterance_list,conversation):
    with conversation:
        for utterance in utterance_list:
            st.session_state["last_utterance_index"] += 1
            speaker = "Prospect" if utterance.get("participant_type") == "external" else "You"
            text = utterance["text"]
            if speaker == "Prospect":
                prospect_placeholder = st.empty()
                # Populate the placeholder with the title and text inside a speech bubble-style container
                with prospect_placeholder:
                    st.markdown(
                        f"""
                        <div style="
                            display: inline-block; 
                            background-color: #333333; 
                            border-radius: 15px; 
                            padding: 15px; 
                            margin-bottom: 10px; 
                            max-width: 50%; 
                            position: relative;
                        ">
                            <h4 style="margin: 0; color: #fccc6f; padding-bottom: 5px;">🧑‍💼 Prospect</h4>
                            <div style="
                                text-align: left;
                                font-family: monospace; 
                                color: #fccc6f; 
                                background-color: #1E1E1E;
                                padding: 15px;
                                border-radius: 15px;
                                margin-top: 5px;
                            ">
                                {text}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                your_placeholder = st.empty()
                with your_placeholder:
                    st.markdown(
                        f"""
                        <div style="
                            display: inline-block; 
                            text-align: right;
                            background-color: #333333; 
                            border-radius: 15px; 
                            padding: 15px; 
                            margin-bottom: 10px; 
                            max-width: 50%; 
                            position: relative;
                            float: right;  /* Aligns the entire block to the right */
                        ">
                            <h4 style="margin: 0; color: #4cdccc; padding-bottom: 5px;">🧑‍💼 You</h4>
                            <div style="
                                font-family: monospace; 
                                color: #4cdccc; 
                                background-color: #1E1E1E;
                                padding: 15px;
                                border-radius: 15px;
                                margin-top: 5px;
                            ">
                                {text}
                                <div style="
                                    text-align: left;
                                    margin-top: 10px; 
                                    padding-left: 10px; 
                                    border: 3px solid #f0767b; 
                                    font-family: monospace;
                                    color: #f0767b;
                                ">
                                    💡 Try this?
                                </div>
                                <div style="
                                    text-align: left;
                                    margin-top: 10px; 
                                    padding-left: 10px; 
                                    border-left: 3px solid #f0767b; 
                                    font-family: monospace;
                                    font-style: italic;
                                    color: #f0767b;
                                ">
                                    {model_predict(text)}
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

# Display waiting message when no transcription is available
def display_empty_state(placeholder):
    with placeholder:
        st.markdown("```\n ⌛ Waiting for your conversation... \n```")

# Mock function to simulate model prediction (replace with actual model function)
def model_predict(prospect_text):
    # This would be the function to call your model ensemble to generate suggestions
    return f"{prospect_text}"