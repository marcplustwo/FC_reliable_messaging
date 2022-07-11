import logging
import argparse

from server.server import run_server


if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)
    
    parser = argparse.ArgumentParser(
        description='Simulate a parking garage edge node. Relies on server for data aggregation and processing.')
    parser.add_argument('--server_port', type=str,
                        help='server ip', required=False, default="5555")

    args = parser.parse_args()

    run_server(server_port=args.server_port)
