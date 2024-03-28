import logging
from nanoid import generate
from datetime import datetime

def getLogger(name):
    log = logging.getLogger(name)
    # handler = logging.StreamHandler(sys.stdout)
    # formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    # handler.setFormatter(formatter)
    # log.addHandler(handler)
    # log.setLevel(logging.INFO)
    return log


def generate_nanoid():
    return generate('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 10)


def preprocess_params(raw_data: dict):
    # first we convert the keys to all lower case, trim spaces, change spaces to underscores
    processed_params = {}
    for k, v in raw_data.items():
        key = k.lower().strip().replace(" ", "_")
        processed_params[key] = v

    # handle the dollar signs
    dollar_fields = ["provider_fees", "allowed_fees", "member_coinsurance", "member_copay"]
    for df in dollar_fields:
        if df in processed_params:
            processed_params[df] = float(processed_params[df].replace("$", "").strip())

    # parse date
    # assumes format MM/DD/YY HH:MM
    if 'service_date' in processed_params:
        processed_params['service_date'] = datetime.strptime(processed_params['service_date'], "%m/%d/%y %H:%M").isoformat()

    custom_field_mapping = {
        "plan/group_#": "plan_group",
        "subscriber#": "subscriber_id",
    }

    for k1, k2 in custom_field_mapping.items():
        if k1 in processed_params:
            processed_params[k2] = processed_params.pop(k1)

    return processed_params
