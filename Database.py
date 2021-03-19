import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_buy_order(conn, order):
    sql = '''INSERT INTO orders(symbol,openPrice,openTime)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, order)
    conn.commit()
    return cur.lastrowid

def count_open_orders(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders where selled = 0")

    rows = cur.fetchall()
    return len(rows)

def getOpenOrderSymbols(conn):
    cur = conn.cursor()
    cur.execute("SELECT id,symbol FROM orders where selled = 0")
    rows = cur.fetchall()
    return rows

def sellOrder(conn, sellOrder):
    sql = ''' UPDATE orders
              SET closePrice = ? ,
                  closeTime = ? ,
                  selled = 1
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, sellOrder)
    conn.commit()

def isExist(conn, symbol):
    cur = conn.cursor()
    cur.execute("SELECT symbol FROM orders where symbol = ?",(symbol,))
    rows = cur.fetchall()
    return len(rows)>0

def delete_all_orders(conn):
    sql = 'DELETE FROM orders'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def profitCalc(conn):
    cur = conn.cursor()
    cur.execute('SELECT symbol,openPrice,closePrice FROM orders where selled = 1')
    rows = cur.fetchall()
    message=""
    if len(rows)==0: return "Satış gerçekleşmemiş..."
    for x in rows:
        prof = round((((x[2]*100)/x[1])-100),2)
        if prof>0:
            message += str(x[0]) +" %"+str(prof).replace(".", ",")+" \U0001F4C8\n Alış: "+str(round(x[1],2)).replace(".", ",")+"\n Satiş: "+str(round(x[2],2)).replace(".", ",")+"\n"
        else:
            message += str(x[0]) +" %"+str(prof).replace(".", ",")+" \U0001F4C9\n Alış: "+str(round(x[1],2)).replace(".", ",")+"\n Satiş: "+str(round(x[2],2)).replace(".", ",")+"\n"
    return message 

sql_create_table = """CREATE TABLE IF NOT EXISTS orders(
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    symbol text NOT NULL,
                                    openPrice real NOT NULL,
                                    openTime integer NOT NULL,
                                    closePrice real DEFAULT NULL,
                                    closeTime integer DEFAULT NULL, 
                                    selled integer NOT NULL DEFAULT 0
                                );"""

drop_table = """DROP TABLE orders"""