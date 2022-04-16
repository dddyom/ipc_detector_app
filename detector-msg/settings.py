from loguru import logger

logger.add("detector-msg.log", format="{time} {level} {message}", level="INFO")
