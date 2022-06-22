from argparse import ArgumentParser
from ipaddress import ip_address

import sys
import utils
import ipc_server

from settings import logger

def get_args():
    """
    Creating server startup arguments
    """
    description = "detector - handle so buffer and receive coordinates to detector-msg"
    arg = ArgumentParser(description=description)


    arg.add_argument("-p", "--port",
                     dest="port", default=6000,
                     help="port number to connect to detector (default=6000)",
                     type=int, metavar="{0...65535}")

    arg.add_argument("-ip", "--ip_address",
                     dest="ip", default='127.0.0.1',
                     help="ip address to connect to detector (default=127.0.0.1)",
                    type=ip_address, metavar="{127.0.0.1}")
    
    arg.add_argument("--start",
                    dest="start",
                    action='store_true',
                    help="Start detector")


    return arg


def parse_args(parser):
    """
    Handling input exceptions
    """
    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    if args.port:
        if not utils.is_port_valid(args.port):
            sys.exit(1)
        args.port = int(args.port)

    if args.ip:
        args.ip = str(args.ip)

    if len(sys.argv) == 2 and args.start:
        try:
            ipc_server.run_server()
        except KeyboardInterrupt:
            logger.info('Stopping server')
            sys.exit(0)
        except OSError:
            logger.error("Address already to use")
        sys.exit(0)

    return vars(args)


def main():
    parser = get_args()

    args = parse_args(parser)

    ipc_server.run_server(
        tcp_ip=args['ip'],
        port_number=args['port'],
    )

if __name__ == '__main__':
    main()
