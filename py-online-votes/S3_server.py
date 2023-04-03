# (A) INIT
# (A1) LOAD MODULES
from flask import Flask, session, render_template, request
from flask_session import Session
import S2_lib as votes

# (A2) FLASK SETTINGS + INIT
HOST_NAME = "localhost"
HOST_PORT = 80
app = Flask(__name__)
# app.debug = True
app.secret_key = "VERY-SECRET-KEY"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# (B) VOTES PAGE
@app.route("/", methods=["GET", "POST"])
def index():
  # (B1) INIT
  qid = 1 # QUESTION ID, FIXED TO 1 IN THIS EXAMPLE
  if "vote" not in session: # SESSION - KEEP TRACK OF VOTES MADE
    session["vote"] = {}

  # (B2) SAVE VOTE ON FORM SUBMIT
  if request.method == "POST":
    oid = int(request.values.get("vote"))
    oldid = None if qid not in session["vote"] else session["vote"][qid]
    votes.save(qid, oid, oldid)
    session["vote"][qid] = oid

  # (B3) GET QUESTION FROM DB
  data = votes.get(qid)
  if data is None:
    return "ERROR!"
  data["qid"] = qid

  # (B4) RENDER PAGE
  return render_template("S4_vote.html", **data)

# (C) START
if __name__ == "__main__":
  app.run(HOST_NAME, HOST_PORT)