
from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd
from urllib.parse import urlparse
from probar_tiktok import obtener_descripcion
from procesar_texto import extraer_pista_ubicacion

app = Dash(__name__)

# Lugares de ejemplo para probar la aplicación
lugares = pd.DataFrame([
    {
        "nombre": "Chocolatería San Ginés",
        "latitud": 40.4167,
        "longitud": -3.7074,
        "categoria": "Cafeterías"
    },
    {
        "nombre": "Parque del Retiro",
        "latitud": 40.4153,
        "longitud": -3.6844,
        "categoria": "Naturaleza"
    },
    {
        "nombre": "Museo del Prado",
        "latitud": 40.4138,
        "longitud": -3.6921,
        "categoria": "Cultura"
    }
])

mapa = px.scatter_map(
    lugares,
    lat="latitud",
    lon="longitud",
    hover_name="nombre",
    color="categoria",
    zoom=12,
    center={"lat": 40.4168, "lon": -3.7038},
    map_style="carto-positron"
)


app.layout = html.Div([
    html.H1("MapMyTok"),
    html.P("Organiza tus lugares guardados de TikTok en un mapa interactivo."),

    html.H3("Añadir un lugar"),

    dcc.Input(
        id="url-tiktok",
        type="url",
        placeholder="Pega aquí la URL de TikTok",
        style={"width": "350px"}
    ),

    html.Button("Añadir lugar", id="boton-anadir"),
    html.Div(id="mensaje-url"),

    dcc.Graph(figure=mapa)
])


@app.callback(
    Output("mensaje-url", "children"),
    Input("boton-anadir", "n_clicks"),
    State("url-tiktok", "value"),
    prevent_initial_call=True
)

def comprobar_url(n_clicks, url):
    if not url:
        return "Introduce primero una URL de TikTok."

    # Analizar la dirección web
    enlace = urlparse(url.strip())

    # Dominios de TikTok que aceptamos
    dominios_validos = [
        "www.tiktok.com",
        "tiktok.com",
        "vm.tiktok.com",
        "vt.tiktok.com",
        "m.tiktok.com"
    ]

    if enlace.scheme not in ["http", "https"] or enlace.hostname not in dominios_validos:
        return "El enlace introducido no es una URL válida de TikTok."

    
    # Intentar obtener la descripción del vídeo
    descripcion = obtener_descripcion(url)

    
    if descripcion:

        # Buscar una posible ubicación en la descripción
        pista = extraer_pista_ubicacion(descripcion)

        return html.Div([
            html.H4("Descripción del vídeo:"),
            html.P(descripcion),

            html.H4("Posible ubicación:"),
            html.P(
                pista if pista
                else "No se ha encontrado una pista de ubicación."
            )
        ])

    else:
        return "No se ha podido obtener la descripción del vídeo."



if __name__ == "__main__":
    app.run(debug=True)
