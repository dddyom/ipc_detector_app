from loguru import logger

# DOCKER_PATH = '/mnt'

DOCKER_PATH = '.'
logger.add(f"{DOCKER_PATH}/detector.log", format="{time} {level} {message}", level="INFO")

