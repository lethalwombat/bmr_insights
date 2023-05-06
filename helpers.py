import numpy as np
import dash_bootstrap_components as dbc
from dash import html

activity_levels = {
    'BMR' : 1.0,
    'Sedentary (1.2)' : 1.2,
    'Lightly active (1.375)' : 1.375,
    'Moderately active (1.55)' : 1.55,
    'Very active (1.725)' : 1.725,
    'Extra active (1.9)' : 1.9,
}

# table headers
generate_table_header = lambda headers : [html.Thead(html.Tr([html.Th(header) for header in headers]))]

# table row
blank_row = lambda x : html.Tr([html.Td('') for _ in range(x)])
table_row = lambda x, y, z : html.Tr([html.Td(x), html.Td(y), html.Td(z)])

def bmr_engine(**kwargs) -> float:
    if kwargs.get('method') == '1':
        s = 5
        if kwargs.get('gender') == '2': # Females
            s = -161
        return 10 * kwargs.get('weight') + 6.25 * kwargs.get('height') - 5 * kwargs.get('age') + s  
    elif kwargs.get('method') == '2':
        return 370 + 21.6 * (1-kwargs.get('bf')/100) * kwargs.get('weight')
    return -1

def blank_table(headers: list, rows:int, bordered=True):
    table_header = generate_table_header(headers)
    table_body = [html.Tbody([
            blank_row(len(headers)) for _ in range(rows)])
        ]
    return dbc.Table(table_header + table_body, bordered=bordered)

def bmr_results_table(headers: list, bmr_result: int, deficit=500, bordered=True):
    # generate headers
    table_header = generate_table_header(headers)

    # table body
    table_body = [html.Tbody([
            table_row(k, '{0:,.0f} kcal'.format(round(bmr_result * activity_levels[k], 0)), '{0:,.0f} kcal'.format(round(bmr_result * activity_levels[k] - deficit, 0)))\
                  for k in activity_levels])
    ]    
    return dbc.Table(table_header + table_body, bordered=bordered)


def macros_table(headers: list, bmr_result: int, deficit=500, weight=90, activity_level='Moderately active (1.55)', protein_kg=1, fat_kg=1, bordered=True):
    # calculate macros
    energy_total = bmr_result * activity_levels.get(activity_level) - deficit
    energy_protein = weight * protein_kg * 4
    energy_fat = weight * fat_kg * 9
    energy_carbs = energy_total - energy_protein - energy_fat

    # generate headers
    table_header = generate_table_header(headers)

    # generate table body
    table_body = [html.Tbody([
            table_row('{0:,.0f} g'.format(round(energy_protein/4, 0)), '{0:,.0f} g'.format(round(energy_carbs/4, 0)), '{0:,.0f} g'.format(round(energy_fat/9, 0))),
        ])]
    return dbc.Table(table_header + table_body, bordered=bordered)

def weight_loss_table(headers: list, bmr_result: int, deficit=500, activity_level='Moderately active (1.55)', bordered=True):
    # calculate metrics
    weekly_weight_loss = (deficit * 7) / 7700
    energy_deficit = deficit / (bmr_result * activity_levels.get(activity_level))

    # generate headers
    table_header = generate_table_header(headers)
    table_row = lambda x, y : html.Tr([html.Td(x), html.Td(y)])

    # generate table body
    table_body = [html.Tbody([
            table_row('{:.1%}'.format(energy_deficit), '{0:,.3f} kg'.format(weekly_weight_loss)) for _ in range(1)])
        ]
    return dbc.Table(table_header + table_body, bordered=bordered)


def calories_to_steps(calories, weight):
    per_step = (weight * 0.55) / 1000
    return calories / per_step
