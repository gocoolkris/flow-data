#!/usr/bin/env python3
import argparse
from src.flowlog.stats_writer import FlowDataMain
from src.flowlog.lookup_generator import LookupTableGenerator

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', "--lookup_file", type=str)
    parser.add_argument('-g', "--generate_lookup_file", action='store_true')
    args = parser.parse_args()
    if args.generate_lookup_file:
        g = LookupTableGenerator()
        filename = g.write_data()
        print(f"Wrote to {filename}")
    else:
        flowdata_main = FlowDataMain()
        flowdata_main.write_stats(filepath=args.lookup_file)
