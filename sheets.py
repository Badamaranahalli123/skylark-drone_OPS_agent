import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Paste your actual Spreadsheet ID here
SPREADSHEET_ID = "1QEfvt3IJr2g8GYq-n8YKtK6S69rnW-YC34r8Wb7YKsg"

def get_sheet(sheet_name):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)

    sheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = sheet.worksheet(sheet_name)

    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    return df, worksheet
