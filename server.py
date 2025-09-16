# -*- coding: utf-8 -*-

from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

@app.route('/', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy():
    # ?url= parametresinden hedef URL'yi al
    target_url = request.args.get("url")
    if not target_url:
        return {"error": "Missing 'url' query parameter"}, 400

    # Orijinal header’ları al (Host hariç)
    headers = {k: v for k, v in request.headers if k.lower() != "host"}
    data = request.get_data()

    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=data,
            allow_redirects=False,
        )
    except Exception as e:
        return {"error": str(e)}, 500

    # İstemciye döndürmeden önce bazı header’ları çıkar
    excluded_headers = ["content-encoding", "transfer-encoding", "connection"]
    response_headers = [
        (name, value) for (name, value) in resp.headers.items()
        if name.lower() not in excluded_headers
    ]

    return Response(resp.content, resp.status_code, response_headers)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render otomatik PORT veriyor
    app.run(host="0.0.0.0", port=port, debug=False)
