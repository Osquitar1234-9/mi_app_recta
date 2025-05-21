import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import os

app = dash.Dash(__name__)
server = app.server  # Necesario para desplegar en Render

app.layout = html.Div([
    html.H1("Interactividad con una recta"),

    html.Label("Pendiente (m):"),
    dcc.Slider(
        id='pendiente-slider',
        min=-10,
        max=10,
        step=0.1,
        value=1,
        marks={i: str(i) for i in range(-10, 11)}
    ),
    html.Br(),

    html.Label("Ordenada al origen (b):"),
    dcc.Input(id='ordenada-input', type='number', value=0),

    html.Br(), html.Br(),
    html.Label("X-intersección:"),
    dcc.Input(id='x-interseccion', type='text', value='', readOnly=True),

    dcc.Graph(id='graph')
])

@app.callback(
    [Output('x-interseccion', 'value'),
     Output('graph', 'figure')],
    [Input('pendiente-slider', 'value'),
     Input('ordenada-input', 'value')]
)
def update_graph(m, b):
    if m == 0:
        x_int = 'Infinito'
    else:
        if b is None:
            b = 0
        x_int = round(-b / m, 2)

    x_range = np.linspace(-50, 50, 400)
    y_values = m * x_range + b

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_range, y=y_values, mode='lines', name='Recta'))

    fig.update_layout(
        xaxis=dict(range=[-50, 50], title='X'),
        yaxis=dict(range=[-50, 50], title='Y'),
        title='Gráfico de la recta',
        plot_bgcolor='white'
    )

    return str(x_int), fig

# 🔥 IMPORTANTE: este bloque permite que Render detecte y use el puerto correctamente
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=True)
