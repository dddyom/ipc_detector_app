import os
import json
import re


def is_path_valid(path_to_so):
    if os.path.exists(path_to_so):

        if str(path_to_so).split('.')[-1].lower() == 'dat':
            return True

        else:
            print(
                f'Unexpected extension of file {path_to_so}'
            )
    else:
        print(
            f'File {path_to_so} does not exist'
        )
    return


def is_coordinate_valid(coordinate):
    if coordinate >= 360 or coordinate < 0:
        print(
            f' Incorrect coordinate value {coordinate}'
        )
    else:
        return True


def is_port_valid(port_number):
    if not 0 < port_number < 2**16:
        print(
            f"port numbers must be between 0 and 2**16"
        )
    else:
        return True


def to_json(dict):
    return json.dumps(dict)

