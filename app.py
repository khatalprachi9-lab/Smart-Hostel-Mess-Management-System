import os
import sqlite3
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, session
from database import get_db, init_db

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = 'smart-hostel-secret-key-2026'

# Initialize database on app startup
init_db()

# =======================================================
# STATIC PAGE ROUTES
# =======================================================

@app.route('/')
def index():
    return send_from_directory('.', 'login.html')

@app.route('/<path:filename>')
def serve_file(filename):
    if os.path.exists(filename):
        return send_from_directory('.', filename)
    return jsonify({"error": "File not found"}), 404

# =======================================================
# HELPER: GET CURRENT USER
# =======================================================

def get_current_user_from_request():
    user_id = session.get('user_id')
    email = request.args.get('email')
    
    if not user_id and request.is_json:
        email = request.json.get('email', email)
        
    conn = get_db()
    cursor = conn.cursor()
    user = None
    
    if user_id:
        cursor.execute("SELECT id, name, email, mobile, room FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
    elif email:
        cursor.execute("SELECT id, name, email, mobile, room FROM users WHERE email = ?", (email.strip(),))
        user = cursor.fetchone()
        
    conn.close()
    if user:
        return dict(user)
    return None

# =======================================================
# AUTHENTICATION APIS
# =======================================================

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    mobile = data.get('mobile', '').strip()
    room = data.get('room', '').strip()
    password = data.get('password', '')

    if not name or not email or not mobile or not room or not password:
        return jsonify({"success": False, "message": "All fields are required."}), 400

    if len(mobile) != 10 or not mobile.isdigit():
        return jsonify({"success": False, "message": "Enter a valid 10-digit mobile number."}), 400

    conn = get_db()
    cursor = conn.cursor()

    try:
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"success": False, "message": "This email is already registered."}), 409

        # Insert user
        cursor.execute('''
            INSERT INTO users (name, email, mobile, room, password)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, mobile, room, password))
        user_id = cursor.lastrowid

        # Create initial fee record for current month
        month_label = datetime.now().strftime("%B %Y")
        cursor.execute('''
            INSERT INTO fees (user_id, month, monthly_fee, paid_amount, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, month_label, 3000, 2000, "Payment Pending"))

        conn.commit()
        session['user_id'] = user_id

        user_data = {
            "id": user_id,
            "name": name,
            "email": email,
            "mobile": mobile,
            "room": room
        }

        return jsonify({
            "success": True,
            "message": "Account created successfully!",
            "user": user_data
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
    finally:
        conn.close()


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required."}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, email, mobile, room, password
        FROM users
        WHERE LOWER(email) = ?
    ''', (email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"success": False, "message": "Please register first."}), 404

    if user['password'] != password:
        return jsonify({"success": False, "message": "Invalid email or password."}), 401

    session['user_id'] = user['id']

    user_data = {
        "id": user['id'],
        "name": user['name'],
        "email": user['email'],
        "mobile": user['mobile'],
        "room": user['room']
    }

    return jsonify({
        "success": True,
        "message": "Login successful!",
        "user": user_data
    }), 200


@app.route('/api/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully."})


@app.route('/api/me', methods=['GET'])
def get_profile():
    user = get_current_user_from_request()
    if not user:
        return jsonify({"success": False, "message": "Not authenticated."}), 401
    return jsonify({"success": True, "user": user})


# =======================================================
# MEAL ATTENDANCE APIS
# =======================================================

@app.route('/api/attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json() or {}
    status = data.get('status', '').strip()  # "Present" or "Absent"
    meal = data.get('meal', 'Lunch').strip()
    date_str = data.get('date', datetime.now().strftime("%Y-%m-%d")).strip()

    if status not in ['Present', 'Absent']:
        return jsonify({"success": False, "message": "Invalid attendance status."}), 400

    user = get_current_user_from_request()
    if not user:
        # Fallback to demo user if not logged in
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, mobile, room FROM users LIMIT 1")
        demo = cursor.fetchone()
        conn.close()
        if demo:
            user = dict(demo)
        else:
            return jsonify({"success": False, "message": "User session not found. Please log in."}), 401

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO attendance (user_id, user_email, date, meal, status)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, date, meal) DO UPDATE SET
                status = excluded.status,
                created_at = CURRENT_TIMESTAMP
        ''', (user['id'], user['email'], date_str, meal, status))
        conn.commit()

        return jsonify({
            "success": True,
            "message": f"{meal} attendance marked as {status}!",
            "status": status,
            "date": date_str,
            "meal": meal
        })
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": f"Error saving attendance: {str(e)}"}), 500
    finally:
        conn.close()


@app.route('/api/attendance/today', methods=['GET'])
def get_today_attendance():
    meal = request.args.get('meal', 'Lunch')
    date_str = request.args.get('date', datetime.now().strftime("%Y-%m-%d"))
    user = get_current_user_from_request()

    conn = get_db()
    cursor = conn.cursor()

    user_id = user['id'] if user else None
    if not user_id:
        cursor.execute("SELECT id FROM users LIMIT 1")
        first = cursor.fetchone()
        if first:
            user_id = first['id']

    if not user_id:
        conn.close()
        return jsonify({"success": True, "attendance": None})

    cursor.execute('''
        SELECT status, date, meal, created_at
        FROM attendance
        WHERE user_id = ? AND date = ? AND meal = ?
        ORDER BY id DESC LIMIT 1
    ''', (user_id, date_str, meal))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({"success": True, "attendance": dict(row)})
    return jsonify({"success": True, "attendance": None})


# =======================================================
# MESS FEES APIS
# =======================================================

@app.route('/api/fees', methods=['GET'])
def get_fees():
    user = get_current_user_from_request()
    conn = get_db()
    cursor = conn.cursor()

    user_id = user['id'] if user else None
    if not user_id:
        cursor.execute("SELECT id FROM users LIMIT 1")
        first = cursor.fetchone()
        if first:
            user_id = first['id']

    if not user_id:
        conn.close()
        return jsonify({"success": False, "message": "No user found."}), 404

    current_month = datetime.now().strftime("%B %Y")
    cursor.execute('''
        SELECT id, month, monthly_fee, paid_amount, status
        FROM fees
        WHERE user_id = ?
        ORDER BY id DESC LIMIT 1
    ''', (user_id,))
    fee_record = cursor.fetchone()

    if not fee_record:
        # Create default record
        cursor.execute('''
            INSERT INTO fees (user_id, month, monthly_fee, paid_amount, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, current_month, 3000, 2000, "Payment Pending"))
        conn.commit()
        cursor.execute("SELECT id, month, monthly_fee, paid_amount, status FROM fees WHERE id = ?", (cursor.lastrowid,))
        fee_record = cursor.fetchone()

    fee_dict = dict(fee_record)
    fee_dict['remaining_amount'] = max(0, fee_dict['monthly_fee'] - fee_dict['paid_amount'])
    conn.close()

    return jsonify({"success": True, "fee": fee_dict})


@app.route('/api/fees/pay', methods=['POST'])
def pay_fees():
    user = get_current_user_from_request()
    conn = get_db()
    cursor = conn.cursor()

    user_id = user['id'] if user else None
    if not user_id:
        cursor.execute("SELECT id FROM users LIMIT 1")
        first = cursor.fetchone()
        if first:
            user_id = first['id']

    if not user_id:
        conn.close()
        return jsonify({"success": False, "message": "No user found."}), 404

    cursor.execute('''
        SELECT id, month, monthly_fee, paid_amount, status
        FROM fees
        WHERE user_id = ?
        ORDER BY id DESC LIMIT 1
    ''', (user_id,))
    fee_record = cursor.fetchone()

    if not fee_record:
        conn.close()
        return jsonify({"success": False, "message": "No fee record found."}), 404

    remaining = max(0, fee_record['monthly_fee'] - fee_record['paid_amount'])
    if remaining <= 0:
        conn.close()
        return jsonify({"success": True, "message": "Fee is already fully paid!", "fee": {
            "month": fee_record['month'],
            "monthly_fee": fee_record['monthly_fee'],
            "paid_amount": fee_record['monthly_fee'],
            "remaining_amount": 0,
            "status": "Paid"
        }})

    txn_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
    new_paid = fee_record['monthly_fee']

    cursor.execute('''
        UPDATE fees
        SET paid_amount = ?, status = 'Paid', updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (new_paid, fee_record['id']))

    cursor.execute('''
        INSERT INTO payments (user_id, amount, month, payment_method, transaction_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, remaining, fee_record['month'], 'Online UPI/Card', txn_id))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": f"Payment of ₹{int(remaining)} successful! Transaction ID: {txn_id}",
        "transaction_id": txn_id,
        "fee": {
            "month": fee_record['month'],
            "monthly_fee": fee_record['monthly_fee'],
            "paid_amount": new_paid,
            "remaining_amount": 0,
            "status": "Paid"
        }
    })


# =======================================================
# NOTICES APIS
# =======================================================

@app.route('/api/notices', methods=['GET'])
def get_notices():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content, date, icon FROM notices ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify({"success": True, "notices": [dict(r) for r in rows]})


# =======================================================
# WEEKLY MENU APIS
# =======================================================

@app.route('/api/menu', methods=['GET'])
def get_menu():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, day, title, items, is_special FROM menu ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify({"success": True, "menu": [dict(r) for r in rows]})


# =======================================================
# RUN APPLICATION
# =======================================================

if __name__ == '__main__':
    print("==================================================")
    print(" SmartHostel Backend & SQLite Database Running!   ")
    print(" Open http://127.0.0.1:5000 in your browser       ")
    print("==================================================")
    app.run(host='0.0.0.0', port=5000, debug=True)

