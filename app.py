
from dash import Dash, html, dcc, Input, Output, State, ctx, no_update
import plotly.express as px
import pandas as pd
from urllib.parse import urlparse
from probar_tiktok import obtener_descripcion
from procesar_texto import extraer_pista_ubicacion
from buscar_coordenadas import buscar_coordenadas

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
    },
    {
        "nombre": "Hotel Claridge",
        "latitud": 40.4062862,
        "longitud": -3.6693722,
        "categoria": "Restaurantes"
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
    html.H3("Buscar ubicación del lugar"),

    dcc.Input(
        id="direccion-busqueda",
        type="text",
        placeholder="Ej. Hotel Claridge, Madrid",
        style={"width": "350px"}
    ),

    html.Button("Buscar ubicación", id="boton-buscar"),

    html.Div(id="resultado-busqueda"),
    dcc.Store(id="ubicacion-encontrada"),
    dcc.Store(id="lugares-confirmados", data=[]),
    html.Button("Confirmar ubicación", id="boton-confirmar"),
    html.Div(id="mensaje-confirmacion"),
    dcc.Graph(id="mapa-lugares", figure=mapa)
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


# Buscar las coordenadas de un lugar
@app.callback(
    Output("resultado-busqueda", "children"),
    Output("ubicacion-encontrada", "data"),
    Input("boton-buscar", "n_clicks"),
    State("direccion-busqueda", "value"),
    prevent_initial_call=True
)
def buscar_ubicacion(n_clicks, direccion):

    if not direccion or not direccion.strip():
        return "Introduce el nombre o la dirección de un lugar.", None

    try:
        resultado = buscar_coordenadas(direccion.strip())
    except Exception:
        return "No se ha podido consultar el servicio de ubicaciones.", None

    if resultado:
        return html.Div([
            html.H4("Lugar encontrado:"),
            html.P(resultado["nombre"]),
            html.P(f"Latitud: {resultado['latitud']}"),
            html.P(f"Longitud: {resultado['longitud']}")
        ]), resultado

    return "No se ha encontrado ningún lugar con esa dirección.", None



# Confirmar la ubicación encontrada
@app.callback(
    Output("mensaje-confirmacion", "children"),
    Output("lugares-confirmados", "data"),
    Input("boton-confirmar", "n_clicks"),
    Input("boton-buscar", "n_clicks"),
    State("ubicacion-encontrada", "data"),
    State("lugares-confirmados", "data"),
    prevent_initial_call=True
)
def confirmar_ubicacion(n_clicks_confirmar, n_clicks_buscar, ubicacion, confirmados):

    # Borrar la confirmación al iniciar una nueva búsqueda
    if ctx.triggered_id == "boton-buscar":
        return "", no_update

    if not ubicacion:
        return "Primero debes buscar una ubicación.", no_update

    # Recuperar los lugares confirmados anteriormente
    confirmados = confirmados or []

    # Preparar el nuevo lugar
    nuevo_lugar = {
        "nombre": ubicacion["nombre"],
        "latitud": ubicacion["latitud"],
        "longitud": ubicacion["longitud"],
        "categoria": "Sin categoría"
    }

    # Evitar añadir dos veces el mismo lugar
    for lugar in confirmados:
        if (lugar["latitud"] == nuevo_lugar["latitud"]
                and lugar["longitud"] == nuevo_lugar["longitud"]):
            return "Este lugar ya está confirmado.", no_update

    # Añadir el lugar a nuestra lista
    confirmados.append(nuevo_lugar)

    return "¡Ubicación confirmada y añadida a la lista!", confirmados

# Actualizar el mapa con los lugares confirmados
@app.callback(
    Output("mapa-lugares", "figure"),
    Input("lugares-confirmados", "data")
)
def actualizar_mapa(confirmados):

    # Empezar con los lugares de ejemplo
    lugares_mapa = lugares.copy()

    # Añadir los lugares confirmados por el usuario
    if confirmados:
        nuevos_lugares = pd.DataFrame(confirmados)

        lugares_mapa = pd.concat(
            [lugares_mapa, nuevos_lugares],
            ignore_index=True
        )

    # Evitar marcadores duplicados en las mismas coordenadas
    lugares_mapa = lugares_mapa.drop_duplicates(
        subset=["latitud", "longitud"]
    )

    # Crear el mapa actualizado
    mapa_actualizado = px.scatter_map(
        lugares_mapa,
        lat="latitud",
        lon="longitud",
        hover_name="nombre",
        color="categoria",
        zoom=12,
        center={"lat": 40.4168, "lon": -3.7038},
        map_style="carto-positron"
    )

    return mapa_actualizado

if __name__ == "__main__":
    app.run(debug=True)
