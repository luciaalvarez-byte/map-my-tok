
from probar_tiktok import obtener_descripcion
from procesar_texto import extraer_pista_ubicacion
from buscar_coordenadas import buscar_coordenadas

# Vídeo de prueba
url = "https://www.tiktok.com/@lara_mamaestra/video/7711448032939707680"

# 1. Obtener descripción
descripcion = obtener_descripcion(url)

if descripcion:

    # 2. Detectar posible ubicación
    pista = extraer_pista_ubicacion(descripcion)

    if pista:
        print("Posible ubicación:", pista)

        # 3. Pedir al usuario que confirme la dirección
        direccion = input("Introduce la dirección para buscarla: ")

        if direccion.strip():
            # 4. Buscar coordenadas
            resultado = buscar_coordenadas(direccion)

            if resultado:
                print("Lugar encontrado:", resultado["nombre"])
                print("Latitud:", resultado["latitud"])
                print("Longitud:", resultado["longitud"])
            else:
                print("No se ha encontrado el lugar.")
    else:
        print("No se ha detectado ninguna ubicación.")
else:
    print("No se ha podido obtener la descripción.")