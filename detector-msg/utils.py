import os

from settings import logger

def is_path_valid(path_to_so):
    """
    Check path validation
    """
    if os.path.exists(path_to_so):

        if str(path_to_so).split('.')[-1].lower() == 'dat':
            return True

        else:
            logger.error(
                f'Unexpected extension of file {path_to_so}'
            )
    else:
        logger.error(
            f'File {path_to_so} does not exist'
        )
    return


def is_coordinate_valid(coordinate):
    """
    Check coordinates validation
    """
    if coordinate >= 360 or coordinate < 0:
        logger.error(
            f' Incorrect coordinate value {coordinate}'
        )
    else:
        return True


def is_port_valid(port_number):
    """
    Check port validation
    """
    if not 0 < port_number < 2**16:
        logger.error(
            f"port numbers must be between 0 and 2**16"
        )
    else:
        return True


