import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output
import plotly.express as px 
import pandas as pd


# loading data

def loading_data():
    df = pd.read_csv('../assets/healthcare_dataset.csv')
    df["Billing Amount"] = pd.to_numeric(df["Billing Amount"], errors ='coerce')
    df["Date of Admission"] = pd.to_datetime(df["Date of Admission"])
    df["YearMonth"] = df["Date of Admission"].dt.to_period("M")
    return df

df = loading_data()

# creating web app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    