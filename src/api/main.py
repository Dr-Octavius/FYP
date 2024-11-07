# Example usage in main.py
from src.api.service_factory import ServiceFactory
from api_token import HubSpotOAuthAPIToken
from src.config import HUBSPOT_OAUTH_TOKEN

def main():
    # Ensures singleton usage
    token = HubSpotOAuthAPIToken(HUBSPOT_OAUTH_TOKEN)  
    company_service = ServiceFactory.get_service('company', token.get_token())
    note_service = ServiceFactory.get_service('note', token.get_token())
    deal_service = ServiceFactory.get_service('deal', token.get_token())

    # Define your filter criteria here
    filter_criteria = {...}  
    companies = company_service.search_companies(filter_criteria)
    
    # Define your filter criteria here
    filter_criteria = {...}  
    notes = note_service.get_note_by_id(filter_criteria)
    
    # Define your filter criteria here
    filter_criteria = {...}  
    deals = deal_service.get_deal_by_id(filter_criteria)
    
    print(companies)
    print(notes)
    print(deals)

if __name__ == '__main__':
    main()