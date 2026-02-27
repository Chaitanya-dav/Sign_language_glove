try:
    import MySQLdb
except ImportError:
    import pymysql as MySQLdb

con = MySQLdb.Connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    passwd="root",
    db="speech",
)
cur = con.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS asignl (
        id INT AUTO_INCREMENT PRIMARY KEY,
        word VARCHAR(50) NOT NULL UNIQUE,
        sign VARCHAR(255) NOT NULL
    )
    """
)
con.commit()
con.close()
