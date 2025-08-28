#!/usr/bin/python3

from flask import Flask, request, make_response
from prometheus_client import generate_latest, Counter, Gauge, Histogram
import os

app = Flask(__name__)

requests_for_headers = Counter(
    'demo_http_requests_total',
    'Total number of HTTP requests for headers',
    ['method', 'endpoint']
)

# Decoration
@app.route('/headers')
def my_headers():

    # For this endpoint call only let's get the count of requests we've had
    requests_for_headers.labels(method='GET', endpoint='/headers').inc()

    header_info = "<h2>Headers From Client</h2><ul>"
    for header, val in request.headers.items():
        header_info += f"<li><strong>{header}:</strong> {val}</li>"
    header_info += "</ul>"
    return header_info

@app.route('/log')
def log_request():
    with open("/test/requests.log", "a") as fptr:
        fptr.write("IP Address: {}\n".format(request.headers['X-Forwarded-For']))
    return "<h2>Request Logged from:</h2><b><i>IP: {}<i></b>".format(request.headers['X-Forwarded-For'])

@app.route('/node')
def node_info():
    return "<h2>Kubernetes Node Hostname: {}</h2>".format(os.environ.get('NODE_HOST'))

@app.route('/live')
def liveness():
    response = make_response("OK")
    response.status_code = 200
    return response

# For Kubernetes to see the metrics
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6500, debug=False)
