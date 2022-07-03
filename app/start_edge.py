from edge.edge import run_edge
import argparse

parser = argparse.ArgumentParser(
    description='Simulate a parking garage edge node. Relies on server for data aggregation and processing.')
parser.add_argument('--garage_name', type=str,
                    help='the name of the garage', required=True)

if __name__ == '__main__':
    args = parser.parse_args()

    run_edge(garage_name=args.garage_name)
