-- (A) QUESTIONS TABLE
CREATE TABLE questions (
  qid INTEGER,
  txt TEXT NOT NULL,
  PRIMARY KEY("qid" AUTOINCREMENT)
);

-- (B) OPTIONS TABLE
CREATE TABLE options (
  oid INTEGER,
  qid INTEGER NOT NULL,
  txt TEXT NOT NULL,
  votes INTEGER DEFAULT 0,
  PRIMARY KEY("oid" AUTOINCREMENT)
);
CREATE INDEX idx_qid ON options (qid);

-- (C) DUMMY DATA
INSERT INTO questions (txt) VALUES ("What is your favorite meme animal?");
INSERT INTO options (qid, txt, votes) VALUES
  (1, "Birb", 11), (1, "Doge", 22), (1, "Cate", 33), (1, "Snek", 44);