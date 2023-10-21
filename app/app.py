import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, callback_context
from helpers import (
    # blank_table,
    bmr_results_table,
    weight_loss_table,
    macros_table,
    bmr_engine,
    activity_levels,
    calories_to_steps,
    weekly_weight_loss
)

# app set-up
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.title = 'BMR Calculator'
server = app.server

# application components
# bmr calculator inputs
inputs_body = dbc.Card(
    [
        dbc.CardHeader('Body', style={'color' : 'green'}),
        dbc.CardBody(
            [
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
                    dbc.InputGroupText('Weight'), dbc.Input(id='input-weight', disabled=True, type="number", min=40, max=150, step=0.1)
                ], class_name ='mb-2', size='sm'),
                dbc.InputGroup([
                    dbc.InputGroupText('Estimated bodyfat %'), dbc.Input(id='input-bf', disabled=True, type="number", min=5, max=40, step=1)
                ], class_name ='mb-2', size='sm'),
                dbc.InputGroup([
                    dbc.InputGroupText('Lean mass'), dbc.Input(id='input-lean-mass', disabled=True, type="text")
                ], class_name ='mb-2', size='sm'),
                dbc.InputGroup([
                    dbc.InputGroupText('Fat mass'), dbc.Input(id='input-fat-mass', disabled=True, type="text")
                ], class_name ='mb-2', size='sm'),
                html.Div([
                    dbc.Button('Calculate BMR', id='bmr-calculate', n_clicks=0, disabled=True, size='sm', color='primary'),
                ], className='d-grid gap-2 col-10 mx-auto')
                ]),
            ],
class_name='card border-secondary mb-3 mt-3')

# energy inputs
inputs_energy = dbc.Card(
    [
        dbc.CardHeader('Energy', style={'color' : 'green'}),
        dbc.CardBody(
            [
                dbc.InputGroup([
                    dbc.InputGroupText('Calorie deficit'), dbc.Input(id='input-calorie-deficit', type="number", min=0, max=1000, step=100, value=0)
                ], class_name ='mb-2', size='sm'),
                dbc.InputGroup([
                    dbc.InputGroupText('Plan duration in weeks'), dbc.Input(id='input-plan-duration', type="number", min=4, max=12, step=1, value=8)
                ], class_name ='mb-2', size='sm'),
                dbc.InputGroup([
                    dbc.InputGroupText('Activity level'), dbc.Select(id='input-activity-level', options=[
                        {'label' : level, "value" : count} for count, level in enumerate(activity_levels)
                    ], value=3)
                ], class_name ='mb-2', size='sm'),    
                dbc.InputGroup([
                    dbc.InputGroupText('Projected total weight loss'), dbc.Input(id='input-estimated-weight-loss', disabled=True)
                ], class_name ='mb-2', size='sm'),
                dbc.InputGroup([
                    dbc.InputGroupText('Projected new weight'), dbc.Input(id='input-estimated-new-weight', disabled=True)
                ], class_name ='mb-2', size='sm'),
                dbc.InputGroup([
                    dbc.InputGroupText('Daily steps'), dbc.Input(id='input-daily-steps', type='text', disabled=True)
                ], class_name ='mb-2', size='sm'),
                ]),
            ],
class_name='card border-secondary mb-3', id='inputs-energy', style={'display' : 'none'})

# macros inputs
inputs_macros = dbc.Card(
    [
        dbc.CardHeader('Macronutrients', style={'color' : 'green'}),
        dbc.CardBody(
            [
                dbc.InputGroup([
                    dbc.InputGroupText('Protein per kg'),  dbc.Input(id='input-protein-kg', type="number", min=1, max=3, step=0.1, value=2)
                ], class_name='mb-2', size='sm'),
                dbc.InputGroup([
                    dbc.InputGroupText('Fat per kg'),  dbc.Input(id='input-fat-kg', type="number", min=0.5, max=1, step=0.1, value=1)
                ], class_name='mb-2', size='sm'),
                html.Div(id='table-macros'),
                html.Div(id='macros-pie-chart')
                ]),
            ],
class_name='card border-secondary mb-3', id='inputs-macros', style={'display' : 'none'})

# results
results_calories = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4('here', style={'text-align' :'center'}, id='bmr-result-calories'),
                html.H4('here', style={'text-align' :'center'}, id='bmr-result-joules'),                
                ]),
            ],
class_name='card text-white bg-dark mb-3', style={'display' : 'none'}, id='results-calories')

results_weight_line_chart = dbc.Card(
    [
        dbc.CardHeader('Projected weekly bodyweight', style={'color' : 'green'}),
        dbc.CardBody(
            [
                html.Div(id='weight-line-chart')                
            ]
        )
    ],
class_name = 'card border-secondary mb-3', style={'display' : 'none'}, id='results-weight-line-chart')

results_tables = dbc.Card(
    [
        dbc.CardHeader('Energy needs', style={'color' : 'green'}),
        dbc.CardBody(
            [
                html.Div(id='table-energy-needs'),
                html.Div(id='table-weight-loss'),
            ]
        )
    ],
class_name='card border-secondary mb-3', id='results-tables', style={'display' : 'none'})


bmr_inputs = html.Div([
    html.Br(),
    html.H4(id='weight-line-chart-title', style={'color' : 'green', 'text-align' : 'center'}),        
])

# macros and weight loss tables
macros = html.Div([
    html.Br(),
    # html.Br(),
    html.H4(id='pie-chart-title', style={'color' : 'green', 'text-align' : 'center'}),
    html.Br(),

])

# application layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            inputs_body,
        ], sm=12, md=8, lg=6, xl=5),
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            results_calories,
        ], sm=12, md=8, lg=6, xl=5),
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            inputs_energy,
        ], sm=12, md=8, lg=6, xl=5),
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            results_tables
        ], sm=12, md=8, lg=6, xl=5),
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            results_weight_line_chart,
        ], sm=12, md=8, lg=6, xl=5),
    ], justify='center'), 
    dbc.Row([
        dbc.Col([
            inputs_macros,
        ], sm=12, md=8, lg=6, xl=5),
    ], justify='center'),    
    # junk
    dbc.Row([
        dbc.Col([
            bmr_inputs, macros
        ])
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

# callback for bmr calculate button state and lean and fat mass
@app.callback(
    Output('bmr-calculate', 'disabled'),
    Output('input-lean-mass', 'value'),
    Output('input-fat-mass', 'value'),
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
        return True, '', ''
    # we have all the inputs
    elif not any(elem is None for elem in required_inputs.get(bmr_formula_input_value)):
        if bmr_formula_input_value == '2':
            return False,\
                '{0:,.1f} kg'.format(input_weight_value*(100-input_bf_value)/100),\
                '{0:,.1f} kg'.format(input_weight_value*(input_bf_value)/100)
        return False, '', ''
    # calculate lean and fat mass if bodyfat is provided
    return True, '', ''

# callback for calorie levels
@app.callback(
    Output('table-energy-needs', 'children'),
    Output('table-weight-loss', 'children'),    
    Output('table-macros', 'children'),
    Output('bmr-result-calories', 'children'),
    Output('bmr-result-joules', 'children'),
    Output('macros-pie-chart', 'children'),
    Output('pie-chart-title', 'children'),
    Output('input-daily-steps', 'value'),
    Output('weight-line-chart', 'children'),
    Output('results-weight-line-chart', 'style'),
    Output('input-estimated-weight-loss', 'value'),
    Output('input-estimated-new-weight', 'value'),
    Output('results-calories', 'style'),
    Output('inputs-energy', 'style'),
    Output('inputs-macros', 'style'),
    Output('results-tables', 'style'),
    Input('bmr-calculate', 'n_clicks'),
    Input('input-calorie-deficit', 'value'),
    Input('input-activity-level', 'value'),
    Input('input-protein-kg', 'value'),
    Input('input-fat-kg', 'value'),
    Input('input-plan-duration', 'value'),
    State('bmr-formula-input', 'value'),
    State('input-age', 'value'),
    State('input-gender', 'value'),
    State('input-height', 'value'),
    State('input-weight', 'value'),
    State('input-bf', 'value'),
)
def calculate_bmr(n_clicks, deficit_value, activity_level_value, protein_kg_value, fat_kg_value,\
                  plan_duration_value,\
                  bmr_formula_input, input_age, input_gender, input_height, input_weight, input_bf):
    
    headers = ['Activity level', 'Maintenance', 'Deficit']
    macro_headers = ['Protein', 'Carbs', 'Fats']
    wl_headers = ['Energy deficit', 'Projected weekly weight loss']
    trigger = callback_context.triggered[0]['prop_id'].split('.')[0]   
    if trigger in ['bmr-calculate', 'input-calorie-deficit', 'input-activity-level', 'input-protein-kg', 'input-fat-kg', 'input-plan-duration']:
        _activity_levels = list(activity_levels.keys())
        # default deficit value
        if deficit_value is None:
            deficit_value = 0
        # default plan duration
        if plan_duration_value is None:
            plan_duration_value = 8
        # default input protein value
        if protein_kg_value is None:
            protein_kg_value = 2
        # default input fat value
        if fat_kg_value is None:
            fat_kg_value = 1
        bmr_result = bmr_engine(
            method=bmr_formula_input, age=input_age, gender=input_gender, height=input_height, weight=input_weight, bf=input_bf)
        calories_result = bmr_result * activity_levels.get(_activity_levels[int(activity_level_value)]) - deficit_value
        # weight line chart dataframe
        df_weight = pd.DataFrame({
            'Week' : [_ for _ in range(plan_duration_value+1)],
            'Weight' : [input_weight - (_ * weekly_weight_loss(deficit_value)) for _ in range(plan_duration_value+1)]
        })
        fig_weight = (
        px.bar(
            df_weight,
            x='Week',
            y='Weight',
            text='Weight'
            )
            .update_layout({
            'plot_bgcolor' : 'rgba(0, 0, 0, 0)',
            'paper_bgcolor' : 'rgba(0, 0, 0, 0)'},
            legend_title='', hovermode=False)
            .update_traces(marker_color='deepskyblue', marker_line_color='silver', marker_line_width=1, textposition='outside', texttemplate='%{y:.1f}', textfont_size=14, textangle=330)
            .update_yaxes(range=[input_weight-15, input_weight+5], fixedrange=True, tick0=input_weight, dtick=5, visible=False)
            .update_xaxes(fixedrange=True)
        )

        # macros graph dataframe
        _protein = (input_weight * protein_kg_value * 4) / calories_result
        _fat = (input_weight * fat_kg_value * 4) / calories_result
        _carbs = 1 - (_protein + _fat)
        df_macros = pd.DataFrame({
            'macro' : macro_headers,
            'macro_pct' : [_protein, _carbs, _fat]
        })
        # macros pie chart
        macros_fig = go.Figure(data=[go.Pie(
            labels=df_macros['macro'], 
            values=df_macros['macro_pct'],
            textinfo='label+percent',
            hoverinfo='skip',
            showlegend=False,
            hole=.4)])
        macros_fig.update_traces(textfont_size=15, marker={'colors' : ['deepskyblue', 'lightpink', 'forestgreen']})
        return \
            bmr_results_table(headers, bmr_result, deficit=deficit_value),\
            weight_loss_table(wl_headers, bmr_result, activity_level=_activity_levels[int(activity_level_value)], deficit=deficit_value),\
            macros_table(macro_headers, bmr_result, weight=input_weight, protein_kg=protein_kg_value, fat_kg=fat_kg_value,\
                          activity_level=_activity_levels[int(activity_level_value)], deficit=deficit_value),\
            '{0:,.0f} kcal'.format(calories_result),\
            '{0:,.0f} kJ'.format(calories_result*4.184),\
            html.Div(dcc.Graph(figure=macros_fig)),\
            '',\
            '{0:,.0f}'.format(max(calories_to_steps(calories_result-(bmr_result*1.2), input_weight),0)),\
            html.Div(dcc.Graph(figure=fig_weight, config={'displayModeBar': False})),\
            {'display' : 'block'},\
            '{0:,.1f} kg'.format(weekly_weight_loss(deficit_value) * plan_duration_value),\
            '{0:,.1f} kg'.format(input_weight - weekly_weight_loss(deficit_value) * plan_duration_value),\
            *[{'display' : 'block'} for i in range(4)]
    return \
        html.Br(),\
        html.Br(),\
        html.Br(),\
        html.Br(),\
        html.Br(),\
        html.Br(),\
        '',\
        '',\
        html.Br(),\
        {'display' : 'none'},\
        '',\
        '',\
        *[{'display' : 'none'} for i in range(4)]

# disable input buttons if no proper input is available
@app.callback(
    Output('input-calorie-deficit', 'disabled'),
    Output('input-plan-duration', 'disabled'),
    Output('input-activity-level', 'disabled'),
    Output('input-protein-kg', 'disabled'),
    Output('input-fat-kg', 'disabled'),    
    Input('bmr-calculate', 'disabled'),
)
def disable_buttons(bmr_calculated_disabled):
    if bmr_calculated_disabled:
        return [True for _ in range(5)]
    return [False for _ in range(5)]

# uncomment below for development and debugging
if __name__ == '__main__':
    app.run_server(port='8051', host='0.0.0.0', debug=True)
