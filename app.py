import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, html
import plotly.express as px 
import pandas as pd


# loading data

def loading_data():
    df = pd.read_csv('assets/healthcare_dataset.csv')
    df["Billing Amount"] = pd.to_numeric(df["Billing Amount"], errors ='coerce')
    df["Date of Admission"] = pd.to_datetime(df["Date of Admission"])
    df["YearMonth"] = df["Date of Admission"].dt.to_period("M")
    return df

df = loading_data()

# creating web app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# app layout and design

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("HealthCare Dashboard"), width=15, className="text-centre my-5")
    ]),
    # hospital statistics
    dbc.Row([dbc.Col(html.Div(f"Total Patient Records:"))])
])




































if __name__ == "__main__":
    app.run_server(debug = True)
    