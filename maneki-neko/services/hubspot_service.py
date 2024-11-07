# services/hubspot_service.py

from src.api.service_factory import ServiceFactory
from src.api.api_token import HubSpotOAuthAPIToken
from src.config import HUBSPOT_OAUTH_TOKEN

# Initialize HubSpot API token and services
token = HubSpotOAuthAPIToken(HUBSPOT_OAUTH_TOKEN)
company_service = ServiceFactory.get_service('company', token.get_token())
note_service = ServiceFactory.get_service('note', token.get_token())
deal_service = ServiceFactory.get_service('deal', token.get_token())

def get_company_data(company_id=None, filters=None):
    if company_id:
        return company_service.search_company(company_id)
    elif filters:
        return company_service.search_companies(filters)
    return {}

def get_note_data(note_id):
    return note_service.get_note_by_id(note_id) if note_id else {}

def get_deal_data(deal_id):
    return deal_service.get_deal_by_id(deal_id) if deal_id else {}