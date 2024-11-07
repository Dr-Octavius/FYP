import base64

class HubSpotOAuthAPIToken:
    _instance = None

    def __new__(cls, api_key):
        if cls._instance is None:
            cls._instance = super(HubSpotOAuthAPIToken, cls).__new__(cls)
            cls._instance.key = api_key
        return cls._instance

    @staticmethod
    def get_token():
        return HubSpotOAuthAPIToken._instance.key
    
class AirCallHTTPAPIToken:
    _instance = None

    def __new__(cls, api_key):
        if cls._instance is None:
            # Encode the api_key (api_id:api_token) in Base64 - commented out cause not working well
            # encoded_key = base64.b64encode(api_key.encode()).decode("utf-8")
            encoded_key = api_key
            cls._instance = super(AirCallHTTPAPIToken, cls).__new__(cls)
            cls._instance.key = encoded_key
        return cls._instance

    @staticmethod
    def get_token():
        return AirCallHTTPAPIToken._instance.key
