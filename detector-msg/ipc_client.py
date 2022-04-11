import socket
# import select
import sys


# def send_message(tcp_ip='127.0.0.1', port_number=6000, message='ipc client is working!'):
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect((tcp_ip, port_number))
    # sock.send(bytes(message, encoding='utf-8'))

    # data = sock.recv(4096)
    # message = str(data.decode('utf-8'))
    # message = message.replace("\\n", '').replace('b','')
    # sys.stdout.write(message)

    # sys.exit(0)

def send_message(tcp_ip='127.0.0.1', port_number=6000, message='ipc client is working!'):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((tcp_ip, port_number))
    sock.send(bytes(message, encoding='utf-8'))

    data = sock.recv(4096)
    answer = str(data.decode('utf-8'))
    answer = answer.replace("\\n", '').replace('b','')
    return str(answer)


def stop_server(tcp_ip='127.0.0.1', port_number=6000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((tcp_ip, port_number))
    sock.send(bytes('stop', encoding='utf-8'))
