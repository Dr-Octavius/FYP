# webhook/aircall_webhook.py

from flask import Flask, request, jsonify
from services.aircall_service import get_transcription
import streamlit as st
import json
import os

def write_to_file(data, filename="data/received_transcriptions_shared.json"):
    """Appends new transcription data to an existing JSON file or creates a new one."""
    # Check if the file already exists
    if os.path.exists(filename):
        # Read the existing data
        with open(filename, "r") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []  # Initialize as empty list if file is corrupted
    else:
        existing_data = []

    # Append the new data
    existing_data.append(data)

    # Write the updated data back to the file
    with open(filename, "w") as file:
        json.dump(existing_data, file, indent=4)

# Initialize Flask app
app = Flask(__name__)

@app.route("/aircall-webhook", methods=["POST"])
def aircall_webhook():
    data = request.json
    if data and data.get("event") == "transcription.created":
        # Extract the relevant information from the payload
        event_type = data["event"]
        timestamp = data["timestamp"]
        token = data["token"]
        conversation_intelligence_data = data["data"]  # This will contain the call object details
        
        # Log or handle the call.answered event
        # For example, you can save this data to session state or a database
        st.session_state["last_call_event"] = {
            "event_type": event_type,
            "timestamp": timestamp,
            "token": token,
            "conversation_intelligence_data": conversation_intelligence_data
        }

        # get the trranscription with the call_id
        call_id = conversation_intelligence_data['call_id']
        try:
            transcription = get_transcription(call_id)["transcription"]
        except Exception as e:
            return jsonify({"status": "Internal Server Error"}), 200
        
        # Update Streamlit session state for real-time display
        if transcription:
            write_to_file({
                "transcription": transcription["content"]
            })
            return jsonify({"status": "transcription.created event received"}), 200
        else:
            return jsonify({"status": "failed to fetch transcription"}), 200
    return jsonify({"status": "event type not supported"}), 200

# Test endpoint to check if the Flask server is running
@app.route("/", methods=["GET"])
def test_endpoint():
    return jsonify({"status": "Webhook server is running"}), 200

# Dummy shutdown endpoint
@app.route("/shutdown", methods=["POST"])
def shutdown():
    # No actual shutdown logic, just a dummy endpoint to trigger final request
    return "Server shutdown signal received.", 200