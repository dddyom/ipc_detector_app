from argparse import ArgumentParser
from ipaddress import ip_address

import pathlib
import sys

import utils
import ipc_client


def get_args():
    description = "detector-msg - Send arguments to detector"
    arg = ArgumentParser(description=description)

    arg.add_argument("-s", "--so_file",
                     dest="path_to_so",
                     help="set path to SO buffer",
                     type=pathlib.Path, metavar="/path/to/SO_buffer.dat")

    arg.add_argument("-p", "--port",
                     dest="port", default=6000,
                     help="port number to connect to detector (default=6000)",
                     type=int, metavar="{0...65535}")

    arg.add_argument("-ip", "--ip_address",
                     dest="ip", default='127.0.0.1',
                     help="ip address to connect to detector (default=127.0.0.1)",
                     type=ip_address, metavar="{127.0.0.1}")

    arg.add_argument("-A", "--azimuth",
                     dest="azimuth", default=0,
                     help="Null azimuth coordinate (default=0)",
                     type=float, metavar="{0...360}")

    arg.add_argument("-D", "--distance",
                     dest="distance", default=0,
                     help="Null distance coordinate (default=0)",
                     type=float, metavar="{0...360}")

    arg.add_argument("--stop",
                     dest="stop",
                     action="store_true",
                     help="Stop detector")

    return arg


def parse_args(parser):
    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    if args.path_to_so:
        if not utils.is_path_valid(args.path_to_so):
            sys.exit(1)
        args.path_to_so = str(args.path_to_so)

    if args.azimuth:
        if not utils.is_coordinate_valid(args.azimuth):
            sys.exit(1)
        args.azimuth = float(args.azimuth)

    if args.distance:
        if not utils.is_coordinate_valid(args.distance):
            sys.exit(1)
        args.distance = float(args.distance)

    if args.port:
        if not utils.is_port_valid(args.port):
            sys.exit(1)
        args.port = int(args.port)

    if args.ip:
        args.ip = str(args.ip)

    return vars(args)


def main():
    parser = get_args()

    args = parse_args(parser)

    to_detectron = {key: args[key]
                    for key in (
        'path_to_so',
        # 'azimuth',
        # 'distance',
    )}
    answer = ipc_client.send_message(
        tcp_ip=args['ip'],
        port_number=args['port'],
        message=utils.to_json(to_detectron)
    )

    sys.stdout.write(answer)

    if args['stop']:
        ipc_client.stop_server()


if __name__ == '__main__':
    main()
