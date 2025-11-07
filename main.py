from flask import Flask, request, jsonify, Response
from requests import get
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Proxy Python 1.0 (Flask) funcionando. Usa /proxy?url=<URL>"

@app.route('/proxy')
def proxy():
    print("INicio")
    target_url = request.args.get("url")
    print("URL recibida:", target_url)
    if not target_url:
        return jsonify({"error": "Falta el parámetro 'url'"}), 400
    try:
        print("📡 Solicitando:", target_url)
        # timeout en segundos
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'smn.conagua.gob.mx',
            'Referer': 'https://smn.conagua.gob.mx/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        }
        target_url = target_url.replace("BBB","%")
        print("URL procesada:", target_url)
        target_url = target_url.split("AAA")
        print("URL dividida:", target_url)
        url_enviar = target_url[0]+"&"+target_url[1]+"&"+target_url[2]
        print("URL a enviar:", url_enviar)
        resp = requests.get(
            url_enviar,
            headers=headers,
            timeout=25
        )
        print("✅ Recibido:", resp.status_code)
        # reenvía el contenido y el content-type
        return Response(resp.text, status=resp.status_code, content_type=resp.headers.get('content-type'))
    except requests.exceptions.Timeout:
        print("⏰ Timeout alcanzado en Render")
        return jsonify({"error": "Timeout: el servidor SMN no respondió a tiempo"}), 504

    except requests.exceptions.SSLError as e:
        print("❌ Error SSL:", e)
        return jsonify({"error": "Error SSL en la conexión al servidor SMN"}), 502

    except requests.exceptions.RequestException as e:
        print("❌ Error general en requests:", e)
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        print("💥 Error inesperado:", e)
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500

if __name__ == '__main__':
    # Solo para desarrollo local; para producción usar gunicorn
    app.run(host='0.0.0.0', port=5000)