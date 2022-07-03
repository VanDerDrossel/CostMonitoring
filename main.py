#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, jsonify, request

import csvadapter
import service


app = Flask(__name__)


@app.route('/api/v1/get_spending', methods=['GET'])
def get_spending():
    spending = csvadapter.read_rows()

    if not spending:
        return jsonify({'error': 'data not found'})

    return jsonify(spending)


@app.route('/api/v1/add_spend', methods=['POST'])
def add_spend():
    field_names = csvadapter.read_fieldnames()
    params = request.args.to_dict()

    # validation params
    validate_params, err_desc = service.validate_params(params)

    if validate_params:
        csvadapter.add_row([params[name] for name in field_names])

    return jsonify({'result': err_desc})


if __name__ == '__main__':
    app.run()
