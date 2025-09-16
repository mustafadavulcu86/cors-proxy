# -*- coding: utf-8 -*-

from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

@app.route('/<path:url>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy(url):
    target_url = f"https://{url}"

    headers = {k: v for k, v in request.headers if k.lower() != "host"}
    data = request.get_data()

    resp = requests.request(
        method=request.method,
        url=target_url,
        headers=headers,
        params=request.args,
        data=data
    )

    excluded_headers = ["content-encoding", "transfer-encoding", "connection"]
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    return Response(resp.content, resp.status_code, headers)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render bize PORT env veriyor
    app.run(host="0.0.0.0", port=port, debug=False)
