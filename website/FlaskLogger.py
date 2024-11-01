import logging
from flask_socketio import SocketIO

class FlaskIOHandler(logging.Handler):
    """Custom logging handler that sends log messages to a Flask SocketIO server."""
    def __init__(self, socketio: SocketIO):
        super().__init__()
        self.socketio = socketio

    def emit(self, record):
        self.socketio.emit('log', { 'message' : self.format(record) })