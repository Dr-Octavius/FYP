from src.api.api_service import HubSpotCompanyService
from src.api.api_service import HubSpotNoteService
from src.api.api_service import HubSpotDealService
from src.api.api_service import AircallLiveTranscriptionService

class ServiceFactory:
    services = {
        'company': HubSpotCompanyService,
        'note': HubSpotNoteService,
        'deal': HubSpotDealService,
        'live_transcription': AircallLiveTranscriptionService
    }

    @staticmethod
    def get_service(service_type, api_key):
        service = ServiceFactory.services.get(service_type)
        if not service:
            raise ValueError("Invalid service type provided.")
        return service(api_key)