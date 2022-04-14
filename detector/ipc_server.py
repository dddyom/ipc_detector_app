import socket
import pickle


import utils
from Detector import Detector
import detection_tools


def run_server(tcp_ip='127.0.0.1', port_number=6000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((tcp_ip, port_number))
    server.listen(5)
    # Detector object
    detector = Detector()
    while True:
        clientsocket, _ = server.accept()

        received_data = pickle.loads(clientsocket.recv(4096))

        if received_data == 'stop':
            break

        msg = pickle.dumps(received_data)
        clientsocket.send(msg)

        answer = utils.handle_received(received_data)

        if not answer:
            # Detector call
            matrix = detection_tools.dat2nparr(received_data['path_to_so'])
            splited = detection_tools.split(matrix, 8, 5)

            nulls = detection_tools.null_coordinate(splited, ncols=5)

            detection_tools.splited_save(splited, "./splited_numpy", nulls)

            answer = detection_tools.predict(detector, "./splited_numpy")

            detection_tools.rm_dir('./splited_numpy')

            # print(matrix.shape)

            pass

        msg = pickle.dumps(answer)
        clientsocket.send(msg)
        if answer == 'stop':
            break
