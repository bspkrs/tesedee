__author__ = 'bspkrs'

import datetime
import time

from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

errors = []


def _find_next_id():
    return len(errors)


@app.get("/errors")
def get_errors():
    return jsonify(errors), 200


@app.delete("/errors")
def delete_errors():
    global errors
    errors = []
    return jsonify(errors), 200


def record_error(data):
    errors.append(dict(id=_find_next_id(), data=data,
                       received_ts=(datetime.datetime.now() + datetime.timedelta(seconds=time.timezone)).strftime("%Y/%m/%d %H:%M:%S")))


@app.post("/temp")
def accept_temperature():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    # Attempt to retrieve the json
    try:
        temperature = request.get_json()
    except BadRequest:
        record_error(request.get_data(as_text=True))
        return jsonify(dict(error='bad request')), 400

    # Get Device ID, and make sure its a valid number
    device_id_str, _, rest = temperature["data"].partition(":")
    if not _ or not rest:
        record_error(request.get_data(as_text=True))
        return jsonify(dict(error='bad request')), 400

    try:
        device_id = int(device_id_str)
    except ValueError:
        record_error(request.get_data(as_text=True))
        return jsonify(dict(error='bad request')), 400

    # Get Epoch MS value, make sure its a valid number, and parse it into a formatted timestamp string
    epoch_ms_str, _, rest = rest.partition(":")
    if not _ or not rest:
        record_error(request.get_data(as_text=True))
        return jsonify(dict(error='bad request')), 400

    try:
        epoch_ms = int(epoch_ms_str)
    except ValueError:
        record_error(request.get_data(as_text=True))
        return jsonify(dict(error='bad request')), 400

    s, ms = divmod(epoch_ms, 1000)
    try:
        formatted_ts = '{}.{:03d}'.format(time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime(s)), ms)
    except ValueError:
        record_error(request.get_data(as_text=True))
        return jsonify(dict(error='bad request')), 400

    # Get 'Temperature' label and temperature value, test them, and return the appropriate result
    temp_label_str, _, temperature_str = rest.partition(":")
    if not _ or not temperature_str or temp_label_str != "'Temperature'":
        record_error(request.get_data(as_text=True))
        return jsonify(dict(error='bad request')), 400

    try:
        temperature = float(temperature_str)
    except ValueError:
        record_error(request.get_data(as_text=True))
        return jsonify(dict(error='bad request')), 400

    ret = dict(overtemp=(temperature >= 90.0))
    if ret["overtemp"]:
        ret.update(dict(device_id=device_id, formatted_time=formatted_ts))

    return jsonify(ret), 200
