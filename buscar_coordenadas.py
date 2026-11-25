import requests

def buscar_coordenadas(direccion):

    respuesta = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={
            "q": direccion,
            "format": "json",
            "limit": 1
        },
        headers={
            "User-Agent": "MapMyTok-ProyectoEducativo/0.1"
        },
        timeout=10
    )

    respuesta.raise_for_status()
    resultados = respuesta.json()

    if not resultados:
        return None

    lugar = resultados[0]

    return {
        "nombre": lugar["display_name"],
        "latitud": float(lugar["lat"]),
        "longitud": float(lugar["lon"])
    }


# Probar la función
if __name__ == "__main__":

    direccion = "Plaza del Conde de Casal, 6, Madrid, España"

    resultado = buscar_coordenadas(direccion)

    if resultado:
        print("Lugar encontrado:", resultado["nombre"])
        print("Latitud:", resultado["latitud"])
        print("Longitud:", resultado["longitud"])
    else:
        print("No se ha encontrado el lugar.")