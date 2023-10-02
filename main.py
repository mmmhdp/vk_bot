import logging

from core.MessageBroker.MessageBroker import MessageBroker
from core.Logging.LoggingConfiguration import LoggingEngine


def main():
    LoggingEngine.configurate_logger()

    logger = logging.getLogger(__name__)
    logger.critical("Server up")

    logger.info("Start server initialization")

    try:
        msg_br = MessageBroker()
        logger.info("Configuring environment")
        msg_br.setup()
        logger.info("Environment configured successfully")
        logger.info("Bot starts to listen")
        msg_br.listen()
    except KeyboardInterrupt:
        logger.critical("Server down")


if __name__ == "__main__":
    main()
