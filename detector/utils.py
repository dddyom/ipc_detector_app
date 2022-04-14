def is_port_valid(port_number):
    if not 0 < port_number < 2**16:
        print(
            f"port numbers must be between 0 and 2**16"
        )
    else:
        return True


def handle_received(received_message):
    if received_message == 'stop':
        return 'stop'

    if isinstance(received_message, dict):
        for key in received_message.keys():
            if key not in ('path_to_so', 'azimuth', 'distance'):
                return f'Unexpected key in client message {received_message}'
                
    else:
        return f'Unexpected client message type {received_message}'
