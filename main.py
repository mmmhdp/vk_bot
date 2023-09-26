from core.MessageBroker.MessageBroker import MessageBroker


def main():
    msg_br = MessageBroker()
    msg_br.setup()
    msg_br.listen()


if __name__ == "__main__":
    main()
