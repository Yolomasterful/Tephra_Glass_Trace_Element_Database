import sqlite3
import csv

con = sqlite3.connect("LaserAbblation.db")

cur = con.cursor()

try:
  cur.executescript(open("LaserAbblation.sql", 'r').read())
  con.commit()
except:
 con.rollback()

with open("Samples.csv", 'r') as file:
  csv_reader = csv.reader(file)
  headers = next(csv_reader)

  insert_sql = f"""INSERT INTO "Samples" VALUES ({', '.join(['null']+['?']*len(headers))})"""
  cur.executemany(insert_sql, csv_reader)

con.commit()