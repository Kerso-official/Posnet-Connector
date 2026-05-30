import logging
from typing import Optional

import serial

from ._helpers import _create_frame

logger = logging.getLogger(__name__)


class PosnetCommunicator:
    def __init__(self, port: str, baudrate: int = 9600, timeout: int = 5):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection: Optional[serial.Serial] = None

    def connect(self):
        # Establishes the serial connection
        try:
            self.connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                rtscts=True,
            )
            logger.info("Connected to %s with RTS/CTS enabled.", self.port)
        except serial.SerialException as e:
            raise ConnectionError(f"Could not connect to {self.port}: {e}") from e

    def disconnect(self):
        # Closes the serial connection
        if self.connection and self.connection.is_open:
            self.connection.close()
            logger.info("Connection closed.")

    def send_command(
        self, command: str, parameters: Optional[dict] = None
    ) -> Optional[str]:
        if not self.connection or not self.connection.is_open:
            raise ConnectionError("Not connected. Call connect() first.")

        frame = _create_frame(command, parameters)
        logger.debug("Sending: %r", frame)

        self.connection.write(frame)

        response = self.connection.read_until(expected=b"\x03")

        if response:
            logger.debug("Received: %r", response)
            return response.decode("cp1250", errors="ignore")

        logger.warning("Timeout: no response received from printer.")
        return None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
