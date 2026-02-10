import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

def get_sheet(sheet_name):
    scope = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)

    # IMPORTANT: replace this with your actual Google Sheet name
    sheet = client.open("Skylark_Drone_DB")

    worksheet = sheet.worksheet(sheet_name)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    return df, worksheet
