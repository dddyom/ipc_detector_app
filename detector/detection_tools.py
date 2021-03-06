import matplotlib.pyplot as plt
import numpy as np
import struct
import os
import shutil

from settings import logger

def dat2nparr(path_to_so):
    """
    Convert source dat buffer to numpy matrix (2048 * 1200)
    """
    buffer = []
    dat_file = open(path_to_so, "rb").read()

    for i in range(0, len(dat_file), 2):
        buffer.append(struct.unpack("<H", dat_file[i: i + 2]))
    
    logger.info('convert .dat to numpy matrix...')
    matrix = np.reshape(np.array(buffer), (2048, 1200))

    return matrix


def split(array, nrows, ncols):

    """
    Splitting source big matrix to fragments
    """

    w, h = array.shape

    splited = np.vsplit(array, nrows)

    logger.info('Splitting matrix...')
    for i in range(len(splited)):
        splited[i] = np.hsplit(splited[i], ncols)

    return np.reshape(splited, (nrows * ncols, int(w / nrows), int(h / ncols)))


def null_coordinate(splited_array, ncols, index=None):
    """
    Get null coordinates for names of fragments
    """
    _, width, height = splited_array.shape

    logger.info('Null coordinates init...')

    if index:

        null_x = width * (index % ncols)

        null_y = height * (index // ncols)

        return np.array((null_x, null_y))

    null_coordinates = []

    for i in range(len(splited_array)):

        null_x = width * (i // ncols)

        null_y = height * (i % ncols)

        null_coordinates.append(np.array((null_x, null_y)))

    return np.array(null_coordinates)


def grades_and_kilometers(x, y):
    """
    Convert lines and points to grades and kilometers
    """
    grades = int((x / 2048) * 360)
    kilometers = int((y / 1200) * 360)

    return grades, kilometers


def splited_save(splited, path, nulls):
    """
    Save fragments with null coordinates in filename
    """
    if not os.path.exists(path):
        os.mkdir(path)

    logger.info('save splited matrix...')
    for i in range(len(splited)):

        null_x, null_y = nulls[i]

        plt.imshow(splited[i].T)
        plt.axis("off")
        plt.tick_params(axis='both', left='off', top='off', right='off', bottom='off',
                        labelleft='off', labeltop='off', labelright='off', labelbottom='off')

        plt.savefig(f'{path}/{i}_{null_x}_{null_y}.png',
                    dpi=100, bbox_inches='tight', pad_inches=0.0)



def name_parser(name):
    """
    Get null coordinates by fragment filename
    """
    index, A, D_ = name.split('_')
    D, _ = D_.split('.')
    return list(map(int, [index, A, D]))


def predict(detector, path_to_splited):
    """
    Return list of dict with targets coordinates 
    """
    finded = []
    fragments = os.listdir(path_to_splited)
    logger.info('Prediction starting...')
    for i in fragments:
        local_coordinates = detector.onImage(f"{path_to_splited}/{i}")

        if local_coordinates:
            _, A_points, D_points = name_parser(i)
            for local_single in local_coordinates:
                A, D = grades_and_kilometers(
                    A_points + local_single[0], D_points + local_single[1])
                logger.info(f'Target found [azimuth = {A}, distance = {D}]')
                finded.append({
                    'azimuth': A,
                    'distance': D
                })
    return finded

def rm_dir(path_to_rm):
    """
    Remove fragments folder
    """
    logger.info(f'Remove {path_to_rm}')
    shutil.rmtree(path_to_rm)

def get_coordinates_from_buffer(detector, path_to_so):
    """
    Return list of coordinates by path to so buffer (dat)
    """
    matrix = dat2nparr(path_to_so)
    splited =split(matrix, 8, 5)
    nulls = null_coordinate(splited, ncols=5)
    splited_save(splited, "./splited_numpy", nulls)
    return predict(detector, "./splited_numpy")
