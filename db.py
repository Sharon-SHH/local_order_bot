import sqlite3, json
from pathlib import Path

DB = Path(__file__).parent / "orders.db"
# DB = sqlite3.connect(":memory:"); save db in RAM
def _connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row # 行构造函数
    return con

def init_db():
    with _connect() as con:  # connect and close the db
        con.execute("""CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payload TEXT NOT NULL,
            total REAL NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")
        con.commit()

def list_orders(limit=50):
    with _connect() as con:
        cur = con.execute("SELECT id, payload, total FROM orders ORDER BY id DESC " \
        "Limit ?", (limit,))
        rows = cur.fetchall()
        return [dict(row) for row in rows]

def get_order(orderId):
    with _connect() as con:
        cur = con.execute("SELECT id, payload, total FROM orders " \
        "WHERE id = ? ORDER BY id DESC", (orderId,))
        row = cur.fetchone()
        return dict(row)

def save_order(payload, total):
    with _connect() as con:
        con.execute("INSERT INTO orders(payload, total) VALUES (?, ?)",
                    (json.dumps(payload), float(total)),)
        con.commit()
        
def delete_order(order_id):
    with _connect() as con:
        cur = con.execute("DELETE from orders where id = ?", (order_id,))
        con.commit()
        return cur.rowcount