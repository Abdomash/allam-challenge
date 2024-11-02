import os
import sys
import logging

class Logger:
    """
    A class that wraps a logger instance and provides methods to log messages at different levels.
    Implements the singleton pattern to ensure that only one logger instance is created.
    """
    _instance = None

    @classmethod
    def initialize(cls, name, filepath=None, socketio=None):
        if cls._instance is not None:
            cls._instance.logger.warning("Logger already initialized.")
            return cls._instance
        cls._instance = cls(name, filepath, socketio)
    
    @classmethod
    def get_logger(cls):
        if cls._instance is None:
            raise RuntimeError("Logger not initialized.")
        return cls._instance

    def __init__(self, name, filepath=None, socketio=None):
        """
        Initialize the logger with a name, an optional file path, and an optional SocketIO instance.
        
        :param name: The name of the logger.
        :param filepath: The path to the log file. If None, logging to file is disabled.
        :param socketio: The SocketIO instance to log to. If None, logging to Flask is disabled.
        """
        if Logger._instance is not None:
            Logger._instance.logger.warning("Logger already initialized.")
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s] - %(message)s', datefmt='%I:%M:%S %p')

        # Logging to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Logging to file
        if filepath is not None:
            file_handler = logging.FileHandler(filepath)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Logging to Flask
        if socketio is not None:

            # Import FlaskIOHandler from the website folder
            website_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'website')
            sys.path.append(website_dir)
            from website import FlaskIOHandler

            flask_handler = FlaskIOHandler()
            flask_handler.setLevel(logging.DEBUG)
            flask_handler.setFormatter(formatter)
            self.logger.addHandler(flask_handler)

    def log(self, message):
        self.logger.log(message)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def fatal(self, message):
        self.logger.fatal(message)