
import settings
from settings import logger

logger.info("starting ...")
logger.info("loading imports...")


import detection_tools
from Detector import Detector
import utils
import pickle
import socket
import os

def run_server(tcp_ip='127.0.0.1', port_number=6000):
    logger.info('server binding')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((tcp_ip, port_number))
    server.listen(5)
    # Detector object
    logger.info("Detector object init...")
    detector = Detector()
    while True:
        logger.info('Server is ready')
        clientsocket, _ = server.accept()
        received_data = pickle.loads(clientsocket.recv(4096))
        if received_data == 'stop':
            logger.info("Stopping server(init by client)")
            break

        answer = utils.handle_received(received_data)

        if not answer:
            so_buf_name = os.path.basename(received_data['path_to_so']) 
            path_to_so = f'{settings.DOCKER_PATH}/{so_buf_name}'
            print(so_buf_name)
            answer = detection_tools.get_coordinates_from_buffer(
                detector, path_to_so)
            detection_tools.rm_dir('./splited_numpy')

        msg = pickle.dumps(answer)
        clientsocket.send(msg)
