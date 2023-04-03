# (A) LOAD SQLITE MODULE
import sqlite3
DBFILE = "votes.db"

# (B) GET QUESTION + OPTIONS + VOTES
def get(qid):
  # (B1) RETURNS A DICTIONARY (NONE ON ERROR/NOT FOUND)
  res = {
    "q" : "", # QUESTION
    "o" : {}, # OPTIONS, OID : TEXT
    "v" : {}  # VOTES, OID : NUMBER OF VOTES
  }

  # (B2) GET QUESTION
  conn = sqlite3.connect(DBFILE)
  cursor = conn.cursor()
  cursor.execute("SELECT txt FROM questions WHERE qid=?", (qid,))
  data = cursor.fetchone()
  if data is None:
    return None

  # (B3) GET OPTIONS
  res["q"] = data[0]
  cursor.execute("SELECT oid, txt, votes FROM options WHERE qid=?", (qid,))
  data = cursor.fetchall()
  if len(data)==0:
    return None
  for row in data:
    res["o"][row[0]] = row[1]
    res["v"][row[0]] = row[2]

  # (B4) RETURN RESULT
  conn.close()
  return res

# (C) SAVE VOTE
def save(qid, oid, oldid):
  # (C1) GET CURRENT VOTES COUNT
  conn = sqlite3.connect(DBFILE)
  cursor = conn.cursor()
  cursor.execute("SELECT oid, votes FROM options WHERE qid=?", (qid,))
  data = {}
  for r in cursor.fetchall():
    data[r[0]] = r[1]

  # (C2) UPDATE OLD VOTE COUNT
  if oldid is not None:
    count = data[oldid] - 1
    count = count if count>0 else 0
    cursor.execute("UPDATE options SET votes=? WHERE qid=? AND oid=?", (count, qid, oldid,))

  # (C3) UPDATE NEW VOTE COUNT
  count = data[oid] + 1
  cursor.execute("UPDATE options SET votes=? WHERE qid=? AND oid=?", (count, qid, oid,))

  # (C4) DONE
  conn.commit()
  conn.close()
  return True