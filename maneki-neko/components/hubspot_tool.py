# components/hubspot_viewer.py

import streamlit as st
from services.hubspot_service import get_company_data, get_note_data, get_deal_data

def hubspot_tool():
    st.header("Dialogue Planner")

    entity_type = st.selectbox("Choose Entity Type", ["Company", "Note", "Deal"], key="entity_type")

    if entity_type == "Company":
        st.subheader("Search Companies")
        company_id = st.text_input("Enter Company ID", key="company_id")
        filter_criteria = st.text_area("Enter Company Search Filters (JSON format)", "{}", key="company_filters")

        if st.button("Search Companies"):
            if company_id:
                company_data = get_company_data(company_id=company_id)
                st.json(company_data)
            else:
                filters = eval(filter_criteria) if filter_criteria else {}
                companies = get_company_data(filters=filters)
                st.json(companies)

    elif entity_type == "Note":
        st.subheader("Retrieve Note by ID")
        note_id = st.text_input("Enter Note ID", key="note_id")

        if st.button("Get Note"):
            if note_id:
                note_data = get_note_data(note_id)
                st.json(note_data)
            else:
                st.error("Please enter a Note ID.")

    elif entity_type == "Deal":
        st.subheader("Retrieve Deal by ID")
        deal_id = st.text_input("Enter Deal ID", key="deal_id")

        if st.button("Get Deal"):
            if deal_id:
                deal_data = get_deal_data(deal_id)
                st.json(deal_data)
            else:
                st.error("Please enter a Deal ID.")