
from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div([
    html.H1("MapMyTok"),
    html.P("Organiza tus lugares guardados de TikTok en un mapa interactivo.")
])

if __name__ == "__main__":
    app.run(debug=True)
