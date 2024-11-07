import random
from src.api.service_factory import ServiceFactory
from src.api.api_token import AirCallHTTPAPIToken
from src.config import AIRCALL_API_ID, AIRCALL_API_TOKEN

# Initialize HubSpot API token and services
token = AirCallHTTPAPIToken(AIRCALL_API_ID + ":" + AIRCALL_API_TOKEN)
live_transcription_service = ServiceFactory.get_service('live_transcription', token.get_token())

# API not available as we don't pay for it 
# def get_transcription(call_id):
#     return live_transcription_service.get_transcription_by_call_id(call_id)

# test function matching Aircall's transcription object
def get_transcription(call_id):
    # List of possible transcription examples
    transcriptions = [
        {
            "transcription": {
                "id": 68271,
                "call_id": call_id,
                "call_created_at": "2024-07-26T13:30:54.000Z",
                "type": "call",
                "content": {
                    "language": "en",
                    "utterances": [
                        {
                            "start_time": 5.12,
                            "end_time": 6.5,
                            "text": "Good morning, this is John from Company XYZ.",
                            "participant_type": "external",
                            "phone_number": "+33679198915"
                        },
                        {
                            "start_time": 7.0,
                            "end_time": 8.2,
                            "text": "Good morning, how can I assist you today?",
                            "participant_type": "internal",
                            "user_id": 123
                        },
                        {
                            "start_time": 9.5,
                            "end_time": 11.0,
                            "text": "I'm looking for information on your PayrollAny solution.",
                            "participant_type": "external",
                            "phone_number": "+33679198915"
                        }
                    ]
                }
            }
        },
        {
            "transcription": {
                "id": 68272,
                "call_id": call_id,
                "call_created_at": "2024-08-15T09:12:00.000Z",
                "type": "call",
                "content": {
                    "language": "en",
                    "utterances": [
                        {
                            "start_time": 0.5,
                            "end_time": 1.2,
                            "text": "Hello, is this StaffAny support?",
                            "participant_type": "external",
                            "phone_number": "+33712345678"
                        },
                        {
                            "start_time": 1.5,
                            "end_time": 2.8,
                            "text": "Yes, how can I help you?",
                            "participant_type": "internal",
                            "user_id": 124
                        },
                        {
                            "start_time": 3.0,
                            "end_time": 4.5,
                            "text": "I'm having issues with clocking in on the app.",
                            "participant_type": "external",
                            "phone_number": "+33712345678"
                        }
                    ]
                }
            }
        },
        {
            "transcription": {
                "id": 68273,
                "call_id": call_id,
                "call_created_at": "2024-09-10T14:45:20.000Z",
                "type": "call",
                "content": {
                    "language": "en",
                    "utterances": [
                        {
                            "start_time": 12.0,
                            "end_time": 13.5,
                            "text": "Hi, I'm interested in learning about your EngageAny solution.",
                            "participant_type": "external",
                            "phone_number": "+33987654321"
                        },
                        {
                            "start_time": 14.0,
                            "end_time": 15.6,
                            "text": "Sure, EngageAny is designed to boost employee engagement through interactive features.",
                            "participant_type": "internal",
                            "user_id": 125
                        },
                        {
                            "start_time": 16.0,
                            "end_time": 17.5,
                            "text": "Great! How can it integrate with my existing HR system?",
                            "participant_type": "external",
                            "phone_number": "+33987654321"
                        }
                    ]
                }
            }
        },
        {
            "transcription": {
                "id": 68274,
                "call_id": call_id,
                "call_created_at": "2024-09-15T11:30:54.000Z",
                "type": "call",
                "content": {
                    "language": "en",
                    "utterances": [
                        {
                            "start_time": 8.0,
                            "end_time": 9.3,
                            "text": "Is there a feature for automated payroll processing?",
                            "participant_type": "external",
                            "phone_number": "+33211223344"
                        },
                        {
                            "start_time": 9.5,
                            "end_time": 11.0,
                            "text": "Yes, PayrollAny automates payroll calculations and compliance checks.",
                            "participant_type": "internal",
                            "user_id": 126
                        }
                    ]
                }
            }
        },
        {
            "transcription": {
                "id": 68275,
                "call_id": call_id,
                "call_created_at": "2024-09-18T16:20:30.000Z",
                "type": "call",
                "content": {
                    "language": "en",
                    "utterances": [
                        {
                            "start_time": 2.0,
                            "end_time": 3.5,
                            "text": "Can StaffAny help with employee scheduling?",
                            "participant_type": "external",
                            "phone_number": "+33123456789"
                        },
                        {
                            "start_time": 4.0,
                            "end_time": 5.5,
                            "text": "Absolutely, our scheduling tool is user-friendly and flexible.",
                            "participant_type": "internal",
                            "user_id": 127
                        }
                    ]
                }
            }
        }
    ]

    # Return a random transcription from the list
    return random.choice(transcriptions)