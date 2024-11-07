import requests
from urllib.parse import urlencode
import datetime

class ApiService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        self.post_config = {
            'filters': [],
            'sorts': [],
            'properties': [],
            'limit': 100,
            'associations': [],
            'paging': None
        }
        self.get_params = {
            'limit': '100',
            'properties': '',
            'archived': 'true'
        }

    def update_post_config(self, key, value):
        if key in self.post_config:
            self.post_config[key] = value
        else:
            raise ValueError(f"Invalid POST configuration key: {key}")

    def update_get_params(self, key, value):
        if key in self.get_params:
            self.get_params[key] = value
        else:
            raise ValueError(f"Invalid GET parameter key: {key}")

    def get(self, url, params=None):
        response = requests.get(url, headers=self.headers, params=self.get_params)
        response.raise_for_status()
        return response.json()

    def post(self, url, data=None):
        response = requests.post(url, headers=self.headers, json=self.post_config)
        response.raise_for_status()
        return response.json()
    
    def patch(self, url, data=None):
        response = requests.patch(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, url, params=None):
        response = requests.delete(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

# Services for specific entities
class HubSpotCompanyService(ApiService):
    BASE_URL = 'https://api.hubapi.com/crm/v3/objects/companies'

    def search_companies(self, filters):
        url = f"{self.BASE_URL}/search"
        return self.post(url, data=filters)
    
    def search_company(self, id):
        url = f"{self.BASE_URL}/{id}"
        return self.get(url)

class HubSpotNoteService(ApiService):
    BASE_URL = 'https://api.hubapi.com/crm/v4/objects/notes'

    def get_note_by_id(self, note_id):
        url = f"{self.BASE_URL}/{note_id}"
        return self.get(url)

class HubSpotDealService(ApiService):
    BASE_URL = 'https://api.hubapi.com/crm/v3/objects/deals'
    PIPELINE_URL = 'https://api.hubapi.com/crm/v3/pipelines/deals'

    def get_deal_by_id(self, deal_id):
        url = f"{self.BASE_URL}/{deal_id}"
        return self.get(url)
    
    def get_deal_pipeline_by_id(self, pipeline_id, stage_id):
        url = f"{self.PIPELINE_URL}/{pipeline_id}/stages/{stage_id}"
        return self.get(url)


class AircallLiveTranscriptionService(ApiService):
    BASE_URL = 'api.aircall.io/v1/calls'

    # Using http keys instead of Bearer Token - requires changing the headers
    def __init__(self, api_key):
        # Initialize the parent class with the encoded token
        super().__init__(api_key)
        
        # Override headers for Basic Auth
        self.headers = {
            'Authorization': f'Basic {self.api_key}'
        }
        self.params = {}

    def get_transcription_by_call_id(self, call_id):
        url = f"https://{self.api_key}@{self.BASE_URL}/{call_id}/transcription"
        return self.get(url)