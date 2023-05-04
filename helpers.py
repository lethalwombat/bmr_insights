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

def bmr_engine(**kwargs) -> float:
    if kwargs.get('method') == '1':
        s = 5
        if kwargs.get('gender') == '2': # Females
            s = -161
        return 10 * kwargs.get('weight') + 6.25 * kwargs.get('height') - 5 * kwargs.get('age') + s  
    elif kwargs.get('method') == '2':
        return 370 + 21.6 * (1-kwargs.get('bf')/100) * kwargs.get('weight')
    return -1

def bmr_results_table(headers: list, bmr_result: int, deficit=500, blank=False, bordered=True):
    # generate headers
    table_header = [html.Thead(
        html.Tr([
            html.Th(header) for header in headers
        ])
    )]
    # generate table body
    table_row = lambda x, y, z : html.Tr([html.Td(x), html.Td(y), html.Td(z)])

    table_body = [html.Tbody([
            table_row(k, '{0:,.0f} kcal'.format(round(bmr_result * activity_levels[k], 0)), '{0:,.0f} kcal'.format(round(bmr_result * activity_levels[k] - deficit, 0)))\
                  for k in activity_levels])
    ]
    # blank table is requested
    if blank:
        table_body = [html.Tbody([
            table_row('', '', '') for k in activity_levels])
        ]
    
    return dbc.Table(table_header + table_body, bordered=bordered)


def macros_table(headers: list, bmr_result: int, deficit=500, weight=90, activity_level='Moderately active (1.55)', protein_kg=1, fat_kg=1, blank=False, bordered=True):
    # calculate macros
    energy_total = bmr_result * activity_levels.get(activity_level) - deficit
    energy_protein = weight * protein_kg * 4
    energy_fat = weight * fat_kg * 9
    energy_carbs = energy_total - energy_protein - energy_fat

    # generate headers
    table_header = [html.Thead(
        html.Tr([
            html.Th(header) for header in headers
        ])
    )]
    # generate table body
    table_row = lambda x, y, z : html.Tr([html.Td(x), html.Td(y), html.Td(z)])

    table_body = [html.Tbody([
            table_row('{0:,.0f} g'.format(round(energy_protein/4, 0)), '{0:,.0f} g'.format(round(energy_carbs/4, 0)), '{0:,.0f} g'.format(round(energy_fat/9, 0))),
        ])]
    # blank table is requested
    if blank:
        table_body = [html.Tbody([
            table_row('', '', '') for k in range(3)])
        ]
    return dbc.Table(table_header + table_body, bordered=bordered)