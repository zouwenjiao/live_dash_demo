import dash
import dash_html_components as html
import dash_core_components as dcc
import altair as alt
import vega_datasets

app = dash.Dash(__name__, assets_folder='assets')
server = app.server

app.title = 'Dash App demo'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def make_plot(x_axis = 'Displacement',
            y_axis = 'Cylinders'):

    # Create a plot of the Displacement and the Horsepower of the cars dataset
    
    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0, 
                #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                # titles are by default vertical left of axis so we need to hack this 
                #"titleAngle": 0, # horizontal
                #"titleY": -10, # move it up
                #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }

# register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)

# enable the newly registered theme
    alt.themes.enable('mds_special')
#alt.themes.enable('none') # to return to default
    chart = alt.Chart(vega_datasets.data.cars.url).mark_point(size=90).encode(
                alt.X(x_axis,
                type = 'quantitative',
                title = x_axis),
                alt.Y(y_axis,
                type = 'quantitative',
                title = 'Horsepower (h.p.)'),
                tooltip = ['Horsepower:Q', 'Displacement:Q']
            ).properties(title='Horsepower vs. Displacement',
                        width=500, height=350).interactive()

    return chart


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='700',
        width='1000',
        style={'border-width': '5px'},

        ################ The magic happens here
        srcDoc=make_plot().to_html()
        ################ The magic happens here
        ),

    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Miles_per_Gallon', 'value': 'Miles_per_Gallon'},
            {'label': 'Cylinders', 'value': 'Cylinders'},
            {'label': 'Displacement', 'value': 'Displacement'},
    # Missing option here
        ],
        value='Displacement',
        style=dict(width='45%',
                    verticalAlign="middle"),
        multi=True
          ),  
    html.Div(id='dd-output-container')
])


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
