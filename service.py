import re
import datetime

import csvadapter


# CURRENT DATE
def get_date() -> str:
    x = datetime.datetime.now()
    return x.strftime("%d-%m-%Y")


# validation for input params
def validate_params(params: dict):
    field_names = csvadapter.read_fieldnames()

    # Check field names in params
    gen_bool = [i in field_names for i in params.keys()]
    if False in gen_bool:
        return False, 'incorrect name of one of the parameters'

    # Check category_id
    try:
        int(params['category_id'])
    except ValueError as e:
        return False, 'category_id not integer'

    # Check category_description. Length.
    if len(params['category_description']) > 32:
        return False, 'too long'

    # Check cost. Float.
    try:
        float(params['cost'])
    except ValueError as e:
        return False, 'cost not float'

    # Check date
    regex = r"^[0-3]{1}[0-9]{1}-[0-1]{1}[0-9]{1}-[1-2]{1}[0-9]{3}$"
    result = bool(re.search(regex, params['date']))
    if not result:
        return False, 'date incorrect'

    return True, 'ok'
