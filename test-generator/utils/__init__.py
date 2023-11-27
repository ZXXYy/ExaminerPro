__version__ = '0.1.0'

import logging

def configure_logging(log_level):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    logging.basicConfig(level=numeric_level, format='%(asctime)s - %(levelname)s - %(message)s')