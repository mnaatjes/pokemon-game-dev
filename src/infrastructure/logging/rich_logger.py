import logging
from rich.logging import RichHandler
from src.engine.core.interfaces import ILogger

class RichConsoleLogger(ILogger):
    """
    A concrete implementation of ILogger that routes messages to the terminal
    using Python's built-in logging module wrapped with rich for visual clarity.
    """

    def __init__(self, level: str = "INFO"):
        # Prevent duplicate handlers if instantiated multiple times
        logger = logging.getLogger("pokemon_engine")
        logger.setLevel(level.upper())
        
        if not logger.handlers:
            handler = RichHandler(
                rich_tracebacks=True,
                markup=True,
                show_path=False  # Hide file paths in console for cleaner game output
            )
            # Define a very clean format: Just the message (rich handles the level/time)
            formatter = logging.Formatter("%(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        self._logger = logger

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)
