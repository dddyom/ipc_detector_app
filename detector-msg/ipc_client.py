import socket
import pickle


def send_message(tcp_ip='127.0.0.1', port_number=6000, message={}):

    msg = pickle.dumps(message)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((tcp_ip, port_number))

    client.send(msg)

    return pickle.loads(client.recv(4096))


def stop_server(tcp_ip='127.0.0.1', port_number=6000):

    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((tcp_ip, port_number))
    sock.send(pickle.dumps('stop'))
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((tcp_ip, port_number))
    client.send(pickle.dumps('stop'))
    return pickle.loads(client.recv(4096))
