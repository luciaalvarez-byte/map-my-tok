
from dash import Dash, html, dcc
import plotly.express as px

app = Dash(__name__)

mapa = px.scatter_map(
    lat=[40.4168],
    lon=[-3.7038],
    hover_name=["Madrid (ejemplo)"],
    zoom=10,
    center={"lat": 40.4168, "lon": -3.7038},
    map_style="carto-positron"
    )

app.layout = html.Div([
    html.H1("MapMyTok"),
    html.P("Organiza tus lugares guardados de TikTok en un mapa interactivo."),
    dcc.Graph(figure=mapa)
])

if __name__ == "__main__":
    app.run(debug=True)
