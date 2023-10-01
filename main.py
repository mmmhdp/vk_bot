from core.MessageBroker.MessageBroker import MessageBroker


def main():
    print("Initializing...")
    msg_br = MessageBroker()
    msg_br.setup()
    print("Bot Starts to Listen...")
    msg_br.listen()


if __name__ == "__main__":
    main()
