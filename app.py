import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, html
import plotly.express as px 
import pandas as pd


# loading/cleaning data

def loading_data():
    df = pd.read_csv('assets/healthcare_dataset.csv')
    df["Billing Amount"] = pd.to_numeric(df["Billing Amount"], errors ='coerce')
    df["Date of Admission"] = pd.to_datetime(df["Date of Admission"])
    df["YearMonth"] = df["Date of Admission"].dt.to_period("M")
    return df

df = loading_data()
num_records = len(df)
avg_billing = df["Billing Amount"].mean()

# creating web app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# app layout and design karing

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("HealthCare Dashboard"), width=15, className="text-centre my-5")
    ]),
    # hospital statistics ko ab hum dekhenge
    dbc.Row([dbc.Col(html.Div(f"Total Patient Records: {num_records}", className="text-centre my-3 top-text"),width=7),
        dbc.Col(html.Div(f"Average Billing Amount: {avg_billing:,.2f}", className="text-centre my-3 top-text"), width=7)     
             ], className="mb-5"),
    
    # aurat ya mard 
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Patient Demographics", className="card-title"),
                    dcc.Dropdown(
                        id="gender-filter",
                        options=[{"label":gender , "value": gender}for gender in df["Gender"].unique()] ,
                        value=None,
                        placeholder="Select a Gender"
                    ),
                    dcc.Graph(id="age-distribution") #bhai kuch mast si cheez code horhi
                    
                ])
            ])
        ], width=7)
    ]),
    # Medical Condition Distribution
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                 html.H4("Medical Condition Distribution", className="card-title"),
                 dcc.Graph(id="Condition-distribution")
                
            ])
            
        ])
    ], width=7),
    # insurance provider ka data
    dbc.Row([
     dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4("Insurance Provider Comparison", className="card-title"),
                 dcc.Graph(id="Insurance-comparison")
                
            ])
        ])
    ], width=12),
    # billing distribution
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Billing Amount Distribution", className="card-title"),
                    dcc.Slider(id="billing-slider",
                               min=df["Billing Amount"].min(),
                               max=df["Billing Amount"].max(),
                               value=df["Billing Amount"].median(),
                               marks={int(value): f"₹{int(value):,}" for value in df["Billing Amount"].quantile([0,0.25,0.5,0.75,1]).values},
                               step=100
                               ),
                    dcc.Graph(id="billing-distribution")
                    
                ])
            ])
        ], width=12)
    ]), 
    # Trends in Admission
     dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Trends in Admission", className="card-title"),
                    
                    dcc.RadioItems(
                        id='chart-type',
                        options=[{"label":"Line Chart", 'value':'Line'},{"label":"Bar Chart", 'value':'Bar'}],
                        value='line',
                        inline=True,
                        className='mb-4'
                    ), 
                    dcc.Dropdown(id="condtition-filter",
                                 options=[{'label':condition, 'value': condition} for 
                                          condition in df["Medical Condition"].unique()],
                                 value=None,
                                 placeholder="Conditions"),
                    dcc.Graph(id="admission-trends")
                    
                ])
            ])
        ], width=12)
    ]), 
])
    
    
    
    
], fluid=True)

# finally we start on callbacksss

@app.callback(
    Output('age-distribution', 'figure'),
    Input('gender-filter', 'value')
    
)
def update_distribution(selected_gender):
    if selected_gender:
        filtered_df = df[df["Gender"]== selected_gender] 
    else:
        filtered_df = df
        
    if filtered_df.empty:
        return {}
    
    fig = px.histogram(
        filtered_df,
        x="Age",
        nbins=10,
        color="Gender",
        title="Age distribution by gender",
        color_discrete_sequence=["#0c10f8", "#f81a0c" ]
        
    )
    return fig



@app.callback(
    Output('Condition-distribution', 'figure'),
    Input('gender-filter', 'value')
)
def update_med_cond(selected_gender):
    filtered_df = df[df["Gender"]==selected_gender] if selected_gender else df
    fig = px.pie(filtered_df, names="Medical Condition", title="Medical Condition Distribution")
    return fig



# bhaari cheez hai haalat behaal hai but WE FIGHT

@app.callback(
    Output('Insurance-comparison', 'figure'),
    Input('gender-filter', 'value')
)
def update_insurance(selected_gender):
    filtered_df = df[df["Gender"]==selected_gender] if selected_gender else df
    fig = px.bar(filtered_df,  x= "Insurance Provider",  y="Billing Amount", color="Medical Condition", 
                 barmode="group",
                 title="Insurance Provider Price Comparison",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    return fig



@app.callback(
    Output('billing-distribution', 'figure'),
    [Input('gender-filter', 'value'), 
     Input('billing-slider', 'value')]
)
def update_billing(selected_gender, slider_value):
    # code ko bhi callbacks aate hai. Mujhe nhi aate but koi nhi. 
    filtered_df = df[df["Gender"]==selected_gender] if selected_gender else df
    filtered_df = filtered_df[filtered_df["Billing Amount"] <= slider_value]
    fig = px.histogram(filtered_df, x="Billing Amount", nbins=10, title="Billing Amount Distribution")
    return fig


# thhak gayi




















if __name__ == "__main__":
    app.run_server(debug = True)
    