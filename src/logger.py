import logging
import sys

def setup_logger(name: str = "rag_app", log_level: int = logging.INFO) -> logging.Logger:
    """
    Sets up a logger with a standard configuration.
    
    Args:
        name (str): Name of the logger.
        log_level (int): Logging level (default: logging.INFO).
        
    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Check if handlers already exist to avoid duplicate logs
    if not logger.handlers:
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(console_handler)

    return logger
