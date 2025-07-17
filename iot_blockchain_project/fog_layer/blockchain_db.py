import sqlite3
import json
import time

def init_db():
    conn = sqlite3.connect('blockchain.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS blocks
                 (id INTEGER PRIMARY KEY,
                 timestamp REAL,
                 data TEXT,
                 previous_hash TEXT,
                 hash TEXT,
                 validator TEXT)''')
    conn.commit()
    conn.close()

def add_block(block_data):
    conn = sqlite3.connect('blockchain.db')
    c = conn.cursor()
    c.execute("INSERT INTO blocks VALUES (?,?,?,?,?,?)",
              (block_data['index'],
               block_data['timestamp'],
               json.dumps(block_data['data']),
               block_data['previous_hash'],
               block_data['hash'],
               block_data['validator']))
    conn.commit()
    conn.close()

def get_latest_block():
    conn = sqlite3.connect('blockchain.db')
    c = conn.cursor()
    c.execute("SELECT * FROM blocks ORDER BY id DESC LIMIT 1")
    result = c.fetchone()
    conn.close()
    
    if result:
        return {
            "index": result[0],
            "timestamp": result[1],
            "data": json.loads(result[2]),
            "previous_hash": result[3],
            "hash": result[4],
            "validator": result[5]
        }
    return None

def get_block_count():
    conn = sqlite3.connect('blockchain.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM blocks")
    count = c.fetchone()[0]
    conn.close()
    return count