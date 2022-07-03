import argparse
import logging

from edge.edge import run_edge


if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)

    parser = argparse.ArgumentParser(
        description='Simulate a parking garage edge node. Relies on server for data aggregation and processing.')
    parser.add_argument('--garage_name', type=str,
                        help='the name of the garage', required=True)

    args = parser.parse_args()

    run_edge(garage_name=args.garage_name)
