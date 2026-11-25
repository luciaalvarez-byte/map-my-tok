
import subprocess
import sys


def obtener_descripcion(url):
    resultado = subprocess.run(
        [
            sys.executable,
            "-m", "yt_dlp",
            "--skip-download",
            "--print", "description",
            url
        ],
        capture_output=True,
        text=True
    )

    if resultado.returncode == 0:
        return resultado.stdout.strip()
    else:
        return None


# Probar la función con un vídeo real
if __name__ == "__main__":
    url = "https://www.tiktok.com/@marcia_ur/video/7643657957426597142"

    descripcion = obtener_descripcion(url)

    if descripcion:
        print(descripcion)
    else:
        print("No se ha podido obtener la descripción.")
