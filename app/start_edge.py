import argparse
import logging

from edge.edge import run_edge


if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.WARNING)

    parser = argparse.ArgumentParser(
        description='Simulate a parking garage edge node. Relies on server for data aggregation and processing.')
    parser.add_argument('--garage_name', type=str,
                        help='the name of the garage', required=True)
    parser.add_argument('--server_ip', type=str,
                        help='server ip', required=False, default="localhost")
    parser.add_argument('--server_port', type=str,
                        help='server ip', required=False, default="5555")

    args = parser.parse_args()

    run_edge(garage_name=args.garage_name, server_ip=args.server_ip, server_port=args.server_port)
