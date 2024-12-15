import logging

logger = logging.getLogger(__name__)


def load_file(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            logger.info("File loaded successfully!")
            return file_content
    except FileNotFoundError:
        logger.error(f"The file located at {file_path} does not exist.")
        return None
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None