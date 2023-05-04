import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, callback_context
import plotly.express as px
import pandas as pd
import numpy as np

from helpers import bmr_results_table, macros_table, bmr_engine, activity_levels

# app set-up
app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])
app.title = 'BMR Insights'
server = app.server


# application components

# bmr calculator inputs
bmr_inputs = html.Div([
    dbc.InputGroup([
        dbc.InputGroupText('BMR formula'),
        dbc.Select(id='bmr-formula-input',
            options=[
                {'label' : 'Mifflin St Jeor', "value" : 1},
                {'label' : 'Katch–McArdle', "value" : 2},
            ], placeholder='Select BMR formula'),
    ], class_name='mb-2', size='sm'),
    dbc.InputGroup([
        dbc.InputGroupText('Age'), dbc.Input(id='input-age', disabled=True, type="number", min=15, max=80, step=1)
    ], class_name ='mb-2', size='sm'),
    dbc.InputGroup([
        dbc.InputGroupText('Gender'),
        dbc.Select(id='input-gender',
            options=[
                {'label' : 'Male', "value" : 1},
                {'label' : 'Female', "value" : 2},
            ], placeholder='Select gender'),
    ], class_name='mb-2', size='sm'),
    dbc.InputGroup([
        dbc.InputGroupText('Height'), dbc.Input(id='input-height', disabled=True, type="number", min=150, max=230, step=1)
    ], class_name ='mb-2', size='sm'),
    dbc.InputGroup([
        dbc.InputGroupText('Weight'), dbc.Input(id='input-weight', disabled=True, type="number", min=40, max=150, step=1)
    ], class_name ='mb-2', size='sm'),
    dbc.InputGroup([
        dbc.InputGroupText('Estimated bodyfat %'), dbc.Input(id='input-bf', disabled=True, type="number", min=5, max=40, step=1)
    ], class_name ='mb-2', size='sm'),
    dbc.Button('Calculate', id='bmr-calculate', n_clicks=0, size='sm', disabled=True)
])

# energy needs table
energy_needs = html.Div([
    html.Div(id='table-energy-needs'),
    dbc.InputGroup([
        dbc.InputGroupText('Calorie deficit'), dbc.Input(id='input-calorie-deficit', type="number", min=0, max=1000, step=100, value=500)
    ], class_name ='mb-2', size='sm'),
])

# macros table
macros = html.Div([
    html.Div(id='table-macros'),
    dbc.InputGroup([
        dbc.InputGroupText('Activity level'), dbc.Select(id='input-activity-level', options=[
            {'label' : level, "value" : count} for count, level in enumerate(activity_levels)
        ], value=3)
    ], class_name ='mb-2', size='sm'),
    dbc.InputGroup([
        dbc.InputGroupText('Protein per kg'),  dbc.Input(id='input-protein-kg', type="number", min=1, max=3, step=0.1, value=2)
    ], class_name='mb-2', size='sm'),
    dbc.InputGroup([
        dbc.InputGroupText('Fat per kg'),  dbc.Input(id='input-fat-kg', type="number", min=0.5, max=1, step=0.1, value=1)
    ], class_name='mb-2', size='sm')    
])

# application layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            bmr_inputs
        ]),
        dbc.Col([
            energy_needs
        ]),
        dbc.Col([
            macros
        ]),        
    ])
], fluid=True)

# callback for bmr inputs
@app.callback(
    Output('input-age', 'disabled'),
    Output('input-age', 'placeholder'),
    Output('input-age', 'value'),
    Output('input-gender', 'disabled'),
    Output('input-gender', 'placeholder'),
    Output('input-gender', 'value'),
    Output('input-height', 'disabled'),
    Output('input-height', 'placeholder'),    
    Output('input-height', 'value'),    
    Output('input-weight', 'disabled'),
    Output('input-weight', 'placeholder'),
    Output('input-bf', 'disabled'),
    Output('input-bf', 'placeholder'),
    Output('input-bf', 'value'),    
    Input('bmr-formula-input', 'value')
    )
def update_bmr_inputs(value):
    # update states of bmr inputs
    input_states = {
        '1' : [
            False, 'Enter your age between 15 and 80', None,
            False, 'Select gender', None,
            False, 'Enter your height in cm', None,
            False, 'Enter your weight in kg',
            True, '', None
            ],
        '2' : [
            True, '', None,
            True, '', None,
            True, '', None,
            False, 'Enter your weight in kg',
            False, 'Enter your estimated bodyfat %', None
        ]
    }
    if input_states.get(value) is None:
        return [
            True, '', None,
            True, '', None,
            True, '', None,
            True, '',
            True, '', None
        ]
    return input_states.get(value)

# callback for bmr calculate button state
@app.callback(
    Output('bmr-calculate', 'disabled'),
    Input('bmr-formula-input', 'value'),
    Input('input-age', 'value'),
    Input('input-gender', 'value'),
    Input('input-height', 'value'),
    Input('input-weight', 'value'),
    Input('input-bf', 'value'),
)
def calculate_bmr(bmr_formula_input_value, input_age_value, input_gender_value, input_height_value, input_weight_value, input_bf_value):
    required_inputs = {
        '1' : [
            input_age_value, input_gender_value, input_height_value, input_weight_value
        ], # Mifflin St Jeor
        '2' : [
            input_weight_value, input_bf_value
        ], # Katch-McArdle
    }
    # nothing selected yet
    if required_inputs.get(bmr_formula_input_value) is None:
        return True
    # don't have all inputs yet
    elif not any(elem is None for elem in required_inputs.get(bmr_formula_input_value)):
        return False
    return True

# callback for calorie levels
@app.callback(
    Output('table-energy-needs', 'children'),
    Output('table-macros', 'children'),    
    Output('input-calorie-deficit', 'disabled'),
    Output('input-activity-level', 'disabled'),
    Output('input-protein-kg', 'disabled'),
    Output('input-fat-kg', 'disabled'),    
    Input('bmr-calculate', 'n_clicks'),
    Input('input-calorie-deficit', 'value'),
    Input('input-activity-level', 'value'),
    Input('input-protein-kg', 'value'),
    Input('input-fat-kg', 'value'),  
    State('bmr-formula-input', 'value'),
    State('input-age', 'value'),
    State('input-gender', 'value'),
    State('input-height', 'value'),
    State('input-weight', 'value'),
    State('input-bf', 'value'),
)
def calculate_bmr(n_clicks, deficit_value, activity_level_value, protein_kg_value, fat_kg_value,\
                  bmr_formula_input, input_age, input_gender, input_height, input_weight, input_bf):
    
    headers = ['Activity level', 'Maintenance', 'Weight loss']
    macro_headers = ['Protein', 'Carbs', 'Fats']
    trigger = callback_context.triggered[0]['prop_id'].split('.')[0]
    if trigger in ['bmr-calculate', 'input-calorie-deficit', 'input-activity-level', 'input-protein-kg', 'input-fat-kg']:
        _activity_levels = list(activity_levels.keys())
        deficit = deficit_value
        if deficit_value is None:
            deficit = 0
        bmr_result = bmr_engine(
            method=bmr_formula_input, age=input_age, gender=input_gender, height=input_height, weight=input_weight, bf=input_bf)
        return \
            bmr_results_table(headers, bmr_result, deficit=deficit),\
            macros_table(macro_headers, bmr_result, weight=input_weight, protein_kg=protein_kg_value, fat_kg=fat_kg_value,\
                          activity_level=_activity_levels[int(activity_level_value)], deficit=deficit),\
            False,\
            False,\
            False,\
            False
    return \
        bmr_results_table(headers, 0, blank=True),\
        macros_table(macro_headers, 0, blank=True),\
        True,\
        True,\
        True,\
        True

# uncomment below for development and debugging
# if __name__ == '__main__':
#     app.run_server(port='8051', host='0.0.0.0', debug=True)
