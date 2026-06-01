from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)

# Your InfinityFree PHP API base URL
INFINITY_API = "https://dtz-tools.xo.je"   # <-- CHANGE

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
def proxy(path):
    if request.method == 'OPTIONS':
        resp = Response()
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return resp, 200

    target = f"{INFINITY_API}/{path}"
    if request.query_string:
        target += f"?{request.query_string.decode()}"

    try:
        if request.method == 'GET':
            r = requests.get(target, timeout=20)
        else:
            r = requests.post(target, json=request.get_json(), timeout=20)

        response = Response(r.content, status=r.status_code, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')
