#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import argparse
import sqlite3

def main(args):
    # Read source
    if args.source_type == "excel":
        df = pd.read_excel(open(args.source,'rb'), sheet_name=args.sheet_name)
    else:
        df = pd.read_csv(args.source)
    # Iterate data
    for row in df.values:
        print(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Path to csv or excel", action="store", type=str)
    parser.add_argument("db_path", help="Path to sqlite3 database", action="store", type=str)
    parser.add_argument("--source-type", help="Type of source", action="store",
                        choices=["csv", "excel"], default="csv", dest="source_type", type=str)
    parser.add_argument("--sheet-name", help="Sheet name for excel", action="store",
                        default="Sheet1", dest="sheet_name", type=str)
    args = parser.parse_args()
    main(args)