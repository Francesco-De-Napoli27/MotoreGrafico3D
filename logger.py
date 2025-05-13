import logging

class Logger:
    def __init__(self, log_file="engine.log", level=logging.INFO):
        logging.basicConfig(
            filename=log_file,
            filemode="w",
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=level
        )
        self.logger = logging.getLogger()

    def log_event(self, message):
        """Registra un evento nel file di log"""
        self.logger.info(message)

    def log_error(self, message):
        """Registra un errore nel file di log"""
        self.logger.error(message)

    def log_warning(self, message):
        """Registra un avviso nel file di log"""
        self.logger.warning(message)

    def log_debug(self, message):
        """Registra un messaggio di debug dettagliato"""
        self.logger.debug(message)
