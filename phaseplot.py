from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import numpy as np
from numpy import cos, sin, tan, tanh, cosh, sinh, arccos, arcsin, exp, log
import pandas  # Required for plotly
import sympy as sp
import plotly.figure_factory as ff
import plotly.express as px
from plotly.subplots import make_subplots
import gunicorn

# TODO: Remove numpy dependency
# TODO: Add x and y range sliders
# TODO: Add perturbation g(t)

my_font = 'normal 20px monospace, Arial, sans-serif'

def plot_vf(input_str, x_range=[-5, 5], y_range=[-5, 5], grid=[21, 21]):
    """Plot vector field for a 2x2 matrix system of ODEs.

    Inspiration: https://gist.github.com/nicoguaro/6767643
    """
    X = np.linspace(x_range[0], x_range[1], grid[0])
    Y = np.linspace(y_range[0], y_range[1], grid[1])
    x , y  = np.meshgrid(X, Y)  # create a grid
    # dxdt = float(A[0,0])*x + float(A[0,1])*y + (1/5)*y**2
    # dydt = float(A[1,0])*x + float(A[1,1])*y  + (3/10)*x**2 + (1/5)*y**2
    dxdt = eval(input_str.split(';')[0])
    dydt = eval(input_str.split(';')[1])
    norm = np.hypot(dxdt, dydt)  # Length of each arrow
    norm[norm == 0] = 1.0  # Avoid zero division errors 
    arrow_len = 3.0  # Adjust this depending on how long you want the arrows
    dxdt = (dxdt / norm) * arrow_len  # Normalize each arrow to have length arrow_len
    dydt = (dydt / norm) * arrow_len
    fig = ff.create_quiver(x, y, dxdt, dydt)
    return fig


app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('Phase Plotter', id='title'),
    html.H4('Author: Isaac Lee | Source: https://github.com/isaacjeffersonlee/phase-dash',
        id='author-and-source-subtitle'),
    html.H2('Input 2D System', id='system-input-subtitle'),
    dcc.Markdown("""
        Input the *expanded* system, using a semi-colon
        to denote the divide between rows. I.e if we have:    
           
        \[x', y'\]^T = A\[x, y\]^T + \[g1(x,y), g2(x,y)\]^T  
             
        Then our input would be:
        a11\*x + a12\*y + g1(x,y); a21\*x + a22\*y + g2(x,y)  

        Where g1(x,y) and g2(x,y) are expressions that can be 
        interpreted by python, e.g (1/5) \* x\*\*2 or cos(x) e.t.c
    """),
    dcc.Textarea(
        id='matrix-input',
        value='-1*x + 0*y + (1/5)*y**2; 0*x + 1*y + (3/10)*x**2 + (1/5)*y**2',
        style={'width': '100%', 'height': 200, 'font': my_font}
    ),
    html.Button('Run', 
        id='run-button',
        n_clicks=0,
        className="my-button"
    ),
    dcc.Loading(
        id="loading-spinner",
        type="cube",
        color="black",
        children=[
            dcc.Graph(id='graph', style={'width': '50vh', 'height': '50vh'})
        ]
    ),
])

@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='run-button', component_property='n_clicks'),
    State(component_id='matrix-input', component_property='value')
)
def update_output(n_clicks, value):
    # Prevent callback errors when we aren't finished inputing our matrix
    fig = plot_vf(input_str=value,
            x_range=[-5, 5], y_range=[-5, 5],
            grid=[21, 21])
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)




