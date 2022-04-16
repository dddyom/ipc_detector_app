from loguru import logger

DOCKER_PATH = '/mnt'

logger.add(f"{DOCKER_PATH}/detector.log", format="{time} {level} {message}", level="INFO")

