from loguru import logger

logger.add("detector.log", format="{time} {level} {message}", level="INFO")

DOCKER_PATH = '/mnt/local_floder'
