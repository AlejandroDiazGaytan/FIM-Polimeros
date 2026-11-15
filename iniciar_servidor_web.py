"""
Script para lanzar el servidor web local de la Presentación Prezi Dinámica
Abre automáticamente la aplicación en el navegador web predeterminado.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def main():
    os.chdir(DIRECTORY)
    url = f"http://localhost:{PORT}/index.html"
    print("=" * 70)
    print("PRESENTACIÓN PREZI INTERACTIVA - CIENCIA DE POLÍMEROS")
    print(f"Servidor iniciado en: {url}")
    print("Directorio de trabajo:", DIRECTORY)
    print("Presiona Ctrl + C para detener el servidor.")
    print("=" * 70)
    
    webbrowser.open(url)

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido correctamente.")
        sys.exit(0)
    except OSError as e:
        if e.errno == 10048: # Puerto ocupado
            alt_port = 8080
            url_alt = f"http://localhost:{alt_port}/index.html"
            print(f"Puerto 8000 en uso. Probando en {alt_port}: {url_alt}")
            webbrowser.open(url_alt)
            with socketserver.TCPServer(("", alt_port), Handler) as httpd:
                httpd.serve_forever()
        else:
            raise

if __name__ == "__main__":
    main()
