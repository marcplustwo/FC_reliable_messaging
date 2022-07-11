import logging
import argparse

from server.server import run_server


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description='Simulate a parking garage edge node. Relies on server for data aggregation and processing.')
    parser.add_argument('--server_port', type=str,
                        help='server ip', required=False, default="5555")
    parser.add_argument('-v', help='verbose output', required=False, action='store_true')

    args = parser.parse_args()

    if args.v:
        logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)
    else:
        logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.CRITICAL)

    run_server(server_port=args.server_port)
