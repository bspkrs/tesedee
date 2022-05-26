__author__ = 'bspkrs'

import time

from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

# TODO: this is clearly something that we'd want to keep persisted between restarts of the application if it isn't empty
errors = []
temperature_threshold = 90.0
DATA_PARSE_ERROR_MESSAGE = 'Data is not in required format'


def _find_next_id():
    return len(errors)


@app.get("/errors")
def get_errors():
    return jsonify(dict(errors=errors)), 200


@app.delete("/errors")
def delete_errors():
    num_deleted = len(errors)
    errors.clear()
    return jsonify(dict(error_records_deleted=num_deleted)), 200


def record_error(_request, msg=None):
    data = _request.get_data(as_text=True)
    # errors.append(dict(error_id=_find_next_id(), errant_data=data, message=msg,
    #                    received_ts=(datetime.datetime.now() +
    #                                 datetime.timedelta(seconds=time.timezone)).strftime("%Y/%m/%d %H:%M:%S")))
    errors.append(data)


@app.post("/temp")
def accept_temperature():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    # Attempt to retrieve the json
    try:
        temperature_data = request.get_json()
    except BadRequest:
        record_error(request, 'Invalid JSON')
        return jsonify(dict(error='bad request')), 400

    # Get Device ID, and make sure it's a valid number
    device_id_str, _, rest = temperature_data["data"].partition(":")
    if not _ or not rest:
        record_error(request, DATA_PARSE_ERROR_MESSAGE)
        return jsonify(dict(error='bad request')), 400

    try:
        device_id = int(device_id_str)
    except ValueError:
        record_error(request, 'Unable to parse device_id as integer')
        return jsonify(dict(error='bad request')), 400

    # Get Epoch MS value, make sure it's a valid number, and parse it into a formatted timestamp string
    epoch_ms_str, _, rest = rest.partition(":")
    if not _ or not rest:
        record_error(request, DATA_PARSE_ERROR_MESSAGE)
        return jsonify(dict(error='bad request')), 400

    try:
        epoch_ms = int(epoch_ms_str)
    except ValueError:
        record_error(request, 'Unable to parse Epoch MS as integer')
        return jsonify(dict(error='bad request')), 400

    s, ms = divmod(epoch_ms, 1000)
    try:
        formatted_ts = '{}.{:03d}'.format(time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime(s)), ms)
    except ValueError:
        record_error(request, 'Unable to convert Epock MS to datetime')
        return jsonify(dict(error='bad request')), 400

    # Get 'Temperature' label and temperature value, test them, and return the appropriate result
    temp_label_str, _, temperature_str = rest.partition(":")
    if not _ or not temperature_str or temp_label_str != "'Temperature'":
        record_error(request, DATA_PARSE_ERROR_MESSAGE)
        return jsonify(dict(error='bad request')), 400

    try:
        temperature_data = float(temperature_str)
    except ValueError:
        record_error(request, 'Unable to parse temperature as float')
        return jsonify(dict(error='bad request')), 400

    ret = dict(overtemp=(temperature_data >= temperature_threshold))
    if ret["overtemp"]:
        ret.update(dict(device_id=device_id, formatted_time=formatted_ts))

    return jsonify(ret), 200
