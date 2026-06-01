from flask import Flask, request, Response
import requests
import json
import time

app = Flask(__name__)

# Your working PHP backend
API_BASE = "https://dtz-tools.xo.je"

# Browser-like headers to avoid any blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
}

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
def proxy(path):
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        resp = Response()
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return resp, 200

    # Build target URL
    target = f"{API_BASE}/{path}"
    if request.query_string:
        target += f"?{request.query_string.decode()}"

    # Retry up to 2 times
    for attempt in range(3):
        try:
            if request.method == 'GET':
                r = requests.get(target, headers=HEADERS, timeout=15)
            else:
                r = requests.post(target, json=request.get_json(), headers=HEADERS, timeout=15)

            # Return the response with CORS header
            response = Response(r.content, status=r.status_code, mimetype='application/json')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        except requests.exceptions.RequestException as e:
            if attempt == 2:
                return Response(
                    json.dumps({"error": f"Proxy error: {str(e)}"}),
                    status=502,
                    mimetype='application/json'
                )
            time.sleep(1)
            continue

# For local testing
if __name__ == '__main__':
    app.run(debug=True, port=5000)
