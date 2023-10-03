import logging

from core.MessageBroker.MessageBroker import MessageBroker
from core.Logging.LoggingConfiguration import LoggingConfiguration


def main():
    LoggingConfiguration.activate_config_for_logger()

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
