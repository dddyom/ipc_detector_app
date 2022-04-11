def is_port_valid(port_number):
    if not 0 < port_number < 2**16:
        print(
            f"port numbers must be between 0 and 2**16"
        )
    else:
        return True


# def is_received_valid(msg):
    # if isinstance(msg, dict):
        # for key in msg.keys():
            # if key not in ('path_to_so', 'azimuth', 'distance'):
                # print(
                    # f'Unexpected key in client message {msg}'
                # )
    # else:
        # print(
            # f'Unexpected client message type {msg}'
        # )
