import sqlite3

con = sqlite3.connect("LaserAbblation.db")
con.execute("PRAGMA foreign_keys = ON;")
cur = con.cursor()

try:
  cur.executescript(open("LaserAbblation.sql", 'r').read())
  con.commit()
except sqlite3.Error as e:
  con.rollback()
  #print(f"Failed {e}")

with open("IoliteDataTableExport_glass(Organized).csv", 'r') as file:
  for line in file.readlines()[1:]:
    
    #line processing
    if line[0] == ',': continue
    
    line = list(filter(str.strip, line.split(",")))

    #changed values generation
    sName = line[1].split(" - ")[0]

    #auto-identifier generation
    cur.execute(f"""SELECT MAX("sID") FROM "Samples" WHERE "sName" = ?""", (sName,))
    
    if not (sID := cur.fetchone()[0]):
      cur.execute(f"""SELECT MAX("sID") FROM "Samples" """)
      if not (sID := cur.fetchone()[0]):
        sID = 1
      else: sID += 1
    
    cur.execute(f"""SELECT MAX("iID") FROM "SampleIterations" WHERE "sID" = ?""", (sID,))
    if not (iID := cur.fetchone()[0]):
      iID = 1
    else: iID += 1

    #rows to add
    sample = (sID, sName, line[0])
    iteration = tuple([iID, sID]+line[1:])

    try:
      if iID == 1:
        cur.execute(f"""INSERT INTO "Samples" VALUES ({",".join(["?"]*len(sample))});""", sample)
      cur.execute(f"""INSERT INTO "SampleIterations" VALUES ({",".join(["?"]*len(iteration))})""", iteration)
    except sqlite3.Error as e:
      con.rollback()
      print(f"Failed {e}")
  
  con.commit()

con.close()