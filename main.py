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

    params = request.args.to_dict()
    limit = 10
    if 'limit' in params and params['limit'].isdigit():
        limit = int(params['limit'])

    return jsonify(spending[0:limit])


@app.route('/api/v1/add_spend', methods=['POST'])
def add_spend():
    field_names = csvadapter.read_fieldnames()
    params = request.args.to_dict()

    if 'date' not in params:
        params['date'] = service.get_date()

    # validation params
    validate_params, err_desc = service.validate_params(params)

    if validate_params:
        csvadapter.add_row([params[name] for name in field_names])

    return jsonify({'result': err_desc})


@app.route('/api/v1/calc_spend', methods=['GET'])
def calc_spend():
    spending = csvadapter.read_rows()

    if not spending:
        return jsonify({'error': 'data not found'})

    res = {}
    for row in spending:
        keys = row['date'], row['category_description'], row['category_id']
        if keys in res:
            res[keys]['cost'] += row['cost']
        else:
            res[keys] = row.copy()
    res = [v for v in res.values()]

    params = request.args.to_dict()
    limit = 7
    if 'limit' in params and params['limit'].isdigit():
        limit = int(params['limit'])

    return jsonify(res[0:limit])


if __name__ == '__main__':
    app.run()
