import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import numpy as np

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Visualizador de recta: y = mx + b", style={"textAlign": "center"}),

    html.Div([
        html.Label("Pendiente (m):"),
        dcc.Slider(
            id="m-slider",
            min=-10,
            max=10,
            step=0.1,
            value=1,
            marks={i: str(i) for i in range(-10, 11)},
            tooltip={"placement": "bottom", "always_visible": True}
        ),
    ], style={"margin": "20px"}),

    html.Div([
        html.Label("Ordenada al origen (b):"),
        dcc.Input(id="b-input", type="number", value=0, step=1)
    ], style={"margin": "20px"}),

    html.Div([
        html.Label("Intersección con el eje X (x cuando y=0):"),
        dcc.Input(id="x-intercept", type="text", readOnly=True)
    ], style={"margin": "20px"}),

    dcc.Graph(id="line-graph"),

    html.Div(id="warning-message", style={"color": "red", "fontWeight": "bold"})
])

@app.callback(
    Output("line-graph", "figure"),
    Output("x-intercept", "value"),
    Output("warning-message", "children"),
    Input("m-slider", "value"),
    Input("b-input", "value")
)
def update_graph(m, b):
    x_range = np.linspace(-50, 50, 500)
    y_values = m * x_range + b

    if m == 0:
        intercept_text = "Infinita (recta horizontal)"
        warning = "La pendiente es cero. No hay intersección con el eje X."
    else:
        x_int = -b / m
        intercept_text = f"{x_int:.2f}"
        warning = ""

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_range, y=y_values, mode='lines', name='Recta'))
    fig.update_layout(
        title="Gráfico de la recta y = mx + b",
        xaxis=dict(range=[-50, 50], title='x'),
        yaxis=dict(range=[-50, 50], title='y'),
        height=600
    )

    return fig, intercept_text, warning

if __name__ == "__main__":
    import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port, debug=True)
