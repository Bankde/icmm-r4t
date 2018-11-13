#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import argparse
import sqlite3
import os
from db import UserDB

def main(args):
    # Read source
    if args.source_type == "excel":
        df = pd.read_excel(open(args.source,'rb'), sheet_name=args.sheet_name, encoding='utf-8')
    else:
        df = pd.read_csv(args.source)

    UserDB.connect(args.db_path)
    UserDB.initSchema()
    # Iterate data
    users = []
    for row in df.values:
        firstname = row[3]
        lastname = row[4]
        teamName = None
        distance = row[8]
        if "10 KM" not in distance:
            # Skip 5K runner
            continue

        first10k_word = row[10]
        if first10k_word == "เคย":
            first10k = 0
        elif first10k_word == "ไม่เคย":
            first10k = 1
        else:
            assert(0)
            
        user = (firstname, lastname, teamName, first10k)
        users.append(user)
    print("Inserting %d users" % (len(users)))
    UserDB.insertUsers(users)
    UserDB.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Path to csv or excel", action="store", type=str)
    parser.add_argument("db_path", help="Path to sqlite3 database ex. ./users.db", action="store", type=str)
    parser.add_argument("--source-type", help="Type of source (default is excel)", action="store",
                        choices=["csv", "excel"], default="excel", dest="source_type", type=str)
    parser.add_argument("--sheet-name", help="Sheet name for excel (default is Sheet1)", action="store",
                        default="Sheet1", dest="sheet_name", type=str)
    args = parser.parse_args()
    main(args)