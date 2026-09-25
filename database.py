import sqlite3
from datetime import datetime

DB_NAME = "database/chatbot.db"

def init_db():
    """Create the complaints table if it does not exist"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE,
            user_message TEXT,
            category TEXT,
            priority TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_complaint(ticket_id, user_message, category, priority):
    """Save a new complaint"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO complaints (ticket_id, user_message, category, priority, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (ticket_id, user_message, category, priority, "Pending", created_at))
    
    conn.commit()
    conn.close()

def get_all_complaints():
    """Fetch all complaints"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT ticket_id, user_message, category, priority, status, created_at FROM complaints ORDER BY id DESC")
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def update_status(ticket_id, new_status):
    """Update complaint status"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE complaints SET status = ? WHERE ticket_id = ?", (new_status, ticket_id))
    
    conn.commit()
    conn.close()

