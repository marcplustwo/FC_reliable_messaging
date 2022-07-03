import logging

from server.server import run_server


if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)

    run_server()
