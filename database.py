import sqlite3
import os
from datetime import datetime

DB_NAME = "smart_hostel.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            mobile TEXT NOT NULL,
            room TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Meal Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            user_email TEXT NOT NULL,
            date TEXT NOT NULL,
            meal TEXT NOT NULL DEFAULT 'Lunch',
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE (user_id, date, meal)
        )
    ''')

    # Mess Fees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            month TEXT NOT NULL,
            monthly_fee REAL NOT NULL DEFAULT 3000,
            paid_amount REAL NOT NULL DEFAULT 2000,
            status TEXT NOT NULL DEFAULT 'Payment Pending',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE (user_id, month)
        )
    ''')

    # Payments transaction history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            month TEXT NOT NULL,
            payment_method TEXT DEFAULT 'Online UPI/Card',
            transaction_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Mess Notices table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL,
            icon TEXT DEFAULT '📢',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Weekly Menu table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            items TEXT NOT NULL,
            is_special INTEGER DEFAULT 0
        )
    ''')

    # Seed initial Notices if table is empty
    cursor.execute('SELECT COUNT(*) FROM notices')
    if cursor.fetchone()[0] == 0:
        default_notices = [
            ("Mess Timing Notice", "Lunch will be served from 12:00 PM to 2:00 PM. Students are requested to take their meals within the given time.", "22 August 2026", "🍛"),
            ("Mess Fee Payment", "All mess students are requested to pay their monthly mess fees before the due date.", "22 August 2026", "💰"),
            ("Sunday Special Lunch", "Special Veg Biryani, Dal Tadka, Chapati and Raita will be served for Sunday lunch.", "23 August 2026", "⭐"),
            ("Attendance Reminder", "Students are requested to mark their meal attendance before taking lunch.", "22 August 2026", "📢"),
            ("Food Feedback", "Students can submit their feedback about food quality and mess service.", "22 August 2026", "🍽️")
        ]
        cursor.executemany(
            'INSERT INTO notices (title, content, date, icon) VALUES (?, ?, ?, ?)',
            default_notices
        )

    # Seed Weekly Menu if table is empty
    cursor.execute('SELECT COUNT(*) FROM menu')
    if cursor.fetchone()[0] == 0:
        default_menu = [
            ("Monday", "Today's Lunch 🍽️", "🍚 Rice\n🥘 Dal\n🫓 Chapati\n🥔 Potato Vegetable\n🥗 Salad", 0),
            ("Tuesday", "Today's Lunch 🍽️", "🍚 Jeera Rice\n🥘 Dal Fry\n🫓 Chapati\n🥕 Mix Vegetable\n🥛 Curd", 0),
            ("Wednesday", "Today's Lunch 🍽️", "🍚 Rice\n🥘 Dal Tadka\n🫓 Chapati\n🍆 Brinjal Vegetable\n🥗 Salad", 0),
            ("Thursday", "Today's Lunch 🍽️", "🍚 Rice\n🥘 Dal\n🫓 Chapati\n🥦 Mixed Vegetable\n🥛 Buttermilk", 0),
            ("Friday", "Today's Lunch 🍽️", "🍚 Veg Pulao\n🥘 Dal\n🫓 Chapati\n🥔 Aloo Gobi\n🥗 Salad", 0),
            ("Saturday", "Today's Lunch 🍽️", "🍚 Rice\n🥘 Dal\n🫓 Chapati\n🍅 Tomato Vegetable\n🥛 Curd", 0),
            ("Sunday", "Special Sunday Lunch 🍽️", "🍛 Special Veg Biryani\n🥘 Dal Tadka\n🫓 Chapati\n🥔 Special Vegetable\n🥛 Raita", 1)
        ]
        cursor.executemany(
            'INSERT INTO menu (day, title, items, is_special) VALUES (?, ?, ?, ?)',
            default_menu
        )

    # Seed a demo student if no users exist
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO users (name, email, mobile, room, password)
            VALUES (?, ?, ?, ?, ?)
        ''', ("Demo Student", "student@smarthostel.com", "9876543210", "A-101", "student123"))
        demo_id = cursor.lastrowid
        cursor.execute('''
            INSERT INTO fees (user_id, month, monthly_fee, paid_amount, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (demo_id, "August 2026", 3000, 2000, "Payment Pending"))

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()

