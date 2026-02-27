from pathlib import Path
try:
    import MySQLdb
except ImportError:
    import pymysql as MySQLdb

ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / "static"

con = MySQLdb.Connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    passwd="root",
    db="speech",
)
cur = con.cursor()

records = []
for video in sorted(STATIC_DIR.glob("*.mp4")):
    word = video.stem.lower()
    sign = video.name
    records.append((word, sign))

if records:
    cur.executemany(
        """
        INSERT INTO asignl (word, sign)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE sign = VALUES(sign)
        """,
        records,
    )
    con.commit()

con.close()
print("Inserted/updated {} rows in asignl.".format(len(records)))
