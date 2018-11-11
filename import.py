#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import argparse
import sqlite3
import os

users_db = "users.db"

def createDb():
    conn = sqlite3.connect(users_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE users
               (firstname TEXT, lastname TEXT, teamName TEXT, first10k INTEGER)''')
    conn.commit()
    conn.close()

def main(args):
    # Read source
    if args.source_type == "excel":
        df = pd.read_excel(open(args.source,'rb'), sheet_name=args.sheet_name, encoding='utf-8')
    else:
        df = pd.read_csv(args.source)

    if not os.path.isfile(users_db):
        createDb()

    conn = sqlite3.connect(users_db)
    cursor = conn.cursor()
    # Iterate data
    for row in df.values:
        firstname = row[3]
        lastname = row[4]
        teamName = None
        first10k_word = row[10]
        if first10k_word == "เคย":
            first10k = 1
        elif first10k_word == "ไม่เคย":
            first10k = 0
        else:
            assert(0)
        values = (firstname, lastname, teamName, first10k)
        cursor.execute("INSERT INTO users VALUES (?,?,?,?)", values)
    conn.commit()
    conn.close()


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