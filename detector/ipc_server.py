import socket
import pickle

# import utils

            
def run_server(tcp_ip='127.0.0.1', port_number=6000):
    server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((tcp_ip, port_number))
    server.listen(5)

    while True:
        clientsocket, _ = server.accept()

        received_data = pickle.loads(clientsocket.recv(4096))

        if received_data == 'stop':
            break


        msg = pickle.dumps(received_data)
        clientsocket.send(msg)

