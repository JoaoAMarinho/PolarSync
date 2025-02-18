import logging


class Logger:
    """
    A singleton-style class to initialize and provide access to a global logger.
    """

    _instance = None

    def __new__(cls):
        """
        Ensure only one instance of Logger is created (singleton pattern).
        """
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        """
        Initialize the logger with a basic configuration.
        """
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(),  # Log to console
            ],
        )
        self.logger = logging.getLogger(__name__)

    def __getattr__(self, name):
        """
        Delegate attribute access to the underlying logger instance.
        """
        if hasattr(self.logger, name):
            return getattr(self.logger, name)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )


# Create a global instance of the logger
logger = Logger()
