from probar_tiktok import obtener_descripcion

def extraer_pista_ubicacion(descripcion):

    # Comprobar si aparece el símbolo de ubicación
    if "📍" not in descripcion:
        return None

    # Obtener el texto que aparece después del símbolo
    texto = descripcion.split("📍", 1)[1]

    # Eliminar la información que aparece después del precio
    texto = texto.split("💶", 1)[0]

    return texto.strip()

if __name__ == "__main__":

    url = "https://www.tiktok.com/@lara_mamaestra/video/7711448032939707680"

    descripcion = obtener_descripcion(url)

    if descripcion:
        lugar = extraer_pista_ubicacion(descripcion)

        if lugar:
            print("Información de ubicación detectada:")
            print(lugar)
        else:
            print("No se ha encontrado una pista de ubicación.")
    else:
        print("No se ha podido obtener la descripción del vídeo.")
