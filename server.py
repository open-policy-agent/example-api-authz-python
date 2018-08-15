#!/usr/bin/env python
"""
Car Store App
"""
import base64
import os
import json
from functools import wraps
import requests
import logging
import sys
import urllib
from flask import Flask, request, jsonify, make_response, abort, url_for

__version__ = "0.1"

app = Flask(__name__, static_url_path=None, static_folder=None)

cars = {}
status = {}


@app.route("/", methods=["GET"])
def list_routes():
    import urllib
    routes = set([])
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = '[{0}]'.format(arg)
        url = urllib.unquote(url_for(rule.endpoint, **options))
        routes.add(url)
    return jsonify(sorted(routes))


@app.route("/cars", methods=["GET"])
def list_cars():
    result = []
    for id in cars:
        result.append(cars[id])
    return jsonify({'result': result})


@app.route("/cars/<id>", methods=["GET"])
def car_detail(id):
    if id not in cars:
        abort(404)
    return jsonify({'result': cars[id]})


@app.route("/cars/<id>", methods=["PUT"])
def car_update(id):
    cars[id] = request.json
    return jsonify({'result': cars[id]})


@app.route("/cars/<id>", methods=["DELETE"])
def delete_car(id):
    if id not in cars:
        abort(404)
    car = cars[id]
    del cars[id]
    return jsonify({'result': car})


@app.route("/cars/<id>/status", methods=["GET"])
def car_status_detail(id):
    if id not in status:
        abort(404)
    return jsonify({'result': status[id]})


@app.route("/cars/<id>/status", methods=["PUT"])
def add_car_status(id):
    status[id] = request.json
    return jsonify({'result': status[id]})


@app.before_request
def check_authorization():
    try:
        input = json.dumps({
            "method": request.method,
            "path": request.path.strip().split("/")[1:],
            "user": get_authentication(request),
        }, indent=2)
        url = os.environ.get("OPA_URL", "http://localhost:8181")
        app.logger.debug("OPA query: %s. Body: %s", url, input)
        response = requests.post(url, data=input)
    except Exception as e:
        app.logger.exception("Unexpected error querying OPA.")
        abort(500)

    if response.status_code != 200:
        app.logger.error("OPA status code: %s. Body: %s",
                         response.status_code, response.json())
        abort(500)

    allowed = response.json()
    app.logger.debug("OPA result: %s", allowed)
    if not allowed:
        abort(403)


def get_authentication(request):
    return request.headers.get("Authorization", "")


def setup_logging():
    for handler in app.logger.handlers:
        handler.setLevel(logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)


def pump_db():

    mock_cars = [
        {
            "id": "663dc85d-2455-466c-b2e5-76691b0ce14e",
            "model": "Honda",
            "vehicle_id": "127482",
            "owner_id": "742"
        },
        {
            "id": "6c018cfa-e9c2-4169-a61b-dd3bf3bc19a7",
            "model": "Toyota",
            "vehicle_id": "19019",
            "owner_id": "742"
        },
        {
            "id": "879a273c-a8dc-41a6-9c30-2bb92288e93b",
            "model": "Ford",
            "vehicle_id": "3784312",
            "owner_id": "6928"
        },
        {
            "id": "fca3ab25-a151-4c76-b238-9aa6ee92c374",
            "model": "Honda",
            "vehicle_id": "22781",
            "owner_id": "30390"
        }
    ]

    for car in mock_cars:
        cars[car["id"]] = car

    mock_status = [
        {
            "id": "663dc85d-2455-466c-b2e5-76691b0ce14e",
            "position": {
                "latitude": -39.91045,
                "longitude": -161.70716
            },
            "mileage": 742,
            "speed": 90,
            "fuel": 6.42
        },
        {
            "id": "6c018cfa-e9c2-4169-a61b-dd3bf3bc19a7",
            "position": {
                "latitude": 12.77061,
                "longitude": 9.05115
            },
            "mileage": 17384,
            "speed": 62,
            "fuel": 8.9
        },
        {
            "id": "879a273c-a8dc-41a6-9c30-2bb92288e93b",
            "position": {
                "latitude": -8.86414,
                "longitude": -142.5982
            },
            "mileage": 9347,
            "speed": 45,
            "fuel": 3.1
        },
        {
            "id": "fca3ab25-a151-4c76-b238-9aa6ee92c374",
            "position": {
                "latitude": 68.86632,
                "longitude": -92.85048
            },
            "mileage": 97698,
            "speed": 50,
            "fuel": 3.22
        }
    ]

    for s in mock_status:
        status[s["id"]] = s


if __name__ == "__main__":
    setup_logging()
    pump_db()
    app.run(host="0.0.0.0", port="8080")
