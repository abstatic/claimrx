import logging
from nanoid import generate


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
