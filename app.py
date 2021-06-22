import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

data = pd.read_csv("basedados.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Murilo"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Img(src="./assets/logo.png", className="header-image"),
                html.P(
                    children="Apresentação de dashboard",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in np.sort(data.region.unique())
                            ],
                            value="Midsouth",
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                ),

                html.Div(
                    children=[
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                            className="dropdown"
                        ),
                    ],
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Img(src="./assets/logo-d.png", className="header-image"),
                html.P(
                    children="Dashboard por Murilo Holtz Foltran para teste de front-end com Python, HTML, CSS para Akaer.",
                ),
                dcc.Link("Código - Github", href="https://github.com/muriloholtz/analytics-app/", className="link"
                ),
            ],
            className="footer",
        ),
    ]
)


@app.callback(
    [Output("price-chart", "figure"), Output("volume-chart", "figure")],
    [
        Input("region-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(region, start_date, end_date):
    mask = (
        (data.region == region)
        & (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AveragePrice"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "<b>Gráfico de preços<b>",
                "x": 3,
                "font": {"color":"#717171", "size": 20, "family": "Lato"},
                "xanchor": "center",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Total Volume"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {
                "text": "<b>Gráfico de vendas<b>",
                "x": 3, 
                "font": {"color":"#717171", "size": 20, "family": "Lato"},
                "xanchor": "center"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return volume_chart_figure, price_chart_figure

if __name__ == "__main__":
    app.run_server(debug=True)
