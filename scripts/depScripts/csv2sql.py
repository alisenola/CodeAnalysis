#!/usr/bin/env python

#csv2sql.py
#Points to directory. For each *.csv file in that directory,
#Converts stitch.csv output files understand into sql database files
#Created: mshakir@keystonestrategy.com
#Updated: ssia@keystonestrategy.com
#Last Updated: 12/14/2016

# Copyright (C) 2015 KEYSTONE STRATEGY - All Rights Reserved

import sqlite3
import sys
from csv import DictReader
import os

class SQLiteDB():
    def __init__(self, dbname=':memory:'):
        print(dbname)
        self.conn=sqlite3.connect(dbname)
 
    def importFromCSV(self, csvfilename, tablename, separator=";"):
        with open(csvfilename, 'r') as fh:
            
            dr = DictReader(fh, delimiter=separator)

            # Replace blank spaces in the headings
            #of the Understand GUI Stitch output with underscores
            field_names = []
            for field in dr.fieldnames:
                new = field.replace(r" ",r"_").strip()

                # Replace the name of "References" to avoid conflict with SQLite syntax
                if "References" in field:
                    new = new.replace("References", "NumRefs")
                field_names.append(new)
                
            fieldlist=",".join(field_names)

            ph=("?,"*len(dr.fieldnames))[:-1]
            self.conn.execute("DROP TABLE IF EXISTS %s"%tablename)
            self.conn.execute("CREATE TABLE %s(%s)"%(tablename, fieldlist))
            ins="insert into %s (%s) values (%s)"%(tablename, fieldlist, ph)
            for line in dr:
                v=[]
                for k in dr.fieldnames: v.append(line[k])
                self.conn.execute(ins, v)
        self.conn.commit()

#Given a CSV stitch file which is the output of generate stitch,
#creates a SQLite database.
def csv2sql(csvfile,tablename,database):

    db=SQLiteDB(database)
    db.importFromCSV(csvfile, tablename)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Point to csv file, and the output db name")
        exit(1)
    csvfile = sys.argv[1]
    database = sys.argv[2]

    csvSQLite(csvfile,database)
