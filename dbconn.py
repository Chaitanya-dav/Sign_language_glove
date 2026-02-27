try:
    import MySQLdb
except ImportError:
    import pymysql as MySQLdb

con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="root")
cur = con.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS speech")
con.commit()
con.close()
